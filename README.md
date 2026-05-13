# GAP - Group Discussion & Collaboration Platform

A Django-based web application for creating and managing discussion rooms with real-time messaging, user profiles, and integrated video conferencing capabilities.

## 📋 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Setup & Configuration](#setup--configuration)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)
- [Usage Guide](#usage-guide)
- [Contributing](#contributing)

## ✨ Features

- **User Authentication**: Secure login and registration system
- **Discussion Rooms**: Create, edit, and delete discussion rooms organized by topics
- **Real-time Messaging**: Post and view messages within discussion rooms
- **User Profiles**: Customizable user profiles with avatar, bio, and contact information
- **Topic Organization**: Organize rooms by different topics/categories
- **Video Conferencing**: Integrated Jitsi Meet for room-specific video meetings
- **Room Search**: Search and filter rooms by name and topic
- **User Management**: View user profiles and participation history
- **REST API**: RESTful API endpoints for programmatic access

## 🛠️ Tech Stack

- **Backend**: Django 6.0.5
- **API**: Django REST Framework 3.17.1
- **Database**: PostgreSQL (with psycopg2)
- **Frontend**: HTML, CSS, JavaScript
- **Image Processing**: Pillow 12.2.0
- **Video Conferencing**: Jitsi Meet
- **ASGI Server**: Asgiref

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL
- pip (Python package manager)

### Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd GAP
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## ⚙️ Setup & Configuration

### Environment Variables

1. **Create a `.env` file** in the project root directory:
```bash
cp .env.example .env
```

2. **Configure the `.env` file** with your settings:
```env
# Django Security
SECRET_KEY=your-secret-key-here
DEBUG=True  # Set to False in production

# Database Configuration
DB_NAME=gap
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### Database Setup

1. **Ensure PostgreSQL is running**
   - On macOS: `brew services start postgresql`
   - On Linux: `sudo systemctl start postgresql`

2. **Create a PostgreSQL database and user** (if not already created):
```bash
psql -U postgres
CREATE DATABASE gap;
CREATE USER your_db_user WITH PASSWORD 'your_db_password';
ALTER ROLE your_db_user SET client_encoding TO 'utf8';
ALTER ROLE your_db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_db_user SET default_transaction_deferrable TO on;
ALTER ROLE your_db_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE gap TO your_db_user;
\q
```

3. **Apply Migrations**
```bash
python manage.py migrate
```

4. **Create a Superuser** (for admin access)
```bash
python manage.py createsuperuser
```

5. **Collect Static Files** (for production)
```bash
python manage.py collectstatic
```

## 📝 Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Django secret key for security | - | ✅ Yes |
| `DEBUG` | Debug mode (True for development, False for production) | `True` | ✅ Yes |
| `DB_NAME` | PostgreSQL database name | `gap` | ✅ Yes |
| `DB_USER` | PostgreSQL database user | - | ✅ Yes |
| `DB_PASSWORD` | PostgreSQL database password | - | ✅ Yes |
| `DB_HOST` | Database host address | `localhost` | ❌ No |
| `DB_PORT` | Database port | `5432` | ❌ No |

## 🚀 Running the Application

### Development Server

Before running the server, ensure your `.env` file is properly configured with all required variables.

```bash
python manage.py runserver
```
The application will be available at `http://localhost:8000`

### Access Admin Panel
Navigate to `http://localhost:8000/admin` and log in with your superuser credentials.

## 📁 Project Structure

```
GAP/
├── base/                          # Main application
│   ├── api/                       # REST API endpoints
│   │   ├── serializers.py        # DRF serializers
│   │   ├── urls.py               # API routing
│   │   └── views.py              # API views
│   ├── migrations/               # Database migrations
│   ├── templates/                # HTML templates
│   │   └── base/                 # App templates
│   ├── templatetags/             # Custom template filters
│   ├── admin.py                  # Django admin configuration
│   ├── forms.py                  # Django forms
│   ├── models.py                 # Database models
│   ├── urls.py                   # App routing
│   └── views.py                  # View logic
├── GAP/                          # Project settings
│   ├── settings.py               # Django settings
│   ├── urls.py                   # Main URL configuration
│   ├── asgi.py                   # ASGI configuration
│   └── wsgi.py                   # WSGI configuration
├── static/                       # Static files
│   ├── assets/                   # Icons and assets
│   ├── images/                   # Image files
│   ├── js/                       # JavaScript files
│   └── styles/                   # CSS stylesheets
├── templates/                    # Global templates
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 📊 Database Models

### User Model
Custom user model extending Django's AbstractUser
- `username`: Unique username
- `email`: Unique email address
- `first_name`: User's first name
- `last_name`: User's last name
- `bio`: User biography
- `avatar`: User profile image

### Topic Model
- `name`: Topic name (e.g., "Technology", "Business", etc.)

### Room Model
- `host`: Foreign Key to User (room creator)
- `topic`: Foreign Key to Topic
- `name`: Room name
- `description`: Room description
- `participants`: Many-to-Many relationship with User
- `created`: Timestamp of room creation
- `updated`: Timestamp of last update
- `meeting_url`: Property that generates Jitsi Meet URL

### Message Model
- `user`: Foreign Key to User (message author)
- `room`: Foreign Key to Room
- `body`: Message content
- `created`: Timestamp of message creation
- `updated`: Timestamp of message last update

## 🔌 API Endpoints

### Authentication
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout

### Rooms
- `GET /api/rooms/` - List all rooms
- `GET /api/rooms/<id>/` - Get specific room details
- `POST /api/rooms/` - Create a new room (authenticated)
- `PUT /api/rooms/<id>/` - Update room (host only)
- `DELETE /api/rooms/<id>/` - Delete room (host only)

### Messages
- `GET /api/rooms/<id>/messages/` - Get messages in a room
- `POST /api/messages/` - Create a new message (authenticated)

### Users
- `GET /api/users/` - List all users
- `GET /api/users/<id>/` - Get user profile

## 💡 Usage Guide

### Creating a Room
1. Login to your account
2. Navigate to "Create Room"
3. Enter room name, description, and select a topic
4. Click "Create"

### Joining a Room
1. Browse available rooms on the home page
2. Click on a room to view messages
3. Add yourself as a participant
4. Start messaging

### Starting a Video Meeting
1. Inside a room, click "Start Meeting" button
2. You'll be redirected to a Jitsi Meet URL: `https://meet.jit.si/gap-room-<room_id>`
3. Share the link with other participants

### Updating Your Profile
1. Click on your profile icon
2. Select "Update Profile"
3. Edit your information and upload avatar
4. Save changes

## 👥 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Important Notes

- **Security**: Update the `SECRET_KEY` in `.env` before production deployment
- **Debug Mode**: Set `DEBUG = False` in `.env` for production
- **Allowed Hosts**: Update `ALLOWED_HOSTS` with your domain in production
- **Static Files**: Run `collectstatic` before deploying to production
- **Environment Variables**: Never commit `.env` file to version control. Use `.env.example` as a template
- **Git Ignore**: Add `.env` to your `.gitignore` file:
  ```
  .env
  *.pyc
  __pycache__/
  db.sqlite3
  venv/
  ```

## 📝 License

This project is open source and available for educational and commercial use.

## 📞 Support

For issues or questions, please open an issue in the repository or contact the development team.
