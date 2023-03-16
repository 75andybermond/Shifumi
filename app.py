from flask import Flask, render_template, request, session
import random

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'key'


@app.route('/')
def home():
    # Initialize the score to 0 if it does not exist in the session
    # Initialize the user and computer scores to 0 if they do not exist in the session
    if 'user_score' not in session:
        session['user_score'] = 0
    if 'computer_score' not in session:
        session['computer_score'] = 0
    
    return render_template('home.html')
 

@app.route('/play', methods=['POST'])
def play():
    # Get the user's choice from the form data
    user_choice = request.form['choice']
    
    # Generate a random move for the computer
    moves = ['rock', 'paper', 'scissors']
    computer_choice = random.choice(moves)
    
    # Determine the result of the game
    if user_choice == computer_choice:
        result_message = "It's a tie!"
    elif user_choice == 'rock' and computer_choice == 'scissors' or \
         user_choice == 'paper' and computer_choice == 'rock' or \
         user_choice == 'scissors' and computer_choice == 'paper':
        result_message = "You win!"
            # Increase the score by 1 if the user wins
        session['user_score'] += 1
    else:
        result_message = "Computer wins!"
        # Increase the computer's score by 1 if the computer wins
        session['computer_score'] += 1

    # Save the result to a file
    with open('result.txt', 'w') as result_file:
        result_file.write(result_message)
        
    # Render the result page with the result message, user's choice, and computer's choice
    return render_template('result.html',
                           result_message=result_message,
                           user_choice=user_choice,
                           computer_choice=computer_choice,
                           user_score=session['user_score'],
                           computer_score=session['computer_score'])
@app.route('/result')
def display_result():
    # Read the saved result from the file
    with open('result.txt', 'r') as result_file:
        result_message = result_file.read()
    # Render a template with the saved result
    return render_template('display_result.html', result_message=result_message)

if __name__ == '__main__':
    app.run(debug=True)
