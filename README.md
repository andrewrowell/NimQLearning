# NimQLearning

I used a reinforcement learning technique called [Q-learning](https://towardsdatascience.com/simple-reinforcement-learning-q-learning-fcddc4b6fe56) to create a bot that can learn to play [Nim](https://en.wikipedia.org/wiki/Nim).

All the bot knows before learning:
* What moves it can make
* How many sticks are on the board

At the end of the game it receives a positive or negative reward, and then applies that reward to its experience in the game to learn which moves are best depending on what the state of the game is.

Fairly quickly, it can learn the game well enough to be impossible to beat.
