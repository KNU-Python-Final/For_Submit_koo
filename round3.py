import pygame
import time
import resources.images.characters
import resources.save_files
import mainmenu
from mainmenu import easter
from mainmenu import easter_now
import ctypes

u32 = ctypes.windll.user32
resolution = u32.GetSystemMetrics(0), u32.GetSystemMetrics(1)

def round3(sound):
    pygame.init()
    pygame.mixer.init()
    buy_button_music = pygame.mixer.Sound('./assets/sounds/2round_bg.mp3')  # 음악 파일 로드
    buy_button_music = pygame.mixer.Sound('./assets/sounds/open_the_box.wav')  # 음악 파일 로드
    buy_button_music.set_volume(0.7) # 볼륨 설정
    save_file = resources.save_files.save_file() # 빈 save_file 생성
    save_file.load() # save_file 변수에 json 입력

    # 초기 설정 및 이미지 로드
    WIDTH, HEIGHT = 900, 950
    #screen = pygame.display.set_mode([WIDTH, HEIGHT],pygame.FULLSCREEN) # 창의크기 설정
    screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    pygame.display.set_caption("3round") # 제목 설정

    font = pygame.font.SysFont('arial', 24)
    price_font = pygame.font.SysFont('arial', 30)
    button_font = pygame.font.SysFont('arial', 40)

    button_colors = [(255, 165, 0), (0, 191, 255), (255, 69, 0), (138, 43, 226), (128, 128, 128)] # 버튼의 색상(RGB) 지정

    exit_img = pygame.transform.scale(pygame.image.load(resources.images.characters.exit_path), (40, 40))
    background_image = pygame.image.load(resources.images.characters.bg_path)
    shop_image = pygame.transform.scale(pygame.image.load(resources.images.characters.shop_sign_path), (400, 150))
    angel_sign_image = pygame.transform.scale(pygame.image.load(resources.images.characters.angel_sign_path), (300, 130))
    king_sign_image = pygame.transform.scale(pygame.image.load(resources.images.characters.king_sign_path), (300, 130))
    leaf_sign_image = pygame.transform.scale(pygame.image.load(resources.images.characters.leaf_sign_path), (300, 130))
    santa_sign_image = pygame.transform.scale(pygame.image.load(resources.images.characters.santa_sign_path), (300, 130))
    buy_sign_image = pygame.transform.scale(pygame.image.load(resources.images.characters.buy_sign_path), (300, 130))
    heart_sign_image = pygame.transform.scale(pygame.image.load(resources.images.characters.heart_convert_path), (60, 60))
    return_sign_image = pygame.transform.scale(pygame.image.load(resources.images.characters.return_sign_path), (40, 40))
    '''
    선택한 이미지 로드하기
    '''
    def get_image(name):
            return pygame.transform.scale(pygame.image.load(resources.images.characters.get_image_path(selected_image)), (300, 300))

    # 이미지마다 가격 설정
    prices = {
        resources.images.characters.king_str : 10000,
        resources.images.characters.angel_str: 6000,
        resources.images.characters.leaf_str: 5000,
        resources.images.characters.santa_str: 8000
    }
    selected_price = None
    buy_button = None
    insufficient_score_message = False
    message_start_time = 0
    run = True
    selected_image = '' # 현재 보고 있는 상품
    while run:
        screen.blit(background_image, (0, 0))

        # buy 버튼 4개 그리기
        button_king = pygame.draw.rect(screen, button_colors[0], (70, 235, 260, 70), border_radius = 35) # x좌표, y좌표, 너비, 높이, R
        button_santa = pygame.draw.rect(screen, button_colors[1], (70, 345, 260, 70), border_radius = 35)
        button_angel = pygame.draw.rect(screen, button_colors[2], (70, 475, 260, 70), border_radius = 35)
        button_leaf = pygame.draw.rect(screen, button_colors[3], (70, 605, 260, 70), border_radius = 35)

        # 기타 버튼 그리기
        restart_button = pygame.draw.rect(screen, (0, 0, 0), (820, 910, 40, 40))

        for event in pygame.event.get(): # 이벤트 순회
            if event.type == pygame.QUIT:
                run = False # 창 끄기
            if event.type == pygame.MOUSEBUTTONDOWN: # 마우스 버튼을 클릭했을 때
                mouse_pos = event.pos # 클릭한 위치를 변수에 지정
                if button_king.collidepoint(mouse_pos): # button_king의 좌표 안에서 마우스 클릭 했다면
                    selected_image = resources.images.characters.king_str # 현재 보고 있는 상품 변경
                    selected_price = prices[resources.images.characters.king_str]
                elif button_angel.collidepoint(mouse_pos):
                    selected_image = resources.images.characters.angel_str
                    selected_price = prices[resources.images.characters.angel_str]
                elif button_leaf.collidepoint(mouse_pos):
                    selected_image = resources.images.characters.leaf_str
                    selected_price = prices[resources.images.characters.leaf_str]
                elif button_santa.collidepoint(mouse_pos):
                    selected_image = resources.images.characters.santa_str
                    selected_price = prices[resources.images.characters.santa_str]
                
                if buy_button and buy_button.collidepoint(mouse_pos): # BUY 버튼을 눌렀을 경우
                    buy_button_music.play() 
                    if save_file.inventory[selected_image]: # 현재 보고 있는 상품이 소지 중인 경우
                        if not save_file.image_file == selected_image: # 현재 착용중인 상품 != 보고 있는 상품
                            save_file.image_file = selected_image
                            save_file.save()
                    else: # 현재 보고 있는 상품이 소지 중이 아닌경우
                        if save_file.score >= selected_price: # 돈 충분
                            save_file.score -= selected_price # 돈 빠져나감
                            save_file.inventory[selected_image] = True # 소지 중으로 변경
                            save_file.save()
                        else: # 돈 없음
                            insufficient_score_message = True # 돈 없다는 메시지
                            message_start_time = time.time()

                elif button_heart_version.collidepoint(mouse_pos):
                    if selected_image == resources.images.characters.king_str: # king 이미지
                        selected_image = resources.images.characters.heart_king_str
                    elif selected_image == resources.images.characters.heart_king_str:
                        selected_image = resources.images.characters.king_str
                    if selected_image == resources.images.characters.angel_str:
                        selected_image = resources.images.characters.heart_angel_str
                    elif selected_image == resources.images.characters.heart_angel_str:
                        selected_image = resources.images.characters.angel_str
                    if selected_image == resources.images.characters.leaf_str:
                        selected_image = resources.images.characters.heart_leaf_str
                    elif selected_image == resources.images.characters.heart_leaf_str:
                        selected_image = resources.images.characters.leaf_str
                    if selected_image == resources.images.characters.santa_str:
                        selected_image = resources.images.characters.heart_santa_str
                    elif selected_image == resources.images.characters.heart_santa_str:
                        selected_image = resources.images.characters.heart_king_str

                elif restart_button.collidepoint(mouse_pos):
                    time.sleep(1)
                    mainmenu.main_menu(easter, easter_now, sound)
                elif exit_button.collidepoint(mouse_pos):
                    run = False

        if not selected_image == '': # 이미지가 할당 되었는지 확인 (비어있지 않다면)
            screen.blit(get_image(selected_image), (500, 300)) # 500, 300에 지정된 이미지 그리기
            buy_button = pygame.draw.rect(screen, button_colors[4], (520, 675, 250, 50), border_radius = 35) # (520, 675)에 250x50 크기의 버튼 생성
            buy_text_str = 'BUY' # 처음엔 사
            if save_file.inventory[selected_image]: # 이미 샀음 (소지 중)
                buy_text_str = 'EQUIP'
                if save_file.image_file == selected_image: # 이미 샀으면서 현재 사용 중
                    buy_text_str = 'EQUIPPED'

            buy_text = button_font.render(buy_text_str, True, (255, 255, 255)) # 텍스트 생성
            # buy_button 중앙에 buy_text 배치
            screen.blit(buy_text, (buy_button.x + (buy_button.width - buy_text.get_width()) // 2, buy_button.y + (buy_button.height - buy_text.get_height()) // 2))
            if selected_price is not None:
                price_text = price_font.render(f'{selected_price}', True, (0, 255, 0))
                screen.blit(price_text, (600, 630))  # 가격 텍스트 위치 조정 필요
        score_text = font.render(f'Score: {save_file.score}', True, (255, 255, 255)) # 텍스트 렌더링
        screen.blit(score_text, (10, 10)) # 렌더링된 텍스트를 화면에 표시

        king_text = font.render('King', True, (0, 0, 0)) # king_text 렌더링
        angel_text = font.render('Angel', True, (0, 0, 0)) # angel_text 렌더링
        leaf_text = font.render('Leaf', True, (0, 0, 0)) # leaf_text 렌더링
        santa_text = font.render('Santa', True, (0, 0, 0)) # Santo_text 렌더링

        button_texts = [king_text, angel_text, leaf_text, santa_text]
        button_positions = [(70, 215), (70, 475), (70, 345), (70, 605)] # 버튼의 위치 지정
        # button_texts, button_position을 결합하여 새로운 튜플 생성 >> text 와 text의 좌표를 생성
        for text, (x, y) in zip(button_texts, button_positions):
            screen.blit(text, (x + 150 - text.get_width() // 2, y + 35 - text.get_height() // 2)) # 텍스트를 버튼의 중앙에 오도록 배치

        button_heart_version = pygame.draw.rect(screen, (255, 255, 255), (550, 250, 30, 30), border_radius = 150)
        exit_button = pygame.draw.rect(screen, (0, 0, 0), (860, 910, 40, 40), border_radius = 150)
        # restart_button = pygame.draw.rect(screen, (255, 255, 255), (820, 910, 40, 40), border_radius = 150)
        
        if insufficient_score_message:
            current_time = time.time()
            if current_time - message_start_time <= 1:  # 1초간 메시지 표시
                insufficient_score_text = font.render("No score", True, (255, 0, 0))
                screen.blit(insufficient_score_text, (WIDTH / 2 - insufficient_score_text.get_width() / 2, HEIGHT / 2))
            else:
                insufficient_score_message = False  # 1초가 지나면 메시지 표시를 중단
        
        # 이미지 화면에 띄우기
        screen.blit(exit_img, exit_button.topleft)
        screen.blit(shop_image, (250, 0))
        screen.blit(angel_sign_image, (50, 440))
        screen.blit(leaf_sign_image, (50, 570))
        screen.blit(santa_sign_image, (50, 320))
        screen.blit(king_sign_image, (50, 200))
        screen.blit(heart_sign_image, (535, 235))
        screen.blit(return_sign_image, (820, 910))


    
        pygame.display.update()

    pygame.quit()