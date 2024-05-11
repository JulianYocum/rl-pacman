# import gymnasium as gym
import pygame
# from stable_baselines3 import PPO
# from stable_baselines3.common.env_util import make_atari_env, make_vec_env
# from stable_baselines3.common.vec_env import VecFrameStack
# from stable_baselines3.common.atari_wrappers import AtariWrapper
from helpers2 import get_model, get_action

FRAMES_PER_SECOND = 23
WINDOW = (480, 640)

def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW)
    clock = pygame.time.Clock()

    # model_path = "train_dir/best_expsticky2222.pth"
    # model_path = "train_dir/paranoidpac.pth"
    # model_path = "train_dir/survivorpac1.pth"
    # model_path = "train_dir/suicidepac.pth"
    # model_path = "train_dir/psychopac5.pth"
    model_path = "train_dir/survivorpac3.pth"
    # model_path = "train_dir/exp2/checkpoint_p0/best_000382288_97865728_reward_130.380.pth"
    model, env = get_model(model_path)
    obs, info = env.reset()
    quit = False
    
    while not quit:
        action = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True

        # Check for key presses independently of the event loop
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            action = 1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            action = 2
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            action = 3
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            action = 4
        # space bar
        elif keys[pygame.K_SPACE]:
            # action = model.predict(obs)[0][0]
            action = get_action(model, obs)

        # Step the environment with the last action set by keyboard input
        # action = [action]
        action = [action]
        obs, reward, done, _, info = env.step(action)
        # print('obs:', obs.shape)
        # obs *= 3
        # switch the axes to match the screen orientation
        # frame = env.get_images()[0]
        frame = env.render()
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.rotate(frame, -90)
        frame = pygame.transform.flip(frame, True, False)
        screen.blit(pygame.transform.scale(frame, WINDOW), (0, 0))
        pygame.display.flip()
        
        if done:
            obs, info = env.reset()

        # Maintain the game loop running at 16 FPS
        clock.tick(FRAMES_PER_SECOND)
    
    env.close()
    pygame.quit()

if __name__ == "__main__":
    main()




# import gymnasium as gym
# import pygame
# from stable_baselines3 import PPO
# from stable_baselines3.common.env_util import make_atari_env, make_vec_env
# from stable_baselines3.common.vec_env import VecFrameStack
# from stable_baselines3.common.atari_wrappers import AtariWrapper

# FRAMES_PER_SECOND = 16
# WINDOW = (480, 640)

# def main():
#     pygame.init()
#     screen = pygame.display.set_mode(WINDOW)
#     clock = pygame.time.Clock()
    
#     # model = PPO.load("vanilla-model")
#     env = gym.make('MsPacman-v4')
#     # env = make_vec_env("MsPacman-v4", n_envs=1, seed=0, monitor_dir=None, wrapper_class=AtariWrapper)
#     # env = VecFrameStack(env, n_stack=4)
#     obs = env.reset()
#     quit = False
    
#     while not quit:
#         action = 0
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 quit = True

#         # Check for key presses independently of the event loop
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_UP] or keys[pygame.K_w]:
#             action = 1
#         elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
#             action = 2
#         elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
#             action = 3
#         elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
#             action = 4

#         # Step the environment with the last action set by keyboard input
#         # action = [action]
#         obs, reward, done, _, info = env.step(action)
#         # obs *= 3
#         # switch the axes to match the screen orientation
#         # obs = env.get_images()[0]
#         frame = pygame.surfarray.make_surface(obs)
#         frame = pygame.transform.rotate(frame, -90)
#         frame = pygame.transform.flip(frame, True, False)
#         screen.blit(pygame.transform.scale(frame, WINDOW), (0, 0))
#         pygame.display.flip()
        
#         if done:
#             obs = env.reset()

#         # Maintain the game loop running at 16 FPS
#         clock.tick(FRAMES_PER_SECOND)
    
#     env.close()
#     pygame.quit()

# if __name__ == "__main__":
#     main()


