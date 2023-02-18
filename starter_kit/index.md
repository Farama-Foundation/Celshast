---
hide-toc: true
firstpage:
lastpage:
---

# <PROJECT>

```{figure} _static/REPLACE_ME.gif
   :alt: REPLACE ME
   :width: 500
```

**Basic example:**

```{code-block} python

import gymnasium as gym
env = gym.make("LunarLander-v2", render_mode="human")
observation, info = env.reset(seed=42)
for _ in range(1000):
   action = env.action_space.sample()  # this is where you would insert your policy
   observation, reward, terminated, truncated, info = env.step(action)

   if terminated or truncated:
      observation, info = env.reset()
env.close()
```

```{toctree}
:hidden:
:caption: Introduction

content/basic_usage
```

```{toctree}
:hidden:
:caption: Development

Github <https://github.com/Farama-Foundation/Gymnasium>
release_notes/index
Contribute to the Docs <https://github.com/Farama-Foundation/Gymnasium/blob/main/docs/README.md>
```
