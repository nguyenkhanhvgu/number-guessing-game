# 🎯 Number Guessing Game

A simple and fun web-based number guessing game built with Python Flask. Players try to guess a randomly generated number between 1 and 100, receiving helpful hints along the way!

## 🎮 Game Features

- **Random Number Generation**: Each game generates a new random number between 1-100
- **Smart Feedback**: Get hints whether your guess is too high, too low, or correct
- **Attempt Tracking**: Keep track of how many guesses you've made
- **Responsive Design**: Works great on desktop and mobile devices
- **Session Management**: Game state is maintained during your session
- **Easy Reset**: Start a new game anytime with one click

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
   - Start playing!

## 🎯 How to Play

1. **Start the Game**: Open the web application in your browser
2. **Make a Guess**: Enter a number between 1 and 100 in the input field
3. **Get Feedback**: The game will tell you if your guess is too high, too low, or correct
4. **Keep Trying**: Continue guessing until you find the correct number
5. **Celebrate**: See how many attempts it took you to win!
6. **Play Again**: Click "New Game" to start over with a new number

## 📁 Project Structure

```
Number Guessing game/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Game interface template
├── static/
│   └── style.css          # Styling and responsive design
├── .github/
│   └── copilot-instructions.md
└── README.md              # This file
```

## 🛠️ Technical Details

### Backend (app.py)
- **Flask Framework**: Lightweight web framework for Python
- **Session Management**: Stores game state (target number, attempts, messages)
- **Route Handlers**: 
  - `/` - Main game page
  - `/guess` - Process player guesses (POST)
  - `/reset` - Start a new game
- **Input Validation**: Ensures valid number inputs and handles errors

### Frontend
- **HTML Template**: Clean, semantic structure with Jinja2 templating
- **CSS Styling**: Modern, responsive design with gradient backgrounds
- **JavaScript**: Enhanced UX with auto-focus and form handling
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### Features
- 🎨 **Beautiful UI**: Modern design with smooth animations
- 📱 **Mobile Friendly**: Responsive layout for all screen sizes
- ⚡ **Fast Performance**: Lightweight and optimized
- 🔒 **Session Security**: Secure session management
- 🎯 **User Friendly**: Intuitive interface suitable for all ages

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
