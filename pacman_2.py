def pacman():
    import copy
    from board import boards # 보드 파일에서 boards리스트 가져오기
    import pygame
    import math # 벽 그릴때 둥글게 그려야 해서
    import mainmenu
    import time
    import round2_1
    import resources.save_files
    import resources.images.characters
    from option import maze_index
    from option import sound # sound 설정에서 받고 들리게 설정했으면(1) -> 소리 들리게 if문 처리...
    import platform

    os_name = platform.system()

    if os_name == "Windows":
        import ctypes

        u32 = ctypes.windll.user32
        resolution = u32.GetSystemMetrics(0), u32.GetSystemMetrics(1)
    else:
        resolution = [1600, 1000]

    save_file = resources.save_files.save_file()
    save_file.load()
    if maze_index == 0:
        color = 'green'
    elif maze_index == 1:
        color = (46, 135, 255)
    elif maze_index == 2:
        color = (251, 171, 197)
    elif maze_index == 3:
        color = (255, 222, 10)


    WIDTH = 900
    HEIGHT = 900  # 창 가로세로 상수로 정해두고 시작 ->이거 해상도마다 다르게 보일 수 있음
    screen = pygame.display.set_mode(resolution,pygame.FULLSCREEN)  # 창 가로세로 정하기
    timer = pygame.time.Clock()  # 속도 제어 위해서
    fps = 60 #게임 플레이할 수 있는 최대속도
    font = pygame.font.Font('assets/pacman_main_menu_images/emulogic.ttf', 20) #글씨 폰트, 크기 freesansbold
    level = copy.deepcopy(boards) #미로 리스트 = level에 넣기
    #color = 'green'#벽 색깔 걍 변수로 미리 해둠(0,255,0)(46,135,255)(251,171,197)(255,222,10)
    PI = math.pi #pi 상수
    player_images = [] #빈리스트 미리 만들기
    # for i in range(1, 5):
        # player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45))) #이미지 1~4를 가져와서 크기는 바꾸는거임 ->45,45로  -> 그리고 리스트에 추가
    for image_path in resources.images.characters.get_images_path(save_file.image_file):
        player_images.append(pygame.transform.scale(pygame.image.load(image_path), (50, 50)))
    # 사운드 가져오기
    powerup_sound = pygame.mixer.Sound("assets/sounds/ghost_time.mp3")
    bgm = pygame.mixer.Sound("assets/sounds/bgm.mp3")
    dead_sound = pygame.mixer.Sound("assets/sounds/dead.mp3")
    gameover_sound = pygame.mixer.Sound("assets/sounds/game_over.mp3")
    win_sound = pygame.mixer.Sound("assets/sounds/round1_win.mp3")
    win_sound.set_volume(0.7)
    gameover_sound.set_volume(0.5)
    bgm.set_volume(0.4)
    powerup_sound.set_volume(0.3)

    #유령 그리기 -> 45,45 사이즈
    blinky_img = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/red_ghost.png'), (45, 45))
    pinky_img = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/pink_ghost.png'), (45, 45))
    inky_img = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/blue_ghost.png'), (45, 45))
    clyde_img = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/orange_ghost.png'), (45, 45))
    spooked_img = pygame.transform.scale(pygame.image.load(f'assets//pacman_main_menu_images/eat_ghost.png'), (45, 45))
    dead_up_img = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/eye_up.png'), (45, 45))
    dead_down_img = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/eye_down.png'), (45, 45))

    exit_img = pygame.transform.scale(pygame.image.load(f'assets/game_over/exit.png'), (40, 40))
    click_exit_img = pygame.transform.scale(pygame.image.load(f'assets/game_over/click_exit.png'), (40, 40))
    heart_img = pygame.transform.scale(pygame.image.load(f'assets/game_over/heart.png'), (40, 40))
    empty_heart_img = pygame.transform.scale(pygame.image.load(f'assets/game_over/empty_heart.png'), (40, 40))
    game_over_img = pygame.transform.scale(pygame.image.load(f'assets/game_over/GOLD_GAMEOVER.png'), (570,102))



    player_x = 450+350 # 플레이어 시작 위치
    player_y = 663
    direction = 0
    # 유령 x좌표, y좌표, 방향
    blinky_x = 56+350 # 혼자서만 박스 밖에서 시작
    blinky_y = 58
    blinky_direction = 0
    inky_x = 450+350
    inky_y = 388
    inky_direction = 2
    pinky_x = 410+350
    pinky_y = 408
    pinky_direction = 2
    clyde_x = 440+350
    clyde_y = 438
    clyde_direction = 2
    counter = 0
    flicker = False  # 큰 원 깜빡이는 거 안 깜빡이는 게 디폴트
    flicker_gameover_won= 0 # 게임 오버,이길때 press enter 텍스트 깜빡이게 하려고
    # 오 왼 위 밑 순서로 지금 돌아도 되는지
    turns_allowed = [False, False, False, False] # 기본 디폴트 다 False
    direction_command = 0
    player_speed = 2 # 이동속도 -> 원작과 비슷한 속도임
    powerup = False # 아이템 아직 안 먹었으니까
    power_counter = 0
    eaten_ghost = [False, False, False, False] # 먹힌 애 : 아직 아무 유령도 안 먹었으니까 다 False
    targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)] # 걍 각 유령 위치 같은 느낌
    # 유령들 죽어있는지 여부
    blinky_dead = False
    inky_dead = False
    clyde_dead = False
    pinky_dead = False
    # 시작 상자에 있나
    blinky_box = False
    inky_box = False
    clyde_box = False
    pinky_box = False
    moving = False
    ghost_speeds = [2, 2, 2, 2] #사실 픽셀값
    startup_counter = 0
    lives = 3 # 남은 생명
    game_over = False # 디폴트 게임오버 아닌거
    game_won = False # 이겼는지
    pause = False # pause 여부
    game_over_sound = 0 # 게임 오버 소리 한 번 나왔는지 여부
    game_won_sound = 0 # 게임 이긴 소리 한 번 나왔는지 여부

    class Ghost:
        def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id): #유령들 가져야하는 정보..id는 유령 번호
            self.x_pos = x_coord
            self.y_pos = y_coord
            self.center_x = self.x_pos + 22
            self.center_y = self.y_pos + 22
            self.target = target
            self.speed = speed
            self.img = img
            self.direction = direct
            self.dead = dead
            self.in_box = box
            self.id = id
            self.turns, self.in_box = self.check_collisions()
            self.rect = self.draw() # 플레이어랑 부딪치는지 알려고..

        def draw(self):
            if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead): # 보통의 상황 (파워업 아닌데 생존한 유령 or 파워업에 살아있는 유령)
                screen.blit(self.img, (self.x_pos, self.y_pos)) # 위치에 평범한 유령 그림
            elif powerup and not self.dead and not eaten_ghost[self.id]: # 유령 안 죽었고 파워업 먹은 상태
                screen.blit(spooked_img, (self.x_pos, self.y_pos)) # 아이템 사용시 유령 이미지
            else:

                if self.y_pos > 900 // 2:
                    screen.blit(dead_up_img, (self.x_pos, self.y_pos)) # 죽은 유령 이미지
                if self.y_pos < 900 // 2:
                    screen.blit(dead_down_img, (self.x_pos, self.y_pos)) # 죽은 유령 이미지
            ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36)) # 유령 주위에 히트박스 (좌표, 크기)
            return ghost_rect

        # 충돌 확인 함수 (box)
        def check_collisions(self):
            # R, L, U, D
            num1 = (HEIGHT  // 32) # 높이 한칸
            num2 = (WIDTH // 30) # 가로 한칸
            num3 = 15 # 오차 -> 벽 한 칸 정중앙에 있음. 30픽셀 -> 15나옴
            self.turns = [False, False, False, False]
            # 유령 이동 가능한지 확인
            if 0 < (self.center_x-350) // 30 < 29: # 밖 안 나가고 미로 안에 있다면
                if level[(self.center_y - num3) // num1][(self.center_x-350) // num2] == 9: # 맵에서 9번에 있을 때
                    self.turns[2] = True # 위로 오르기
                    '''
                    if문 순서대로 객체가 왼쪽으로, 오른쪽으로, 위로, 아래로 움직일 수 있는지를 판단
                    가능하다면 turns 리스트를 이용해 방향 전환
                    '''
                if level[self.center_y // num1][((self.center_x-350) - num3) // num2] < 3 \
                        or (level[self.center_y // num1][((self.center_x-350) - num3) // num2] == 9 and (
                        self.in_box or self.dead)):
                    self.turns[1] = True
                if level[self.center_y // num1][((self.center_x-350) + num3) // num2] < 3 \
                        or (level[self.center_y // num1][((self.center_x-350) + num3) // num2] == 9 and (
                        self.in_box or self.dead)):
                    self.turns[0] = True
                if level[(self.center_y + num3) // num1][(self.center_x-350) // num2] < 3 \
                        or (level[(self.center_y + num3) // num1][(self.center_x-350) // num2] == 9 and (
                        self.in_box or self.dead)):
                    self.turns[3] = True
                if level[(self.center_y - num3) // num1][(self.center_x-350) // num2] < 3 \
                        or (level[(self.center_y - num3) // num1][(self.center_x-350) // num2] == 9 and (
                        self.in_box or self.dead)):
                    self.turns[2] = True

                if self.direction == 2 or self.direction == 3: # 위, 아래
                    # 객체 중심의 x좌표가 특정 범위 내에 있을 때, 위 or 아래로 움직일 수 있는지를 확인
                    if 14 <= (self.center_x-350) % num2 <= 16:
                        if level[(self.center_y + num3) // num1][(self.center_x-350) // num2] < 3 \
                                or (level[(self.center_y + num3) // num1][(self.center_x-350) // num2] == 9 and (
                                self.in_box or self.dead)):
                            self.turns[3] = True # 밑으로 갈 수 있는지
                        if level[(self.center_y - num3) // num1][(self.center_x-350) // num2] < 3 \
                                or (level[(self.center_y - num3) // num1][(self.center_x-350) // num2] == 9 and (
                                self.in_box or self.dead)):
                            self.turns[2] = True # 위으로 갈 수 있는지
                    if 14 <= self.center_y % num1 <= 16:
                        if level[self.center_y // num1][((self.center_x-350) - num2) // num2] < 3 \
                                or (level[self.center_y // num1][((self.center_x-350) - num2) // num2] == 9 and (
                                self.in_box or self.dead)):
                            self.turns[1] = True
                        if level[self.center_y // num1][((self.center_x-350) + num2) // num2] < 3 \
                                or (level[self.center_y // num1][((self.center_x-350) + num2) // num2] == 9 and (
                                self.in_box or self.dead)):
                            self.turns[0] = True

                if self.direction == 0 or self.direction == 1: # 오른쪽, 왼쪽
                    if 14 <= (self.center_x-350) % num2 <= 16:
                        if level[(self.center_y + num3) // num1][(self.center_x-350) // num2] < 3 \
                                or (level[(self.center_y + num3) // num1][(self.center_x-350) // num2] == 9 and (
                                self.in_box or self.dead)):
                            self.turns[3] = True # 밑으로 갈 수 있는지
                        if level[(self.center_y - num3) // num1][(self.center_x-350) // num2] < 3 \
                                or (level[(self.center_y - num3) // num1][(self.center_x-350) // num2] == 9 and (
                                self.in_box or self.dead)):
                            self.turns[2] = True # 위으로 갈 수 있는지
                    if 14 <= (self.center_x-350) % num1 <= 16:
                        if level[self.center_y // num1][((self.center_x-350) - num3) // num2] < 3 \
                                or (level[self.center_y // num1][((self.center_x-350) - num3) // num2] == 9 and (
                                self.in_box or self.dead)):
                            self.turns[1] = True
                        if level[self.center_y // num1][((self.center_x-350) + num3) // num2] < 3 \
                                or (level[self.center_y // num1][((self.center_x-350) + num3) // num2] == 9 and (
                                self.in_box or self.dead)):
                            self.turns[0] = True
            else:
                self.turns[0] = True
                self.turns[1] = True # 오른쪽, 왼쪽 못 가니까
            if 390+350 < self.x_pos < 480+350 and 370 < self.y_pos < 480: # x,y좌표가 상자 안이면
                self.in_box = True # 상자 안에 있는 거 True
            else:
                self.in_box = False
            return self.turns, self.in_box # 돌아도 되는지 turns리스트 반환, 상자에 있는지 반환

        def move_clyde(self):
            # r, l, u, d  - 오 왼 위 아
            '''
            clyde의 움직임 패턴
            1. 추격에 유리하다면 방향을 바꾼다

            self.direction : 유령의 현재 이동 방향
            self.x_pos : 유령의 현재 x좌표
            self.y_pos : 유령의 현재 y좌표
            self.target[0] : 유령의 목표 x좌표
            self.target[1] : 유령의 목표 y좌표
            self.turns : 유령의 회전 가능성
            '''
            if self.direction == 0: #오른쪽 가려고 함
                if self.target[0] > self.x_pos and self.turns[0]: # 타겟은 (x,y)쌍 -> 내 목표 x좌표 > 내 x좌표  and 오른쪽 갈 수 있으면
                    self.x_pos += self.speed
                elif not self.turns[0]: # 오른쪽 못 감 오른쪽에 뭐 있음.
                    if self.target[1] > self.y_pos and self.turns[3]: # 아래로 내려가는 거 가능 + 타겟 y좌표 더 작음
                        self.direction = 3 # 내려가자
                        self.y_pos += self.speed # 픽셀 이만큼 이동
                    elif self.target[1] < self.y_pos and self.turns[2]:# 위로 내려가는 거 가능 + 타겟 y좌표 더 작음
                        self.direction = 2 #위로 가자
                        self.y_pos -= self.speed # 위로 속도 픽셀만큼
                    elif self.target[0] < self.x_pos and self.turns[1]: # 내 목표 x좌표 < 내 x 좌표 and 왼쪽 갈 수 있음
                        self.direction = 1 # 왼쪽 가자
                        self.x_pos -= self.speed # 왼쪽으로 속도 픽셀만큼
                    elif self.turns[3]: #아래 가능
                        self.direction = 3 # 아래로 속도 픽셀만큼
                        self.y_pos += self.speed
                    elif self.turns[2]: #위 가능
                        self.direction = 2 #위 가자
                        self.y_pos -= self.speed
                    elif self.turns[1]: #왼쪽 가능
                        self.direction = 1 #왼쪽 가자
                        self.x_pos -= self.speed
                elif self.turns[0]: # 오른쪽 가는 거 가능. 장애물 없음
                    if self.target[1] > self.y_pos and self.turns[3]: #타켓 y좌표 아래 + 아래 가능
                        self.direction = 3 # 아래 가자
                        self.y_pos += self.speed
                    if self.target[1] < self.y_pos and self.turns[2]: #타켓 y좌표 위 + 위 가능
                        self.direction = 2 #위 가자
                        self.y_pos -= self.speed
                    else:
                        self.x_pos += self.speed
            elif self.direction == 1: # 왼쪽 가려고 하고
                if self.target[1] > self.y_pos and self.turns[3]: #타겟이 밑에 있고 밑으로 갈 수 있으면
                    self.direction = 3 # 걍 밑으로 ㄱㄱ
                elif self.target[0] < self.x_pos and self.turns[1]:#타겟이 왼쪽에 있고 왼쪽으로 갈 수 있으면
                    self.x_pos -= self.speed #왼쪽으로
                elif not self.turns[1]: # 왼쪽에 뭐 있음. 못감 -> 다른 길 찾아야지
                    if self.target[1] > self.y_pos and self.turns[3]: #타겟이 밑에 있고 밑으로 갈 수 있으면
                        self.direction = 3 # 밑으로 가자
                        self.y_pos += self.speed # 픽셀만큼
                    elif self.target[1] < self.y_pos and self.turns[2]:#타겟이 위에 있고 위로 갈 수 있으면
                        self.direction = 2 # 위로 가자
                        self.y_pos -= self.speed #픽셀만큼
                    elif self.target[0] > self.x_pos and self.turns[0]:#타겟이 오른쪽에 있고 오른쪽으로 갈 수 있으면
                        self.direction = 0 #오른쪽으로 가자
                        self.x_pos += self.speed
                    elif self.turns[3]: #차선책 -> 타겟이랑 멀어지지만 아래 갈 수 있으면
                        self.direction = 3 # 아래가자
                        self.y_pos += self.speed
                    elif self.turns[2]:#차선책 -> 타겟이랑 멀어지지만 위 갈 수 있으면
                        self.direction = 2 #위 가자
                        self.y_pos -= self.speed
                    elif self.turns[0]:#차선책 -> 타겟이랑 멀어지지만 오른쪽 갈 수 있으면
                        self.direction = 0 #오른쪽 가자
                        self.x_pos += self.speed
                elif self.turns[1]:#왼쪽으로 가는 거 가능
                    if self.target[1] > self.y_pos and self.turns[3]: #목표 y좌표 밑 + 밑 가능
                        self.direction = 3 #밑으로 가자
                        self.y_pos += self.speed
                    if self.target[1] < self.y_pos and self.turns[2]: #목표 y좌표 위 + 위 가능
                        self.direction = 2 #위로 가자
                        self.y_pos -= self.speed
                    else:
                        self.x_pos -= self.speed
            elif self.direction == 2:# 위로 가려고 함
                if self.target[0] < self.x_pos and self.turns[1]: # 목표 x좌표 왼쪽 + 왼쪽이 가능
                    self.direction = 1 # 왼쪽으로
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]: #목표 y좌표 위 + 위 가능
                    self.direction = 2 #위로
                    self.y_pos -= self.speed
                elif not self.turns[2]: # 위으로 못 감 -> 다른 길 찾아야 함
                    if self.target[0] > self.x_pos and self.turns[0]: #목표 x좌표 오른쪽 + 오른쪽 가능
                        self.direction = 0 # 오른쪽 가자
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]: #목표 왼쪽 + 왼쪽 가능
                        self.direction = 1 # 왼쪽 가자
                        self.x_pos -= self.speed
                    elif self.target[1] > self.y_pos and self.turns[3]: # 목표 아래 + 아래 가능
                        self.direction = 3 #아래 가자
                        self.y_pos += self.speed
                    # 목표랑 멀어지지만 방법 없음 -> 목표랑 멀어져도 가자
                    elif self.turns[1]: #왼쪽 가능
                        self.direction = 1 #왼쪽 가자
                        self.x_pos -= self.speed
                    elif self.turns[3]: #아래 가능
                        self.direction = 3 #아래 가자
                        self.y_pos += self.speed
                    elif self.turns[0]: #오른쪽 가능
                        self.direction = 0 #오른쪽 가자
                        self.x_pos += self.speed
                elif self.turns[2]: #위 가능 + 목표 y좌표 위가 아님
                    if self.target[0] > self.x_pos and self.turns[0]: #목표 x좌표 오른쪽 + 오른쪽 가능
                        self.direction = 0 #오른쪽 가자
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    else:
                        self.y_pos -= self.speed # 걍 디폴트 이동
            elif self.direction == 3:# 밑으로 가려고 한다
                if self.target[1] > self.y_pos and self.turns[3]: # 밑이 가능?
                    self.y_pos += self.speed # 밑으로 가자
                elif not self.turns[3]: # 밑을 못가? -> 다른 길 찾자
                    if self.target[0] > self.x_pos and self.turns[0]: # 오 가능?
                        self.direction = 0 # 가능
                        self.x_pos += self.speed # 오른쪽 가자
                    elif self.target[0] < self.x_pos and self.turns[1]: # 왼 가능?
                        self.direction = 1 # 왼 가능
                        self.x_pos -= self.speed # 왼쪽 가자
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                elif self.turns[3]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    else:
                        self.y_pos += self.speed
            if self.x_pos < -30+350: # 왼쪽으로 화면 밖 나가면
                self.x_pos = 900+350
            elif self.x_pos > 900+350: # 오른쪽으로 화면 밖 나가면
                self.x_pos = -30+350 # 이거 원본은 오타 나있음.
            return self.x_pos, self.y_pos, self.direction


        def move_blinky(self):
            '''
            blinky 움직임 패턴
            1. 아무것도 없다면 직진
            2. 벽을 만난다면 회전
            '''
            if self.direction == 0:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.x_pos += self.speed
                elif not self.turns[0]:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                elif self.turns[0]:
                    self.x_pos += self.speed
            elif self.direction == 1:
                if self.target[0] < self.x_pos and self.turns[1]:
                    self.x_pos -= self.speed
                elif not self.turns[1]:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                elif self.turns[1]:
                    self.x_pos -= self.speed
            elif self.direction == 2:
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif not self.turns[2]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                elif self.turns[2]:
                    self.y_pos -= self.speed
            elif self.direction == 3:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.y_pos += self.speed
                elif not self.turns[3]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                elif self.turns[3]:
                    self.y_pos += self.speed
            if self.x_pos < -30+350:
                self.x_pos = 900+350
            elif self.x_pos > 900+350:
                self.x_pos = - 30+350
            return self.x_pos, self.y_pos, self.direction # #

        def move_inky(self):
            '''
            inky의 움직임 패턴
            1. 위, 아래로 움직임
            2. 충돌시에만 좌우로 이동
            '''
            if self.direction == 0:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.x_pos += self.speed
                elif not self.turns[0]:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                elif self.turns[0]:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    if self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    else:
                        self.x_pos += self.speed #디폴트 이동
            elif self.direction == 1:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.x_pos -= self.speed
                elif not self.turns[1]:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                elif self.turns[1]:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    if self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    else:
                        self.x_pos -= self.speed
            elif self.direction == 2:
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif not self.turns[2]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                elif self.turns[2]:
                    self.y_pos -= self.speed
            elif self.direction == 3:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.y_pos += self.speed
                elif not self.turns[3]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                elif self.turns[3]:
                    self.y_pos += self.speed
            if self.x_pos < -30+350:
                self.x_pos = 900+350
            elif self.x_pos > 900+350:
                self.x_pos = - 30+350
            return self.x_pos, self.y_pos, self.direction

        def move_pinky(self):
            '''
            pinky의 움직임 패턴
            1. 유리할 때마다 왼쪽, 오른쪽으로 회전
            2. 충돌시 위, 아래로만 회전
            '''
            if self.direction == 0:
                if self.target[0] > self.x_pos and self.turns[0]: #목표 x좌표 오른쪽 + 오른쪽 이동 가능
                    self.x_pos += self.speed
                elif not self.turns[0]:#목표 x좌표 오른쪽 + 오른쪽 이동 불가능
                    if self.target[1] > self.y_pos and self.turns[3]: #목표 y좌표 아래 + 아래 이동 가능
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                elif self.turns[0]:
                    self.x_pos += self.speed
            elif self.direction == 1:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.x_pos -= self.speed
                elif not self.turns[1]:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                elif self.turns[1]:
                    self.x_pos -= self.speed
            elif self.direction == 2:
                if self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif not self.turns[2]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                elif self.turns[2]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    else:
                        self.y_pos -= self.speed
            elif self.direction == 3:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.y_pos += self.speed
                elif not self.turns[3]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                elif self.turns[3]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    else:
                        self.y_pos += self.speed
            if self.x_pos < -30+350:
                self.x_pos = 900+350
            elif self.x_pos > 900+350:
                self.x_pos = - 30+350
            return self.x_pos, self.y_pos, self.direction

    def draw_pause(): # pause 눌렀을 때
        screen.fill('black')
        font = pygame.font.Font("assets/pacman_main_menu_images/emulogic.ttf", 60)
        pause_text = font.render(f'PAUSE', True,
                                                           'yellow')  # antialias : True -> 선 부드럽게..
        screen.blit(pause_text, (300+350, 350))
        font = pygame.font.Font("assets/pacman_main_menu_images/emulogic.ttf", 20)
        press_enter_to_continue_text = font.render(f'press [SPACE] to continue', True,
                                                           'white')  # antialias : True -> 선 부드럽게..
        screen.blit(press_enter_to_continue_text, (200+350, 550))
        pygame.display.flip()

    def draw_misc(): #score 출력
        if not pause:
            score_text = font.render('Score:', True, 'white') # antialias : True -> 선 부드럽게..
            screen.blit(score_text, (30, 30))
            score_text2 = font.render(f'{save_file.score}', True, 'white')  # antialias : True -> 선 부드럽게..
            screen.blit(score_text2, (190, 30))
            screen.blit(exit_img, (resolution[0]//2+450, 850)) # exit 이미지 화면에 만들기
            lives_text = font.render('Lives:', True, 'white')  # lives : 출력
            screen.blit(lives_text, (resolution[0]//2+450, 30))
            for i in range(lives):
                screen.blit(pygame.transform.scale(heart_img, (30, 30)), (resolution[0]//2+580 + i * 40, 30)) # 사이즈 30인 생명마다 40픽셀씩 뛰고 생명 개수 알려줌.
            for j in range(lives,3):
                screen.blit(pygame.transform.scale(empty_heart_img,(31, 31)), (resolution[0]//2+580 + j * 40, 28)) # 이미 쓴 빈 하트

            exitbutton = mainmenu.Button(exit_img, click_exit_img, resolution[0]//2+450, 850, 40, 40, None, action = mainmenu.quitgame)


            pygame.display.flip()


    def check_collisions(scor, power, power_count, eaten_ghosts):
        num1 = HEIGHT// 32
        num2 = WIDTH // 30
        if 0 +350< player_x < 870+350:
            if level[center_y // num1][(center_x-350) // num2] == 1: # 내 위치 미로 리스트에서 값 찾고 -> 내가 있는 위치 코인 있는 칸일때
                level[center_y // num1][(center_x-350) // num2] = 0 # 동전 먹었으니까 빈 통로로 바꿈
                scor += 10

            if level[center_y // num1][(center_x-350) // num2] == 2: # 내 위치 미로 리스트에서 값 찾고 -> 내가 있는 위치 큰코인 있는 칸일때
                level[center_y // num1][(center_x-350) // num2] = 0 # 큰 코인 먹었으니까 빈 통로로 바꿈
                scor += 50 # 큰 코인 하나 50점
                power = True # 파워업 됨 -> 아이템 먹었으니까(큰코인)
                power_count = 0 # 파워업 먹을 때마다 초기화
                eaten_ghosts = [False, False, False, False] #유령 먹었는지
        return scor, power, power_count, eaten_ghosts


    def draw_board(): #미로 그리기
        num1 = (HEIGHT  // 32) # 맨 밑에 50픽셀 남기고 boards리스트 줄 32줄이니까 그거로 나눔
        num2 = (WIDTH // 30) # 가로는 미로 개수로 나눔
        for i in range(len(level)): # 행
            for j in range(len(level[i])): #열
                if level[i][j] == 1:
                    pygame.draw.circle(screen, 'white', ((j * num2 + (0.5 * num2))+350, i * num1 + (0.5 * num1)), 4) # 스크린에 그릴거임,하얀색으로, 그 칸에 정중앙에 할거임,반지름 4
                if level[i][j] == 2 and not flicker:
                    pygame.draw.circle(screen, 'white', ((j * num2 + (0.5 * num2))+350, i * num1 + (0.5 * num1)), 10) # 반지름 10
                if level[i][j] == 3:
                    pygame.draw.line(screen, color, ((j * num2 + (0.5 * num2))+350, i * num1),
                                     ((j * num2 + (0.5 * num2))+350, i * num1 + num1), 3) # 선 시작, 끝, 선두께 => 얜 선 그리는 거라 y가 그 칸의 맨 위에서 시작임.
                if level[i][j] == 4:
                    pygame.draw.line(screen, color, ((j * num2)+350, i * num1 + (0.5 * num1)),
                                     ((j * num2 + num2)+350, i * num1 + (0.5 * num1)), 3) # 3번 가로버전
                if level[i][j] == 5:
                    pygame.draw.arc(screen, color, [((j * num2 - (num2 * 0.4)) - 2)+350, (i * num1 + (0.5 * num1)), num2, num1],
                                    0, PI / 2, 3) # 이 원이 무슨 직사각형에 딱맞는지 주는 거임 -> 왼쪽 위 x,y좌표,가로,세로, 0~1/2pi까지 그리겠다(살짝 동경 느낌)
                if level[i][j] == 6:
                    pygame.draw.arc(screen, color,
                                    [(j * num2 + (num2 * 0.5))+350, (i * num1 + (0.5 * num1)), num2, num1],PI / 2, PI, 3)
                if level[i][j] == 7:
                    pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5))+350, (i * num1 - (0.4 * num1)), num2, num1], PI,
                                    3 * PI / 2, 3)
                if level[i][j] == 8:
                    pygame.draw.arc(screen, color,
                                    [((j * num2 - (num2 * 0.4)) - 2)+350, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                    2 * PI, 3)
                    # 부드럽게 선 이어지게 살짝씩 숫자 조정
                if level[i][j] == 9:
                    pygame.draw.line(screen, 'white', ((j * num2)+350, i * num1 + (0.5 * num1)),
                                     ((j * num2 + num2)+350, i * num1 + (0.5 * num1)), 3) # 이거 걍 4에서 색만 하얀색으로 바꾼거임


    def draw_player():
        # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
        if direction == 0:
            screen.blit(player_images[counter // 5], (player_x, player_y)) # 화면에 표시 -> 나타낼 아이, 위치
            # 한 이미지 당 5 프레임씩 사진 보임 -> 4개 사진 -> 1초 60프레임 1초에 3번 반복 가능
        elif direction == 1:
            screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
        elif direction == 2:
            screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y)) # 위로 올라가면 90도 회전
        elif direction == 3:
            screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y)) # 아래로 내려가면 270도 회전


    def check_position(centerx, centery): # 내가 어디있나
        turns = [False, False, False, False]
        num1 = HEIGHT  // 32 # 한 칸 높이
        num2 = (WIDTH // 30) # 가로 한칸 크기
        num3 = 15 # fudge factor -> 벽이 칸의 중간에 애매하게 있으니까 그 오차
        # check collisions based on center x and center y of player +/- fudge number -> 오차 +/- 하면서 centerx,centery로 충돌 체크
        if (centerx-350) // 30 < 29:
            if direction == 0:#오른쪽 갈때
                if level[centery // num1][((center_x-350) - num3) // num2] < 3: # 미로에서 전 칸 찾고 -> 그 칸이 0~2일 때-> 빈 통로, 코인, 큰 코인
                    turns[1] = True # 전칸 통로에 포함되면 돌아갈 수 있게
            if direction == 1: # 왼쪽 갈때
                if level[centery // num1][((center_x-350) + num3) // num2] < 3: # 미로에서 전 칸 찾고 -> 그 칸이 0~2일 때-> 빈 통로, 코인, 큰 코인
                    turns[0] = True
            if direction == 2: # 위로 갈때
                if level[(centery + num3) // num1][(center_x-350) // num2] < 3: # 미로에서 전 칸 찾고 -> 그 칸이 0~2일 때-> 빈 통로, 코인, 큰 코인
                    turns[3] = True
            if direction == 3:
                if level[(centery - num3) // num1][(center_x-350) // num2] < 3: # 미로에서 전 칸 찾고 -> 그 칸이 0~2일 때-> 빈 통로, 코인, 큰 코인
                    turns[2] = True

            if direction == 2 or direction == 3: # 위로 가든 아래로 가든
                if 11 <= (centerx-350) % num2 <= 19: # (12,18 보다 11,19가 더 잘 되는 듯)내가 그 칸의 대충 중간에 있느냐 -> 칸의 중간 아니면 벽 뚫고 갈수도 있 -> 완벽한 숫자는 아니지만 걍 자연스럽. 6픽셀 크지 않음. 생각보다 -> 900픽셀 30개로 나누면 30이니까 한칸이 30픽셀
                    if level[(centery + num3) // num1][(center_x-350) // num2] < 3: # 내 바로 밑의 애가 가능하면
                        turns[3] = True
                    if level[(centery - num3) // num1][(center_x-350) // num2] < 3: # 내 위가 가능하면
                        turns[2] = True # 위를 True -> 위로 돌아갈 수 있
                if 11 <= centery % num1 <= 19: # 내가 지금 y좌표 한칸의 대충 중간이면 -> 얘도 마참가지로 칸의 중간아니면 벽 뚫고 갈 수 있
                    if level[centery // num1][((center_x-350) - num2) // num2] < 3: # 내가 지금 왼쪽 비어있으면
                        turns[1] = True # 왼쪽 돌아갈 수 있음
                    if level[centery // num1][((center_x-350) + num2) // num2] < 3: # 오른쪽 비어있으면
                        turns[0] = True # 오른쪽 돌아갈수 있음
            if direction == 0 or direction == 1:
                if 11 <= (centerx-350) % num2 <= 19: # 내가 그 칸의 대충 중간에 있느냐~ 완벽한 숫자는 아니지만 걍 자연스럽. 6픽셀 크지 않음. 생각보다 -> 900픽셀 30개로 나누면 30이니까 한칸이 30픽셀
                    if level[(centery + num1) // num1][(center_x-350) // num2] < 3: # 내 바로 밑의 애가 가능하면
                        turns[3] = True # 밑을 True로 -> 갈 수 있음
                    if level[(centery - num1) // num1][(center_x-350) // num2] < 3: # 내 위가 가능하면
                        turns[2] = True # 위를 True -> 갈 수 있음
                if 11 <= centery % num1 <= 19: # 내가 지금 y좌표 한칸의 대충 중간이면
                    if level[centery // num1][((center_x-350) - num3) // num2] < 3: # 내가 지금 왼쪽 비어있으면
                        turns[1] = True # 왼쪽 갈 수 있음
                    if level[centery // num1][((center_x-350) + num3) // num2] < 3: # 오른쪽 비어있으면
                        turns[0] = True # 오른쪽 갈수 있음

        else:
            turns[0] = True
            turns[1] = True # 오,왼 못 가니까

        return turns # 돌아도 되는지 turns리스트 반환


    def move_player(play_x, play_y): # 플레이어 위치 받고
        # r, l, u, d
        if direction == 0 and turns_allowed[0]: # 오른쪽으로 가려고 하고 오른쪽으로 가는게 가능하면
            play_x += player_speed # x좌표 2만큼 오른쪽으로~
        elif direction == 1 and turns_allowed[1]:
            play_x -= player_speed # x좌표 2만큼 왼쪽으로~
        if direction == 2 and turns_allowed[2]:
            play_y -= player_speed # y좌표 2만큼 위로~
        elif direction == 3 and turns_allowed[3]:
            play_y += player_speed # y좌표 2만큼 아래로~
        return play_x, play_y # 변경된 플레이어 위치 반화


    def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
        if player_x < 450+350: # 플레이어 위치
            runaway_x = 900+350 # 플레이어에게서 어떻게 벗어나는지(아이템 먹은 경우) 방향
        else:
            runaway_x = 0+350
        if player_y < 450:
            runaway_y = 900
        else:
            runaway_y = 0
        return_target = (450+350, 420)
        if powerup: # 파워업 먹었고
            if not blinky.dead and not eaten_ghost[0]: # 유령 안 죽고 안 먹혔고
                blink_target = (runaway_x, runaway_y) # 유령 플레이어한테서 도망치자
            elif not blinky.dead and eaten_ghost[0]: # 죽은 애인데 상자에서 살아난 애
                if 340+350 < blink_x < 560+350 and 340 < blink_y < 450: # 상자
                    blink_target = (400+350, 100) # 상자에서 나오기
                else:
                    blink_target = (player_x, player_y) # 상자 밖 -> 플레이어가 목표
            else: # 파워업 활성화 중이고 유령 죽어있음
                blink_target = return_target # 상자로 돌아가자
            if not inky.dead and not eaten_ghost[1]: # 유령 안 죽고 안 먹혔고
                ink_target = (runaway_x, player_y)
            elif not inky.dead and eaten_ghost[1]: # 죽은 애인데 상자에서 살아난 애
                if 340+350 < ink_x < 560+350 and 340 < ink_y < 450: # 상자
                    ink_target = (400+350, 100) # 문을 향하는게 목표
                else:
                    ink_target = (player_x, player_y)
            else:
                ink_target = return_target
            if not pinky.dead:
                pink_target = (player_x, runaway_y)
            elif not pinky.dead and eaten_ghost[2]:
                if 340+350 < pink_x < 560+350 and 340 < pink_y < 450:
                    pink_target = (400+350, 100)
                else:
                    pink_target = (player_x, player_y)
            else:
                pink_target = return_target
            if not clyde.dead and not eaten_ghost[3]:
                clyd_target = (450, 450)
            elif not clyde.dead and eaten_ghost[3]:
                if 340+350 < clyd_x < 560+350 and 340 < clyd_y < 450:
                    clyd_target = (400+350, 100)
                else:
                    clyd_target = (player_x, player_y)
            else:
                clyd_target = return_target
        else:
            if not blinky.dead:
                if 340+350 < blink_x < 560+350 and 340 < blink_y < 450:
                    blink_target = (400+350, 100)
                else:
                    blink_target = (player_x, player_y)
            else:
                blink_target = return_target
            if not inky.dead:
                if 340+350 < ink_x < 560+350 and 340 < ink_y < 450:
                    ink_target = (400+350, 100)
                else:
                    ink_target = (player_x, player_y)
            else:
                ink_target = return_target
            if not pinky.dead:
                if 340+350 < pink_x < 560+350 and 340 < pink_y < 450:
                    pink_target = (400+350, 100)
                else:
                    pink_target = (player_x, player_y)
            else:
                pink_target = return_target
            if not clyde.dead:
                if 340+350 < clyd_x < 560+350 and 340 < clyd_y < 450:
                    clyd_target = (400+350, 100)
                else:
                    clyd_target = (player_x, player_y)
            else:
                clyd_target = return_target
        return [blink_target, ink_target, pink_target, clyd_target] # 타겟 리스트 반환

    '''
    while True 구문에서 break가 없어도 되는 이유
    pygame.quit()가 되면 run = False로 바뀜
    '''
    run = True
    while run: # 무한루프
        timer.tick(fps) # 프레임 속도
        '''
        counter = 특정 시간 간격으로 발생해야 하는 이벤트가 잇을 때, 시간의 간격을 측정
        flicker = 객체가 일시적으로 보이거나 숨겨지는 효과를 구현하기 위한 변수
        깜빡임 효과의 주기를 제어, 특정 이벤트가 일정 시간 간격으로 반복되도록 하는데 사용
        '''

        if sound == 1:
            if powerup == False and not pause:
                powerup_sound.stop()
                bgm.play(-1)
            if powerup and not pause:
                bgm.stop()
                powerup_sound.play(-1)

        if counter < 19:
            counter += 1
            if counter > 3:
                flicker = False
        else: #counter//5가 계속 0~3이 됨
            counter = 0
            flicker = True
        if powerup and power_counter < 600:
            power_counter += 1
        elif powerup and power_counter >= 600:
            power_counter = 0 # power_counert : 'powerup = Ture'의 지속상태
            powerup = False # 아이템 효과 끝
            eaten_ghost = [False, False, False, False] # 아이템 끝났으면 초기화
        if startup_counter < 180 and not game_over and not game_won and not pause: # 게임 시작하기 전에 3초 시간 주고 시작, 게임 안끝났고 안 이겼으면
            flicker = False
            moving = False # moving 불가
            ready_text = font.render(f'GET READY', True, 'white')  # antialias : True -> 선 부드럽게..
            screen.blit(ready_text, (360+350, 500))
            startup_counter += 1
            pygame.display.flip()
        elif startup_counter >= 180 and not game_over and not game_won: # 3초 지나고 게임 끝난 상태 아니면
            moving = True


        screen.fill('black') # 스크린 색
        draw_board() # draw_board()함수 호출로 미로 그리기
        # 플레이어의 중심점을 주려고 중심점 만든거임. 한칸이 (45,45라서) -> 이게 정확한 반의 수치는 아닌데 좀 더 자연스럽게 딱 중간이라...
        center_x = player_x + 23
        center_y = player_y + 24
        if powerup: # 파워업 먹으면 유령 속도 느려짐
            ghost_speeds = [1, 1, 1, 1]
        else: # 아니면 디폴트값
            ghost_speeds = [2, 2, 2, 2]
        if eaten_ghost[0]: # 내가 이미 먹었던 애면
            ghost_speeds[0] = 2
        if eaten_ghost[1]:
            ghost_speeds[1] = 2
        if eaten_ghost[2]:
            ghost_speeds[2] = 2
        if eaten_ghost[3]:
            ghost_speeds[3] = 2
        # 죽으면 유령 엄청 빨라져서 상자로 들어가게
        if blinky_dead:
            ghost_speeds[0] = 4
        if inky_dead:
            ghost_speeds[1] = 4
        if pinky_dead:
            ghost_speeds[2] = 4
        if clyde_dead:
            ghost_speeds[3] = 4

        game_won = True
        for i in range(len(level)):
            if 1 in level[i] or 2 in level[i]: # 칸 중에 코인이 남아있는 칸 있는가?
                game_won = False # 코인 남아있으면 게임 끝 x





        # player_circle = pygame.draw.circle(screen, 'purple', (center_x, center_y), 20, 2) #플레이어 히트박스 제대로 됐는지 확인하는 코드
        player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 10, 2) # 플레이어 히트박스
        draw_player()
        blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_img, blinky_direction, blinky_dead,
                       blinky_box, 0)
        inky = Ghost(inky_x, inky_y, targets[1], ghost_speeds[1], inky_img, inky_direction, inky_dead,
                     inky_box, 1)
        pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_img, pinky_direction, pinky_dead,
                      pinky_box, 2)
        clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speeds[3], clyde_img, clyde_direction, clyde_dead,
                      clyde_box, 3)

        if game_over:  # 졌을 경우
            flicker_gameover_won+=1
            bgm.stop()
            powerup_sound.stop()
            if game_won == False: # 유령과 닿음 + 코인 전부 먹는 거 동시에 했을 시 -> win gameover 텍스트 동시에 안 뜨게
                screen.blit(game_over_img, (WIDTH // 2 - 250+350, 350))
                if flicker_gameover_won % 60 >= 5:
                    press_enter_to_restart_text = font.render(f'press [SPACE] to restart', True,
                                                              'white')  # antialias : True -> 선 부드럽게..
                    screen.blit(press_enter_to_restart_text, (230 + 350, 480))
        if game_won:  # 이겼을 경우
            flicker_gameover_won += 1
            bgm.stop()
            powerup_sound.stop()
            if game_won_sound == False and sound == 1:
                win_sound.play(0)
                game_won_sound = True
            game_over = False  # GAME OVER
            moving = False #이겼을 때 이동 못하게
            trophy = pygame.transform.scale(pygame.image.load(f'assets/game_over/gold_trophy.png'), (200, 200))
            win = pygame.transform.scale(pygame.image.load(f'assets/game_over/win.png'), (623, 102))
            screen.blit(trophy, (WIDTH // 2 - 350+350, 300))
            screen.blit(win, (WIDTH // 2 - 250+350, 370))
            if flicker_gameover_won % 60 >= 5:
                press_enter_to_continue_text = font.render(f'press [SPACE] to continue', True,
                                                           'white')  # antialias : True -> 선 부드럽게..
                screen.blit(press_enter_to_continue_text, (230 + 350, 500))

        if powerup: # 파워업 먹었으면
            pygame.draw.circle(screen, 'blue', (162, 46), 10)
        draw_misc()

        # pause 화면
        if pause:
            bgm.stop()
            powerup_sound.stop()
            draw_pause()



        targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y) # 유령 정보들 주고 타겟 리스트

        turns_allowed = check_position(center_x, center_y) # 내 캐릭터 중심 좌표 주고 -> 내가 돌 수 있는지, 움직여도 되는지~
        if moving == True and not pause:
            player_x, player_y = move_player(player_x, player_y) # 플레이어 움직임
            if not blinky_dead and not blinky.in_box: # 유령 안 죽고 상자 밖
                blinky_x, blinky_y, blinky_direction = blinky.move_blinky() #유령1 움직임
            else: #죽었으니까 clyde로
                blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
            if not pinky_dead and not pinky.in_box:
                pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
            else:
                pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
            if not inky_dead and not inky.in_box:
                inky_x, inky_y, inky_direction = inky.move_inky()
            else:
                inky_x, inky_y, inky_direction = inky.move_clyde()
            clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
        save_file.score, powerup, power_counter, eaten_ghost = check_collisions(save_file.score, powerup, power_counter, eaten_ghost) #코인이랑 충돌하는지 + 점수 획득, 유령 먹었는지, 파워업

        if not powerup: # 파워업 비활성화 됐는데
            if (player_circle.colliderect(blinky.rect) and not blinky.dead) or \
                    (player_circle.colliderect(inky.rect) and not inky.dead) or \
                    (player_circle.colliderect(pinky.rect) and not pinky.dead) or \
                    (player_circle.colliderect(clyde.rect) and not clyde.dead): # 살아있는 유령이랑 닿았으면
                if lives > 0:
                    if sound == 1:
                        bgm.stop()
                        powerup_sound.stop()
                        dead_sound.play(0)
                    time.sleep(1)
                    lives -= 1 # 목숨 개수를 1 빼기
                    # 밑에 애들 리셋 -> 박스에 있는지 없는지는 딱히 리셋 안해도 됨.
                    startup_counter = 0
                    powerup = False
                    power_counter = 0
                    player_x = 450+350
                    player_y = 663
                    direction = 0
                    direction_command = 0
                    blinky_x = 56+350
                    blinky_y = 58
                    blinky_direction = 0
                    inky_x = 410+350
                    inky_y = 388
                    inky_direction = 2
                    pinky_x = 450+350
                    pinky_y = 408
                    pinky_direction = 2
                    clyde_x = 440+350
                    clyde_y = 438
                    clyde_direction = 2
                    eaten_ghost = [False, False, False, False]
                    blinky_dead = False
                    inky_dead = False
                    clyde_dead = False
                    pinky_dead = False
                else: #생명 0개 남았으면
                    bgm.stop()
                    powerup_sound.stop()
                    if game_over_sound == False and sound == 1:
                        gameover_sound.play(0)
                        game_over_sound = True
                    game_over = True #GAME OVER
                    moving = False #움직 x
                    startup_counter = 0
        # 방금 나한테 죽었는데 상자에서 살아나서 나온 애랑 파워업 활성화중에 마주치면 -> 안죽게
        if powerup and player_circle.colliderect(blinky.rect) and eaten_ghost[0] and not blinky.dead: # 파워업 있는데 살아있는 유령이랑 닿음 + 먹힌 유령임
            if lives > 0:
                if sound == 1:
                    bgm.stop()
                    powerup_sound.stop()
                    dead_sound.play(0)
                time.sleep(1)
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x = 450+350
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 56+350
                blinky_y = 58
                blinky_direction = 0
                inky_x = 450+350
                inky_y = 388
                inky_direction = 2
                pinky_x = 405+350
                pinky_y = 350
                pinky_direction = 2
                clyde_x = 430+350
                clyde_y = 438
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
            else:
                bgm.stop()
                powerup_sound.stop()
                if game_over_sound == False and sound == 1:
                    gameover_sound.play(0)
                    game_over_sound = True
                game_over = True
                moving = False
                startup_counter = 0
        if powerup and player_circle.colliderect(inky.rect) and eaten_ghost[1] and not inky.dead:
            if lives > 0:
                if sound == 1:
                    bgm.stop()
                    powerup_sound.stop()
                    dead_sound.play(0)
                time.sleep(1)
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x = 450+350
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 56+350
                blinky_y = 58
                blinky_direction = 0
                inky_x = 430+350
                inky_y = 388
                inky_direction = 2
                pinky_x = 450+350
                pinky_y = 350
                pinky_direction = 2
                clyde_x = 410+350
                clyde_y = 438
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
            else:
                bgm.stop()
                powerup_sound.stop()
                if game_over_sound == False and sound == 1:
                    gameover_sound.play(0)
                    game_over_sound = True
                game_over = True
                moving = False
                startup_counter = 0
        if powerup and player_circle.colliderect(pinky.rect) and eaten_ghost[2] and not pinky.dead:
            if lives > 0:
                if sound == 1:
                    bgm.stop()
                    powerup_sound.stop()
                    dead_sound.play(0)
                time.sleep(1)
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x = 450+350
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 56+350
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440+350
                inky_y = 388
                inky_direction = 2
                pinky_x = 410+350
                pinky_y = 420
                pinky_direction = 2
                clyde_x = 450+350
                clyde_y = 438
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
            else:
                bgm.stop()
                powerup_sound.stop()
                if game_over_sound == False and sound == 1:
                    gameover_sound.play(0)
                    game_over_sound = True
                game_over = True
                moving = False
                startup_counter = 0
        if powerup and player_circle.colliderect(clyde.rect) and eaten_ghost[3] and not clyde.dead:
            if lives > 0:
                if sound == 1:
                    bgm.stop()
                    powerup_sound.stop()
                    dead_sound.play(0)
                time.sleep(1)
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x = 450+350
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 56+350
                blinky_y = 58
                blinky_direction = 0
                inky_x = 450+350
                inky_y = 388
                inky_direction = 2
                pinky_x = 420+350
                pinky_y = 418
                pinky_direction = 2
                clyde_x = 350+350
                clyde_y = 438
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
            else:
                bgm.stop()
                powerup_sound.stop()
                if game_over_sound == False and sound == 1:
                    gameover_sound.play(0)
                    game_over_sound = True
                game_over = True
                moving = False
                startup_counter = 0
        if powerup and player_circle.colliderect(blinky.rect) and not blinky.dead and not eaten_ghost[0]:#파워업 있는데 살아있는 유령이랑 닿음 + 안 먹힌 유령임
            blinky_dead = True #유령 죽음
            eaten_ghost[0] = True #먹은 것도 True
            save_file.score += (3 ** eaten_ghost.count(True)) * 100 #몇 개 먹었는지에 따라 점수 증가

            ghost_score_text = font.render(f'{(3 * eaten_ghost.count(True)) * 100}', True, 'red')
            screen.blit(ghost_score_text, (blinky_x, blinky_y))
            pygame.display.flip()
            time.sleep(1)  # 1초 지연
        #유령 죽이면 점수 획득+출력
        if powerup and player_circle.colliderect(inky.rect) and not inky.dead and not eaten_ghost[1]:
            inky_dead = True
            eaten_ghost[1] = True
            save_file.score += (3 ** eaten_ghost.count(True)) * 100

            ghost_score_text = font.render(f'{(3 * eaten_ghost.count(True)) * 100}', True, 'red')
            screen.blit(ghost_score_text, (inky_x, inky_y))
            pygame.display.flip()
            time.sleep(1)  # 1초 지연
        if powerup and player_circle.colliderect(pinky.rect) and not pinky.dead and not eaten_ghost[2]:
            pinky_dead = True
            eaten_ghost[2] = True
            save_file.score += (3 ** eaten_ghost.count(True)) * 100

            ghost_score_text = font.render(f'{(3 * eaten_ghost.count(True)) * 100}', True, 'red')
            screen.blit(ghost_score_text, (pinky_x, pinky_y))
            pygame.display.flip()
            time.sleep(1)  # 1초 지연
        if powerup and player_circle.colliderect(clyde.rect) and not clyde.dead and not eaten_ghost[3]:
            clyde_dead = True
            eaten_ghost[3] = True
            save_file.score += (3 ** eaten_ghost.count(True)) * 100

            ghost_score_text = font.render(f'{(3 * eaten_ghost.count(True)) * 100}', True, 'red')
            screen.blit(ghost_score_text, (clyde_x, clyde_y))
            pygame.display.flip()
            time.sleep(1)  # 1초 지연


        for event in pygame.event.get(): # 모든 이벤트들 리스트로해서 event에 하나씩 for문으로 넣어줌
            if event.type == pygame.QUIT:
                run = False # 나갈려고 x표 누르면 무한루프 나감
            if event.type == pygame.KEYDOWN: # 키 이벤트가 키가 눌리는 거일때
                if event.key == pygame.K_RIGHT: # 오른쪽 누를때
                    direction_command = 0
                if event.key == pygame.K_LEFT: # 왼쪽 누를때
                    direction_command = 1
                if event.key == pygame.K_UP: # 위 누를때
                    direction_command = 2
                if event.key == pygame.K_DOWN: # 아래 누를때
                    direction_command = 3
                if event.key == pygame.K_SPACE and game_over: # 게임 끝났을 때 스페이스바 눌렀으면
                    # 게임 초기화 -> 다시 시작
                    gameover_sound.stop()
                    game_over_sound = False
                    powerup = False
                    power_counter = 0
                    lives -= 1
                    startup_counter = 0
                    player_x = 450+350
                    player_y = 663
                    direction = 0
                    direction_command = 0
                    blinky_x = 56+350
                    blinky_y = 58
                    blinky_direction = 0
                    inky_x = 420+350
                    inky_y = 408
                    inky_direction = 2
                    pinky_x = 450+350
                    pinky_y = 448
                    pinky_direction = 2
                    clyde_x = 440+350
                    clyde_y = 438
                    clyde_direction = 2
                    eaten_ghost = [False, False, False, False]
                    blinky_dead = False
                    inky_dead = False
                    clyde_dead = False
                    pinky_dead = False
                    lives = 3
                    level = copy.deepcopy(boards) #게임 도는 동안 level은 오리지널함.
                    game_over = False
                    game_won = False
                elif event.key == pygame.K_SPACE and game_won:
                    win_sound.stop()
                    round2_1.round2(sound)
                elif event.key == pygame.K_SPACE: # pause
                    if pause == True:
                        pause = False
                    else:
                        pause = True




            if event.type == pygame.KEYUP: # 키 이벤트가 키가 떼는 거일때
                if event.key == pygame.K_RIGHT and direction_command == 0: # 오른쪽 누를때
                    direction_command = direction
                if event.key == pygame.K_LEFT and direction_command == 1: # 왼쪽 누를때
                    direction_command = direction
                if event.key == pygame.K_UP and direction_command == 2: # 위 누를때
                    direction_command = direction
                if event.key == pygame.K_DOWN and direction_command == 3: # 아래 누를때
                    direction_command = direction

        for i in range(4):
            if direction_command == i and turns_allowed[i] == True:
                direction = i

        if player_x > 900+350: # 화면 너비 오른쪽으로 넘으면
            player_x = -40+350
        elif player_x < -40+350: # 왼쪽으로 너무 가서 완전히 사라지는
            player_x = 897+350

        if blinky.in_box and blinky_dead: # 유령 상자에 있고 죽었으면
            blinky_dead = False # 죽은거 False로 -> 다시 유령 상자에서 살아나게
        if inky.in_box and inky_dead:
            inky_dead = False
        if pinky.in_box and pinky_dead:
            pinky_dead = False
        if clyde.in_box and clyde_dead:
            clyde_dead = False

        save_file.save()
        pygame.display.flip() # 화면 전체 업데이트
    pygame.quit() # 종료
