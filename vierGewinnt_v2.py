import random
import time
import math
import pygame

class Connect_vier:
    def __init__(self):
        self.board_x = 0b00000000_0000000_0000000_0000000_0000000_0000000_0000000_0000000_0000000  # 64 Bit
        self.board_o = 0b00000000_0000000_0000000_0000000_0000000_0000000_0000000_0000000_0000000  # 64 Bit
        self.player = "X"
        self.computer = "O"
        self.zaehler = 0
        self.transposition_table = {}

    def player_move(self, position):
        self.board_x = self.board_x | (1 << self.make_move(position, self.board_x, self.board_o))

    def computer_move(self):
        self.start_time = time.time()
        bestScore = -1000000000
        bestMove = 0
        for i in range(1, 8):
            if self.valid_move(self.board_x, self.board_o, i):
                pos = self.make_move(i, self.board_x, self.board_o)
                if pos != True:
                    self.board_o |= 1 << pos
                    score = self.minimax(self.board_x, self.board_o, 10, -math.inf, math.inf, False)
                    self.board_o = self.board_o & ~(1 << pos)
                    print(f"{self.zaehler} Züge für i - {i} bis jetzt berechnet")
                    print("score: ", score)
                    if score > bestScore:
                        bestScore = score
                        bestMove = i

        # macht den besten Move
        if bestMove == 0:
            while True:
                bestMove = random.choice([1, 2, 3, 4, 5, 6, 7])
                if self.valid_move(self.board_x, self.board_o, bestMove):
                    print("war nurnoch random übrig")
                    break
        self.board_o = self.board_o | (1 << self.make_move(bestMove, self.board_x, self.board_o))
        self.end_time = time.time()
        print("Bestscore: ", bestScore)
        print(f"Anzahl der berechneten Züge: {self.zaehler} und benötigte Zeit: {round(self.end_time - self.start_time, 2)} sek.")
        self.zaehler = 0

    def valid_move(self, board_x, board_o, col):
        # Überprüfen, ob die oberste Reihe im angegebenen Col noch nicht voll ist und die Position innerhalb des Boards liegt
        if (board_x & (1 << ((col - 1) * 7 + 5))) == 0 and (board_o & (1 << ((col - 1) * 7 + 5))) == 0:
            return True
        else:
            return False

    def make_move(self, col, board_x, board_o):
        # Ermitteln der nächsten freien Position im angegebenen Col
        liste_leere_pos = [6, 13, 20, 27, 34, 41, 48]
        for row in range(0, 7):
            position = row + ((col - 1) * 7)
            if position >= 0 and position <= 48:
                if position not in liste_leere_pos:
                    if (board_x & (1 << position)) == 0 and (board_o & (1 << position)) == 0:
                        return position
        return True

    def check_draw(self, board_x, board_o):
        if board_x | board_o == 0b00000000_0000000_0111111_0111111_0111111_0111111_0111111_0111111_0111111:
            return True

    def check_win(self, board):
        # Überprüfen, ob einer der Spieler gewonnen hat
        if (board & (board >> 6) & (board >> 12) & (board >> 18) != 0):  # diagonal \
            return True
        elif (board & (board >> 8) & (board >> 16) & (board >> 24) != 0):  # diagonal /
            return True
        elif (board & (board >> 7) & (board >> 14) & (board >> 21) != 0):  # horizontal -
            return True
        elif (board & (board >> 1) & (board >> 2) & (board >> 3) != 0):  # vertikal |
            return True
        else:
            return False

    def scores_return(self, board_x, board_o, x_or_o):
        gesamtscore = 0
        bitboard = board_x if x_or_o == "X" else board_o
        bitboard_gegner = board_o if x_or_o == "X" else board_x

        # Zusätzliche Bewertung für die Mitte des Spielfelds
        positions = [21, 22, 23, 24, 25, 26]
        gesamtscore += 3 * sum(((bitboard >> position) & 1) for position in positions)

        # Horizontale Linien
        if bitboard & (bitboard >> 7) != 0:
            gesamtscore += 2
        if (bitboard & 1) == 0 and (bitboard_gegner & 1) == 0:
            if (bitboard >> 7) & (bitboard >> 14) & (bitboard >> 21) != 0:
                gesamtscore += 10
        if (bitboard >> 7) & 1 == 0 and (bitboard_gegner >> 7) & 1 == 0:
            if (bitboard & 1) & (bitboard >> 14) & (bitboard >> 21) != 0:
                gesamtscore += 10
        if (bitboard >> 14) & 1 == 0 and (bitboard_gegner >> 14) & 1 == 0:
            if (bitboard >> 7) & (bitboard & 1) & (bitboard >> 21) != 0:
                gesamtscore += 10
        if (bitboard >> 21) & 1 == 0 and (bitboard_gegner >> 21) & 1 == 0:
            if bitboard & (bitboard >> 7) & (bitboard >> 14) != 0:
                gesamtscore += 10

        # Vertikale Linien
        if bitboard & (bitboard >> 1) != 0:
            gesamtscore += 2
        if (bitboard & 1) == 0 and (bitboard_gegner & 1) == 0:
            if (bitboard >> 1) & (bitboard >> 2) & (bitboard >> 3) != 0:
                gesamtscore += 10
        if (bitboard >> 1) & 1 == 0 and (bitboard_gegner >> 1) & 1 == 0:
            if (bitboard & 1) & (bitboard >> 2) & (bitboard >> 3) != 0:
                gesamtscore += 10
        if (bitboard >> 2) & 1 == 0 and (bitboard_gegner >> 2) & 1 == 0:
            if (bitboard & 1) & (bitboard >> 1) & (bitboard >> 3) != 0:
                gesamtscore += 10
        if (bitboard >> 3) & 1 == 0 and (bitboard_gegner >> 3) & 1 == 0:
            if bitboard & (bitboard >> 1) & (bitboard >> 2) != 0:
                gesamtscore += 10

        # Diagonale Linien \
        if bitboard & (bitboard >> 6) != 0:
            gesamtscore += 2
        if (bitboard & 1) == 0 and (bitboard_gegner & 1) == 0:
            if (bitboard >> 6) & (bitboard >> 12) & (bitboard >> 18) != 0:
                gesamtscore += 10
        if (bitboard >> 6) & 1 == 0 and (bitboard_gegner >> 6) & 1 == 0:
            if (bitboard & 1) & (bitboard >> 12) & (bitboard >> 18) != 0:
                gesamtscore += 10
        if (bitboard >> 12) & 1 == 0 and (bitboard_gegner >> 12) & 1 == 0:
            if (bitboard & 1) & (bitboard >> 6) & (bitboard >> 18) != 0:
                gesamtscore += 10
        if (bitboard >> 18) & 1 == 0 and (bitboard_gegner >> 18) & 1 == 0:
            if bitboard & (bitboard >> 6) & (bitboard >> 12) != 0:
                gesamtscore += 10

        # Diagonale Linien /
        if bitboard & (bitboard >> 8) != 0:
            gesamtscore += 2
        if (bitboard & 1) == 0 and (bitboard_gegner & 1) == 0:
            if (bitboard >> 8) & (bitboard >> 16) & (bitboard >> 24) != 0:
                gesamtscore += 10
        if (bitboard >> 8) & 1 == 0 and (bitboard_gegner >> 8) & 1 == 0:
            if (bitboard & 1) & (bitboard >> 16) & (bitboard >> 24) != 0:
                gesamtscore += 10
        if (bitboard >> 16) & 1 == 0 and (bitboard_gegner >> 16) & 1 == 0:
            if (bitboard & 1) & (bitboard >> 8) & (bitboard >> 24) != 0:
                gesamtscore += 10
        if (bitboard >> 24) & 1 == 0 and (bitboard_gegner >> 24) & 1 == 0:
            if bitboard & (bitboard >> 8) & (bitboard >> 16) != 0:
                gesamtscore += 10

        if x_or_o == self.player:
            gesamtscore = (gesamtscore * -1)
        return gesamtscore

    def get_valid_movers(self, board_x, board_o):
        valid_moves = []
        for i in range(1, 8):
            if self.valid_move(board_x, board_o, i):
                valid_moves.append(i)
        return valid_moves

    def minimax(self, board_x, board_o, tiefe, alpha, beta, isMaxemising):
        self.zaehler += 1
        # transposition table
        if (board_x, board_o, tiefe) in self.transposition_table:
            return self.transposition_table[(board_x, board_o, tiefe)]

        x = self.computer if isMaxemising else self.player
        if self.check_win(board_x):
            return -10000000000
        if self.check_win(board_o):
            return 10000000000
        elif tiefe == 0:
            return self.scores_return(board_x, board_o, x)

        if isMaxemising:
            bestScore = -100000000
            valid_moves = self.get_valid_movers(board_x, board_o)
            for i in valid_moves:
                pos = self.make_move(i, board_x, board_o)
                if pos is not False:
                    board_o |= 1 << pos
                    score = self.minimax(board_x, board_o, tiefe - 1, alpha, beta, False)
                    board_o = board_o & ~(1 << pos)
                    bestScore = max(bestScore, score)
                    alpha = max(alpha, bestScore)
                    if beta <= alpha:
                        break
            self.transposition_table[(board_x, board_o, tiefe)] = bestScore
            return bestScore
        else:
            bestScore = 100000000
            valid_moves = self.get_valid_movers(board_x, board_o)
            for i in valid_moves:
                pos = self.make_move(i, board_x, board_o)
                if pos is not False:
                    board_x |= 1 << pos
                    score = self.minimax(board_x, board_o, tiefe - 1, alpha, beta, True)
                    board_x = board_x & ~(1 << pos)
                    bestScore = min(bestScore, score)
                    beta = min(beta, bestScore)
                    if beta <= alpha:
                        break
            self.transposition_table[(board_x, board_o, tiefe)] = bestScore
            return bestScore

