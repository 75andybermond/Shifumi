from flask import Flask, render_template, request, session
import random
import cv2
import numpy as np
from 
app = Flask(__name__)
app.secret_key = 'key'

# Load the trained model
model = load_model('hand_gesture_model.h5')

@app.route('/play', methods=['POST'])
def play():
    # Capture an image from the user's webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    # Preprocess the image and pass it through the model to predict the hand gesture
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, (64, 64))
    image = np.expand_dims(image, axis=0)
    image = np.expand_dims(image, axis=3)
    prediction = model.predict(image)
    gesture = np.argmax(prediction)

    # Map the predicted gesture to rock, paper, or scissors
    if gesture == 0:
        user_choice = 'rock'
    elif gesture == 1:
        user_choice = 'paper'
    else:
        user_choice = 'scissors'

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

    # Render the result page with the result message, user's choice, and computer's choice
    return render_template('result.html',
                           result_message=result_message,
                           user_choice=user_choice,
                           computer_choice=computer_choice,
                           user_score=session['user_score'],
                           computer_score=session['computer_score'])

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
    if 'choice' not in request.form:
        return home()
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

    # Render the result page with the result message, user's choice, and computer's choice
    return render_template('result.html',
                           result_message=result_message,
                           user_choice=user_choice,
                           computer_choice=computer_choice,
                           user_score=session['user_score'],
                           computer_score=session['computer_score'])

@app.route('/reset', methods=['POST'])
def reset_scores():
    # Clear the session variables for the scores
    session['user_score'] = 0
    session['computer_score'] = 0
    
    # Redirect back to the home page
    return home()


if __name__ == '__main__':
    app.run(debug=True)
