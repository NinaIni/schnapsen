"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""
# Import the API objects
from api import State, util
import random

class Bot:

	__num_samples = -1
	__depth = -1

	def __init__(self, num_samples=2, depth=10):
		self.__num_samples = num_samples
		self.__depth = depth

	def get_move(self, state):

		# See if we're player 1 or 2
		player = state.whose_turn()

		# Get a list of all legal moves
		moves = state.moves()

		# Sometimes many moves have the same, highest score, and we'd like the bot to pick a random one.
		# Shuffling the list of moves ensures that.
		random.shuffle(moves)

		best_score = float("-inf")
		best_move = None

		scores = [0.0] * len(moves)

		for move in moves:
			for s in range(self.__num_samples):

				score = self.evaluate(state.next(move), player)

				if score > best_score:
					best_score = score
					best_move = move

		return best_move # Return the best scoring move

	def evaluate(self,
				 state,     # type: State
				 player     # type: int
			):
		# type: () -> float
		"""
		Evaluates the value of the given state for the given player
		:param state: The state to evaluate
		:param player: The player for whom to evaluate this state (1 or 2)
		:return: A float representing the value of this state for the given player. The higher the value, the better the
			state is for the player.
		"""

		score = 0.0

		for _ in range(self.__num_samples):

			st = state.clone()

			# Do some random moves
			for i in range(self.__depth):
				if st.finished():
					break

				st = st.next(random.choice(st.moves()))

			score += self.heuristic(st, player)

		return score/float(self.__num_samples)

	def heuristic(self, state, player):
		return util.ratio_points(state, player)