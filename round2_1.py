import pygame
import random
import time
from datetime import datetime
import round3
import resources.save_files
import resources.images.characters

def round2(sound):
    # 1. 게임 초기화
    pygame.init()
    
    pygame.mixer.init()  # 믹서 초기화
    bg_music = pygame.mixer.Sound('./assets/sounds/2round_bg.mp3')  # 음악 파일 로드
    if sound == True:
        bg_music.set_volume(0.4)
        bg_music.play(-1) # 반복 재생

    save_file = resources.save_files.save_file()
    save_file.load() # 세이브파일 로드하기
    coin_list = []
    last_bullet_time = 0
    bullet_cooldown = 500  # 500ms = 0.5초

    startup_counter = 0 # 3초 후 시작하기 위해

    # 2. 게임창 옵션 설정
    size = [900, 950]
    screen = pygame.display.set_mode(size)

    title = "2R"
    pygame.display.set_caption(title)

    # 3. 게임 내 필요한 설정
    clock = pygame.time.Clock() # 시간

    class obj:
        '''
        초기상태 설정
        '''
        def __init__(self): # 초기화 함수
            self.x = 0
            self.y = 0
            self.move = 0
        '''
        이미지 파일을 로드하여 객체에 할당 (address = 이미지 파일 경로)
        '''
        def put_image(self, address):
            if address[-3:] == "png": # png 파일인지 확인
                self.img = pygame.image.load(address).convert_alpha() # png의 경우 투명도(alpha)를 지원
            else:
                self.img = pygame.image.load(address)
                self.sx, self.sy = self.img.get_size()
        '''
        객체의 이미지 크기를 변경
        sx, sy = 이미지의 가로, 세로 크기
        pygame.transform.scale을 이용하여 이미지의 크기를 조절
        '''
        def change_size(self, sx, sy): 
            self.img = pygame.transform.scale(self.img, (sx, sy))
            self.sx, self.sy = self.img.get_size()
        '''
        이미지(self.img)를 위치(self.x, self.y)에 그리기
        '''
        def show(self): 
            screen.blit(self.img, (self.x, self.y))

    '''
    .x = x축 위치, .y = y축 위치
    .sx = 가로 크기,.sy = 세로 크기
    '''

    # 히트박스(원형)
    def circle_crash(obj1, obj2):
        center1 = (obj1.x + obj1.sx / 2, obj1.y + obj1.sy / 2)
        center2 = (obj2.x + obj2.sx / 2, obj2.y + obj2.sy / 2)

        distance = ((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2) ** 0.5 # 중심 사이의 거리 계산
        radius_sum = (obj1.sx / 2) + (obj2.sx / 2)

        return distance <= radius_sum


    # ss = SpaceShip = player
    ss = obj()

    pacman_images = []
    for image_path in resources.images.characters.get_images_path(save_file.image_file):
        pacman_images.append(pygame.transform.scale(pygame.image.load(image_path), (50, 50))) # 이미지 파일을 50x50으로 로드

    ss.put_image(resources.images.characters.default_1_path) # 시작 이미지 설정
    ss.change_size(50, 50) # 이미지 크기 조정

    ss.x = round(size[0] / 2 - ss.sx / 2) # 플레이어의 x좌표
    ss.y = size[1] - ss.sy - 15 # 플레이어의 y좌표
    ss.move = 17 # 속도

    left_go = False
    right_go = False
    space_go = False

    bullet_list = []
    ghost_list = []

    black = (0, 0, 0)
    white = (255, 255, 255)
    k = 0

    is_gameovered = False
    kill = 0
    loss = 0

    # 4-0. 게임 시작 대기화면
    is_stopped = False  # Start/Stop Boolean
    while not is_stopped:
        clock.tick(60) # 60fps
        if startup_counter < 180: # 3초
            font = pygame.font.Font("assets/pacman_main_menu_images/emulogic.ttf", 50)
            screen.fill('black')
            ready_text = font.render(f'GET READY {3-startup_counter//60}', True, 'yellow')  # antialias : True -> 선 부드럽게..
            screen.blit(ready_text, (190, 450))
            startup_counter += 1
            pygame.display.flip()
        else:
            is_stopped = True


    # 4. 메인 이벤트
    start_time = datetime.now() # 현재 시간을 얻어서 경과 시간을 확인
    is_stopped = False
    while not is_stopped:

        # 4-1. FPS 설정
        clock.tick(60) # 60 fps
        current_time = pygame.time.get_ticks() # 현재 시간을 밀리세컨드 단위로 가져옴

        # 4-2. 각종 입력 감지
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_stopped = True
            if event.type == pygame.KEYDOWN: # 눌렀을 때
                if event.key == pygame.K_LEFT: # 왼쪽 화살표를
                    left_go = True # 왼쪽으로 이동
                elif event.key == pygame.K_RIGHT:
                    right_go = True
                elif event.key == pygame.K_SPACE:
                    space_go = True
                    k = 0
            elif event.type == pygame.KEYUP: # 뗐을 때
                if event.key == pygame.K_LEFT: # 왼쪽 화살표를
                    left_go = False # 왼쪽으로 이동 그만
                elif event.key == pygame.K_RIGHT:
                    right_go = False
                elif event.key == pygame.K_SPACE:
                    space_go = False
        current_image_index = k // 10 % len(pacman_images) # 10프레임마다 이미지 변경
        ss.img = pacman_images[current_image_index] # 현재 이미지 업데이트
        ss.img = pygame.transform.rotate(ss.img, 90) # 현재 이미지 90도 돌리기

        # 4-3. 입력, 시간에 따른 변화
        now_time = datetime.now() # 현재 시간 얻기
        delta_time = round((now_time - start_time).total_seconds()) # 게임 경과 시간

        if delta_time > 20: # 게임 시간은 20초
            is_stopped = True
            is_gameovered = True

        if left_go == True:
            ss.x = ss.x - ss.move # 플레이어의 x좌표 이동
            # player가 왼쪽 밖으로 나가지 않도록 조정
            if ss.x < 0:
                ss.x = 0
        elif right_go == True:
            ss.x = ss.x + ss.move
            # player가 오른쪽 밖으로 나가지 않도록 조정
            if ss.x >= size[0] - ss.sx:
                ss.x = size[0] - ss.sx
        if space_go == True and save_file.score >= 10 and current_time - last_bullet_time > bullet_cooldown: # 총알 공격속도 지정
            last_bullet_time = current_time # 마지막 총알 발사 시간 업데이트
            # mm = 총알
            mm = obj()
            mm.put_image("assets/2round_images/bullet.png")
            mm.change_size(5, 15)
            mm.x = round(ss.x + ss.sx / 2 - mm.sx / 2) # 총알의 히트박스
            mm.y = ss.y - mm.sy - 10 # player의 주둥이보다 조금 더 앞에서 총알이 나가도록 조정
            mm.move = 20 # 총알의 이동속도
            bullet_list.append(mm)
            save_file.score -= 10 # score 차감
        '''
        if 문 밖에 k가 있는 이유 :
        k는 게임의 메인루프가 반복 될때마다 증가
        프레임마다 이미지를 변경할 수 있도록 함
        '''
        k = k + 1

        d_list = [] # delete list
        for i in range(len(bullet_list)):
            m = bullet_list[i]
            m.y = m.y - m.move # 총알을 위로 이동
            if m.y <= - m.sy: # 총알이 특정 지점에 도달한다면
                d_list.append(i)
        for d in d_list:
            del bullet_list[d] # 총알 삭제

        if random.random() > 0.85: # 15% 확률 (0 ~ 1)
            aa = obj()
            ghost_images = ["assets/2round_images/orange_ghost.png", "assets/2round_images/pink_ghost.png", "assets/2round_images/red_ghost.png", "assets/2round_images/blue_ghost.png"]
            ghost_image = random.randrange(0, 4)
            aa.put_image(ghost_images[ghost_image]) # 이미지를 반복하여 생성
            aa.change_size(40, 40)
            aa.x = random.randrange(0, size[0] - aa.sx - round(ss.sx / 2)) # 유령 x좌표
            aa.y = 10 # 유령 y좌표
            # 유령마다 떨어지는 속도 다르게
            if ghost_image == 0:
                aa.move = 22
            elif ghost_image == 1:
                aa.move = 18
            elif ghost_image == 2:
                aa.move = 16
            elif ghost_image == 3:
                aa.move = 13

            ghost_list.append(aa)

        if random.random() > 0.9: # 10% 확률로 코인 생성
            coin = obj()
            coin.put_image("assets/2round_images/coin.png")
            coin.change_size(20, 20) # 코인의 크기 설정
            coin.x = random.randrange(0, size[0] - coin.sx)
            coin.y = 10 # 코인의 초기 위치
            coin.move = 8 # 코인의 이동 속도
            coin_list.append(coin)

        # 코인 삭제 로직
        coin_delete_list = []
        for i in range(len(coin_list)):
            c = coin_list[i]
            c.y = c.y + c.move # 코인을 아래로 이동
            if c.y >= size[1]:
                coin_delete_list.append(i)

        # 코인과 우주선의 충돌 감지
        for coin in coin_list[:]: # coin_list 순회
            if circle_crash(coin, ss):
                coin_list.remove(coin) # 코인 제거
                save_file.score += 10  # 플레이어 점수 증가

        # 코인 삭제 로직
        for d in reversed(coin_delete_list):
            del coin_list[d]

        d_list = []
        for i in range(len(ghost_list)):
            a = ghost_list[i]
            a.y = a.y + a.move # 유령을 아래로 이동
            if a.y >= size[1]:
                d_list.append(i)
        d_list.reverse()
        for d in d_list:
            del ghost_list[d]
            loss = loss + 1 # loss 개수 + 1

        dm_list = []
        da_list = []

        for i in range(len(bullet_list)):
            for j in range(len(ghost_list)):
                m = bullet_list[i]
                a = ghost_list[j]
                if circle_crash(m, a) == True: # 총알과 유령이 부딪혔다면
                    dm_list.append(i) # 총알 삭제 로직
                    da_list.append(j) # 유령 삭제 로직
        dm_list = list(set(dm_list))
        da_list = list(set(da_list))

        for dm in dm_list:
            del bullet_list[dm]
        for da in da_list:
            del ghost_list[da]
            kill = kill + 1

        for i in range(len(ghost_list)):
            a = ghost_list[i]
            if circle_crash(a, ss) == True:
                is_stopped = True
                is_gameovered = True

        # 4-4. 그리기
        screen.fill(black)
        ss.show()
        for m in bullet_list:
            m.show()
        for a in ghost_list:
            a.show()
        for c in coin_list:
            c.show()

        font = pygame.font.Font("assets/2round_images/SOYO.ttf", 20)
        text_kill = font.render("killed : {} loss : {}".format(kill, loss), True, (255, 255, 0))
        screen.blit(text_kill, (10, 5))

        text_time = font.render("time : {}".format(delta_time), True, (255, 255, 255))
        screen.blit(text_time, (size[0] - 100, 5))

        text_score = font.render("score : {}".format(save_file.score), True, (255, 255, 255))
        screen.blit(text_score, (size[0] - 250, 5))

        # 4-5. 업데이트
        pygame.display.flip()

    end_counter = 0 #종료 화면 후 round3 넘어가는 시간
    # 5. 게임 종료
    while is_gameovered:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_file.save()  # 게임 종료 시 점수 저장
                is_gameovered = 0
        font = pygame.font.Font("assets/pacman_main_menu_images/emulogic.ttf", 35)
        text = font.render(f"Final Score : {save_file.score}", True, 'white')
        screen.blit(text, (100, round(size[1] / 2 - 130)))
        text = font.render(f"SCORE -> COIN", True, 'yellow')
        screen.blit(text, (160, round(size[1] / 2 - 30)))
        text = font.render(f"Final Coin  : {save_file.score}", True, 'white')
        screen.blit(text, (100, round(size[1] / 2 + 70)))
        if end_counter < 60*8: # 8초
            font = pygame.font.Font("assets/pacman_main_menu_images/neodgm.ttf", 25)
            pygame.draw.rect(screen, 'black', [540,round(size[1] / 2 + 200) , 25, 25], 13)
            text = font.render(f"상점까지 남은 시간 앞으로 {7-end_counter//60}초..", True, 'white') #7~0까지 나오게
            screen.blit(text, (220, round(size[1] / 2 + 200)))
            end_counter += 1
            pygame.display.flip()
        else:
            round3.round3(sound)
            pygame.display.flip()
        bg_music.stop()
    pygame.quit()