class TicTacToe:
    """
    A Tic-Tac-Toe game class
    """

    def __init__(self):
        """
        Creates an empty game
        """

        self.map = [' '] * 9
        self.moves = []
        self.winFunction = lambda winner: \
            print("The winner is {}".format(winner))
        self.winner = ' '

    def render(self):
        """
        Renders the current game in ASCII
        """

        print("{0}|{1}|{2}".format(self.map[0], self.map[1], self.map[2]))
        print("------")
        print("{0}|{1}|{2}".format(self.map[3], self.map[4], self.map[5]))
        print("------")
        print("{0}|{1}|{2}".format(self.map[6], self.map[7], self.map[8]))

    def play(self, player, pos):
        """
        Make a move for a specified player

        Args:
            player (str): The player making the move
            pos (int): The location for the player

        Raises:
            Exception: Illegal player if you have sent a player other than X or O

        Returns:
            bool: If the move is valid it will return True, False otherwise
        """

        if not (player == 'O' or player == 'X'):
            raise Exception("Illegal player {}".format(player))

        if self.map[pos] == ' ':
            self.map[pos] = player
            self.moves.append(
                {
                    "pos": pos,
                    "player": player
                }
            )
            self.winner = self.check_win()
            if self.winner != ' ':
                self.winFunction(self.winner)
            return True
        else:
            return False

    def check_win(self):
        """
        Checks if there is a winner for the current game

        Returns:
            str: Returns the winner of the game or a blank space if there is no winner
        """

        for i in range(3):
            # Vertical
            if self.map[i] != ' ':
                if self.map[i] == self.map[i + 3] and self.map[i + 3] == self.map[i + 6]:
                    return self.map[i]
            # Horizontal
            if self.map[i * 3] != ' ':
                if self.map[i * 3] == self.map[i * 3 + 1] and self.map[i * 3 + 1] == self.map[i * 3 + 2]:
                    return self.map[i]
        # Diagonal
        if self.map != ' ' and self.map[0] == self.map[4] and self.map[4] == self.map[8]:
            return self.map[0]
        if self.map != ' ' and self.map[2] == self.map[4] and self.map[4] == self.map[6]:
            return self.map[2]
        return ' '

    def quiet_copy(self):
        """
        Makes a copy of the current game

        Returns:
            TicTacToe: A copy of the current game
        """

        tictactoe = TicTacToe()
        tictactoe.map = self.map.copy()
        tictactoe.winFunction = lambda x: x
        tictactoe.winner = tictactoe.check_win()
        return tictactoe

    @staticmethod
    def other_player(current_player):
        """Gets the opponent player

        Args:
            current_player (str): The current player

        Returns:
            str: The opponent
        """

        if current_player == 'X':
            return 'O'
        if current_player == 'O':
            return 'X'


def check_branch(max_depth, current_game, current_player, win_player, depth=1):
    """
    Brute forcing a branch of possible moves

    Args:
        max_depth (int): Max moves the algorithm can think up ahead
        current_game (TicTacToe): The current game
        current_player (str): The current player
        win_player (str): The player who should win
        depth (int, optional): The current depth. Defaults to 1.

    Returns:
        float: The score of the current branch
    """

    if max_depth == 0:
        return 10 ** -depth
    if current_game.winner == win_player:
        return 20 ** -depth
    if current_game.winner != ' ':
        return -25 ** -depth
    r = 0
    for i in range(9):
        game_copy = current_game.quiet_copy()
        if not game_copy.play(current_player, i):
            continue
        r += check_branch(max_depth - 1, game_copy, TicTacToe.other_player(current_player), win_player, depth + 1)
    return r


def play_bot(current_game):
    """
    The bot logic

    Args:
        current_game (TicTacToe): The current game

    Returns:
        int: The bot move
    """
    # Bot logic
    branch_wins = [0] * 9
    for i in range(9):
        game_copy = current_game.quiet_copy()
        if not game_copy.play(player, i):
            branch_wins[i] = -10000000
            continue
        branch_wins[i] = check_branch(7, game_copy, TicTacToe.other_player(player), player)

    max_element = -1
    max_index = -1
    for i in range(9):
        if branch_wins[i] > max_element:
            max_element = branch_wins[i]
            max_index = i
    return max_index

# game = TicTacToe()
# player = 'X'
# while game.winner == ' ':
#     game.render()
#     play = int(input("Where to write a {}: ".format(player)))
#     game.play(player, play)
#     player = TicTacToe.other_player(player)
# game.render()


game = TicTacToe()
player = 'X'

good_play = play_bot(game)
game.play(player, good_play)

player = TicTacToe.other_player(player)

while game.winner == ' ':
    game.render()
    play = int(input("Where to write a {}: ".format(player))) - 1
    game.play(player, play)
    player = TicTacToe.other_player(player)

    good_play = play_bot(game)
    game.play(player, good_play)

    player = TicTacToe.other_player(player)
game.render()
