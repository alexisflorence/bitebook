# Python Flask application that integrates our various services
# Including Google Cloud Storage
# OpenAI 
# Potentially Google Sheets for data handling 
from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, set_access_cookies, verify_jwt_in_request, unset_jwt_cookies
from werkzeug.utils import secure_filename
from hmac import compare_digest
from google.cloud import storage
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import openai
import os
import json
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv
import base64
import pytz

'''
Key Functionalities:
    User Authentication: Using JWT for securing routes and managing sessions.
    File Handling: Uploading images to Google Cloud Storage and generating public URLs for access.
    AI Integration: Using OpenAI's API to perform tasks, likely related to image or data analysis.
    ata Logging: Potentially logging analysis results or other data in a Google Sheet
'''

# Checks if the application is running in development mode & loads env variables from .env
if os.getenv('FLASK_ENV') == 'development':
    load_dotenv()

# Decode the base64 environment variable to JSON
decoded_credentials = base64.b64decode(os.getenv("GOOGLE_APPLICATION_CREDENTIALS_BASE64"))

# Write the decoded credentials to a temp file
temp_credentials_path = "/tmp/google_credentials.json"
with open(temp_credentials_path, "wb") as temp_file:
    temp_file.write(decoded_credentials)

# Point GOOGLE_APPLICATION_CREDENTIALS to the temp file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_credentials_path

# Flask app configuration
# JSON Web Tokens for authentication
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

# Initialize JWT Manager
jwt = JWTManager(app)

# Mock user database, mapping usernames to passwords
USERS = {
    "user": os.getenv('USER_PW')
}

# Initialize Google Cloud Storage
storage_client = storage.Client()
bucket = storage_client.bucket(os.getenv('GCS_BUCKET_NAME'))

# Initialize OpenAI client
openai_client = openai.OpenAI()

# Helper function to check login status
def is_logged_in():
    try:
        verify_jwt_in_request()
        return True
    except:
        return False

expected_response_format = {
    "Food Name": "N/A",
    "Calories (kcal)": "N/A",
    "Protein (g)": "N/A",
    "Carbohydrates (g)": "N/A",
    "Fats (g)": "N/A",
    "Fiber (g)": "N/A",
    "Sugars (g)": "N/A",
    "Sodium (mg)": "N/A",
    "Cholesterol (mg)": "N/A",
    "Vitamin A (µg)": "N/A",  # µg for micrograms
    "Vitamin C (mg)": "N/A",
    "Vitamin D (µg)": "N/A",
    "Vitamin E (mg)": "N/A",
    "Vitamin K (µg)": "N/A",
    "Calcium (mg)": "N/A",
    "Iron (mg)": "N/A",
    "Magnesium (mg)": "N/A",
    "Phosphorus (mg)": "N/A",
    "Potassium (mg)": "N/A",
    "Zinc (mg)": "N/A",
    "Water Content (mL)": "N/A",
    "Serving Description": "Describe the Serving Size",
    "Meal Type": "Breakfast, Lunch, Dinner, or Snack",
    "Cuisine Type": "e.g., Italian, Mexican, Japanese",
    "Notes": "Any additional notes or observations",
}

def buildPrompt(details):
    formatted_expected_response = json.dumps(expected_response_format, indent=4)

    prompt = (
        f"Based on the description and any visible details in the food photo provided, "
        f"analyze and estimate the nutritional information. Consider the description which may include "
        f"meal type, ingredients, preparation method, portion size, and any known nutrition facts or "
        f"consumption details: '{details}'. Please provide all responses in strict RFC8259 compliant JSON format. "
        f"Include any necessary explanations, disclaimers, or notes within the JSON object itself, "
        f"ensuring the entire response is valid JSON. "
        f"The recipient of this data will be a spreadsheet tracking estimates, so marking fields with words like 'approximatly' is redundant. "
        f"Please provide estimates where exact numbers are not available and mark any unknown fields as 'N/A'.\n\n"
        f"Expected JSON Response Format:\n{formatted_expected_response}\n\n"
        "The JSON object:\n\n"
    )
    return prompt

