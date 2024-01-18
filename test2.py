import math
import pygame
import sys
import numpy as np

# Initialize Pygame
pygame.init()


# Set up display
width, height = 600, 600
screen = pygame.display.set_mode((width, height)) #bn-creat el screen
pygame.display.set_caption("X_O GUI")  #el esm fel boarder fo2

# el alwan el hane7tagha
white = (255, 255, 255)
black = (0, 0, 0)
#creat l board el X_O 3obara 3an 2d array kolo zeros
board=np.zeros((3,3))
print(board)

def draw_board():
    # Draw horizontal lines
    for i in range(1, 3): #bt3ml 2 itteration btrsm f kol wahd khat men el shemal lel yemin
        pygame.draw.line(screen, white, (0, i * height / 3), (width, i * height / 3), 2)

    # Draw vertical lines
    for i in range(1, 3):
        pygame.draw.line(screen, white, (i * width / 3, 0), (i * width / 3, height), 2)

def draw_xo(row, col, player):
    #ba3mel initiallization lel font 3ashan al3ab fel size brahty
    font = pygame.font.Font(None, 120)
    #player 1 da el howa el user el byl3ab
    if player == 1:
        text = font.render('X', True,white) #btdakhal fiha el text w lono w true dy 3ashan tkhali atraf el horouf smooth
        text_rect = text.get_rect(center=(col * 600 / 3 + 600/6, row * 600 / 3 + 600 / 6))#coordinations center el rectangle el fih el harf
        screen.blit(text, text_rect)# bt draw el kalam zai print keda
    if player == 2: #player 2 da el AI
        text = font.render('O', True, white)
        text_rect = text.get_rect(center=(col * 600 / 3 + 600 / 6, row * 600 / 3 + 600 / 6))
        screen.blit(text, text_rect)




def check_win(board, player):
    # horizontal win
    for r in range(3):
        if board[r][0] == player and board[r][1] == player and board[r][2] == player:
            return True
    # vertical win
    for c in range(3):
        if board[0][c] == player and board[1][c] == player and board[2][c] == player:
            return True
            # diagonal win
    if (board[0][0] == player and board[1][1] == player and board[2][2] == player)or (board[0][2] == player and board[1][1] == player and board[2][0] == player):
            return True

def check_tie(board):
    return np.count_nonzero(board) == 9 #by3ed el non zero slots fa law tala3 el 9 slots fel doard malianin yeb2a tie

AI = 2
PLAYER = 1
def minmax(board , maximizing_player):   #el parameters homa el board delwa2ty wasalet l eh + min el player el 3aleh el dor
    if check_win(board,AI): #law el AI hayeksab bel haraka dy han return 1 3ashan el AI maximizing player w bydawar 3ala a3la positive number
        return 1
    elif check_win(board , PLAYER ):#law el player hayeksab bel haraka dy han return -1 3ashan el player minimizing player w bydawar 3ala a3la negative number
        return -1
    elif check_tie(board):
        return 0
    if maximizing_player:
        best_score = -math.inf #3ashan howa maximizing fa bydawar 3ala a3la rakam ygelo fa bnbda2 b -inf 3ashan lama ygelo ay rakam a3la ybadelo bel rakam el gdid

        for c in range(3):#loop 3ala kol slot fel board
            for r in range(3):
                if (board[r][c] == 0):#bashouf law el slot dy fadya wala la
                    board[r][c] = 2   #law fadya el AI bygarab yel3ab fiha
                    score = minmax(board, False) #w bakhosh el minmax function tany bas el marady byl3ab akeno dor el player
                    #ba3d ma y3raf el score bnrga3 nfady el board tany 3ashan nel3ab el best move
                    board[r][c] = 0
                    if (score > best_score):  #kol ma yla2y score a3la men el best el 3ando byhot el score el gdid yeb2a howa el best
                        best_score = score
        return best_score
    else: #nafs el kalam bas dy el itteration el byl3abha el AI akeneo el player 3shan y predict el moves el gaya bta3et el user
        best_score = math.inf
        for c in range(3):
            for r in range(3):
                if (board[r][c] == 0):
                    board[r][c] = 1
                    score = minmax(board , True)
                    board[r][c] = 0
                    if (score < best_score):
                        best_score = score
        return best_score
#3ashan tebda2 enta el game
current_player = 1
game_over = False
while True:
    for event in pygame.event.get(): #by itterate f kol el events el dakhlalo
        #dy 3ashan lama tdos exit ye2fel el app
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:#law dost bel mouse
            mouseX, mouseY = event.pos #byakhod position el mouse makan ma dost
            clicked_row = int(mouseY / (600 / 3)) #el y bn3mlaha round l 22rab row liha
            clicked_col = int(mouseX / (600 / 3))#el x bn3mlaha round l 22rab col liha

            if current_player==1:
                if board[clicked_row][clicked_col] == 0: #by check el makan fady wala had la3ab fih abl keda
                    board[clicked_row][clicked_col] = current_player    #by make the move
                    draw_xo(clicked_row, clicked_col, current_player)   #dy 3ashan tetla3lena fel gui el haga el la3abtaha
                    if check_win(board, 1 ):
                        print(f"you win!")
                        game_over = True
                    elif check_tie(board):
                        print("It's a draw!")
                        game_over = True
                    else:
                        current_player = 2  #btghayar men el turn el user l turn el AI

            if current_player==2:
                bestscore=-math.inf # ba7otaha 3ashan el AI el maximizing player hena w 3aizen ne3raf anhy col w row ahsan le3ba lih
                bestcol=0
                bestrow=0
                for c in range(3): #nafs loop el minmax bzbt bas btraga3ly ahsan col w row kaman msh bas el best score
                    for r in range(3):
                        if board[r][c]==0:
                            board[r][c]=2
                            score = minmax(board,False)
                            board[r][c] = 0
                            if score>bestscore: #kol ma ala2y new best score baghayar el best col w row (el best move 3amatan)
                                bestscore= score
                                bestcol=c
                                bestrow=r
                board[bestrow][bestcol] = current_player
                draw_xo(bestrow, bestcol, current_player)

                if check_win(board, 2):
                    print(f"AI win!")
                    game_over = True
                elif check_tie(board):
                    print("It's a draw!")
                    game_over = True
                else:
                    current_player = 1
    # btrsem el board el gdida
    draw_board()

    # Update el screen ba3d kol le3ba
    pygame.display.flip()
