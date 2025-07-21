from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
import os
import urllib.parse

app = Flask(__name__)
app.secret_key = 'number-guessing-game-secret-key-2025-enhanced'

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'game.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to play the game!'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scores = db.relationship('GameScore', backref='player', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_best_score(self):
        best = db.session.query(GameScore).filter_by(user_id=self.id).order_by(GameScore.attempts).first()
        return best.attempts if best else None
    
    def get_total_games(self):
        return len(self.scores)

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

# Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Username already exists. Please choose a different one.', 'error')
            return render_template('auth.html', form=form, mode='register')
        
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth.html', form=form, mode='register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('index'))
        flash('Invalid username or password', 'error')
    
    return render_template('auth.html', form=form, mode='login')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully!', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    if 'target_number' not in session:
        session['target_number'] = random.randint(1, 100)
        session['attempts'] = 0
        session['game_over'] = False
        session['message'] = f"Welcome {current_user.username}! I'm thinking of a number between 1 and 100. Can you guess it?"
        session['message_type'] = "info"
    
    # Get user statistics
    best_score = current_user.get_best_score()
    total_games = current_user.get_total_games()
    
    return render_template('index.html',
                         attempts=session.get('attempts', 0),
                         message=session.get('message', ''),
                         message_type=session.get('message_type', 'info'),
                         game_over=session.get('game_over', False),
                         best_score=best_score,
                         total_games=total_games,
                         current_user=current_user)

@app.route('/guess', methods=['POST'])
@login_required
def guess():
    try:
        user_guess = int(request.form['guess'])
        target = session['target_number']
        session['attempts'] += 1
        
        if user_guess == target:
            # Game won - save score to database
            score = GameScore(
                user_id=current_user.id,
                attempts=session['attempts'],
                target_number=target
            )
            db.session.add(score)
            db.session.commit()
            
            # Generate sharing message
            session['latest_score'] = session['attempts']
            session['share_message'] = get_achievement_message(current_user, session['attempts'])
            
            session['message'] = f"🎉 Congratulations! You guessed it in {session['attempts']} attempts! Score saved!"
            session['message_type'] = "success"
            session['game_over'] = True
        elif user_guess < target:
            session['message'] = f"Too low! Try a higher number. (Attempt {session['attempts']})"
            session['message_type'] = "warning"
        else:
            session['message'] = f"Too high! Try a lower number. (Attempt {session['attempts']})"
            session['message_type'] = "warning"
            
    except ValueError:
        session['message'] = "Please enter a valid number!"
        session['message_type'] = "error"
    
    return redirect(url_for('index'))

@app.route('/reset')
@login_required
def reset():
    session.pop('target_number', None)
    session.pop('attempts', None)
    session.pop('game_over', None)
    session.pop('message', None)
    session.pop('message_type', None)
    return redirect(url_for('index'))

@app.route('/leaderboard')
@login_required
def leaderboard():
    # Get top 10 best scores (fewest attempts)
    top_scores = db.session.query(GameScore, User).join(User).order_by(GameScore.attempts).limit(10).all()
    
    # Get user rankings
    user_best_scores = db.session.query(
        User.id,
        User.username,
        db.func.min(GameScore.attempts).label('best_score'),
        db.func.count(GameScore.id).label('total_games')
    ).join(GameScore).group_by(User.id).order_by(db.func.min(GameScore.attempts)).all()
    
    return render_template('leaderboard.html', 
                         top_scores=top_scores,
                         user_rankings=user_best_scores,
                         current_user=current_user)

@app.route('/profile')
@login_required
def profile():
    # Get user's game history
    user_scores = GameScore.query.filter_by(user_id=current_user.id).order_by(GameScore.completed_at.desc()).limit(20).all()
    
    # Calculate statistics
    if user_scores:
        best_score = min(score.attempts for score in user_scores)
        avg_score = sum(score.attempts for score in user_scores) / len(user_scores)
    else:
        best_score = None
        avg_score = None
    
    # Get achievements
    achievements = get_user_achievements(current_user)
    
    return render_template('profile.html',
                         user_scores=user_scores,
                         best_score=best_score,
                         avg_score=avg_score,
                         total_games=len(user_scores),
                         achievements=achievements,
                         current_user=current_user)

@app.route('/share/achievement/<achievement_type>')
@login_required
def share_achievement(achievement_type):
    """Generate Facebook share URL for achievements"""
    base_url = request.url_root.rstrip('/')
    
    if achievement_type == 'best_score':
        best_score = current_user.get_best_score()
        if best_score:
            message = get_achievement_message(current_user, best_score)
            share_url = generate_facebook_share_url(message, f"{base_url}/leaderboard")
            return jsonify({'share_url': share_url, 'message': message})
    
    elif achievement_type == 'total_games':
        total_games = current_user.get_total_games()
        message = f"🎮 {current_user.username} has played {total_games} games on the Number Guessing Game! Join the fun and test your skills!"
        share_url = generate_facebook_share_url(message, base_url)
        return jsonify({'share_url': share_url, 'message': message})
    
    elif achievement_type == 'latest_win':
        latest_score = GameScore.query.filter_by(user_id=current_user.id).order_by(GameScore.completed_at.desc()).first()
        if latest_score:
            message = get_achievement_message(current_user, latest_score.attempts)
            share_url = generate_facebook_share_url(message, base_url)
            return jsonify({'share_url': share_url, 'message': message})
    
    # Default sharing
    message = f"🎯 Join {current_user.username} on the Number Guessing Game! Test your logic and compete with friends!"
    share_url = generate_facebook_share_url(message, base_url)
    return jsonify({'share_url': share_url, 'message': message})

if __name__ == '__main__':
    import os
    # Create database tables
    with app.app_context():
        db.create_all()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
