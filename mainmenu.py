import pygame
import time
import sys
import pacman_2
import option
import resources.save_files
import resources.images.characters
import platform

os_name = platform.system()

if os_name == "Windows":
    import ctypes

    u32 = ctypes.windll.user32
    resolution = u32.GetSystemMetrics(0), u32.GetSystemMetrics(1)
else:
    resolution = [1600, 1000]

sound = 1

pygame.mixer.init() # 사운드 초기화
pygame.init() # pygame 초기화

#WIDTH = 900
#HEIGHT = 950 # 창 가로세로 상수로 정해두고 시작 ->이거 해상도마다 다르게 보일 수 있음
fps = 60
timer = pygame.time.Clock() # 속도 제어 위해서
#screen = pygame.display.set_mode([WIDTH, HEIGHT],pygame.FULLSCREEN) # 창 가로세로 정하기
screen = pygame.display.set_mode(resolution,pygame.FULLSCREEN)

easter_egg1=[0, 0, 0, 0, 0, 0] # 1번 이스터 조건
easter = 0 # 1번 이스터 상자를 떨궜는지
easter_now = [0, 0] # 이스터 에그 발견 현황 -> 1번 이스터 상자 열기까지 했는지
global is_earned # global : 전역변수로 사용할 것이다
is_earned = False

save_file = resources.save_files.save_file() # 빈 save_file 생성
save_file.load() # save_file 변수에 json 입력

# 사운드 가져오기
click_easter = pygame.mixer.Sound("assets/sounds/click_easter.wav")
open_the_box = pygame.mixer.Sound("assets/sounds/open_the_box.wav")
box_drop = pygame.mixer.Sound("assets/sounds/box_drop.wav")
button_sound = pygame.mixer.Sound("assets/sounds/button.wav")
button_sound.set_volume(0.5)

