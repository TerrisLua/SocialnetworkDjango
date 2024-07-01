# Social Network Django App

## Overview
This is a social networking application built using Django. The app allows users to register, login, update their profiles, send friend requests, and post media. Additionally, it includes an API to fetch user details and a WebSocket-based chat feature.

## Features
- **User Registration and Login:** Secure authentication for users.
- **Profile Management:** Users can update their status, profile picture, and other personal information.
- **Friend Requests Management:** Send, accept, and manage friend requests.
- **Media Posting:** Users can post photos, videos, and other media content.
- **Real-Time Chat:** WebSocket-based real-time chat feature for users.
- **REST API:** Fetch user details and other related information through a REST API.

## Requirements
- Python 3.6+
- Django 3.0+
- Django Channels
- Django REST framework
- Other dependencies listed in `requirements.txt`

## Setup

### Step 1: Create a Virtual Environment and Install Dependencies
```bash
python3 -m venv myvenv
source myvenv/bin/activate  # On Windows, use `myvenv\Scripts\activate`
pip install -r requirements.txt
```
### Step 2: Configure the Database
Update database settings in settings.py if necessary.

### Step 3: Apply Migrations
```bash
python manage.py migrate
```

### Step 4: Create a Superuser
```bash
python manage.py createsuperuser
```

### Step 5: Run the Development Server
```bash
python manage.py runserver
```



