import pygame, json, sys, winlose
from lib import color, save_manager, win_checker, text_switcher

theme_color = json.load(open('themes/theme.json'))
setting = json.load(open('data/setting.json'))
# screen
SCREEN_WIDTH  = setting['screen']['width']
SCREEN_HEIGHT = setting['screen']['height']
# grid
NUM_OF_LINES  = setting['grid']['num_of_lines']
SIZE_X        = setting['grid']['size_x']
SIZE_Y        = setting['grid']['size_y']
THICKNESS     = setting['grid']['thickness']
# GRID_COLOR    = ["#5D5FEF", "#843CE0"]
# GRID_COLOR = [setting['grid']['color_0'], setting['grid']['color_1']]
BACKGROUND_COLOR = "#501be8"
LINE_COLOR       = color.BLACK
# theme
THEME = setting['theme']

class Game:

    # khởi tạo
    def __init__(self, screen):

        # pygame clock
        self.clock = pygame.time.Clock()

        # ảnh lưới và cờ
        self.img_grid  =  pygame.image.load('res/images/' + THEME + '/grid.png')
        self.img_piece = [pygame.image.load('res/images/' + THEME + '/piece_' + str(i) + '.png') for i in range(2)]

        # một số thông tin về lưới
        # self.grid_width  = 32
        # self.grid_height = 32
        # self.grid_width  = (SCREEN_WIDTH  - THICKNESS * NUM_OF_LINES) // (NUM_OF_LINES - 1) + THICKNESS
        # self.grid_height = (SCREEN_HEIGHT - THICKNESS * NUM_OF_LINES) // (NUM_OF_LINES - 1) + THICKNESS
        self.grid_width   = self.img_grid.get_width() // 2
        self.grid_height  = self.img_grid.get_width() // 2
        self.grid_start_x = (SCREEN_HEIGHT - self.grid_height * SIZE_Y) // 2
        self.grid_start_y = (SCREEN_HEIGHT - self.grid_height * SIZE_Y) // 2
        self.grid_end_x   = self.grid_start_x + self.grid_width  * SIZE_X
        self.grid_end_y   = self.grid_start_y + self.grid_height * SIZE_Y

        # Khởi tạo Screen
        self.screen = screen

        # Screen Win Lose
        self.win_lose_screen = winlose.WinLose(SCREEN_WIDTH, SCREEN_HEIGHT ,self.screen)

        # các thành phần điều khiển của game
        self.save_manager  = save_manager.SaveManager('game_data.json', 'data')
        self.game_data     = self.save_manager.load()
        self.win_checker   = win_checker.WinChecker()
        self.player_1      = self.game_data['PlayerName']['Player1']
        self.player_2      = self.game_data['PlayerName']['Player2']
        self.text_switcher = text_switcher.TextSwitcher(self.screen, BACKGROUND_COLOR, [self.player_1, self.player_2])

    # khởi tạo game mới
    def new_game(self):
        self.draw_grid_on()
        self.game_data = self.save_manager.refresh()

    # tiếp tục game từ save
    def continue_game(self):
        self.draw_grid_on()
        for row in range(SIZE_X):
            for column in range(SIZE_Y):
                piece_data = self.game_data['Board'][row][column]
                # nếu không chứa cờ thì bỏ qua
                if piece_data == -1:
                    continue
                # lấy hình ảnh cờ tương ứng theo data
                cur_piece = self.img_piece[piece_data]
                # tính vị trí của cờ để vẽ
                pos_piece = (self.grid_start_x + self.grid_width * row, self.grid_start_y + self.grid_height * column)
                # vẽ cờ lên màn hình
                self.screen.blit(cur_piece, pos_piece)

    # vẽ lưỡi lên một surface
    def draw_grid_on(self):

        # tô screen bằng màu background
        self.screen.fill(BACKGROUND_COLOR)
        # for i in range(self.grid_start_x, SCREEN_WIDTH - self.grid_width * 2, self.grid_width * 2):
        #     for j in range(self.grid_start_y, SCREEN_HEIGHT - self.grid_height * 2, self.grid_height * 2):
        #         self.screen.blit(self.img_grid, (i, j))

        cur_y = self.grid_start_y
        for i in range(SIZE_X // 2):
            cur_x = self.grid_start_x
            for j in range(SIZE_Y // 2):
                self.screen.blit(self.img_grid, (cur_x, cur_y))
                cur_x += self.grid_height * 2
            cur_y += self.grid_width * 2

        delta = 10
        pygame.draw.rect(self.screen, LINE_COLOR, (self.grid_start_x - delta, self.grid_start_y - delta, self.grid_end_x - self.grid_start_x + delta * 2, self.grid_end_y - self.grid_start_y + delta * 2), 5, 10)

        # # vẽ các ô màu xen kẽ
        # for i in range(0, SCREEN_WIDTH, self.grid_width):
        #     for j in range(0, SCREEN_HEIGHT, self.grid_height):
        #         pygame.draw.rect(self.screen, GRID_COLOR[(i + j) % 2], (i, j, self.grid_width, self.grid_height))
        
        # # vẽ các đường dọc
        # for i in range(self.grid_width, SCREEN_WIDTH - self.grid_width, self.grid_width):
        #     pygame.draw.line(self.screen, color.BLACK, (i + THICKNESS // 2, 40), (i + THICKNESS // 2, SCREEN_HEIGHT - 40), THICKNESS)

        # # vẽ cách đường ngang
        # for i in range(self.grid_height, SCREEN_HEIGHT - self.grid_height, self.grid_height):
        #     pygame.draw.line(self.screen, color.BLACK, (40, i + THICKNESS // 2), (SCREEN_WIDTH - 40, i + THICKNESS // 2), THICKNESS)

    # vòng lặp
    def loop_on(self):

        # duyệt qua các event
        for event in pygame.event.get():

            # nếu người chơi bấm chuột trái
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # lấy hình ảnh của cờ theo turn
                    cur_piece = self.img_piece[self.game_data['Turn']]

                    # lấy vị trí của chuột khi click
                    (mouse_x, mouse_y) = pygame.mouse.get_pos()

                    # nếu vị trí click nằm ngoài bàn cờ thì bỏ qua
                    if mouse_x < self.grid_start_x or mouse_x > self.grid_end_x or mouse_y < self.grid_start_y or mouse_y > self.grid_end_y:
                        continue
                    
                    # đưa về vị trí trong bảng
                    (board_x, board_y) = ((mouse_x - self.grid_start_x) // self.grid_width, (mouse_y - self.grid_start_y) // self.grid_width)

                    # nếu bảng đã chứa cờ thì bỏ qua
                    if self.game_data['Board'][board_x][board_y] != -1:
                        continue

                    # switch tên đang hiển thị
                    self.text_switcher.switch()
                    
                    # đưa về dạng tâm của bàn cờ
                    (center_x, center_y) = (board_x * self.grid_width + (self.grid_width + THICKNESS) // 2, board_y * self.grid_width + (self.grid_width + THICKNESS) // 2)

                    # đưa về dạng góc trái trên của cờ trong bàn cờ
                    display_pos = (center_x + self.grid_start_x - cur_piece.get_width() / 2, center_y + self.grid_start_y - cur_piece.get_height() / 2)
                    
                    # vẽ cờ lên màn hình
                    self.screen.blit(cur_piece, display_pos)

                    # lưu lại giá trị trong bảng
                    self.game_data['Board'][board_x][board_y] = self.game_data['Turn']
                    
                    # kiểm tra đã thắng chưa
                    if self.win_checker.check_win(self.game_data['Board'], self.game_data['Turn'], board_x, board_y):
                        self.win_lose_screen.run()
                        
                    # Thay đổi Turn ở cuối mỗi lượt
                    self.game_data['Turn'] = 1 - self.game_data['Turn']
                    
            
            # nếu người dùng bấm thoát
            if event.type == pygame.QUIT:
                # save game trước khi thoát
                self.save_manager.save(self.game_data)
                pygame.quit()
                sys.exit()
        
        self.text_switcher.draw_on(600, 40)

        # cập nhật display
        pygame.display.update()
        
        # delay 120ms
        self.clock.tick(120)
        
        # nếu không có sự kiện gì thì trả về -1
        return -1