class Board:
    def __init__(self):
        self.width = 600
        self.height = 600
        self.window = pygame.display.set_mode((self.width, self.height))
        self.ist_dran = 1
        self.rendered_text = ""
        self.vier_gewinnt = Connect_vier()
        self.zeig_kreis = False if self.ist_dran == 1 else True

    def redraw_window(self):
        self.window.fill((255, 255, 255))
        self.draw_board()
        pygame.display.update()

    def grey_filter(self):
        rect_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        rect_surface.fill((128, 128, 128, 150))
        self.window.blit(rect_surface, (0, 0))

    def choose_mode(self):
        self.redraw_window()
        self.grey_filter()
        #pygame.draw.rect(self.window, (255, 255, 255), (50, 200, self.width - 100, 140))
        font = pygame.font.SysFont("PressStart2P-Regular.ttf", 62)
        self.rendered_text = font.render("Press [1] to be Player 1", True, (0, 0, 0))
        self.rendered_text_2 = font.render("Press [2] to be Player 2", True, (0, 0, 0))
        self.window.blit(self.rendered_text, (self.width / 9, self.height / 3 + 10))
        self.window.blit(self.rendered_text_2, (self.width / 9, self.height / 3 + 90))
        pygame.display.update()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            key = pygame.key.get_pressed()
            if key[pygame.K_1]:
                self.ist_dran = 0
                self.zeig_kreis = True
                self.game_loop()
            elif key[pygame.K_2]:
                self.ist_dran = 1
                self.zeig_kreis = False
                self.game_loop()

    def draw_board(self):
        pygame.draw.rect(self.window, (28, 28, 220), (0, 100, self.width, 500))
        for i in range(1, 8):
            x = 81.5
            pygame.draw.circle(self.window, (0, 0, 0), (-25 + x * i, 150), 34) # black outline
            pygame.draw.circle(self.window, (255, 255, 255), (-25 + x * i, 150), 32)
            for a in range(1, 6):
                y = 80
                pygame.draw.circle(self.window, (0, 0, 0), (-25 + x * i, 150 + a * y), 34)  # black outline
                pygame.draw.circle(self.window, (255, 255, 255), (-25 + x * i, 150 + a * y), 32)
        # board x
        for i in range(0, len(str(bin(self.vier_gewinnt.board_x))) - 2):
            x = i // 7
            if self.vier_gewinnt.board_x & (1 << i):
                z = i % 7
                pygame.draw.circle(self.window, (0, 0, 0), (56 + 81.5 * x, self.height - 50 - 80 * z), 34) # black outline
                pygame.draw.circle(self.window, (255, 0, 0), (56 + 81.5 * x, self.height - 50 - 80 * z), 32) # yellow circle
        # board o
        for i in range(0, len(str(bin(self.vier_gewinnt.board_o))) - 2):
            x = i // 7
            if self.vier_gewinnt.board_o & (1 << i):
                z = i % 7
                pygame.draw.circle(self.window, (0, 0, 0), (56 + 81.5 * x, self.height - 50 - 80 * z), 34) # black outline
                pygame.draw.circle(self.window, (255, 215, 0), (56 + 81.5 * x, self.height - 50 - 80 * z), 32) # yellow circle

        if self.game_over():
            self.grey_filter()
            self.window.blit(self.rendered_text, (self.width / 15, 30))
            pygame.display.update()
            time.sleep(5)
            self.vier_gewinnt = Connect_vier()
            self.choose_mode()

    def draw_player(self, posx):
        col = 0
        x = 81.5
        if posx <= 12 + 81.5 and posx >= 0: # nur für das erste col
            col = 1
        for i in range(2, 7):
            if posx <= 12 + x * i and posx >= 12 + x * (i-1):
                col = i
            if posx >= 12 + x * i and i == 6:  # nur für das letzte co
                col = 7
        #macht den move
        if self.vier_gewinnt.valid_move(self.vier_gewinnt.board_x, self.vier_gewinnt.board_o, col):
            self.vier_gewinnt.player_move(col)
            self.ist_dran = 1

    def game_over(self):
        font = pygame.font.SysFont("PressStart2P-Regular.ttf", 65)
        if self.vier_gewinnt.check_win(self.vier_gewinnt.board_o):
            self.rendered_text = font.render("Gelb hat GEWONNEN !!!", True, (0, 0, 0))
            return True
        elif self.vier_gewinnt.check_win(self.vier_gewinnt.board_x):
            self.rendered_text = font.render(" Rot hat GEWONNEN !!!", True, (0, 0, 0))
            return True
        elif self.vier_gewinnt.check_draw(self.vier_gewinnt.board_x, self.vier_gewinnt.board_o):
            font = pygame.font.SysFont("PressStart2P-Regular.ttf", 62)
            self.rendered_text = font.render("Schade Unentschieden!", True, (0, 0, 0))
            return True

    def game_loop(self):
        self.running = True
        self.redraw_window()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click_x, click_y = event.pos
                    if self.ist_dran == 0 and not self.game_over():
                        self.draw_player(click_x)
                        self.redraw_window()
                        self.zeig_kreis = False
                if event.type == pygame.MOUSEMOTION:
                    posx = event.pos[0]
                    if self.zeig_kreis:
                        self.window.fill((255, 255, 255))
                        self.draw_board()
                        pygame.draw.circle(self.window, (0, 0, 0), (posx, 50), 34)  # black outline
                        pygame.draw.circle(self.window, (255, 0, 0), (posx, 50), 32)  # red circle
                        pygame.display.update()
            if self.ist_dran == 1 and not self.game_over():
                self.vier_gewinnt.computer_move()
                self.ist_dran = 0
                self.redraw_window()
                self.zeig_kreis = True
            if self.game_over():
                self.zeig_kreis = False
                self.redraw_window()

pygame.init()
b = Board()
b.choose_mode()
pygame.quit()
