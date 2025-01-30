import pygame
import chess
import chess.engine
import os

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 8
WHITE, BLACK = (255, 255, 255), (0, 0, 0)  # Updated to Black and White
HIGHLIGHT_COLOR = (246, 246, 105)

# Ensure assets folder exists
ASSETS_DIR = "assets"
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)
    print("Assets folder created. Please add chess piece images (bP.png, wK.png, etc.) to the 'assets' directory.")

# Load chess piece images
piece_images = {}
for piece in ['p', 'r', 'n', 'b', 'q', 'k', 'P', 'R', 'N', 'B', 'Q', 'K']:
    color = 'b' if piece.islower() else 'w'
    piece_type = piece.upper()
    image_path = os.path.join(ASSETS_DIR, f'{color}{piece_type}.png')
    if os.path.exists(image_path):
        piece_images[piece] = pygame.transform.scale(
            pygame.image.load(image_path), (SQUARE_SIZE, SQUARE_SIZE)
        )
    else:
        print(f"Warning: Missing image {image_path}. Please add the necessary chess piece images.")

# Initialize board
board = chess.Board()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")


# Draw board
def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces():
    for row in range(8):
        for col in range(8):
            square = chess.square(col, 7 - row)
            piece = board.piece_at(square)
            if piece and piece.symbol() in piece_images:
                screen.blit(piece_images[piece.symbol()], (col * SQUARE_SIZE, row * SQUARE_SIZE))


def highlight_moves(square):
    if square is None:
        return
    for move in board.legal_moves:
        if move.from_square == square:
            to_row = 7 - chess.square_rank(move.to_square)
            to_col = chess.square_file(move.to_square)
            pygame.draw.rect(
                screen, HIGHLIGHT_COLOR,
                (to_col * SQUARE_SIZE, to_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            )


# Main game loop
running = True
selected_square = None
while running:
    draw_board()
    if selected_square is not None:
        highlight_moves(selected_square)
    draw_pieces()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
            square = chess.square(col, 7 - row)

            if selected_square is None:
                selected_square = square
            else:
                move = chess.Move(selected_square, square)
                if move in board.legal_moves:
                    board.push(move)
                selected_square = None

pygame.quit()