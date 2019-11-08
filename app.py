from flask import Flask, render_template, session, request
import random
import os
import pickle
import time

FNAME = "data/scores.pickle"

app = Flask(__name__)


@app.route("/game")
def generateNumber():
    session["start"] = time.perf_counter()
    session['randomNum'] = random.randint(0, 100)
    session["numOfAttempts"] = 0
    return render_template(
        "game.html",
        the_title="Game", 
        the_message = "Input a number between 0 - 100"
    )

@app.route("/guessResult", methods=["POST"])
def guessResult():
   guess = int(request.form["guess"])
   randomNumber = session['randomNum']
   message = ""
   attempts = session['numOfAttempts']
   attempts += 1
   session["numOfAttempts"] = attempts
   if guess == randomNumber:
       session["end"] = time.perf_counter() # wont count time as the player inputs their name here
       return render_template(
             "score.html",
              the_score = guess
       )
       pass
   elif guess > randomNumber:
       message = "The number you guessed was too high, guess another number between 1 and 1000"
       pass
   elif guess < randomNumber:
       message = "The number you guessed was too low, guess another number between 1 and 1000"
       pass
   #this call is a safety for if the code ever messed up and the ifs fail me
   
   return render_template(
           "game.html",
           the_title="Game",
           the_message = message
       )
   
 

@app.route("/recordhighscore", methods=["POST"])
def store_score():
    score = round(session["end"] - session["start"], 2)
    player_name = request.form["player"]
    attemps = session['numOfAttempts']
    if not os.path.exists(FNAME):
        data = []
    else:
        with open(FNAME, "rb") as pf:
            data = pickle.load(pf)
    data.append((score, player_name, attemps))  ## RACE CONDITION.
    with open(FNAME, "wb") as pf:
        pickle.dump(data, pf)

    return "Your highscore has been recorded."


@app.route("/highscores")
def show_scores():
    with open(FNAME, "rb") as pf:
        data = pickle.load(pf)
    return render_template(
        "winners.html",
        the_title="Here are the High Scores",
        the_data=sorted(data, reverse=True),
    )


app.secret_key = (
    " wen'0ut93u4t0934ut93u4t09 3u4t9 u3   40tuq349tun34#-9tu3#4#vetu #    -4"
)

app.run(debug=True)
