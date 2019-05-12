import random
import matplotlib.pyplot as plt

GRAPH_SMOOTHING = 20

GAME_SIZE = 10
ACTION_SPACE = [i for i in range(1,4)]

class Game:
    def __init__(self):
        self.sticks = GAME_SIZE

    def remove(self, count):
        self.sticks -= count
        if self.sticks <= 0:
            return True
        return False

    def getState(self):
        return self.sticks - 1

    def getReward(self):
        if self.sticks <= 0:
            return -1
        return 0

    def getActionSpace(self):
        return ACTION_SPACE

    def isOver(self):
        return self.sticks <= 0

# Q Learning Agent
class QLearner:
    def __init__(self):
        self.q = []
        for i in range(GAME_SIZE):
            self.q.append([0] * len(ACTION_SPACE))

    def getMove(self, state):
        # Pick action that the agent remembers having the best reward, on average.
        potential_actions = self.q[state]
        action_chosen = potential_actions.index(max(potential_actions))
        return action_chosen

    def learn(self, state, action, new_state, reward, is_over):
        if is_over:
            # If the game was over, new_state is not a valid state.
            # Remembers that doing "action" in "state" gave some reward.
            self.q[state][action] = reward
        else:
            # Remember that taking the given action in "state" lead to "new_state"
            # (whose value we may have an idea of) and gave some reward.
            self.q[state][action] = reward + sum(self.q[new_state]) / len(self.q[new_state])

# Opponent that just takes random actions.
class RandomOpponent:
    def __init__(self):
        return

    def getMove(self, state):
        return random.choice(Game().getActionSpace())

    def learn(self, state, action, new_state, reward, is_over):
        return

# Opponent that lets a human decide the moves.
class HumanOpponent:
    def __init__(self):
        return

    def getMove(self, state):
        return int(input("Sticks to remove? "))

    def learn(self, state, action, new_state, reward, is_over):
        return

def runTrial(learner, number_of_trials, opponent_learner_type, verbose, make_graph, print_q_values):
    q_wins = []

    opponent = opponent_learner_type()
    for _ in range(number_of_trials):
        want_to_exit = False
        game = Game()
        state = game.getState()
        if (verbose):
            print("Starting game with sticks " + str(game.sticks))
        while True:
            reward = 0
            if (verbose):
                print("Sticks left: " + str(game.getState() + 1))
            action = learner.getMove(state)
            move = game.getActionSpace()[action]
            if (verbose):
                print("Q chose to remove " + str(move))
            game.remove(move)
            if game.isOver():
                if (verbose):
                    print("Opponent won.")
                reward = -1
                q_wins.append(0)
            else:
                if (verbose):
                    print("Sticks left: " + str(game.getState() + 1))
                opponent_move = opponent.getMove(game.getState())
                if (opponent_move == -1):
                    want_to_exit = True
                    break
                game.remove(opponent_move)
                if game.isOver():
                    if (verbose):
                        print("Q-Learner won.")
                    reward = 0
                    q_wins.append(1)

            new_state = game.getState()
            learner.learn(state, action, new_state, reward, game.isOver())
            if (print_q_values):
                print(learner.q)
            state = new_state

            if (verbose):
                print("----------------------------")

            if game.isOver():
                break

        if want_to_exit:
            break


    if (make_graph):
        q_win_x = []
        q_win_y = []
        for x in range(GRAPH_SMOOTHING, len(q_wins)):
            values_to_average = q_wins[max(0, x - GRAPH_SMOOTHING):x+1]
            rolling_average = float(sum(values_to_average)) / len(values_to_average)
            q_win_y.append(rolling_average)
            q_win_x.append(x)
        plt.plot(q_win_x, q_win_y, label="Q-Learner Win Rate")
        plt.fill_between(q_win_x, 0, q_win_y, label="Q-Learner Win Rate")
        plt.show()



learner = QLearner()

# Train against a random opponent.
runTrial(learner, 100, RandomOpponent, False, True, False)

# Let human play against it.
runTrial(learner, 1000, HumanOpponent, True, False, False)