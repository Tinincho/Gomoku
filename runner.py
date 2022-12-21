"""
Gomoku runner.
"""
# Imports.
import pygame
import sys
import time

import gomoku

# Window size.
pygame.init()
width = 1280
height = 720
size = (width, height)

# Colors.
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

medium_font = pygame.font.Font("OpenSans-Regular.ttf", 28)
large_font = pygame.font.Font("OpenSans-Regular.ttf", 40)
move_font = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None
board = gomoku.initial_state()
bot_turn = False

# Run game.
while True:
    # Exit game.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Refresh screen.
    screen.fill(black)

    # Let user choose a player.
    if user is None:
        # Draw title.
        title = large_font.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons.
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = medium_font.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton, border_radius=16)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = medium_font.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton, border_radius=16)
        screen.blit(playO, playORect)

        # Check if button is clicked.
        click, ignore, ignore = pygame.mouse.get_pressed()

        if click == 1:
            mouse = pygame.mouse.get_pos()

            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = gomoku.X

            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = gomoku.O

    else:
        # Draw game board.
        tiles = []
        tile_size = 80
        tile_origin = (width / 2 - ((gomoku.board_width * tile_size) / 2),
                       height / 2 - ((gomoku.board_heigth * tile_size) / 2))

        for row in range(gomoku.board_width):
            tiles_rows = []

            for column in range(gomoku.board_heigth):
                rect = pygame.Rect(tile_origin[0] + column * tile_size,
                                   tile_origin[1] + row * tile_size,
                                   tile_size, tile_size)

                pygame.draw.rect(screen, white, rect, 3)

                if board[row][column] != gomoku.E:
                    move = move_font.render(board[row][column], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)

                tiles_rows.append(rect)
            tiles.append(tiles_rows)

        game_over = gomoku.terminal(board)
        player = gomoku.player(board)

        # Show title.
        if game_over:
            winner = gomoku.winner(board)

            if winner is None:
                title = f"Game Over: Tie."

            else:
                title = f"Game Over: {winner} wins."

        elif user == player:
            title = f"Play as {user}"

        else:
            title = f"Computer thinking..."

        title = large_font.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Check for bot move.
        if user != player and not game_over:
            if bot_turn:
                time.sleep(0.5)
                move = gomoku.minimax(board)
                board = gomoku.result(board, move)
                bot_turn = False

            else:
                bot_turn = True

        # Check for a user move.
        click, ignore, ignore = pygame.mouse.get_pressed()

        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()

            for row in range(gomoku.board_width):
                for column in range(gomoku.board_heigth):
                    if (board[row][column] == gomoku.E and tiles[row][column].collidepoint(mouse)):
                        board = gomoku.result(board, (row, column))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = medium_font.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton, border_radius=16)
            screen.blit(again, againRect)
            click, ignore, ignore = pygame.mouse.get_pressed()

            if click == 1:
                mouse = pygame.mouse.get_pos()

                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = gomoku.initial_state()
                    bot_turn = False

    pygame.display.flip()