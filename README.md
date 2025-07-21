# 🎯 Number Guessing Game - Enhanced with Authentication & Database

A sophisticated web-based number guessing game built with Pyt### Security Features
- 🔒 **Password Hashing**: Secure password storage using Werkzeug
- 🛡️ **CSRF Protection**: Form security with Flask-WTF
- 🔐 **Login Required**: Protected routes for authenticated users only
- 🍪 **Secure Sessions**: Flask session management
- ⚡ **Input Validation**: Form validation and sanitization

### 📱 Social Features
- 📤 **Facebook Integration**: Share achievements and scores
- 🎯 **Dynamic Messages**: Custom share text based on performance
- 🏆 **Achievement Sharing**: Celebrate milestones with friends
- 📊 **Leaderboard Sharing**: Challenge others to compete
- 🔗 **Smart URLs**: Automatic link generation for sharingask, featuring user authentication, score tracking, and competitive leaderboards. Players create accounts, track their progress, and compete with others!

## 🎮 Enhanced Game Features

- **🔐 User Authentication**: Secure registration and login system
- **📊 Score Tracking**: All your games are saved to a database
- **🏆 Leaderboards**: Compete with other players for the best scores
- **📈 Personal Statistics**: Track your improvement over time
- **🎯 Performance Analysis**: Get insights and achievement badges
- **💾 Persistent Sessions**: Your progress is never lost
- **🔒 Secure Database**: SQLite with proper password hashing
- **📱 Responsive Design**: Works perfectly on all devices

## 🆕 New Features Added

### User System
- **Registration**: Create your unique player account
- **Login/Logout**: Secure session management
- **Profile Page**: View your personal statistics and game history

### Database Integration
- **Score Storage**: Every completed game is saved
- **Game History**: See all your previous attempts and results
- **Statistics**: Best score, average score, total games played

### Competitive Features
- **Global Leaderboard**: Top 10 best scores from all players
- **Player Rankings**: See how you rank against other players
- **Achievements**: Unlock badges for exceptional performance
- **Performance Tips**: Get suggestions to improve your game

### 📱 Social Media Integration
- **Facebook Sharing**: Share your achievements and scores
- **Achievement Sharing**: Celebrate your milestones with friends
- **Leaderboard Sharing**: Challenge others to beat your rank
- **Custom Share Messages**: Dynamic messages based on performance
- **One-Click Sharing**: Easy social media integration

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation & Setup

1. **Clone or download the project files**
   ```bash
   # Navigate to the project directory
   cd "Number Guessing game"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   - Go to `http://localhost:5000`
   - Register a new account or login
   - Start playing and tracking your scores!

## 🎯 How to Play

1. **Create Account**: Register with a username and password
2. **Login**: Access your personal game dashboard
3. **Start Playing**: The game generates a random number between 1-100
4. **Make Guesses**: Enter numbers and receive "too high" or "too low" feedback
5. **Win the Game**: Find the correct number and save your score
6. **Track Progress**: View your statistics and compete on leaderboards
7. **Improve**: Use the performance analysis to get better at the game

## 📁 Enhanced Project Structure

```
Number Guessing game/
├── app.py                  # Main Flask application with auth & database
├── game.db                 # SQLite database (auto-created)
├── requirements.txt        # Python dependencies (updated)
├── templates/
│   ├── index.html         # Enhanced game interface
│   ├── auth.html          # Login/Registration forms
│   ├── leaderboard.html   # Global leaderboards
│   └── profile.html       # User profile and statistics
├── static/
│   └── style.css          # Enhanced styling with auth support
├── .github/
│   └── copilot-instructions.md
├── DEPLOYMENT.md          # Deployment guide
└── README.md              # This file
```

## 🛠️ Technical Details

### Backend (app.py)
- **Flask Framework**: Lightweight web framework for Python
- **Flask-SQLAlchemy**: Database ORM for managing user data and scores
- **Flask-Login**: User session management and authentication
- **Flask-WTF**: Form handling and CSRF protection
- **SQLite Database**: Lightweight database for storing users and game scores
- **Password Security**: Werkzeug password hashing for secure authentication
- **Session Management**: Secure game state and user sessions

