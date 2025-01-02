import pygame
import random


class Color:
    RED = (255, 36, 36)
    GREEN = (29, 219, 22)
    PINK = (255, 0, 221)
    ORANGE = (255, 94, 0)
    SKYBLUE = (0, 216, 255)
    YELLOW = (225, 228, 0)
    BLUE = (225, 228, 0)
    HINT_RED = (205, 0, 0)
    HINT_GREEN = (0, 169, 0)
    HINT_PINK = (205, 0, 171)
    HINT_ORANGE = (205, 44, 0)
    HINT_SKYBLUE = (0, 166, 205)
    HINT_YELLOW = (175, 178, 0)
    HINT_BLUE = (175, 178, 0)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (140, 140, 140)


SCREEN_WIDTH = 960
SCREEN_HEIGHT = 700
PLAY_WIDTH = 300
PLAY_HEIGHT = 600
BLOCK_SIZE = PLAY_WIDTH // 10
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
SCREEN_START_X = 50
SCREEN_START_Y = 100
DROP_TIME = 850

blocks_info = [
    [
        [
            '0100',
            '0100',
            '0100',
            '0100'
        ],
        [
            '0000',
            '0000',
            '1111',
            '0000',
        ],
        [
            '0100',
            '0100',
            '0100',
            '0100'
        ],
        [
            '0000',
            '0000',
            '1111',
            '0000',
        ],

    ],  # ㅣ
    [
        [
            '0000',
            '0110',
            '0110',
            '0000'
        ],
        [
            '0000',
            '0110',
            '0110',
            '0000'
        ],
        [
            '0000',
            '0110',
            '0110',
            '0000'
        ],
        [
            '0000',
            '0110',
            '0110',
            '0000'
        ],
    ],  # ㅁ
    [
        [
            '0000',
            '0100',
            '0111',
            '0000'
        ],
        [
            '0010',
            '0010',
            '0110',
            '0000',
        ],
        [
            '0000',
            '0111',
            '0001',
            '0000',
        ],
        [
            '0011',
            '0010',
            '0010',
            '0000',
        ],
    ],  # ㄴ
    [
        [
            '0000',
            '0001',
            '0111',
            '0000'
        ],
        [
            '0110',
            '0010',
            '0010',
            '0000',
        ],
        [
            '0000',
            '0111',
            '0100',
            '0000',
        ],
        [
            '0100',
            '0100',
            '0110',
            '0000',
        ],
    ],  # ㄱ
    [
        [
            '0000',
            '0010',
            '0111',
            '0000'
        ],
        [
            '0010',
            '0110',
            '0010',
            '0000',
        ],
        [
            '0000',
            '0111',
            '0010',
            '0000'
        ],
        [
            '0010',
            '0011',
            '0010',
            '0000'
        ]
    ],  # ㅗ
    [
        [
            '0100',
            '0110',
            '0010',
            '0000'
        ],
        [
            '0000',
            '0011',
            '0110',
            '0000'
        ],
        [
            '0100',
            '0110',
            '0010',
            '0000'
        ],
        [
            '0000',
            '0011',
            '0110',
            '0000'
        ],
    ],  # 번
    [
        [
            '0010',
            '0110',
            '0100',
            '0000'
        ],
        [
            '0000',
            '0110',
            '0011',
            '0000'
        ],
        [
            '0010',
            '0110',
            '0100',
            '0000'
        ],
        [
            '0000',
            '0110',
            '0011',
            '0000'
        ],
    ]  # 역번
]
hint_color = [Color.HINT_RED, Color.HINT_GREEN, Color.HINT_PINK, Color.HINT_ORANGE, Color.HINT_SKYBLUE,
              Color.HINT_YELLOW, Color.HINT_BLUE]
blocks_color = [Color.RED, Color.GREEN, Color.PINK, Color.ORANGE, Color.SKYBLUE, Color.YELLOW, Color.BLUE]


class Block:
    def __init__(self, x, y, shape):
        self.shape = blocks_info[shape]
        self.rotation = 0
        self.x = x
        self.y = y
        self.color = blocks_color[shape]
        self.idx = shape

    def init_pos(self):
        self.x = 4
        self.y = -4
        self.rotation = 0
    def copy(self):
        new_block = Block(0, 0, 0)
        new_block.shape = self.shape.copy()
        new_block.rotation = self.rotation
        new_block.x = self.x
        new_block.y = self.y
        new_block.color = self.color
        new_block.idx = self.idx
        return new_block



