# BiteBook Project

## Overview

BiteBook is more than just a dynamic web application for food lovers; it's a personal project born out of a need to support my brother during his expereince with Hodgkin's Lymphoma. As he undergoes a stem cell transplant, a crucial part of his recovery involves meticulously logging his dietary intake for his nutritionist. This necessity sparked the creation of BiteBook.

Developed using Flask and styled with TailwindCSS, BiteBook is designed to make the process of tracking and logging food intake as seamless and supportive as possible. It utilizes Google Cloud Storage for robust data management and leverages OpenAI's GPT to generate creative, nutritious meal suggestions tailored to specific dietary needs.

While BiteBook serves a critical role in my brother's recovery journey, offering a specialized platform for him to log his meals and monitor his nutrition, it also invites food enthusiasts from around the world to explore culinary arts, share recipes, and find their next meal inspiration. Whether you're in a similar health situation, looking to manage your diet, or simply passionate about food, BiteBook provides a comprehensive platform for all things related to food and nutrition.

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
git clone https://github.com/alexisflorence/bitebook-main.git
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
