from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from datetime import datetime
import random
import os
import urllib.parse

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'number-guessing-game-secret-key-2025-enhanced')

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or \
    'sqlite:///' + os.path.join(basedir, 'game.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Facebook OAuth configuration
facebook_bp = make_facebook_blueprint(
    client_id=os.environ.get('FACEBOOK_OAUTH_CLIENT_ID'),
    client_secret=os.environ.get('FACEBOOK_OAUTH_CLIENT_SECRET'),
    scope="email,public_profile"
)
app.register_blueprint(facebook_bp, url_prefix="/login")

# Login manager setup
login_manager = LoginManager()
# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth'
login_manager.login_message = 'Please log in to play the game!'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(120), nullable=True)
    facebook_id = db.Column(db.String(100), unique=True, nullable=True)
    profile_picture = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scores = db.relationship('GameScore', backref='player', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        if self.password_hash:
            return check_password_hash(self.password_hash, password)
        return False
    
    def get_best_score(self):
        best = db.session.query(GameScore).filter_by(user_id=self.id).order_by(GameScore.attempts).first()
        return best.attempts if best else None
    
    def get_total_games(self):
        return len(self.scores)
    
    def get_achievements(self):
        best_score = self.get_best_score()
        total_games = self.get_total_games()
        achievements = []
        
        if best_score == 1:
            achievements.append({"name": "Perfect Shot", "description": "Guessed the number in 1 attempt!", "icon": "🎯"})
        if best_score and best_score <= 3:
            achievements.append({"name": "Sharp Shooter", "description": "Guessed the number in 3 or fewer attempts!", "icon": "⭐"})
        if best_score and best_score <= 5:
            achievements.append({"name": "Good Guesser", "description": "Guessed the number in 5 or fewer attempts!", "icon": "👍"})
        if total_games >= 10:
            achievements.append({"name": "Dedicated Player", "description": "Played 10 or more games!", "icon": "🏆"})
        if total_games >= 50:
            achievements.append({"name": "Game Master", "description": "Played 50 or more games!", "icon": "👑"})
            
        return achievements

# Simple OAuth storage model
class FacebookOAuth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    facebook_user_id = db.Column(db.String(100), unique=True, nullable=False)
    token = db.Column(db.Text, nullable=True)
    user = db.relationship('User', backref='facebook_oauth')

class GameScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    attempts = db.Column(db.Integer, nullable=False)
    target_number = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Helper functions for Facebook sharing
def get_achievement_message(user, score):
    """Generate achievement message for sharing"""
    messages = {
        1: f"🎯 AMAZING! {user.username} guessed the number in just 1 attempt! Perfect shot! 🏆",
        2: f"🔥 INCREDIBLE! {user.username} nailed it in only 2 attempts! Sharp shooter! 🎯",
        3: f"⭐ EXCELLENT! {user.username} conquered the number game in 3 attempts! 🌟",
        4: f"🎉 GREAT JOB! {user.username} solved it in 4 attempts! Getting better! 💪",
        5: f"👏 WELL DONE! {user.username} cracked the code in 5 attempts! Nice work! 🎮"
    }
    
    if score <= 5:
        return messages.get(score, f"🎮 {user.username} just won the Number Guessing Game in {score} attempts! Can you beat this score?")
    else:
        return f"🎮 {user.username} just completed the Number Guessing Game in {score} attempts! Join the fun and try to beat this score!"

def generate_facebook_share_url(message, url):
    """Generate Facebook share URL with custom message"""
    base_url = "https://www.facebook.com/sharer/sharer.php"
    params = {
        'u': url,
        'quote': message,
        'hashtag': '#NumberGuessingGame'
    }
    return f"{base_url}?{urllib.parse.urlencode(params)}"

def get_user_achievements(user):
    """Get list of user achievements"""
    achievements = []
    best_score = user.get_best_score()
    total_games = user.get_total_games()
    
    if best_score:
        if best_score == 1:
            achievements.append({
                'title': '🎯 Perfect Shot',
                'description': 'Guessed the number in 1 attempt!',
                'icon': '🏆',
                'shareable': True
            })
        elif best_score <= 3:
            achievements.append({
                'title': '🔥 Sharp Shooter',
                'description': f'Best score: {best_score} attempts',
                'icon': '🎯',
                'shareable': True
            })
        elif best_score <= 5:
            achievements.append({
                'title': '⭐ Number Master',
                'description': f'Best score: {best_score} attempts',
                'icon': '🌟',
                'shareable': True
            })
    
    if total_games >= 10:
        achievements.append({
            'title': '🎮 Dedicated Player',
            'description': f'Played {total_games} games',
            'icon': '🏅',
            'shareable': True
        })
    
    if total_games >= 50:
        achievements.append({
            'title': '🏆 Game Legend',
            'description': f'Played {total_games} games!',
            'icon': '👑',
            'shareable': True
        })
    
    return achievements

# Simple OAuth storage model
class FacebookOAuth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    facebook_user_id = db.Column(db.String(100), unique=True, nullable=False)
    token = db.Column(db.Text, nullable=True)
    user = db.relationship('User', backref='facebook_oauth')

class GameScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    attempts = db.Column(db.Integer, nullable=False)
    target_number = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Utility functions
def get_achievement_message(user, attempts):
    """Generate achievement messages based on score"""
    if attempts == 1:
        return f"🎯 AMAZING! {user.username} guessed the number in just 1 attempt! Perfect shot! 🏆"
    elif attempts <= 3:
        return f"⭐ EXCELLENT! {user.username} conquered the number game in {attempts} attempts! 🌟"
    elif attempts <= 5:
        return f"👏 GREAT JOB! {user.username} solved it in {attempts} attempts! 🎲"
    else:
        return f"🎯 {user.username} is mastering the Number Guessing Game! Latest score: {attempts} attempts"

def generate_facebook_share_url(message, url):
    """Generate Facebook share URL"""
    base_url = "https://www.facebook.com/sharer/sharer.php"
    params = {
        'u': url,
        'quote': message
    }
    return f"{base_url}?{urllib.parse.urlencode(params)}"

def get_user_achievements(user):
    """Get user achievements for display"""
    return user.get_achievements()

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# Facebook OAuth login route
@app.route('/login/facebook')
def facebook_login():
    if not facebook.authorized:
        return redirect(url_for("facebook.login"))
    
    # Get Facebook user info
    resp = facebook.get("/me?fields=id,name,email,picture")
    if not resp.ok:
        flash('Failed to fetch user info from Facebook', 'error')
        return redirect(url_for('auth'))
    
    facebook_info = resp.json()
    facebook_user_id = str(facebook_info["id"])
    
    # Check if this Facebook account is already linked
    oauth_record = FacebookOAuth.query.filter_by(facebook_user_id=facebook_user_id).first()
    
    if oauth_record and oauth_record.user:
        # User exists, log them in
        login_user(oauth_record.user)
        flash(f'Welcome back, {oauth_record.user.username}!', 'success')
        return redirect(url_for('home'))
    else:
        # Check if user already exists with this email
        existing_user = None
        if facebook_info.get("email"):
            existing_user = User.query.filter_by(email=facebook_info["email"]).first()
        
        if existing_user:
            # Link the existing account with Facebook
            existing_user.facebook_id = facebook_user_id
            if facebook_info.get("email") and not existing_user.email:
                existing_user.email = facebook_info["email"]
            if facebook_info.get("picture", {}).get("data", {}).get("url"):
                existing_user.profile_picture = facebook_info["picture"]["data"]["url"]
            
            # Create OAuth record
            oauth_record = FacebookOAuth(
                user_id=existing_user.id,
                facebook_user_id=facebook_user_id
            )
            db.session.add(oauth_record)
            user_to_login = existing_user
        else:
            # Create new user
            username = facebook_info.get("name", f"facebook_user_{facebook_user_id}")
            # Ensure username is unique
            base_username = username
            counter = 1
            while User.query.filter_by(username=username).first():
                username = f"{base_username}_{counter}"
                counter += 1
            
            user = User(
                username=username,
                email=facebook_info.get("email"),
                facebook_id=facebook_user_id,
                profile_picture=facebook_info.get("picture", {}).get("data", {}).get("url")
            )
            db.session.add(user)
            db.session.flush()  # Get the user ID
            
            # Create OAuth record
            oauth_record = FacebookOAuth(
                user_id=user.id,
                facebook_user_id=facebook_user_id
            )
            db.session.add(oauth_record)
            user_to_login = user

        db.session.commit()
        login_user(user_to_login)
        flash(f'Welcome to Number Guessing Game, {user_to_login.username}!', 'success')
        return redirect(url_for('home'))

# Routes
@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('index.html', user=current_user)
    return redirect(url_for('auth'))

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    login_form = LoginForm()
    register_form = RegisterForm()
    
    if login_form.validate_on_submit() and 'login' in request.form:
        user = User.query.filter_by(username=login_form.username.data).first()
        if user and user.password_hash and check_password_hash(user.password_hash, login_form.password.data):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('home'))
        flash('Invalid username or password', 'error')
    
    if register_form.validate_on_submit() and 'register' in request.form:
        if User.query.filter_by(username=register_form.username.data).first():
            flash('Username already exists', 'error')
        else:
            user = User(
                username=register_form.username.data,
                password_hash=generate_password_hash(register_form.password.data)
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash(f'Welcome to the Number Guessing Game, {user.username}!', 'success')
            return redirect(url_for('home'))
    
    return render_template('auth.html', login_form=login_form, register_form=register_form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('auth'))

@app.route('/game')
@login_required
def game():
    if 'target_number' not in session:
        session['target_number'] = random.randint(1, 100)
        session['attempts'] = 0
        session['game_over'] = False
    
    return render_template('index.html', user=current_user)

@app.route('/guess', methods=['POST'])
@login_required
def guess():
    if session.get('game_over'):
        return redirect(url_for('game'))
    
    try:
        user_guess = int(request.form['guess'])
        if user_guess < 1 or user_guess > 100:
            flash('Please enter a number between 1 and 100', 'error')
            return redirect(url_for('game'))
    except ValueError:
        flash('Please enter a valid number', 'error')
        return redirect(url_for('game'))
    
    session['attempts'] += 1
    target = session['target_number']
    
    if user_guess == target:
        # Save the game score
        game_score = GameScore(
            user_id=current_user.id,
            attempts=session['attempts'],
            target_number=target
        )
        db.session.add(game_score)
        db.session.commit()
        
        session['game_over'] = True
        flash(f'Congratulations! You guessed the number {target} in {session["attempts"]} attempts!', 'success')
        
        # Check for achievements
        if session['attempts'] == 1:
            flash('🎯 Achievement Unlocked: Perfect Shot!', 'achievement')
        elif session['attempts'] <= 3:
            flash('⭐ Achievement Unlocked: Sharp Shooter!', 'achievement')
        elif session['attempts'] <= 5:
            flash('👍 Achievement Unlocked: Good Guesser!', 'achievement')
            
    elif user_guess < target:
        flash(f'Too low! Try a higher number. Attempts: {session["attempts"]}', 'info')
    else:
        flash(f'Too high! Try a lower number. Attempts: {session["attempts"]}', 'info')
    
    return redirect(url_for('game'))

@app.route('/new_game')
@login_required
def new_game():
    session.pop('target_number', None)
    session.pop('attempts', None)
    session.pop('game_over', None)
    flash('New game started! Good luck!', 'info')
    return redirect(url_for('game'))

@app.route('/leaderboard')
@login_required
def leaderboard():
    # Get top 10 best scores
    top_scores = db.session.query(
        User.username, 
        User.profile_picture,
        db.func.min(GameScore.attempts).label('best_score'),
        db.func.count(GameScore.id).label('total_games')
    ).join(GameScore).group_by(User.id).order_by(db.func.min(GameScore.attempts).asc()).limit(10).all()
    
    return render_template('leaderboard.html', top_scores=top_scores, user=current_user)

@app.route('/profile')
@login_required
def profile():
    user_games = GameScore.query.filter_by(user_id=current_user.id).order_by(GameScore.completed_at.desc()).limit(10).all()
    achievements = current_user.get_achievements()
    
    stats = {
        'best_score': current_user.get_best_score(),
        'total_games': current_user.get_total_games()
    }
    
    if user_games:
        stats['average_score'] = sum(game.attempts for game in user_games) / len(user_games)
    else:
        stats['average_score'] = None
    
    return render_template('profile.html', 
                         user=current_user, 
                         games=user_games, 
                         achievements=achievements,
                         stats=stats)

# Sharing functionality
def generate_share_message(share_type, user, **kwargs):
    """Generate dynamic sharing messages based on type and user data"""
    messages = {
        'best_score': {
            1: f"🎯 AMAZING! {user.username} guessed the number in just 1 attempt! Perfect shot! 🏆",
            2: f"🌟 INCREDIBLE! {user.username} nailed it in only 2 attempts! 🎯",
            3: f"⭐ EXCELLENT! {user.username} conquered the number game in 3 attempts! 🌟",
            4: f"👏 GREAT JOB! {user.username} solved it in 4 attempts! 🎲",
            5: f"👍 WELL DONE! {user.username} cracked the code in 5 attempts! 🔢"
        },
        'achievement': f"🏆 Achievement Unlocked: {kwargs.get('achievement_name', 'Master Player')}! Best score: {kwargs.get('best_score', 'N/A')} attempts",
        'total_games': f"🎮 {user.username} has played {kwargs.get('total_games', 0)} games on the Number Guessing Game! Join the fun!",
        'leaderboard': f"🏆 Check out the Number Guessing Game leaderboard! Can you beat the top players?"
    }
    
    if share_type == 'best_score':
        score = kwargs.get('score', 6)
        if score <= 5:
            message = messages['best_score'].get(score, f"🎯 {user.username} guessed the number in {score} attempts!")
        else:
            message = f"� {user.username} is mastering the Number Guessing Game! Latest score: {score} attempts"
    else:
        message = messages.get(share_type, f"🎯 {user.username} is playing the Number Guessing Game!")
    
    # Add common hashtags and call to action
    message += f"\n\n🎯 Can you beat this score? Play now: #NumberGuessingGame #GameChallenge #BeatTheScore"
    
    return message

@app.route('/share/achievement/<share_type>')
@login_required
def share_achievement(share_type):
    """Generate sharing URL for different achievement types"""
    
    # Get user stats
    best_score = current_user.get_best_score()
    total_games = current_user.get_total_games()
    
    # Generate message based on share type
    if share_type == 'best_score' and best_score:
        message = generate_share_message('best_score', current_user, score=best_score)
    elif share_type == 'total_games':
        message = generate_share_message('total_games', current_user, total_games=total_games)
    elif share_type == 'leaderboard':
        message = generate_share_message('leaderboard', current_user)
    else:
        message = f"🎯 Join {current_user.username} on the Number Guessing Game! #NumberGuessingGame"
    
    # Create sharing URL (you can customize this with your actual domain)
    app_url = request.url_root
    share_url = f"https://www.facebook.com/sharer/sharer.php?u={urllib.parse.quote(app_url)}&quote={urllib.parse.quote(message)}"
    
    return jsonify({
        'share_url': share_url,
        'message': message
    })

@app.route('/share/game_complete')
@login_required
def share_game_complete():
    """Generate sharing URL after completing a game"""
    if not session.get('game_over'):
        return jsonify({'error': 'No completed game to share'}), 400
    
    attempts = session.get('attempts', 0)
    message = generate_share_message('best_score', current_user, score=attempts)
    
    app_url = request.url_root
    share_url = f"https://www.facebook.com/sharer/sharer.php?u={urllib.parse.quote(app_url)}&quote={urllib.parse.quote(message)}"
    
    return jsonify({
        'share_url': share_url,
        'message': message,
        'attempts': attempts
    })

if __name__ == '__main__':
    import os
    # Create database tables
    with app.app_context():
        db.create_all()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
