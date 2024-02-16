# BiteBook Project

## Overview

BiteBook is a dynamic web application designed to connect food enthusiasts from around the globe. Built with Flask, it leverages TailwindCSS for styling, Google Cloud Storage for data handling, and OpenAI's GPT for generating creative content. Whether you're sharing recipes, exploring culinary arts, or just browsing for your next meal inspiration, BiteBook offers a platform for all things food.

## Features

- **User Authentication:** Secure login and signup functionalities powered by Flask-JWT-Extended.
- **Recipe Sharing:** Users can post, edit, and delete their recipes.
- **Content Generation:** Utilizes OpenAI's GPT for generating recipe descriptions and food-related content.
- **Cloud Storage:** All user-generated content is securely stored and managed in Google Cloud Storage.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Pip package manager
- A Google Cloud account for storage services
- An OpenAI API key for content generation features

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/bitebook-main.git
cd bitebook-main
```

2. **Set up a virtual environment (optional)**
   This will help create an isolated environment for your workspace

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
   These are key value pairs stored outside of our application's source code.
   They are used to configure behavior in development, testing, & production
   without changing code
   (Useful for keeping API keys and passwords out of source code)

   Create a `.env` file in the project root and add the following variables
   FLASK_APP=app.py
   FLASK_ENV=development
   GOOGLE_CLOUD_STORAGE_BUCKET=your_bucket_name
   OPENAI_API_KEY=your_openai_api_key

Replace `your_bucket_name` and `your_openai_api_key` with your actual Google Cloud Storage bucket name and OpenAI API key

5. **Run the application**

```bash
flask run
```

Your application should now be running on http://localhost:5000

Project Link: https://github.com/alexisflorence/bitebook-main