def clean_json_string(s):
    # Find the first occurrence of a JSON-like object
    json_pattern = re.compile(r'\{.*\}', re.DOTALL)
    match = json_pattern.search(s)
    if match:
        json_str = match.group(0)
        try:
            # Validate if the extracted string is valid JSON
            json_obj = json.loads(json_str)
            return json.dumps(json_obj, indent=4)
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            return None
    else:
        print("No JSON object found.")
        return None

# Flask Routes

# The main page of the application, accessible only if the user is logged in
@app.route('/')
def index():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('index.html')

# handles both displaying the login form and processing login attempts
# verifies the user credentials against the mock database
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = list(USERS)[0]
        password = request.form['password']
        user_password = USERS.get(username)
        if user_password and compare_digest(user_password, password):
            access_token = create_access_token(identity=username)
            resp = redirect(url_for('index'))
            set_access_cookies(resp, access_token)
            return resp
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

# Logs out the user by clearing JWT cookies
@app.route('/logout', methods=['POST'])
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)  # This will remove the JWT cookies
    return resp, 302, {'Location': url_for('login')}

# A protected route that processes image uploads
# stores the uploaded image in Google Cloud Storage generates a public URL for the image
# and potentially analyzes the image or associated data using OpenAI
# the route builds a prompt for OpenAI's API, analyze the response, and integrate with Google Sheets
@app.route('/upload', methods=['POST'])
@jwt_required()

def upload_image():
    image_file = request.files.get('file')
    details = request.form.get('details', '')

    if image_file and image_file.filename:
        filename = secure_filename(image_file.filename)
        seattle = pytz.timezone('America/Los_angeles')
        date_path = datetime.now(seattle).strftime('%Y-%m-%d')
        blob = bucket.blob(f"{date_path}/{int(round(datetime.now().timestamp()))}")
        blob.upload_from_string(image_file.read(), content_type=image_file.content_type)
        #blob.make_public()
        image_url = blob.public_url
        print(image_url)

        # Call OpenAI Vision API
        response = openai_client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": buildPrompt(details)},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
            max_tokens=900
        )
        json_response = clean_json_string(response.choices[0].message.content)

        # Parse the JSON response
        try:
            nutritional_info = json.loads(json_response)
        except json.JSONDecodeError:
            print(json_response)
            return f'<div id="response" class="font-mono">Failed to parse nutritional information.</div>', 400

        # Google Sheets API to store image URL, description, and user details
        service = build('sheets', 'v4', credentials=Credentials.from_service_account_file(
            os.getenv('GOOGLE_APPLICATION_CREDENTIALS')), cache_discovery=False)
        SPREADSHEET_ID = '1Ten82u29-uVFVLEqz9W-GpbDcgv6g-nr_3m-2rFKL6c'
        estimates = {key: nutritional_info.get(key, expected_response_format[key]) for key in expected_response_format.keys()}
        #formula = f"=HYPERLINK(\"{image_url}\", IMAGE(\"{image_url}\", 4, 96, 72))"
        values_row = [date_path]
        for key in expected_response_format.keys():
            values_row.append(estimates.get(key, "N/A")) 
        values_row.append(details)
        food_name = values_row[1]
        formula = f"=HYPERLINK(\"{image_url}\", \"{food_name}\")"
        values_row[1] = formula
        values = [values_row]
        body = {'values': values}
        range_name = 'meals!A:S'
        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption='USER_ENTERED',
            body=body,
            insertDataOption='INSERT_ROWS'
        ).execute()


        return f'<div id="response" class="font-mono"> Added <a href="{image_url}" class="mt-4 font-mono text" target="_blank">{estimates["Food Name"]}</a> to the spreadsheet.</div>', 200
    return f'<div id="response" class="font-mono">Error no photo provided.</div>', 400

# specifies the default port and runs the flask application
# making it accessible over the network
if __name__ == '__main__':
    port = int(os.getenv('PORT', '8080'))
    app.run(host='0.0.0.0', port=port, debug=True)
