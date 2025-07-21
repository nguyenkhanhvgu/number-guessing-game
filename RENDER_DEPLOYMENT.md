# Render Deployment Guide

## Updated Configuration for SQLAlchemy Compatibility

The application has been updated to resolve SQLAlchemy deployment issues on Render. Here are the key changes made:

### 1. Database Configuration Updates
- Updated to SQLAlchemy 2.0.23 for better compatibility
- Added proper database pool settings:
  ```python
  app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
      'pool_pre_ping': True,
      'pool_recycle': 300,
  }
  ```
- Fixed PostgreSQL URL handling for Render's database URLs

### 2. OAuth Storage Configuration
- Fixed Flask-Dance SQLAlchemy integration
- Proper OAuth storage initialization after database setup

### 3. Dependencies Updated
- SQLAlchemy==2.0.23
- psycopg2-binary==2.9.7 (for PostgreSQL support)
- All other dependencies pinned for stability

## Deployment Steps for Render

1. **Push to GitHub**: Ensure all changes are committed and pushed to your GitHub repository.

2. **Create PostgreSQL Database**:
   - Go to Render Dashboard
   - Create a new PostgreSQL database
   - Copy the database URL

3. **Deploy Web Service**:
   - Create a new Web Service on Render
   - Connect your GitHub repository
   - Set the build command: `pip install -r requirements.txt`
   - Set the start command: `gunicorn app:app`

4. **Environment Variables**:
   Set these environment variables in Render:
   ```
   DATABASE_URL=<your-postgresql-database-url>
   FACEBOOK_OAUTH_CLIENT_ID=<your-facebook-app-id>
   FACEBOOK_OAUTH_CLIENT_SECRET=<your-facebook-app-secret>
   ```

5. **Deploy**: Click "Create Web Service" and wait for deployment to complete.

## Facebook OAuth Setup

Make sure your Facebook App settings include:
- Valid OAuth Redirect URI: `https://your-app-name.onrender.com/login/facebook/authorized`
- App Domain: `your-app-name.onrender.com`

## Troubleshooting

If you encounter any SQLAlchemy errors:
1. Check that DATABASE_URL is properly set
2. Ensure the PostgreSQL database is accessible
3. Verify that the app connects to the database with the updated pool settings

The application should now deploy successfully on Render with all the SQLAlchemy compatibility fixes in place.
