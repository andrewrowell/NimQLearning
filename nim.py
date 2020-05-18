import random
import matplotlib.pyplot as plt

# Window size for rolling average in win rate graph
GRAPH_SMOOTHING = 5

# Number of sticks
GAME_SIZE = 10

# Max number of sticks that can be removed in a single turn
MAX_STICKS_REMOVABLE = 3

ACTION_SPACE = [i for i in range(1,MAX_STICKS_REMOVABLE + 1)]

class Game:
    '''
    Keeps track of the game state.
    '''
    def __init__(self):
        '''
        Sets the initial number of sticks.
        '''
        self.sticks = GAME_SIZE

    def remove(self, count):
        '''
        Remove a number of sticks from the board.
        :param count: Number of sticks to remove.
        '''
        self.sticks -= count

    def getState(self):
        '''
        Converts the number of sticks to a "state id" for the learner.
        :return: state id.
        '''
        return self.sticks - 1

    def getActionSpace(self):
        '''
        :return: Possible actions in the game.
        '''
        return ACTION_SPACE

    def isOver(self):
        '''
        :return: True if all sticks have been removed and the game is "done".
        '''
        return self.sticks <= 0

class QLearner:
    '''
    Tabular Q Learner.

    Keeps track of every possible state of the game, and determines the
    expected value of any move in any state. Eventually builds up enough
    data to choose the optimal action in any state.

    The learner is not aware of the rules, goals, or other player's
    decision process. It operates solely based on game state, available
    actions, and positive/negative rewards depending on win/loss.
    '''

    def __init__(self):
        '''
        Initialize the Q-Table
        '''
        self.q = []
        for i in range(GAME_SIZE):
            self.q.append([0] * len(ACTION_SPACE))

    def getMove(self, state):
        '''
        Pick action with the best expected value.
        :param state: Game state.
        :return: Chosen action.
        '''
        potential_actions = self.q[state]
        action_chosen = potential_actions.index(max(potential_actions))
        return action_chosen

    def learn(self, state, action, new_state, reward, is_over):
        '''
        Add new information about the game to the table.

        :param state: Original state before move.
        :param action: Move chosen.
        :param new_state: State of game after opponent's move.
        :param reward: Reward to assign to the action.
        :param is_over: Whether the game is over or not.
        '''
        if is_over:
            # If the game was over, new_state is not a valid state.
            # Remembers that doing "action" in "state" gave some reward.
            self.q[state][action] = reward
        else:
            # Remember that taking the given action in "state" lead to "new_state"
            # (whose value we may have an idea of) and gave some reward.
            self.q[state][action] = reward + sum(self.q[new_state]) / len(self.q[new_state])

class RandomOpponent:
    '''
    Opponent that just takes random actions.
    '''

    def __init__(self):
        return

    def getMove(self, state):
        '''
        Choose random action from the action space.
        '''
        return random.choice(Game().getActionSpace())

    def learn(self, state, action, new_state, reward, is_over):
        return

class HumanOpponent:
    '''
    Opponent that lets a human decide the moves.
    '''
    def __init__(self):
        return

    def getMove(self, state):
        return int(input("Sticks to remove? "))

    def learn(self, state, action, new_state, reward, is_over):
        return

def runTrial(learner, number_of_trials, opponent_learner_type, verbose, make_graph, print_q_values):
    '''
    Play multiple games.
    :param learner: Player that learns.
    :param number_of_trials:
    :param opponent_learner_type:
    :param verbose:
    :param make_graph:
    :param print_q_values:
    :return:
    '''
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
        plt.title("Win Rate (Rolling Window Size = " + str(GRAPH_SMOOTHING) +" Games)")
        plt.savefig("result.png")



learner = QLearner()

# Train against a random opponent.
runTrial(learner, 100, RandomOpponent, False, True, False)

# Let human play against it.
#runTrial(learner, 5, HumanOpponent, True, True, True)
