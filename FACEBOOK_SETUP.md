# Facebook OAuth Setup Guide

## 📘 Facebook App Configuration

To enable Facebook login for your Number Guessing Game, you need to create a Facebook App and configure OAuth settings.

### Step 1: Create Facebook App

1. **Go to Facebook Developers**
   - Visit [developers.facebook.com](https://developers.facebook.com)
   - Click "Get Started" or "My Apps"

2. **Create New App**
   - Click "Create App"
   - Choose "Consumer" as app type
   - Fill in App Name: "Number Guessing Game"
   - Add your email address
   - Click "Create App"

### Step 2: Configure Facebook Login

1. **Add Facebook Login Product**
   - In your app dashboard, click "Add Product"
   - Find "Facebook Login" and click "Set Up"

2. **Configure OAuth Settings**
   - Go to Facebook Login → Settings
   - Add Valid OAuth Redirect URIs:
     - For local development: `http://localhost:5000/login/facebook/authorized`
     - For production: `https://yourdomain.com/login/facebook/authorized`

3. **Get App Credentials**
   - Go to Settings → Basic
   - Copy your App ID and App Secret

### Step 3: Environment Variables

Set up your environment variables:

#### For Local Development (.env file)
```bash
FACEBOOK_OAUTH_CLIENT_ID=your_facebook_app_id
FACEBOOK_OAUTH_CLIENT_SECRET=your_facebook_app_secret
```

#### For Production (Render, Railway, etc.)
Add these environment variables in your deployment platform:
- `FACEBOOK_OAUTH_CLIENT_ID`: Your Facebook App ID
- `FACEBOOK_OAUTH_CLIENT_SECRET`: Your Facebook App Secret

### Step 4: App Review (For Production)

1. **App Review Process**
   - For public use, submit your app for review
   - Add Privacy Policy URL
   - Add Terms of Service URL
   - Request permissions for "email" and "public_profile"

2. **Business Verification**
   - May be required for larger scale apps
   - Verify your business information

### Step 5: Testing

1. **Test Users**
   - Add test users in App Dashboard → Roles → Test Users
   - Test users can use the app before public release

2. **App Modes**
   - Development Mode: Only admins/developers/testers can use
   - Live Mode: Public access (requires app review)

## 🔧 Configuration Files

### Required Environment Variables
```bash
# Facebook OAuth
FACEBOOK_OAUTH_CLIENT_ID=123456789012345
FACEBOOK_OAUTH_CLIENT_SECRET=abcdef1234567890abcdef1234567890

# Flask Secret Key (generate a secure one)
SECRET_KEY=your-super-secret-key-here

# Database URL (optional, defaults to SQLite)
DATABASE_URL=sqlite:///game.db
```

### Facebook App Settings Checklist

- ✅ App created with "Consumer" type
- ✅ Facebook Login product added
- ✅ Valid OAuth redirect URIs configured
- ✅ App ID and App Secret obtained
- ✅ Environment variables set
- ✅ Privacy Policy added (for production)
- ✅ App reviewed and approved (for public use)

## 🚀 Deployment Notes

### Render.com
```bash
# Add these environment variables in Render dashboard
FACEBOOK_OAUTH_CLIENT_ID=your_app_id
FACEBOOK_OAUTH_CLIENT_SECRET=your_app_secret
```

### Railway.app
```bash
# Add in Railway project variables
FACEBOOK_OAUTH_CLIENT_ID=your_app_id
FACEBOOK_OAUTH_CLIENT_SECRET=your_app_secret
```

### Vercel
```bash
# Add in Vercel project settings
FACEBOOK_OAUTH_CLIENT_ID=your_app_id
FACEBOOK_OAUTH_CLIENT_SECRET=your_app_secret
```

## 🔒 Security Notes

1. **Keep App Secret Secure**
   - Never commit App Secret to version control
   - Use environment variables only
   - Regenerate if compromised

2. **Redirect URI Validation**
   - Only add trusted domains
   - Use HTTPS in production
   - Validate all redirect URIs

3. **Permissions**
   - Only request necessary permissions
   - "email" and "public_profile" are sufficient for login

## 📱 User Experience

### Facebook Login Flow
1. User clicks "Continue with Facebook"
2. Redirected to Facebook login
3. User authorizes your app
4. Redirected back to your game
5. Account created/linked automatically
6. User logged in and ready to play!

### Benefits for Users
- ✅ No password to remember
- ✅ Quick registration process
- ✅ Profile picture automatically imported
- ✅ Secure authentication via Facebook
- ✅ Easy sharing with Facebook friends

## 🛠️ Troubleshooting

### Common Issues

1. **"Invalid OAuth redirect URI"**
   - Check the redirect URI in Facebook app settings
   - Ensure it matches exactly (including protocol)

2. **"App Not Set Up"**
   - Verify Facebook Login product is added
   - Check environment variables are set

3. **"This app is in development mode"**
   - Add test users or submit for app review
   - Switch to live mode after approval

### Local Development
- Use `http://localhost:5000` for local testing
- Add test users to bypass app review
- Facebook provides detailed error messages in console
