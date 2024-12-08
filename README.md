# Byte Currency Platform

## Overview
Byte Currency is a digital currency platform that allows users to create accounts, transfer funds, and manage their digital currency balance.

## Features
- User Registration and Authentication
- Peer-to-Peer Transfers
- Transaction History
- Admin Balance Management
- Secure JWT Authentication

## Tech Stack
- Backend: Python Flask
- Frontend: React
- Database: SQLAlchemy with SQLite
- Authentication: JWT

## Setup Instructions

### Backend Setup
1. Navigate to `backend` directory
2. Create a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the backend:
   ```
   python app.py
   ```

### Frontend Setup
1. Navigate to `frontend` directory
2. Install dependencies:
   ```
   npm install
   ```
3. Start the React development server:
   ```
   npm start
   ```

## Default Credentials
- Admin Username: admin
- Admin Password: admin_password

## Deployment
The application is designed to be easily deployed on platforms like Netlify and Heroku.

## Security Notes
- Use environment variables for sensitive information
- Always use HTTPS in production
- Regularly update dependencies

## License
MIT License
