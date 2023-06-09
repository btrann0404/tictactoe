import socket
import tkinter as tk
from gameboard import BoardClass

class player2:
    def __init__(self):
        """player2 object intialization in order to keep track BoardClass object, socket connection, and tkinter GUI
        capable in multiple function. This would be helpful so that all function in the class have ability to use all 
        three in a single function.
        """
        self.board = BoardClass('user1', 'user2', 'o', 0, 0, 0)
        self.root = tk.Tk()
        self.errorList = []
        self.header = tk.StringVar()
        self.header.set(self.getHeader())

    def startGame(self) -> None:
        """Starting the GUI interface using tkinter and adjusting the format of the interface that will start the
        the mainloop of the whole interface.
        """
        self.root.title('Brandon\'s TTT Player 2')
        self.root.geometry("600x750")
        self.root.config(bg='#CBC3E3')
        label = tk.Label(self.root, text = "Brandon's Tic-Tac-Toe", font= ("Ariel", 26, "bold"), borderwidth=5, relief="solid", bg='#4C4E52')
        label.pack(padx = 20, pady = 20)
        
        self.login()

        self.root.mainloop()

    def login(self) -> None:
        """Will pop up a screen to ask for a IP Address and Port to join the server and will have an enter button
        to submit the IP Address and Port desire to use.
        """
        self.serverFrame = tk.Frame(self.root, bg='#4C4E52', relief="solid", borderwidth=2)
        self.serverFrame.pack()
        self.serverFrame.config(borderwidth=5, relief="solid")
        ip_label = tk.Label(self.serverFrame, text='Enter Host Address To Play On: ', bg='#4C4E52')
        ip_label.grid(row=0, column=0)
        self.serverIP = tk.Entry(self.serverFrame)
        self.serverIP.grid(row=0, column=1)

        port_label = tk.Label(self.serverFrame, text='Enter Port To Play On: ', bg='#4C4E52')
        port_label.grid(row=1, column=0)
        self.serverPort = tk.Entry(self.serverFrame)
        self.serverPort.grid(row=1, column=1)

        submitButton = tk.Button(self.serverFrame, text = 'Enter', command = self.getInfo, borderwidth=0)
        submitButton.grid(row=2, column=1)

    def getInfo(self) -> None:
        """Button command to test the validity of IP Address and Port. If an error occurs a message will pop that 
        will let the user know to try again.
        """
        try:
            self.root.update()
            self.run_server(self.serverIP.get(), int(self.serverPort.get()))
        except Exception as e:
            if len(self.errorList) == 0:
                errorMsg = tk.Label(self.root, text = 'Invalid Try Another Host Address and Port', bg='orange', fg='black', pady = 30, width = 30)
                errorMsg.pack()
                self.errorList.append(errorMsg)

    def run_server(self, host_address = str, host_port = int) -> None:
        """After creating server will wait for other player to join will appear to another page that will a function 
        for the username.
        Args:
            Args:
            host_address: the ip address the player would like to create the server with.
            host_port: the port address the player would like to create the server with.
        """
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.bind((host_address, host_port))
        servermsg = tk.Label(self.root, text = 'Created, Waiting for player to join...', bg = 'green', fg = 'black')
        servermsg.pack()
        for error in self.errorList:
                error.destroy()
        self.errorList = []
        srv.listen(5)
        self.root.update()
        self.connection, host_address = srv.accept()
        self.userLogin()
        self.showUserLogin()
        self.root.update()
        self.errorList = []
        servermsg.destroy()
        self.root.update()
        self.serverFrame.destroy()
        self.root.update()
        username2 = self.connection.recv(1024).decode('utf-8')
        self.board.setUsername2(username2)
        self.userIntro.config(text = f'Player 1\'s Username is {username2}\n Status: Enter Your Username', bg='#4C4E52')
        
    def showUserLogin(self) -> None:
        """Reveal the login interface to show the user.
        """
        self.userFrame.pack()
        self.root.update()

    def userLogin(self) -> None:
        """Username submission interface that will have an option to entry usename desired and message of the status
        the player is at when sending or waiting.
        """
        self.root.update()
        self.userFrame = tk.Frame(self.root, bg='#4C4E52', relief="solid", borderwidth=2)
        self.userEntry = tk.Label(self.userFrame, text='Enter Username: ', bg='#4C4E52')
        self.userEntry.grid(row=1, column=0)
        self.userEntry2 = tk.Entry(self.userFrame)
        self.userEntry2.grid(row=1, column=1)
        submitButton2 = tk.Button(self.userFrame, text = 'Enter', command = lambda: self.getUser())
        submitButton2.grid(row=2, column=1)
        self.userIntro = tk.Label(self.root, text = 'Status: Waiting For Player 1 Username', bg='#4C4E52')
        self.userIntro.pack()
        self.root.update()

    def getUser(self) -> None:
        """Retrieve the username desired from the player and check the validity of the username that will have no 
        special characters or space and preceed to retrieve the other player's username in order start the game. 
        If the username is invalid it will pop up an error to let the user know to try again.
        """
        username1 = self.userEntry2.get()
        if username1.isalnum():
            self.board.setUsername1(username1)
            self.connection.sendall(username1.encode('utf-8'))
            for error in self.errorList:
                error.destroy()
            self.errorList = []
            self.userFrame.destroy()
            self.userIntro.destroy()
            self.createBoard()
        else: 
            if len(self.errorList) == 0:
                errorMsg = tk.Label(self.root, text = 'Invalid Try Again\n(No Special Character / Spaces)', bg='orange', fg='black', pady = 30, width = 30)
                errorMsg.pack()
                self.errorList.append(errorMsg)

    def getHeader(self) -> str:
        """Will return the information for the header of the players, wins, losses, and ties to update throughtout the
        game.
        Return:
            Return a the following string in order to help display score when the game starts
        """
        return f'{self.board.getUsername1()}  VS  {self.board.getUsername2()}\n   Games: {self.board.updateGamesPlayed()}    Wins: {self.board.getWins()}   Losses: {self.board.getLoss()}   Ties: {self.board.getTies()}'

    def createBoard(self) -> None:
        """Will setup the interface for the user to play the game with Tic-Tac-Toe board with each button that will 
        make move on the Tic-Tac-Toe.
        """
        self.root.update()

        self.header.set(self.getHeader())

        self.status2 = tk.Label(self.root, textvariable = self.header, bg='white', borderwidth=2, relief='solid', fg = 'black', font= ("Ariel", 18, "bold"))
        self.status2.pack()

        self.status = tk.Label(self.root, text = f'Status: Waiting for {self.board.getUsername2()}\'s Move', bg='#4C4E52', font= ("Ariel", 16, "bold"))
        self.status.pack()

        self.gameframe = tk.Frame(self.root)
        self.gameframe.columnconfigure(0, weight = 1)
        self.gameframe.columnconfigure(1, weight = 1)
        self.gameframe.columnconfigure(2, weight = 1)
        self.board.setLastuser('o')
        self.labelList = {}

        self.space1 = tk.Button(self.gameframe, text = '', font=("Arial 60"), width=3, height = 2, command = lambda: self.buttonCommand(1))
        self.space1.grid(row = 0, column = 0, padx = 0, pady = 0)

        self.space2 = tk.Button(self.gameframe, text = '', font=("Arial 60"), width=3, height = 2, command = lambda: self.buttonCommand(2))
        self.space2.grid(row = 0, column = 1)

        self.space3 = tk.Button(self.gameframe, text = '', font=("Arial 60"), width=3, height = 2, command = lambda: self.buttonCommand(3))
        self.space3.grid(row = 0, column = 2)

        self.space4 = tk.Button(self.gameframe, text = '', font=("Arial 60"), width=3, height = 2, command = lambda: self.buttonCommand(4))
        self.space4.grid(row = 1, column = 0)

        self.space5 = tk.Button(self.gameframe, text = '', font=("Arial 60"), width=3, height = 2, command = lambda: self.buttonCommand(5))
        self.space5.grid(row = 1, column = 1)

        self.space6 = tk.Button(self.gameframe, text = '', font=("Arial 60"), width=3, height = 2, command = lambda: self.buttonCommand(6))
        self.space6.grid(row = 1, column = 2)

        self.space7 = tk.Button(self.gameframe, text = '', font=("Arial 60"), width=3, height = 2, command = lambda: self.buttonCommand(7))
        self.space7.grid(row = 2, column = 0)

        self.space8 = tk.Button(self.gameframe, text = '', font=("Arial 60"), width=3, height = 2, command = lambda: self.buttonCommand(8))
        self.space8.grid(row = 2, column = 1)

        self.space9 = tk.Button(self.gameframe, text = '', font=("Arial 60"), width=3, height = 2, command = lambda: self.buttonCommand(9))
        self.space9.grid(row = 2, column = 2)


        self.gameframe.pack(expand = False)
        self.root.update()

        if self.board.countPieces() % 2 == 0 and self.board.countPieces() == 0:
            self.root.update()
            self.getMove()

        self.endframe = tk.Frame(self.root, bg='#4C4E52', borderwidth= 5 , relief='solid')

        self.result = tk.Label(self.endframe, text = " ", bg='#4C4E52')
        self.result.pack()

        result2_msg = f'Waiting for {self.board.getUsername2()} To Play Again'
        self.result2 = tk.Label(self.endframe, text = result2_msg, bg='#4C4E52')
        self.result2.pack()

    def buttonCommand(self, space: int) -> None:
        """Button command for the Tic-Tac-Toe board and will configure the board on interface, update the internal
        BoardClass board to keep track and will check if the move a winning move or not before continuing.
        Args:
            space: an integer value correspond to the move that user would would like to make in order to
            update the board and such.
        Return:
            return none to break out of the function if theres a winning move from the function moveChecker.
        """
        if self.board.updateGamesPlayed() != 0:
            self.delete_endframe()
        turn = self.board.getLastuser()
        if self.board.countPieces() % 2 == 1:
            if space == 1 and (self.space1.cget('text') == '') and not self.moveChecker(2):
                self.space1.config(text = turn)
                self.makeMove(space)
                self.board.updateGameBoard(space)
                if self.moveChecker(2):
                    return
            elif space == 2 and (self.space2.cget('text') == '') and not self.moveChecker(2):
                self.space2.config(text = turn)
                self.makeMove(space)
                self.board.updateGameBoard(space)
                if self.moveChecker(2):
                    return
            elif space == 3 and (self.space3.cget('text') == '') and not self.moveChecker(2):
                self.space3.config(text = turn)
                self.makeMove(space)
                self.board.updateGameBoard(space)
                if self.moveChecker(2):
                    return
            elif space == 4 and (self.space4.cget('text') == '') and not self.moveChecker(2):
                self.space4.config(text = turn)
                self.makeMove(space)
                self.board.updateGameBoard(space)
                if self.moveChecker(2):
                    return
            elif space == 5 and (self.space5.cget('text') == '') and not self.moveChecker(2):
                self.space5.config(text = turn)
                self.makeMove(space)
                self.board.updateGameBoard(space)
                if self.moveChecker(2):
                    return
            elif space == 6 and (self.space6.cget('text') == '') and not self.moveChecker(2):
                self.space6.config(text = turn)
                self.makeMove(space)
                self.board.updateGameBoard(space)
                if self.moveChecker(2):
                    return
            elif space == 7 and (self.space7.cget('text') == '') and not self.moveChecker(2):
                self.space7.config(text = turn)
                self.makeMove(space)
                self.board.updateGameBoard(space)
                if self.moveChecker(2):
                    return
            elif space == 8 and (self.space8.cget('text') == '') and not self.moveChecker(2):
                self.space8.config(text = turn)
                self.makeMove(space)
                self.board.updateGameBoard(space)
                if self.moveChecker(2):
                    return
            elif space == 9 and (self.space9.cget('text') == '') and not self.moveChecker(2):
                self.space9.config(text = turn)
                self.makeMove(space)
                self.board.updateGameBoard(space)
                self.moveChecker(2)
            else: 
                return
            if not self.board.isWinner('o') and not self.board.isWinner('x') and type(space) == int:
                self.status.config(text = f'Status: Waiting for {self.board.getUsername2()}\'s Move')
                self.root.update()
                self.getMove()
                self.moveChecker(2)

    def show_endGame(self) -> None:
        """Reveals the option to play again after the games end including the outcome of the game.
        """
        self.endframe.pack()

    def yesResp(self) -> None:
        """yes button command that will activiate to reset everything in the board from the boardclass board internally
        to the interface UI board and will ask for the user to input a move in order to start the game.
        """
        if ('yesOut' not in self.labelList) and ('noOut' not in self.labelList):
            self.resetBoard()
            yesOut = tk.Label(self.endframe, text = "Reseted Board")
            yesOut.pack()
            self.labelList['yesOut'] = yesOut
            self.delete_endframe()
            self.root.update()
            if self.board.countPieces() % 2 == 0:
                self.getMove()
                self.root.update()
            self.root.update()


    def noResp(self) -> None:
        """no button command that will delete everything from the game and will activate the fucntion the will 
        start the game stats and will set a message to player 2 to let player 2 they don't want to play again.
        """
        if ('yesOut' not in self.labelList) and ('noOut' not in self.labelList):
            self.gameframe.destroy()
            self.endframe.destroy()
            self.delete_endframe()
            self.status.destroy()
            noOut = tk.Label(text = "Thanks for Playing!", font= ("Ariel", 22, "bold"), bg='#4C4E52', borderwidth = 5, relief="solid")
            self.header.set('Thanks For Playing!!')
            self.showStats()
            self.labelList['noOut'] = noOut

    def showStats(self) -> None:
        """Will print the final stats for the game such as player's usernames, total games, games won, games lost, games
        tied, and including a button to exit out the game.
        """
        self.statsFrame = tk.Frame(self.root, bg='#4C4E52', borderwidth = 2, relief="solid")
        self.statsFrame.pack()
        introStats = tk.Label(self.statsFrame, text = 'FINAL STATISTICS', font= ("Ariel", 18, "bold"), bg='#4C4E52')
        introStats.pack()
        user1 = tk.Label(self.statsFrame, text = f'Player 1 is {self.board.getUsername2()}', bg='#4C4E52', font= ("Ariel", 14, "bold"))
        user1.pack()
        user2 = tk.Label(self.statsFrame, text = f'Player 2 is {self.board.getUsername1()}', bg='#4C4E52',font= ("Ariel", 14, "bold"))
        user2.pack()
        totalgames = tk.Label(self.statsFrame, text = f'Total Games is {self.board.updateGamesPlayed()}', bg='#4C4E52', font= ("Ariel", 14, "bold"))
        totalgames.pack()
        loss = tk.Label(self.statsFrame, text = f'Games Won is {self.board.getWins()}', bg='#4C4E52', font= ("Ariel", 14, "bold"))
        loss.pack()
        wins = tk.Label(self.statsFrame, text = f'Games Lost is {self.board.getLoss()}', bg='#4C4E52', font= ("Ariel", 14, "bold"))
        wins.pack()
        ties = tk.Label(self.statsFrame, text = f'Games Tied is {self.board.getTies()}', bg='#4C4E52', font= ("Ariel", 14, "bold"))
        ties.pack()
        exitgame = tk.Button(self.statsFrame, text = 'Exit', command = lambda: self.exitGameButton())
        exitgame.pack()

    def exitGameButton(self) -> None:
        """Button command to exit out of the game when done looking at the stats or just wanting to exit it out.
        """
        self.statsFrame.destroy()
        self.root.destroy()

    def delete_endframe(self) -> None:
        """delete the ending frame to such as the yes and no option including the outcome of the game. 
        """
        self.endframe.pack_forget()
        for val in self.labelList.values():
            val.destroy()
        self.labelList.clear()

    def resetBoard(self) -> None:
        """resets the internal and external board to start a new game
        """
        self.board.resetGameBoard()
        self.space1.config(text = '')
        self.space2.config(text = '')
        self.space3.config(text = '')
        self.space4.config(text = '')
        self.space5.config(text = '')
        self.space6.config(text = '')
        self.space7.config(text = '')
        self.space8.config(text = '')
        self.space9.config(text = '')
        self.board.setLastuser('o')

    def waitingResp(self) -> None:
        """Will listen a response from player 1 to know whether are not to continue playing or not.
        """
        resp = self.connection.recv(1024).decode('utf-8')
        if resp == 'Play Again':
            self.yesResp()
        elif resp == 'Fun Times':
            self.noResp()

    def moveChecker(self, player: int) -> bool:
        """checks the moves validity and will update the header and pop up a play again option if there is winning 
        move or tied/ full board.
        Args:
            Player: Reference to which player 1 or 2 to get accurate output and score keeping
        Return:
            Return a booelan expression to see whether or no the board is valid or not to continue helpful for function
            to know whether to continue or not.
        """
        self.root.update()
        if player == 2 and self.board.isWinner('o'):
            if 'conLabel' not in self.labelList:
                msg = str(f'{self.board.getUsername1()} is the Winner!')
                self.board.isWinner('o', True)
                self.header.set(self.getHeader())
                self.show_endGame()
                self.result.config(text = msg)
                self.labelList['conLabel'] = tk.Label()
                self.root.update()
                self.waitingResp()
            return True
        elif player == 2 and self.board.isWinner('x'):
            if 'conLabel' not in self.labelList:
                msg = str(f'{self.board.getUsername2()} is the Winner!')
                self.board.isWinner('o', True)
                self.header.set(self.getHeader())
                self.show_endGame()
                self.result.config(text = msg)
                self.labelList['conLabel'] = tk.Label()
                self.root.update()
                self.waitingResp()
            return True
        elif not self.board.boardIsFull():
            if 'conLabel' not in self.labelList:
                msg = str('TIE GAME, FULL BOARD')
                self.board.boardIsFull(tie_update = True)
                self.header.set(self.getHeader())
                self.show_endGame()
                self.result.config(text = msg)
                self.labelList['conLabel'] = tk.Label()
                self.root.update()
                self.waitingResp()
            return True
        return False

    def playerSwitch(self) -> None:
        """Switch the players icon so if the player is x icon then the player will to an o icon and vice versa.
        """
        if 'x' == self.board.getLastuser():
            self.board.setLastuser('o')
        elif 'o' == self.board.getLastuser():
            self.board.setLastuser('x')

    def getMove(self) -> None:
        """Will recieve the move from the other player in order to make move on the internal and external board from
        the other player's side.
        """
        data = self.connection.recv(1024).decode('utf-8')
        self.playerSwitch()
        self.board.updateGameBoard(data)
        self.playerSwitch()
        if data == 'no play':
            self.noResp()
            return
        elif data == '1':
            self.space1.config(text = 'x')
        elif data == '2':
            self.space2.config(text = 'x')
        elif data == '3':
            self.space3.config(text = 'x')
        elif data == '4':
            self.space4.config(text = 'x')
        elif data == '5':
            self.space5.config(text = 'x')
        elif data == '6':
            self.space6.config(text = 'x')
        elif data == '7':
            self.space7.config(text = 'x')
        elif data == '8':
            self.space8.config(text = 'x')
        elif data == '9':
            self.space9.config(text = 'x')
        self.root.update()
        self.moveChecker(2)
        temp = f'Status: Make Your Move {self.board.getUsername1()}'
        self.status.config(text = temp)
        self.root.update()
    
    def makeMove(self, move: int) -> None:
        """Will send the move to the space to the other player through sockets and update the window.
        Args:
            move: integer value that will correspond to the move that the player would like to make sending it
            over to the other player.
        """
        move = str(move)
        move = move.encode()
        move = self.connection.sendall(move)
        self.root.update()

if __name__ == "__main__":
    p2 = player2()
    p2.startGame()

