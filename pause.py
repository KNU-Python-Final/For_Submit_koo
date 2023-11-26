def pause():
    import pygame
    pygame.init()
    WIDTH = 900
    HEIGHT = 950  # 창 가로세로 상수로 정해두고 시작 ->이거 해상도마다 다르게 보일 수 있음
    fps = 60
    timer = pygame.time.Clock()  # 속도 제어 위해서
    screen = pygame.display.set_mode([WIDTH, HEIGHT])  # 창 가로세로 정하기

    for event in pygame.event.get():  # 모든 이벤트들 리스트로 해서 event에 하나씩 for문으로 넣어줌
        if event.type == pygame.QUIT:
            pygame.quit()
    while True:
        screen.fill('black')  # 스크린 색
        font = pygame.font.Font("assets/pacman_main_menu_images/emulogic.ttf", 30)
        pause_img = pygame.transform.scale(pygame.image.load(f'assets/pause/pause.png'),
                                             (500, 180))
        screen.blit(pause_img, (WIDTH // 2 - 500//2, 300))
        press_enter_to_continue_text = font.render(f'press [SPACE] to continue', True,
                                                   'white')  # antialias : True -> 선 부드럽게..
        screen.blit(press_enter_to_continue_text, (100, 550))

        timer.tick(fps)
        pygame.display.flip()  # 화면 전체 업데이트
pause()