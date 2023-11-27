import pygame
import ctypes

u32 = ctypes.windll.user32
resolution = u32.GetSystemMetrics(0), u32.GetSystemMetrics(1)

import time
WIDTH = 900
HEIGHT = 950  # 창 가로세로 상수로 정해두고 시작 ->이거 해상도마다 다르게 보일 수 있음
#screen = pygame.display.set_mode([WIDTH, HEIGHT],pygame.FULLSCREEN) #창 가로세로 정하기
screen = pygame.display.set_mode(resolution,pygame.FULLSCREEN)

timer = pygame.time.Clock()  # 속도 제어 위해서
fps = 60  # 게임 플레이할 수 있는 최대속도
# 옵션 이미지 가져오기
setting = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/setting.png'), (709, 841))
yes = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/yes.png'), (100,100))
clicked_yes = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/clicked_yes.png'), (100,100))
no = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/no.png'), (100,100))
clicked_no = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/clicked_no.png'), (100,100))
save = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/save.png'), (201,98))
clicked_save = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/clicked_save.png'), (201,98))
green = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/green.png'), (100,100))
blue = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/blue.png'), (100,100))
pink = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/pink.png'), (100,100))
yellow = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/yellow.png'), (100,100))
best = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/best.png'), (76,76))
check = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/best.png'), (100,100))
clicked_green = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/clicked_green.png'), (100, 100))
clicked_blue = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/clicked_blue.png'), (100, 100))
clicked_pink = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/clicked_pink.png'), (100, 100))
clicked_yellow = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/clicked_yellow.png'), (100, 100))
# 미로 색상 리스트 만들기
colors = []
colors.append(green)
colors.append(blue)
colors.append(pink)
colors.append(yellow)

# 안 누른 기본 sound 리스트 만들기
unclicked_sound = []
unclicked_sound.append(no)
unclicked_sound.append(yes)

maze_index = 0
sound = 1
maze_color = green
def Button(img, click_img, x, y, width, height, a,b,c, action = None):
    import pygame
    import time


    button_sound = pygame.mixer.Sound("assets/sounds/button.wav")
    button_sound.set_volume(0.5)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()#클릭시
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        screen.blit(click_img,(x,y))
        if click[0] and action != None: #실행할 함수 있고 클릭
            screen.blit(click_img, (x, y))
            button_sound.play(0)
            time.sleep(1) #1초 지연
            action(a,b,c)
        elif click[0] and action == None: #왼쪽 마우스 눌린 경우 + 이후 실행할 함수 없는 경우 -> 아직 버튼에 함수 안 이은 상태일 때
            button_sound.play(0)
            screen.blit(click_img,(x,y))
    else:
        screen.blit(img, (x, y))
def sound_button(img, click_img,x,y, width, height):
    global sound
    clicked_sound = []
    clicked_sound.append(clicked_no)
    clicked_sound.append(clicked_yes) #이 순서는 sound를 인덱스로 주려고.. sound 참일 때 누른 yes sound 거짓일 때 누른 no

    sound_button = pygame.mixer.Sound("assets/sounds/click_sound.mp3")
    sound_button.set_volume(0.5)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()  # 클릭시


    screen.blit(clicked_sound[sound], (resolution[0] // 2 - 400 // 2+sound*300, 400))  # 현재 선택되어있는 색 체크중
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        # screen.blit(click_img,(x,y))
        if click[0] and img==yes:  # 현재 색상 아닌 색 선택
            screen.blit(unclicked_sound[0], (resolution[0] // 2 - 400 // 2+0*300, 400))
            screen.blit(click_img, (x, y))
            if sound != 1:
                sound_button.play(0)
            return 1
        if click[0] and img == no:  # 지금 누르는 색이 원래 결정되었던 색인 경우
            screen.blit(unclicked_sound[1], (resolution[0] // 2 - 400 // 2+1*300, 400))
            screen.blit(click_img, (x, y))
            if sound != 0:
                sound_button.play(0)
            return 0
        else:
            return sound
    else:
        return sound
def color(img, click_img, x, y, width, height): #color_index : 그 직전 결정되어있었던 색 무엇이었는지
    global maze_index
    global maze_color


    clicked_colors = []
    clicked_colors.append(clicked_green)
    clicked_colors.append(clicked_blue)
    clicked_colors.append(clicked_pink)
    clicked_colors.append(clicked_yellow)

    if maze_color == green:
        maze_index = 0
    elif maze_color == blue:
        maze_index = 1
    elif maze_color == pink:
        maze_index = 2
    elif maze_color == yellow:
        maze_index = 3

    # 소리
    color_button_sound = pygame.mixer.Sound("assets/sounds/color_button.mp3")
    color_button_sound.set_volume(0.5)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed() # 클릭시

    screen.blit(clicked_colors[maze_index], (resolution[0] // 2 - 620 // 2+maze_index*170, 650)) #현재 선택되어있는 색 체크중
    if maze_index == 0: # 초록색은 위에 베스트 표시 있어야해서..
        screen.blit(best, (resolution[0] // 2 - 685 // 2, 610))
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        # screen.blit(click_img,(x,y))
        if click[0] and maze_color!=img: # 현재 색상 아닌 색 선택
            screen.blit(colors[maze_index], (resolution[0] // 2 - 620 // 2+maze_index*170, 650))
            screen.blit(click_img, (x, y))
            color_button_sound.play(0)
            return img
        if click[0] and maze_color==img: # 지금 누르는 색이 원래 결정되었던 색인 경우
            screen.blit(click_img, (x, y))
            return img

def options(l):
    import mainmenu

    easter, easter_now = l

    global sound # 전역변수로 사용
    global maze_color
    while True:
        for event in pygame.event.get():  # 모든 이벤트들 리스트로 해서 event에 하나씩 for문으로 넣어줌
            if event.type == pygame.QUIT:
                mainmenu.quitgame()
        screen.blit(setting,(resolution[0]//2-709//2,30)) # option 밑그림
        for i in range(4): #색 체크칸
            screen.blit(colors[i], (resolution[0] // 2 - 620 // 2+i*170, 650))
        screen.blit(best, (resolution[0] // 2 - 685 // 2, 610))

        for i in range(2): #사운드 칸
            screen.blit(unclicked_sound[i], (resolution[0] // 2 - 400 // 2+i*300, 400))

        Button(save, clicked_save, resolution[0] // 2 - 201//2, 800, 201,98, easter,easter_now,sound,action=mainmenu.main_menu)

        sound = sound_button(yes, clicked_yes,resolution[0] // 2 - 400 // 2+1*300, 400,100,100) # 사운드 O
        sound = sound_button(no, clicked_no, resolution[0] // 2 - 400 // 2+0*300, 400,100,100) # 사운드 X

        maze_color = color(green, clicked_green, resolution[0] // 2 - 620 // 2 + 0 * 170, 650, 100, 100)
        maze_color = color(blue, clicked_blue, resolution[0] // 2 - 620 // 2+1*170, 650, 100, 100)
        maze_color = color(pink, clicked_pink, resolution[0] // 2 - 620 // 2 + 2 * 170, 650, 100, 100)
        maze_color = color(yellow, clicked_yellow, resolution[0] // 2 - 620 // 2 + 3 * 170, 650, 100, 100)


        timer.tick(fps)
        pygame.display.flip()