import pygame
from helpers2 import get_model, get_action
import gym

FRAMES_PER_SECOND = 23
HEIGHT = 640
WIDTH = 480
WINDOW = (WIDTH, HEIGHT)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw_start_screen(screen):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    text = font.render('Press any key to start', True, WHITE)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, text_rect)

def draw_death_screen(screen):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    text = font.render('Game Over! Press any key to restart', True, WHITE)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, text_rect)

def game_init():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW)
    clock = pygame.time.Clock()
    
    model_path = "models/winnerpac.pth"
    # model_path = "models/psychopac.pth"
    # model_path = "models/suicidepac.pth"
    # model_path = "models/paranoidpac.pth"
    model, env = get_model(model_path)
    obs, info = env.reset()
    
    return screen, clock, model, env, obs

def main():
    screen, clock, model, env, obs = game_init()
    quit = False
    
    draw_start_screen(screen)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            if event.type == pygame.KEYDOWN:
                waiting = False

    while not quit:
        action = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            action = 1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            action = 2
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            action = 3
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            action = 4
        elif keys[pygame.K_SPACE]:
            action = get_action(model, obs)

        action = [action]
        obs, reward, done, _, info = env.step(action)
        frame = env.render()
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.rotate(frame, -90)
        frame = pygame.transform.flip(frame, True, False)
        screen.blit(pygame.transform.scale(frame, WINDOW), (0, 0))
        pygame.display.flip()
        
        if done:
            if info[0]['lives'] == 0:
                draw_death_screen(screen)
                pygame.display.flip()
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        
                        if event.type == pygame.QUIT:
                            quit = True
                        if event.type == pygame.KEYDOWN:
                            waiting = False
            obs, info = env.reset()

        clock.tick(FRAMES_PER_SECOND)
    
    env.close()
    pygame.quit()

if __name__ == "__main__":
    main()