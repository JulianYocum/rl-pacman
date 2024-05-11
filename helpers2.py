import time
from collections import deque
from typing import Dict, Tuple

import gymnasium as gym
import numpy as np
import torch
from torch import Tensor

from sample_factory.algo.learning.learner import Learner
from sample_factory.algo.utils.make_env import make_env_func_batched
from sample_factory.algo.utils.rl_utils import prepare_and_normalize_obs
from sample_factory.algo.utils.tensor_utils import unsqueeze_tensor
from sample_factory.cfg.arguments import load_from_checkpoint
from sample_factory.model.actor_critic import create_actor_critic
from sample_factory.utils.attr_dict import AttrDict

from sf_examples.atari.train_atari import parse_atari_args, register_atari_components

device = "cpu"

def get_model(model_path):

    experiment_name = "."
    train_dir = "./models"
    argv = ["--algo=APPO", "--env=atari_mspacman", f"--experiment={experiment_name}", "--no_render", "--max_num_episodes=10", "--save_video", f"--train_dir={train_dir}"]

    register_atari_components()
    cfg = parse_atari_args(argv=argv, evaluation=True)
    cfg = load_from_checkpoint(cfg)

    eval_env_frameskip: int = cfg.env_frameskip if cfg.eval_env_frameskip is None else cfg.eval_env_frameskip
    assert (
        cfg.env_frameskip % eval_env_frameskip == 0
    ), f"{cfg.env_frameskip=} must be divisible by {eval_env_frameskip=}"
    render_action_repeat: int = cfg.env_frameskip // eval_env_frameskip
    cfg.env_frameskip = cfg.eval_env_frameskip = eval_env_frameskip
    print(f"Using frameskip {cfg.env_frameskip} and {render_action_repeat=} for evaluation")

    env = make_env_func_batched(
        cfg, env_config=AttrDict(worker_index=0, vector_index=0, env_id=0), render_mode="rgb_array"
    )

    actor_critic = create_actor_critic(cfg, env.observation_space, env.action_space)
    actor_critic.eval()
    actor_critic.model_to_device(device)

    checkpoint_dict = torch.load(model_path, map_location=device)
    actor_critic.load_state_dict(checkpoint_dict["model"])

    return actor_critic, env

def get_action(actor_critic, obs):

    with torch.no_grad():
        normalized_obs = prepare_and_normalize_obs(actor_critic, obs)
        actions = actor_critic(normalized_obs, 0)["actions"]
        return actions.item()