### Database Schema
- **Users Table**: User accounts with hashed passwords
- **GameScore Table**: Individual game records with attempts and timestamps
- **Relationships**: Users linked to their game scores

### Route Handlers
- `/register` - User registration (GET/POST)
- `/login` - User authentication (GET/POST)
- `/logout` - User logout
- `/` - Main game page (login required)
- `/guess` - Process player guesses (POST, login required)
- `/reset` - Start new game (login required)
- `/leaderboard` - Global rankings (login required)
- `/profile` - User statistics and history (login required)

### Frontend
- **Enhanced Templates**: Multiple HTML templates with Jinja2
- **Navigation System**: User-friendly navbar with authentication status
- **Responsive Tables**: Leaderboards and statistics display
- **Flash Messages**: User feedback for actions and errors
- **Modern UI**: Enhanced styling with gradients and animations

### Security Features
- � **Password Hashing**: Secure password storage using Werkzeug
- 🛡️ **CSRF Protection**: Form security with Flask-WTF
- 🔐 **Login Required**: Protected routes for authenticated users only
- 🍪 **Secure Sessions**: Flask session management
- ⚡ **Input Validation**: Form validation and sanitization

## 🎨 Customization

You can easily customize the game by modifying:

- **Number Range**: Change the range in `app.py` (currently 1-100)
- **Styling**: Update `static/style.css` for different colors/themes
- **Messages**: Modify feedback messages in `app.py`
- **Difficulty**: Add multiple difficulty levels

## 🚀 Deployment Options

### Local Development
```bash
python app.py
```

### Free Production Deployment with Real Domains

#### Option 1: Render.com (Recommended - FREE with custom domain)
1. **Push code to GitHub** (if not already done)
2. **Sign up at [render.com](https://render.com)** with GitHub
3. **Create New Web Service** → Connect your GitHub repo
4. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
   - Environment: Python 3
5. **Deploy** → Get free `.onrender.com` subdomain
6. **Custom Domain** (optional): Add your own domain for free

#### Option 2: Railway.app (FREE tier available)
1. **Sign up at [railway.app](https://railway.app)**
2. **Deploy from GitHub** → Select your repo
3. **Auto-deploys** on code changes
4. **Free subdomain** + custom domain support

#### Option 3: Vercel (FREE with great performance)
1. **Sign up at [vercel.com](https://vercel.com)**
2. **Import GitHub project**
3. **Add `vercel.json` configuration**:
   ```json
   {
     "builds": [{"src": "app.py", "use": "@vercel/python"}],
     "routes": [{"src": "/(.*)", "dest": "app.py"}]
   }
   ```
4. **Deploy** → Get `.vercel.app` domain

#### Option 4: PythonAnywhere (FREE tier)
1. **Sign up at [pythonanywhere.com](https://pythonanywhere.com)**
2. **Upload files** via web interface
3. **Create web app** → Flask
4. **Configure WSGI** file
5. **Get `username.pythonanywhere.com` domain**

#### Option 5: Heroku (FREE tier discontinued, but alternatives exist)
- Consider **Heroku alternatives**: Railway, Render, or Fly.io

### Free Domain Options
- **Freenom**: Free `.tk`, `.ml`, `.ga` domains
- **GitHub Pages**: Free with custom domain support
- **Netlify/Vercel**: Free subdomains + custom domain support

## 🤝 Contributing

Feel free to contribute to this project! You can:
- Report bugs or issues
- Suggest new features
- Submit pull requests
- Improve documentation

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🎉 Enjoy the Game!

Have fun guessing numbers and try to beat your best score! 🏆

---

**Estimated Play Time**: 2-5 minutes per game  
**Difficulty**: Beginner-friendly  
**Age Range**: All ages  
**Skills**: Logic, deduction, probability
