import pygame, json, pygame_gui, sys
from lib import button, color, save_manager
import game

from lib.paint import Paint
from name import *
from lib.options import Options
from lib.exit_window import *
from lib.no_game_window import *
from lib.setting_window import *
import lib.setting_warning
# from winlose import WinLose
from lib.music_player import MusicPlayer

class Menu:
    # khởi tạo
    def __init__(self, screen, music_player):
        # Import DATA
        self.setting = json.load(open('data/setting.json'))
        self.game_data = json.load(open('data/game_data.json'))
        
     
        # LOAD DATA

        self.SCREEN_WIDTH  = self.setting['screen']['width']
        self.SCREEN_HEIGHT = self.setting['screen']['height']
        self.PLAYER_NAME = self.game_data["PlayerName"]
        
        
        
        self.music_player=music_player
        # self.music_player.menu_play()
        # self.music_player.bgsound_pause()

        self.clock = pygame.time.Clock()
        pygame.display.set_caption('MAIN MENU')

        self.screen = screen
        

        # Dùng để vẽ các image và render text
        self.paint = Paint(self.screen)
        
        # Khởi tạo toàn màn hình
        # if self.options.fullscreen:
        #     self.screen = pygame.display.set_mode(self.options.resolution, pygame.FULLSCREEN)
        # else:
        #     self.screen = pygame.display.set_mode(self.options.resolution)
        
        self.options = Options(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)   

        # Tạo một manager UI (Quản lý Giao diện màn hình)
        # Tham số truyền vào sẽ là kích thước màn hình và package
        # Hãy xem manager như là một người quản lý màn hình:
        # Với công việc là set up background và vẽ button quản lý các hiệu ứng v.v
        self.manager = pygame_gui.UIManager(self.options.resolution, 
                                            pygame_gui.PackageResource(package='themes',
                                                            resource='theme.json'))

        # Import Fonts                                                        
        # self.manager.preload_fonts([{'name': 'fira_code', 'point_size': 10, 'style': 'bold'},
        #                                {'name': 'fira_code', 'point_size': 10, 'style': 'regular'},
        #                                {'name': 'fira_code', 'point_size': 10, 'style': 'italic'},
        #                                {'name': 'fira_code', 'point_size': 14, 'style': 'italic'},
        #                                {'name': 'fira_code', 'point_size': 14, 'style': 'bold'}
        #                                ])

        # Màn hình Nhập Tên người chơi
        self.name_screen = None

        # Màn hình setting
        self.setting_screen = None

        # Màn hình Quit
        self.exit_screen = None

        # self.running = True
        self.running_mode = "menu"
        
        # Tạo background (sẽ setup sau)
        self.background_surface = None

        # Tạo Title Game
        self.title_game_caro = None

        # Tạo Button
        self.btn_AIplay = None
        self.btn_PvPplay = None
        self.btn_continue = None
        self.btn_settings = None
        self.btn_quit = None


        # Thiết kế giao diện
        self.image_list = []
        self.image_position = []

        # Import picture
        for index in range(1,5):
            # Import Image
            image = pygame.image.load(f"./res/images/menu/image-{index}.png").convert_alpha()
            # Apend image_list
            self.image_list.append(image)

        # Tạo Box Setting
        self.settings_window = None

        # Dropdown Box Setting size
        self.setting_resolution = None

        # Tạo Box Quit
        self.quit_window = None
        
        self.btn_size = (int(self.options.resolution[0] * 0.4), int(self.options.resolution[1] * 0.1))
        self.label_size = (int(self.options.resolution[0] * 0.6), int(self.options.resolution[1] * 0.25))
        
        # chiều rộng (ngang) cửa sổ settings, quit
        self.sub_window_width = self.options.resolution[0] * 5 // 8
        # chiều cao (dọc) cửa sổ settings, quit
        self.sub_window_height = self.options.resolution[1] * 5 // 8
        
        self.setting_changed = False
        # print("Init called")
        
        self.update_ui()
        
        #self.exit_screen.hide()


    # Hàm cập nhật kích thước màn hình
    def update_ui(self):
        self.manager.set_window_resolution(self.options.resolution)
        self.manager.clear_and_reset()

        #self.name_screen = Name(self.options.resolution[0], self.options.resolution[1], self.screen)

        # Setup Background
        self.background_surface = pygame.Surface(self.options.resolution)
        self.background_surface.fill(self.manager.get_theme().get_colour("dark_bg"))  # dark_bg nằm trong file theme.json

        # Tạo ra các button ở màn hình Intro
        # self.btn_AIplay = pygame_gui.elements.UIButton(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2),
        #                                                 int(self.options.resolution[1] / 2 - 200)), self.btn_size),
        #                                                 "BOT",
        #                                                 self.manager,
        #                                                 object_id="#all_button")
        
        self.btn_PvPplay = pygame_gui.elements.UIButton(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2),
                                                        int(self.options.resolution[1] / 2 - 100)), self.btn_size),
                                                        "PVP",
                                                        self.manager,
                                                        object_id="#all_button")
        
        self.btn_continue = pygame_gui.elements.UIButton(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2),
                                                        int(self.options.resolution[1] / 2)), self.btn_size),
                                                        "CONTINUE",
                                                        self.manager,
                                                        object_id="#all_button")                                        
        
        self.btn_settings = pygame_gui.elements.UIButton(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2),
                                                        int(self.options.resolution[1] / 2 + 100)), self.btn_size),
                                                        "SETTINGS",
                                                        self.manager,
                                                        object_id="#all_button")
        
        self.btn_quit = pygame_gui.elements.UIButton(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2),
                                                        int(self.options.resolution[1] / 2 + 200)), 
                                                        self.btn_size),
                                                        "QUIT",
                                                        self.manager,
                                                        object_id="#all_button")
        
        
        self.title_game_caro = pygame_gui.elements.UILabel(pygame.Rect((int(self.options.resolution[0] / 2 - self.label_size[0] / 2),
                                                        int(self.options.resolution[1] / 2 - 400)), self.label_size),
                                                        text="Game Caro", 
                                                        manager=self.manager,
                                                        object_id="#label")
        

        self.image_position = [(int(self.options.resolution[0] * 0.1), int(self.options.resolution[1] * 0.65)), 
                                (int(self.options.resolution[0] * 0.125), int(self.options.resolution[1] * 0.125)), 
                                (int(self.options.resolution[0] * 0.75), int(self.options.resolution[1] * 0.7)), 
                                (int(self.options.resolution[0] * 0.75), int(self.options.resolution[1] * 0.1))]


        self.title_game_caro.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)
        
        self.no_game = NoGameWindow(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2 - 150),
                                                    int(self.options.resolution[1] / 2) - 125), 
                                                    (self.sub_window_width, self.sub_window_height * 3 // 5)),
                                                    self.manager, self.options.resolution[0], self.options.resolution[1])
        
        self.setting_screen = SettingWindow(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2 - 150),
                                                        int(self.options.resolution[1] / 2) - 200), 
                                                        (self.sub_window_width, self.sub_window_height)), 
                                                        self.manager, self.options.resolution[0], self.options.resolution[1],
                                                        self.music_player.ingame_sound,
                                                        self.music_player.win_sound,
                                                        self.music_player.click_sound,
                                                        self.music_player.menu_sound)
        
        self.setting_warning = lib.setting_warning.SettingWarningWindow(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2 - 150),
                                                        int(self.options.resolution[1] / 2) - 125), 
                                                        (self.sub_window_width, self.sub_window_height * 3 // 5)),
                                                        self.manager, self.options.resolution[0], self.options.resolution[1])
        
        self.exit_screen = ExitWindow(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2 - 50),
                                                        int(self.options.resolution[1] / 2) - 125), 
                                                        (self.sub_window_width * 3 // 4, self.sub_window_height * 3 // 5)),
                                                        self.manager, self.options.resolution[0], self.options.resolution[1])
        
        # Ban đầu ẩn màn hình nhỏ đi
        self.no_game.hide()
        self.setting_screen.hide()
        self.exit_screen.hide()
        self.setting_warning.hide()
        
        
        # Kích thước 
        current_resolution = f"{self.options.resolution[0]}x{self.options.resolution[1]}"
        
        
        # self.size_arr = ['640x480', '800x600', '1024x768', '1280x960']
        self.size_arr = ['1280x960']
        # self.setting_resolution = pygame_gui.elements.UIDropDownMenu(self.size_arr,
        #                                      current_resolution,
        #                                      pygame.Rect((int(self.options.resolution[0] * 0.7),
        #                                                 int(self.options.resolution[1] * 0.8)),
        #                                                  (200, 25)),
        #                                      self.manager,
        #                                      object_id="#drop_down_options_list")

        
    def change_size(self, text):
        resolution_str = text.split('x')
        resolution_width = int(resolution_str[0])
        resolution_height = int(resolution_str[1])
        if (resolution_width != self.options.resolution[0] or
                resolution_height != self.options.resolution[1]):
            self.options.resolution = (resolution_width, resolution_height)
            self.screen = pygame.display.set_mode(self.options.resolution)
            self.update_ui()

    
    def process_events(self):
        #self.exit_screen_created = False
        for event in pygame.event.get():
            #if event.type == pygame.QUIT:
            #    self.running = False

            # Quản lý và xử lý các sự kiện (như click, hover, ...)
            self.manager.process_events(event)
            
            quit_button_pressed = (event.type == pygame.QUIT)
            
            if quit_button_pressed or event.type == pygame_gui.UI_BUTTON_PRESSED:
                #print("Help")
                if quit_button_pressed or event.ui_element == self.btn_quit:
                    #print("Help")
                    self.exit_screen.show()
                
                # elif event.ui_element == self.btn_AIplay:
                #     # Truyền hàm khởi tạo trò chơi vào
                #     self.name_screen = Name(self.options.resolution[0], self.options.resolution[1], self.screen, "Bot")
                #     self.name_screen.run()
                    
                elif event.ui_element == self.btn_PvPplay:
                    # Truyền hàm khởi tạo trò chơi vào
                    self.running_mode = "PvP"
                    break
                    # self.name_screen = Name(self.options.resolution[0], self.options.resolution[1], self.screen, "PvP")
                    # self.name_screen.run()
                
                
                elif event.ui_element == self.btn_settings:
                    # self.setting_screen.show()
                    self.setting_warning.show()
                
                    
                elif event.ui_element == self.btn_continue:          
                    self.game_data = json.load(open('data/game_data.json'))
                    if (self.game_data["GameEnded"] == True or self.setting_changed):
                        self.game_data["GameEnded"] = True
                        save_manager.SaveManager('game_data.json', 'data').save(self.game_data)
                        self.no_game.show()
                    else:
                        save_manager.SaveManager('game_data.json', 'data').save(self.game_data)
                        self.running_mode = "continue_game"
                        break
                        # self.game_screen = game.Game(self.screen)
                        # self.game_screen.run()
                
                #self.exit_screen_created = quit_button_pressed or btn_quit_clicked
                
                #print(self.exit_screen_created)
                
                elif self.exit_screen.visible:
                    if event.ui_element == self.exit_screen.btn_Exit:
                        #print("Hello")
                        self.running_mode = "end"
                        break
                            
                    elif event.ui_element == self.exit_screen.btn_continue:
                        self.exit_screen.hide()
                        #self.exit_screen_created = False
                
                elif self.setting_warning.visible:
                    if event.ui_element == self.setting_warning.btn_continue:
                        self.setting_warning.hide()
                        self.setting_screen.show()
                        self.music_player.menu_sound.get_volume()
                    
                    elif event.ui_element == self.setting_warning.btn_back:
                        self.setting_warning.hide()
                
                elif self.no_game.visible and event.ui_element == self.no_game.btn_Back:
                    self.no_game.hide()


            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                self.setting_changed = True
                if event.ui_element == self.setting_screen.pieces_mode_drop_down:
                    # print("Pieces mode changed from %d to %s" % (self.setting["game"]["win_cnt"], event.text))
                    # print(self.setting_screen.pieces_mode_drop_down.selected_option)
                    # print(type(self.setting_screen.pieces_mode_drop_down.selected_option))
                    # self.setting_screen.update_pieces_mode_index()
                    self.setting_screen.update_board_size_drop_down()
                    res = self.setting_screen.board_size_drop_down.selected_option.split('x')
                    self.setting["grid"]["size_x"] = int(res[0])
                    self.setting["grid"]["size_y"] = int(res[1])
                    self.setting["game"]["win_cnt"] = int(event.text)
                    # print("print in pieces mode drop down update\n", self.setting["grid"])
                elif event.ui_element == self.setting_screen.board_size_drop_down:
                    # print("Board size changed from %dx%d to %s" 
                        #   % (self.setting["grid"]["size_x"], self.setting["grid"]["size_y"], 
                            #  event.text))
                    # print(self.setting_screen.board_size_drop_down.selected_option)
                    # print(type(self.setting_screen.board_size_drop_down.selected_option))
                    res = event.text.split('x')
                    self.setting["grid"]["size_x"] = int(res[0])
                    self.setting["grid"]["size_y"] = int(res[1])
                    # print(self.setting["grid"])
                elif event.ui_element == self.setting_screen.resolution_drop_down:
                    self.change_size(event.text)
                    res = event.text.split('x')
                    self.setting["screen"]["width"] = int(res[0])
                    self.setting["screen"]["height"] = int(res[1])
                # https://www.programiz.com/python-programming/json
            json.dump(self.setting, open('data/setting.json', 'w'), indent = 4)
            

    def run(self):
        """Chạy màn hình game
        """
        while self.running_mode == "menu":
            time_delta = self.clock.tick(120) / 1000.0
            #print(time_delta)
            # Vẽ hình nền lên screen
            self.screen.blit(self.background_surface, (0,0))

            # Vẽ các hình mini
            for index in range(4):
                self.paint.render_surface(self.image_list[index], self.image_position[index])
            #print("Help")
            self.process_events()

            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            #pygame.time.delay(25)
            pygame.display.update()
        return self.running_mode
        # pygame.quit() 
        # sys.exit()
