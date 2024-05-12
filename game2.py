import pygame
from helpers2 import get_model, get_action, get_env

FRAMES_PER_SECOND = 23
HEIGHT = 640
WIDTH = 480
WINDOW = (WIDTH, HEIGHT)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PACS_INIT = {
    'paranoidpac': {
        'path': 'models/paranoidpac.pth',
        'price': 100,
        'key': 'J',
        'pykey': pygame.K_j
    },
    'psychopac': {
        'path': 'models/psychopac.pth',
        'price': 200,
        'key': 'K',
        'pykey': pygame.K_k
    },
    'suicidepac': {
        'path': 'models/suicidepac.pth',
        'price': 50,
        'key': 'L',
        'pykey': pygame.K_l
    },
    'winnerpac': {
        'path': 'models/winnerpac.pth',
        'price': 250,
        'key': ';',
        'pykey': pygame.K_SEMICOLON
    }
}

def draw_start_screen(screen):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    text = font.render('Press any key to start', True, WHITE)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, text_rect)
    pygame.display.flip()

def game_init():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW)
    clock = pygame.time.Clock()
    money = 0
    env, cfg = get_env()
    pacs = PACS_INIT.copy()

    for pac_name, pac_attrs in pacs.items():
        pacs[pac_name]['purchased'] = False
        pacs[pac_name]['model'] = get_model(pac_attrs['path'], env, cfg)

    obs, _ = env.reset()
    
    return {
        'screen': screen,
        'clock': clock,
        'env': env,
        'obs': obs,
        'money': money,
        'pacs': pacs
    }

def draw_death_screen(screen, pacs, money):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    text = font.render('Game Over! Press R to restart', True, WHITE)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(text, text_rect)

    money_font = pygame.font.Font(None, 20)
    money_text = money_font.render(f'Money: {money}', True, WHITE)
    money_rect = money_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(money_text, money_rect)

    i = 0
    for pac_name, pac_attrs in pacs.items():
        pac_price = f"Price: {pac_attrs['price']}, Press {pac_attrs['key']} to purchase" if not pac_attrs['purchased'] else 'Purchased'
        pac_text = money_font.render(f'{pac_name} ({pac_price})', True, WHITE)
        pac_rect = pac_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50 + i * 30))
        screen.blit(pac_text, pac_rect)
        i += 1

    keys = pygame.key.get_pressed()
    for pac_name, pac_attrs in pacs.items():
        if keys[pac_attrs['pykey']] and money >= pac_attrs['price'] and pac_attrs['purchased'] == False:
            money -= pac_attrs['price']
            pacs[pac_name]['purchased'] = True
    
    return pacs, money

def main():
    init = game_init()
    screen = init['screen']
    clock = init['clock']
    env = init['env']
    obs = init['obs']
    money = init['money']
    pacs = init['pacs']

    playing = True
    
    # wait at start screen until any key is pressed
    draw_start_screen(screen)
    waiting_to_start = True
    while waiting_to_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                waiting_to_start = False
            if event.type == pygame.KEYDOWN:
                waiting_to_start = False

    # main game loop
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False

        action = 0
        keys = pygame.key.get_pressed()
        models = {pac['pykey']: (pac['model'], pac_name) for pac_name, pac in pacs.items() if pac['purchased']}
        model_keys = models.keys()
        policy = None
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            action = 1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            action = 2
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            action = 3
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            action = 4
        elif any(keys[key] for key in model_keys):
            for key in model_keys:
                if keys[key]:
                    action = get_action(models[key][0], obs)
                    policy = models[key][1]
                    break

        action = [action]
        obs, reward, done, _, info = env.step(action)
        money += int(reward.item())
        frame = env.render()
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.rotate(frame, -90)
        frame = pygame.transform.flip(frame, True, False)
        screen.blit(pygame.transform.scale(frame, WINDOW), (0, 0))
        font = pygame.font.Font(None, 20)
        possible_keys = ["W - up", "A - left", "S - down", "D - right"]
        possible_keys += [f"{pac['key']} - {pac_name}" for pac_name, pac in pacs.items() if pac['purchased']]
        playable_keys_text = font.render(', '.join(possible_keys), True, WHITE)
        text_rect = playable_keys_text.get_rect(center=(WIDTH//2, HEIGHT - 10))
        screen.blit(playable_keys_text, text_rect)
        if policy:
            policy_text = font.render(f'Policy: {policy}', True, WHITE)
            policy_rect = policy_text.get_rect(center=(WIDTH//2, HEIGHT - 30))
            screen.blit(policy_text, policy_rect)
        pygame.display.flip()
        
        if done:
            if info[0]['lives'] == 0:
                death_screen_waiting = True
                while death_screen_waiting:
                    pacs, money = draw_death_screen(screen, pacs, money)
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            playing = True
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                            death_screen_waiting = False
            obs, info = env.reset()

        clock.tick(FRAMES_PER_SECOND)
    
    env.close()
    pygame.quit()

if __name__ == "__main__":
    main()