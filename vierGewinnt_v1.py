import random
import time
import math

class Connect_vier:
    def __init__(self):
        self.spielfeld = {1: [" ", " ", " ", " ", " ", " ", " "], 2: [" ", " ", " ", " ", " ", " ", " "], 3: [" ", " ", " ", " ", " ", " ", " "],
                          4: [" ", " ", " ", " ", " ", " ", " "], 5: [" ", " ", " ", " ", " ", " ", " "], 6: [" ", " ", " ", " ", " ", " ", " "]}
        self.player = "X"
        self.computer = "O"
        self.draw(self.spielfeld)
        self.zaehler = 0
        self.table_of_moves = {}

    def draw(self, spielfeld):
        for key in spielfeld.keys():
            print(spielfeld[key])
        print(" [1]  [2]  [3]  [4]  [5]  [6]  [7]")
        print("")

    def player_move(self):
        try:
            self.move = int(input(f"{self.player} wähle eine Spalte (1 - 7): "))
        except ValueError:
            print("INVALID MOVE!")
            self.player_move()
        print("")

        if self.valid_move(self.spielfeld, self.move):
            self.move = self.make_move(self.spielfeld, self.move)
            self.spielfeld[int(self.move[0])][int(self.move[1])] = self.player
            self.draw(self.spielfeld)
            if self.has_won():
                exit()
        else:
            print(f"{self.move} - Invalid move!")
            self.draw(self.spielfeld)
            self.player_move()

    def computer_move(self):
        self.start_time = time.time()
        bestScore = -1000000000
        bestMove = 0
        for i in range(1, 8):
            if self.valid_move(self.spielfeld, i):
                move = self.make_move(self.spielfeld, i)
                self.spielfeld[int(move[0])][int(move[1])] = self.computer
                score = self.minimax(self.spielfeld, 7, -math.inf, math.inf, False)
                self.spielfeld[int(move[0])][int(move[1])] = " "
                print("Moves bis jetzt berechnet:", self.zaehler)
                if score > bestScore:
                    bestScore = score
                    bestMove = move

        if bestMove == 0:  # falls egal welcher move eine Niederlage ist
            for i in range(1, 7):
                if self.valid_move(self.spielfeld, i):
                    move = self.make_move(self.spielfeld, i)
                    print(f"war nurnoch random übrig - Spalte [{int(move[1]) + 1}]]")
                    self.spielfeld[int(move[0])][int(move[1])] = self.computer
                    break
        else:
            self.spielfeld[int(bestMove[0])][int(bestMove[1])] = self.computer
            print(f"AI wählt Spatle: [{int(bestMove[1]) + 1}] und Zeile: {bestMove[0]}")
            print("Bestscore: ", bestScore)
        self.draw(self.spielfeld)
        if self.check_win(self.spielfeld, self.computer):
            print("AI hat gewonnen!!!!")
            exit()

        self.end_time = time.time()
        print(f"Anzahl der berechneten Züge: {self.zaehler} und benötigte Zeit: {round(self.end_time - self.start_time, 2)} sek.")
        self.zaehler = 0

    def make_move(self, spielfeld, move):
        if self.valid_move(spielfeld, move):
            for i in range(6, 0, -1):
                if spielfeld[i][move - 1] == " ":
                    ergebnis = str(i) + str(move - 1)
                    return ergebnis

    def valid_move(self, spielfeld, move):
        if move > 0 and move < 8:
            # checkt oberste Zelle
            if spielfeld[1][move - 1] == " ":
                return True
        else:
            return False

    def check_draw(self):
        for key in self.spielfeld.keys():
            if " " in self.spielfeld[key]:
                return True
        return False

    def check_win(self, spielfeld, x_or_o):
        # waagerecht win
        for key in self.spielfeld.keys():
            for i in range(0, 4):
                try:
                    if self.spielfeld[key][i] == x_or_o and spielfeld[key][i+ 1] == x_or_o and spielfeld[key][i+ 2] == x_or_o and spielfeld[key][i+ 3] == x_or_o:
                        return True
                except IndexError:
                    continue
        # win senkrecht
        for i in range(0, 7):
            for x in range(1, 4):
                if spielfeld[x][i] == x_or_o and spielfeld[x + 1][i] == x_or_o and spielfeld[x + 2][i] == x_or_o and spielfeld[x + 3][i] == x_or_o:
                    return True

        # win schräg links oben nach rechts unten
        for x in range(1, 4):
            for i in range(1, 5):
                if spielfeld[x][i - 1] == x_or_o and spielfeld[x + 1][i] == x_or_o and spielfeld[x + 2][i + 1] == x_or_o and spielfeld[x + 3][i + 2] == x_or_o:
                    return True

        # win schräg links unten nach rechts oben
        for x in range(6, 3, -1):
            for i in range(1, 5):
                if spielfeld[x][i - 1] == x_or_o and spielfeld[x - 1][i] == x_or_o and spielfeld[x - 2][i + 1] == x_or_o and spielfeld[x - 3][i + 2] == x_or_o:
                    return True

    def has_won(self):
        if self.check_win(self.spielfeld, self.player):
            print("Glückwunsch --Player-- hat gewonnen!")
            return True
        elif self.check_win(self.spielfeld, self.computer):
            print("AI hat gewonnen!")
            return True
        elif not self.check_draw():
            print("Schade unentschieden!")
            return True
        return False

    def scores_return(self, spielfeld, x_or_o):
        gesamtscore = 0

        # zuerst in die mitte dann gibt 4 Puntke
        for key in spielfeld:
            if spielfeld[key][3] == x_or_o:
                gesamtscore += 3

        # vergibt waagerecht Punkte
        for key in spielfeld:
            for i in range(0, 4):
                window = [spielfeld[key][i], spielfeld[key][i + 1], spielfeld[key][i + 2], spielfeld[key][i + 3]]
                if window.count(x_or_o) == 2:
                    gesamtscore += 2
                if window.count(x_or_o) == 3 and window.count(" ") == 1:
                    gesamtscore += 10

        # vergibt senkrecht Punkte
        for i in range(6, 3, -1):
            for x in range(0, 6):
                if spielfeld[i][x] == spielfeld[i - 1][x] and spielfeld[i][x] != " ":
                    if spielfeld[i][x] == x_or_o:
                        gesamtscore += 2
                # 3
                if spielfeld[i][x] == spielfeld[i - 1][x] and spielfeld[i - 1][x] == spielfeld[i - 2][x] and \
                        spielfeld[i][x] != " ":
                    if spielfeld[i - 3][x] == " " and spielfeld[i][x] == x_or_o:
                        gesamtscore += 10

        # 2 Punkte wenn schräg links oben nach rechts unten
        for x in range(1, 6):
            for i in range(0, 6):
                if spielfeld[x][i] == spielfeld[x + 1][i + 1] and spielfeld[x][i] != " ":
                    if spielfeld[x][i] == x_or_o:
                        gesamtscore += 2

        # 10 Punkte wenn schräg links oben nach rechts unten
        for x in range(1, 4):
            for i in range(0, 4):
                if spielfeld[x][i] == spielfeld[x + 1][i + 1] and spielfeld[x + 1][i + 1] == spielfeld[x + 2][i + 2] and \
                        spielfeld[x][i] != " ":
                    if spielfeld[x + 3][i + 3] == " " and spielfeld[x][i] == x_or_o:
                        gesamtscore += 10

        # 2 Punkte wenn links unten nach rechts ob
        for x in range(6, 2, -1):
            for i in range(0, 6):
                if spielfeld[x][i] == spielfeld[x - 1][i + 1] and spielfeld[x][i] != " ":
                    if spielfeld[x][i] == x_or_o:
                        gesamtscore += 2

        # 10 Punkte wenn links unten nach rechts ob
        for x in range(6, 3, -1):
            for i in range(0, 4):
                if spielfeld[x][i] == spielfeld[x - 1][i + 1] and spielfeld[x - 1][i + 1] == spielfeld[x - 2][i + 2] and \
                        spielfeld[x][i] != " ":
                    if spielfeld[x - 3][i + 3] == " " and spielfeld[x][i] == x_or_o:
                        gesamtscore += 10

        if x_or_o == self.player:
            gesamtscore = (gesamtscore * -1)
        return gesamtscore

    def minimax(self, spielfeld, tiefe, alpha, beta, isMaxemising):
        self.zaehler += 1
        if self.check_win(spielfeld, self.player):
            return -10000000000
        if self.check_win(spielfeld, self.computer):
            return 10000000000
        elif tiefe == 0:
            if isMaxemising:
                x = self.computer
            else:
                x = self.player
            return self.scores_return(spielfeld, x)

        # transposition table
        if str(spielfeld) in self.table_of_moves:
            if self.table_of_moves[str(spielfeld)]["tiefe"] >= tiefe:
                return self.table_of_moves[str(spielfeld)]["score"]

        if isMaxemising:
            bestScore = -100000000
            for i in range(1, 8):
                if self.valid_move(spielfeld, i):
                    move = self.make_move(spielfeld, i)
                    spielfeld[int(move[0])][int(move[1])] = self.computer
                    score = self.minimax(spielfeld, tiefe - 1, alpha, beta, False)
                    self.table_of_moves[str(spielfeld)] = {"score": score, "tiefe": tiefe}
                    spielfeld[int(move[0])][int(move[1])] = " "
                    if score > bestScore:
                        bestScore = score
                    alpha = max(alpha, bestScore)
                    if beta <= alpha:
                        break
            return bestScore
        else:
            bestScore = 100000000
            for i in range(1, 8):
                if self.valid_move(spielfeld, i):
                    move = self.make_move(spielfeld, i)
                    spielfeld[int(move[0])][int(move[1])] = self.player
                    score = self.minimax(spielfeld, tiefe - 1, alpha, beta, True)
                    self.table_of_moves[str(spielfeld)] = {"score": score, "tiefe": tiefe}
                    spielfeld[int(move[0])][int(move[1])] = " "
                    if score < bestScore:
                        bestScore = score
                    beta = min(score, beta)
                    if beta <= alpha:
                        break
            return bestScore

vier_gewinnt = Connect_vier()
while not vier_gewinnt.has_won():
    vier_gewinnt.computer_move()
    vier_gewinnt.player_move()




