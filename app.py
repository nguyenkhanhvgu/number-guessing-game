from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'number-guessing-game-secret-key-2025'

@app.route('/')
def index():
    if 'target_number' not in session:
        session['target_number'] = random.randint(1, 100)
        session['attempts'] = 0
        session['game_over'] = False
        session['message'] = "I'm thinking of a number between 1 and 100. Can you guess it?"
        session['message_type'] = "info"
    
    return render_template('index.html',
                         attempts=session.get('attempts', 0),
                         message=session.get('message', ''),
                         message_type=session.get('message_type', 'info'),
                         game_over=session.get('game_over', False))

@app.route('/guess', methods=['POST'])
def guess():
    try:
        user_guess = int(request.form['guess'])
        target = session['target_number']
        session['attempts'] += 1
        
        if user_guess == target:
            session['message'] = f"🎉 Congratulations! You guessed it in {session['attempts']} attempts!"
            session['message_type'] = "success"
            session['game_over'] = True
        elif user_guess < target:
            session['message'] = f"Too low! Try a higher number."
            session['message_type'] = "warning"
        else:
            session['message'] = f"Too high! Try a lower number."
            session['message_type'] = "warning"
            
    except ValueError:
        session['message'] = "Please enter a valid number!"
        session['message_type'] = "error"
    
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