def create_board(set_position):
    board = [[Color.BLACK for i in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            if (x, y) in set_position:
                board[y][x] = set_position[(x, y)]
    return board


def draw_board(screen, board):
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            if board[y][x] is Color.BLACK:
                continue
            pygame.draw.rect(screen, board[y][x],
                             (SCREEN_START_X + x * BLOCK_SIZE, SCREEN_START_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                             0)
    pygame.draw.rect(screen, Color.GRAY, (SCREEN_START_X, SCREEN_START_Y, PLAY_WIDTH, PLAY_HEIGHT), 3)

    font = pygame.font.SysFont('Arial', 32, True)
    text = font.render('Next Block', True, Color.WHITE)
    screen.blit(text, (410, 50))

def get_block_position(block):
    positions = []
    block_shape = block.shape[block.rotation % len(block.shape)]
    for i, line in enumerate(block_shape):
        for j, column in enumerate(line):
            if column == '1':
                positions.append((block.x + j, block.y + i))
    return positions


def collision_check(block, board):
    positions = []
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            if board[i][j] == Color.BLACK:
                positions.append((j, i))
    data = get_block_position(block)
    for pos in data:
        if pos not in positions:
            if pos[1] > -1:
                return False
    return True


def create_block_queue():
    data = []
    for i in range(len(blocks_info)):
        block = Block(4, -4, i)
        data.append(block)
    random.shuffle(data)
    return data


def clear_line(board, set_positions):
    count = 0  # 제거된 줄의 개수
    idx = 0  # 마지막으로 제거된 위치 y
    start_idx = -float('inf')  # 마지막으로 제거된 위치 y
    deletes = list()
    down_ = list()
    for i in range(len(board) - 1, -1, -1):
        line = board[i]
        if Color.BLACK not in line:
            count += 1
            idx = i
            start_idx = max(start_idx, i)
            deletes.append(i)
            for j in range(len(line)):
                try:
                    del set_positions[j, i]
                except KeyError:
                    continue
    if count > 0:  # 제거된 라인이 존재한다면
        for last_idx in deletes[::-1]:
            for x, y in sorted(set_positions, key=lambda x: -x[1]):
                if y < last_idx:
                    new_pos = (x, y + 1)
                    set_positions[new_pos] = set_positions.pop((x, y))


def create_hint_block(block, board):
    hint_block = block.copy()
    hint_block.color = hint_color[hint_block.idx]
    while collision_check(hint_block, board) or hint_block.y < 0:
        hint_block.y += 1
    hint_block.y -= 1
    return hint_block


def draw_hint_block(screen, block):
    for i in range(4):
        for j in range(4):
            if block.shape[block.rotation % 4][i][j] == '0':
                continue
            pygame.draw.rect(screen, block.color, (SCREEN_START_X + (block.x + j) * BLOCK_SIZE, SCREEN_START_Y + (block.y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)


def draw_next_block(screen, block):
    for i in range(4):
        for j in range(4):
            if block.shape[0][i][j] == '0':
                continue
            pygame.draw.rect(screen, block.color, (400 + j * BLOCK_SIZE, 100 + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                             0)
    pygame.draw.rect(screen, Color.GRAY, (400, 100, BLOCK_SIZE*4, BLOCK_SIZE*4), 3)


def game(screen):
    is_run = True
    clock = pygame.time.Clock()
    # 테트리스를 위한 변수
    block_queue = create_block_queue()
    current_block = block_queue.pop()
    next_block = block_queue.pop()
    hint_block = current_block.copy()
    hint_block.color = hint_color[hint_block.idx]
    hold_block = None
    hold_able = True

    set_positions = dict()
    drop_time = 0

    while is_run:
        board = create_board(set_positions)
        drop_time += clock.get_time()
        is_fixable = False
        if drop_time > DROP_TIME:
            drop_time = 0
            current_block.y += 1
            if not collision_check(current_block, board) and current_block.y > 0:
                current_block.y -= 1
                is_fixable = True
        # EVENT
        for event in pygame.event.get():
            if drop_time == 0:
                break
            if event.type == pygame.QUIT:
                is_run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_block.rotation += 1
                    if not collision_check(current_block, board):
                        current_block.rotation -= 1
                if event.key == pygame.K_DOWN:
                    current_block.y += 1
                    if not collision_check(current_block, board):
                        current_block.y -= 1
                        is_fixable = True
                if event.key == pygame.K_LEFT:
                    current_block.x -= 1
                    if not collision_check(current_block, board):
                        current_block.x += 1
                if event.key == pygame.K_RIGHT:
                    current_block.x += 1
                    if not collision_check(current_block, board):
                        current_block.x -= 1
                if event.key == pygame.K_SPACE:
                    while collision_check(current_block, board) or current_block.y < 0:
                        current_block.y += 1
                    current_block.y -= 1
                    is_fixable = True
                if event.key == pygame.K_c:
                    if hold_block is None:
                        hold_block = current_block
                        hold_block.init_pos()
                        current_block = next_block
                        next_block = block_queue.pop()
                        hold_able = False
                    elif hold_able:
                        current_block, hold_block = hold_block, current_block
                        hold_block.init_pos()
                        hold_able = False


        hint_block = create_hint_block(current_block, board)
        block_position = get_block_position(current_block)
        for x, y in block_position:
            if y > -1:
                board[y][x] = current_block.color

        if is_fixable:
            hold_able = True
            for pos in block_position:
                set_positions[pos] = current_block.color
            current_block = next_block
            next_block = block_queue.pop()

            if not block_queue:
                block_queue =  create_block_queue()
            # 라인 제거
            clear_line(board, set_positions)

        screen.fill(Color.BLACK)
        draw_hint_block(screen, hint_block)
        draw_board(screen, board)
        draw_next_block(screen, next_block)
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    _screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('PYTRIS')
    game(_screen)
    pygame.quit()