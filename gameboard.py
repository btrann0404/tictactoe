import copy
import tkinter as tk

class BoardClass:
    # Initialization
    def __init__(self , username1 = '', username2 = '',lastuser = '', wins = 0, ties = 0, loss = 0):
        """BoardClass object initialization including player 1, player 2, last_user to make a move, win count, tie count, and loss count.
        This is to help keep track of the game's attirbutes, helpful to keep track of score and player names later on.
        Attributes:
            username1: Request Username of Player 1
            username2: Request Username of Player 2
            lastuser: Last User's Shape put down on the board
            wins = the incremented win count throughout the games automatically set to 0
            ties = the incremented tie count throughout the games automatically set to 0
            loss = the incremented loss count throughout the games automatically set to 0
            game_board = list containing 3 list that contains number 1 - 9 to keep track of moves through the game
        """
        self.setUsername1(username1)
        self.setUsername2(username2)
        self.setLastuser(lastuser)
        self.wins = wins
        self.ties = ties
        self.loss = loss
        self.game_board = [['1' ,'2' ,'3' ], ['4' ,'5' ,'6' ], ['7' ,'8' ,'9' ]]

    # Attribute Functions
    def setUsername1(self, username1: str) -> None:
        """Functions that changes the username1 attribute from the BoardClass object attribute
        Args:
            username1: username request to set in the attribute"""
        self.username1 = username1
    
    def setUsername2(self, username2: str) -> None:
        """Functions that changes the username1 attribute from the BoardClass object attribute
        Args:
            username2: username request to set in the attribute"""
        self.username2 = username2
    
    def setLastuser(self, lastuser: str) -> None:
        """Functions that changes the lastuser's shape attribute from the BoardClass object attribute
        Args:
            lastuser: lastuser's shape request to set in the attribute"""
        self.lastuser = lastuser

    def setWins(self, wins: int) -> None:
        """Functions that changes the win count attribute from the BoardClass object attribute
        Args:
            wins: the number request to change the win count to"""
        self.wins = wins
    
    def setTies(self, ties: int) -> None:
        """Functions that changes the tie count attribute from the BoardClass object attribute
        Args:
            ties: the number request to change the tie count to"""
        self.ties = ties
    
    def setLoss(self,loss: int):
        """Functions that changes the loss count attribute from the BoardClass object attribute
        Args:
            loss: the number request to change the loss count to"""
        self.loss = loss

    def getUsername1(self) -> str:
        """Retrives the information of player 1's user from the BoardClass object
        Return: 
            Returns the player 1's name that was set from the BoardClass object"""
        return str(self.username1)
    
    def getUsername2(self) -> str:
        """Retrives the information of player 2's user from the BoardClass object
        Return: 
            Returns the player 2's name that was set from the BoardClass object"""
        return str(self.username2)
    
    def getLastuser(self) -> str:
        """Retrives the information of the last player's shape from the BoardClass object
        Return: 
            Returns the player's last player's shape that was set from the BoardClass object"""
        return str(self.lastuser)

    def getWins(self) -> int:
        """Retrives the information of player's win count from the BoardClass object
        Return: 
            Returns the player's win count that set from the BoardClass object"""
        return self.wins
    
    def getTies(self) -> int:
        """Retrives the information of player's loss count from the BoardClass object
        Return: 
            Returns the player's loss count that set from the BoardClass object"""
        return self.ties

    def getLoss(self) -> int:
        """Retrives the information of player's loss count from the BoardClass object
        Return: 
            Returns the player's loss count that set from the BoardClass object"""
        return self.loss
    
    def incrementWins(self):
        self.wins += 1

    def incrementLoss(self):
        self.loss += 1

    def getBoard(self) -> list:
        """Retrives information for the board array assigned with the gameboard object and returns game board information
        Return:
            A list contains 3 list which information of the tic-tac-toe board helpful when keeping track and printing the list
        """
        return self.game_board
    
    # Normal Functions:
    def updateGamesPlayed(self) -> int:
        """Functions that keeps track of all games played
        Returns:
            the number of complete games played by adding all possible wins, losses, and ties
        """
        return int(self.getWins()) + int(self.getLoss()) + int(self.getTies())

    def resetGameBoard(self):
        """Reset's the gameboard to it's original state with list in list number through 1-9 with the numbers representing possible
        moves to play"""
        self.game_board = [['1' ,'2' ,'3' ], ['4' ,'5' ,'6' ], ['7' ,'8' ,'9' ]]

    def updateGameBoard(self, move: int) -> None: 
        """Changes the game board from the BoardClass attributes with player's intended move
        Args:
            move: a numbered move that player would want to place there shape into the gameboard to update
        """
        move = str(move)
        turn = str(self.getLastuser())
        for row in self.game_board:
            if move in row:
                x = row.index(move)
                row[x] = turn
    
    def countPieces(self) -> None:
        lst = []
        for row in self.game_board:
            for ele in row:
                if ele == 'x' or ele == 'o':
                    lst.append(ele)
        return len(lst)

    def isWinner(self, player, win_update = False) -> bool:
        """Checks the condition of the board if there are any winning moves on the board to stop any proceding moves.
        Args:
            player: The player shape's that you want to chck the win condition for
            win_update: Set automatically False, but if changes to True will gives the function the options to increment
            win count if one of the condition is met
        Return:
            A boolean expression which returns False if no conditions are met, but if condition is met will return True
        """
        win_con = False
        s = self.game_board
        for row in range(len(s)):
            if s[row - 1][0] == player and s[row - 1][1] == player and s[row - 1][2] == player:
                win_con = True
        for col in range(len(s)):
            if s[0][col - 1] == player and s[1][col - 1] == player and s[2][col - 1] == player:
                win_con = True
        if s[1][1] == player and s[0][-1] == player and s[-1][0] == player:
            win_con = True
        if s[1][1] == player and s[0][0] == player and s[-1][-1] == player:
            win_con = True
        if win_update == True:
            if win_con and player == 'x':
                self.wins += 1
            elif not win_con and player == 'x':
                self.loss += 1
            elif win_con and player == 'o':
                self.wins += 1
            elif not win_con and player == 'o':
                self.loss += 1
        return win_con

    def boardIsFull(self, tie_update = False) -> bool:
        """Checks the board's data and to see if all spots are filled on the board before proceeding to other moves.
        Args:
            tie_update: If set True gives the function the ability to alter the tie count if all position on the board 
            are filled
        Return:
            A boolean expression that returns True saying the board is not full and False saying the board is full.
        """
        i = 0
        for row in self.game_board:
            for ele in row:
                if ele.isnumeric():
                    i += 1
        if i == 0:
            if not self.isWinner('o') and not self.isWinner('x') and tie_update:
                self.ties += 1
            return False
        else:
            return True

    def computeStats(self, player = str ,lastplayer = str) -> None:
        """Prints the stats of each of the players from there usernames, games played, win count, loss count, and tie count
        Args: 
            Player: the requested player's stats that is wanted to print out 'p1' or 'p2'
            Lastplayer: recieves who the last player to make the move is from the last game
        """
        print('-------------------------')
        print('FINAL GAME STATS')
        print('-------------------------')
        print(f'Player 1: {str(self.getUsername1())}')
        print(f'Player 2: {str(self.getUsername2())}')
        print(f'Last to make move: {lastplayer}')
        print(f'Total Games: {self.updateGamesPlayed()}')
        if player == 'p1':
            print(f'Your Wins Count: {int(self.getWins())}')
            print(f'Your Losses Count: {int(self.getLoss())}')
        elif player == 'p2':
            print(f'Your Wins Count: {int(self.getLoss())}')
            print(f'Your Losses Count: {int(self.getWins())}')
        print(f'Your Tie Count: {int(self.getTies())}')
        print('-------------------------')

    def printBoard(self) -> None:
        """Prints the game board using the argument of the board data to print our a board without the numbers and better format that
        is easier on the eyes of the player playing the game
        Args:
            boarddata: the board information which is list of 3 list containing the information of the board
        """
        copy_board = copy.deepcopy(self.game_board)

        for index, row2 in enumerate(copy_board):
            for index2, ele in enumerate(row2):
                if ele.isnumeric():
                    row2[index2] = ' '
            row2 = ' | '.join(row2)
            print(row2)
            if index != 2:
                print( '- + - + -')

    def welcome(self) -> None:
        """Prints the welcome board showing the player's how place the move first by printing a board with an arrary from 1-9.
        """
        print('\n-------------------')
        print('LETS PLAY')
        print('-------------------\n')
        sample = [['1' ,'2' ,'3' ], ['4' ,'5' ,'6' ], ['7' ,'8' ,'9' ]]
        for index, row in enumerate(sample):
            row = ' | '.join(row)
            print(row)
            if index != 2:
                print( '- + - + -')
        print('Select a number 1-9 above to make your move!')
    
    def __str__(self) -> str:
        """Turns the class objects to a string form
        Returns: 
            the information of all the attributes of BoardClass in string format
        """
        return f'Username: {self.getUsername}, Lastuser: {self.getLastuser}, Wins: {self.getWins}, Ties: {self.getTies}, Loss: {self.getLoss}'
    
    def __int__(self) -> int:
        """Turns the class objects to a integer form
        Returns: 
            the information of all the attributes of BoardClass in string format
        """
        return int(self)