# sound : 소리 여부, action : 실행할 함수, func : 어떤 함수에서 들어갔는지 -> main_menu에서 들어갈 떄만 실행되는 애 있었으면 해서..
def Button(img, click_img, x, y, width, height, sound , param = None, action = None, func = None):
    mouse = pygame.mouse.get_pos() # 마우스 커서의 위치를 변수에 지정
    click = pygame.mouse.get_pressed() # 클릭시
    if x + width > mouse[0] > x and y + height > mouse[1] > y: # 마우스가 버튼 영역에 있다면
        screen.blit(click_img, (x, y)) # click_img 렌더링
        if func != None: # func 파라미터가 주어진 경우
            pygame.draw.polygon(screen, (195,195,195), [[x-50, y+height//2 - 20], [x-50,y+height//2+20], [x-30, y+height//2]], 5) # 삼각형 요소 추가
        if click[0] and action != None and param != None: # 왼쪽 마우스 눌린 경우 + 이후 실행할 함수 있는 경우 + score주는 경우 -> 걍 사실상 pacman실행 or option 실행
            if func != None: # func 파라미터가 주어진 경우
                pygame.draw.polygon(screen, (255, 255, 255),
                                [[x - 50, y + height // 2 - 20], [x - 50, y + height // 2 + 20],
                                 [x - 30, y + height // 2]], 5) # 삼각형 요소 추가
                pygame.draw.polygon(screen, 'Red', [[x - 50, y + height // 2 - 20], [x - 50, y + height // 2 + 20],
                                                [x - 30, y + height // 2]], 5) # ???
            pygame.display.flip() # 화면에 변경사항 저장
            if sound == 1:
                button_sound.play(0)
            time.sleep(1) #1초 지연
            
            if action == pacman_2.pacman: # 게임 실행인 경우
                action() # 파라미터 불필요
            else: # 게임 실행이 아닌 경우 (option 실행인 경우)
                action(param) # 파라미터 전달

        elif click[0] and action != None and param == None: # 왼쪽 마우스 눌린 경우 + 이후 실행할 수 있는 함수 있는 경우 + score가 없는 경우
            if func != None: # func 파라미터가 주어진 경우
                pygame.draw.polygon(screen, (255, 255, 255), 
                                [[x - 50, y + height // 2 - 20], [x - 50, y + height // 2 + 20],
                                 [x - 30, y + height // 2]], 5)
                pygame.draw.polygon(screen, 'Red', [[x - 50, y + height // 2 - 20], [x - 50, y + height // 2 + 20],
                                                [x - 30, y + height // 2]], 5)
            pygame.display.flip() 
            if sound == 1:
                button_sound.play(0)
            time.sleep(1) 
            action()
        elif click[0] and action == None: # 왼쪽 마우스 눌린 경우 + 이후 실행할 함수 없는 경우 -> 아직 버튼에 함수 안 이은 상태일 때
            if func != None: # func 파라미터가 주어진 경우
                pygame.draw.polygon(screen, (255, 255, 255), [[x - 50, y + height // 2 - 20], [x - 50, y + height // 2 + 20],
                                                    [x - 30, y + height // 2]], 5)
                pygame.draw.polygon(screen, 'Red', [[x - 50, y + height // 2 - 20], [x - 50, y + height // 2 + 20],
                                                [x - 30, y + height // 2]], 5)
            pygame.display.flip()
            if sound == 1:
                button_sound.play(0)
    else:
        if func != None: # func 파라미터가 주어진 경우
            pygame.draw.polygon(screen, (0, 0, 0),[[x - 50, y + height // 2 - 20], [x - 50, y + height // 2 + 20], [x - 30, y + height // 2]],5)
        screen.blit(img, (x, y))
        pygame.display.flip()


def chain_letters(easter_now,sound): # 이스터 에그 보물상자 열 경우 텍스트와 사운드 sound : 소리여부
    if easter_now[0] == 0 and sound == 1: # 이스터에그 1번 상자 열기 + 사운드 O
        open_the_box.play(0)
    easter_now[0] = 1
    font = pygame.font.Font("assets/pacman_main_menu_images/NPSfont_regular.ttf", 26)
    chain_letter = font.render(f'강남대 구모씨가 숨긴 이스터에그를 발견하셨습니다! 남은 이스터에그 :  0개', True,
                            'green')
    screen.blit(chain_letter, (resolution[0]//2-450, 350))
    chain_letter = font.render(f'Extra Coin +100000', True,
                               'red')
    screen.blit(chain_letter, (resolution[0]//2-180, 400))
    global is_earned # global : 전역변수로 지정
    if not is_earned:
        save_file.score += 100000
        save_file.save()  # 게임 종료 시 점수 저장
        is_earned = True

def quitgame(): # 게임 끄기 함수
    pygame.quit()
    sys.exit() # ???
def main_menu(easter, easter_now, sound):
    screen.fill('black')  # 배경 색
    pacman_logo = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/pacman_logo.png'), (600, 300))
    image = []

    #이미지 가져오기
    pacman = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/pacman.png'),(45, 45))
    black1 = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/black.png'), (45, 45))
    black2 = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/black.png'), (150, 120))
    red_ghost = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/red_ghost.png'),(45,45))
    blue_ghost = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/blue_ghost.png'), (45, 45))
    pink_ghost = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/pink_ghost.png'), (45, 45))
    orange_ghost = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/orange_ghost.png'), (45, 45))
    start_img = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/START.png'), (208,50))
    options_img = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/OPTIONS.png'), (230, 65))
    exit_img = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/EXIT.png'),(160, 52))
    click_start_img = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/CLICK_START.png'), (208, 50))
    click_options_img = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/CLICK_OPTIONS.png'),(230, 65))
    click_exit_img = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/CLICK_EXIT.png'), (160, 52))
    closed_treasure_box = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/closed_treasure_box.png'), (150, 120))
    opened_treasure_box = pygame.transform.scale(pygame.image.load(f'assets/pacman_main_menu_images/opened_treasure_box.png'),
                                            (150, 120))

    image.append(pacman)
    image.append(red_ghost)
    image.append(pink_ghost)
    image.append(blue_ghost)
    image.append(orange_ghost)
    light_yellow = (255, 255, 150)

    menu = True
    while menu:
        for event in pygame.event.get():  # 모든 이벤트들 리스트로 해서 event에 하나씩 for문으로 넣어줌
            if event.type == pygame.QUIT:
                quitgame()
            # 이스터에그 -> 모든 유령과 팩맨, 코인 눌러서 없애기
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # 왼쪽 마우스 클릭
                    mouse_x, mouse_y = event.pos
                    for i in range(len(image)):
                        if resolution[0] // 2 - 150 + i*50 + 45 > mouse_x > resolution[0] // 2 - 150 + i*50 and 370 + 45-25 > mouse_y > 370-25 and not easter and not easter_now[0]: # ???
                            if easter_egg1[i] == 0 and sound == 1:
                                click_easter.play(0)
                            easter_egg1[i] = 1
                            screen.blit(black1,(resolution[0] // 2 - 150 + i*50, 370-25))
                    if resolution[0] // 2 - 175 + 10 > mouse_x > resolution[0] // 2 - 175 - 10 and 405-25 > mouse_y > 385-25 and not easter and not easter_now[0]: #동전 이스터 클릭
                        if easter_egg1[5] == 0 and sound == 1:
                            click_easter.play(0)
                        easter_egg1[5] = 1
                        screen.blit(black1, (resolution[0] // 2 - 175 - 10, 395 - 10 -25))
                    # 이스터에그 깨고 보물상자 나와서 그 보물상자 누르면 -> 보물상자 열리고 행운의 편지 등장
                    elif (resolution[0]//2 - 125 + 150 > mouse_x > resolution[0]//2 - 125) and (300+120 > mouse_y > 300) and easter: #상자 나왔지만 아직 안 열었음 근데 상자 클릭함
                        screen.blit(black2, (resolution[0] // 2 - 125, 300))
                        screen.blit(opened_treasure_box, (resolution[0] // 2 - 125, 300))
                        time.sleep(1/4)  # 1초 지연
                        chain_letters(easter_now,sound)
                        pygame.display.flip()
        if easter and easter_now[0]:
            screen.blit(opened_treasure_box, (resolution[0] // 2 - 125, 300))
            chain_letters(easter_now,sound)

        screen.blit(pacman_logo, (resolution[0]//2-350,60))
        if easter == False and easter_now[0] == False:
            # 그 이미지의 이스터에그 안눌렀을 때만 가능
            if easter_egg1[5] == 0:
                pygame.draw.circle(screen, light_yellow, (resolution[0] // 2 - 175, 395-25), 10)
            for i in range(len(image)): #로고랑 그 메뉴들 사이에 있는 유령이랑 팩맨 이미지 그리기
                if easter_egg1[i] == 0:
                    screen.blit(image[i], (resolution[0] // 2 - 150 + i*50, 370-25))


        # 이스터에그 조건 확인 -> 다 했으면 보물상자 등장
        if easter == False and easter_now[0] == False:
            for i in range(len(easter_egg1)):
                if easter_egg1.count(1) == 6:
                    time.sleep(1/8)  # 1초 지연
                    if easter == False:
                        if sound == 1:
                            box_drop.play(0)
                        easter = True
                        screen.blit(closed_treasure_box,(resolution[0]//2 - 125 ,300))
                        pygame.display.flip()




        font = pygame.font.Font("assets/pacman_main_menu_images/neodgm.ttf", 30)
        #우리 이름
        name_text = font.render(f'파이썬 응용 - 구서연 김민재 양현준 이윤석', True,
                                                   'white')  # antialias : True -> 선 부드럽게..
        font = pygame.font.Font("assets/pacman_main_menu_images/emulogic.ttf", 30)
        screen.blit(name_text, (resolution[0]//2-350, 0))

        startButton = Button(start_img, click_start_img, resolution[0] // 2-308//2, resolution[1]//2+50, 208,50, sound, save_file.score, pacman_2.pacman, main_menu)
        opionButton = Button(options_img, click_options_img, resolution[0] // 2 - 325 // 2, resolution[1]//2+150, 230, 65,sound,[easter,easter_now], action = option.options,func = main_menu)
        exitbutton = Button(exit_img, click_exit_img, resolution[0] // 2 - 260 // 2, resolution[1]//2+260, 160, 52, sound,None, quitgame,func = main_menu)

        timer.tick(fps)
        pygame.display.flip()  # 화면 전체 업데이트
if __name__ == "__main__": # 여기 py안에서 실행될 때만
    main_menu(easter, easter_now, sound)
