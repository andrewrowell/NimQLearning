# NimQLearning

I used a reinforcement learning technique called [Q-learning](https://towardsdatascience.com/simple-reinforcement-learning-q-learning-fcddc4b6fe56) to create a bot that can learn to play [Nim](https://en.wikipedia.org/wiki/Nim).

All the bot knows before learning:
* What moves it can make
* How many sticks are on the board

At the end of the game it receives a positive or negative reward, and then
applies that reward to its experience in the game to learn which moves are
best depending on what the state of the game is.

Because of the deterministic nature of Nim, it can quickly learn the game well
 enough to be impossible to beat.
 
## How to Run

You'll need matplotlib. To see how it plays against an opponent that chooses
random actions, you can just run `nim.py`. It will generate a chart,
`result.png`, that will show its win rate (using a rolling average).

You can find code at the bottom of `nim.py` that can be modified so that you
can play against the learner. If you let it play against the random opponent
first, you will lose, so turn that off if you want to see it learn the game
against you.
 
## Files
* `nim.py` - Play a number of games. Can be Q-Learner vs Random or Q-Learner vs
Human.
* `web/qnim.html` and `web/qnim.js` - In progress, javascript Q-Learner (for demo on web).

## To Do
* Finish javascript implementation
* Split classes into separate files
  * Learners.py, Game.py, etc. ?
* Add other learners (using neural net rather than table?)