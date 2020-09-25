from gym_minigrid.minigrid import *
from gym_minigrid.register import register
import random

class SimpleGrid(MiniGridEnv):
    """
    Simple 5x5, 7x7 grid environment, no obstacles
    """
    
    def __init__(
        self,
        size=8,
        agent_start_pos=(1,1),
        agent_start_dir=0,
    ):
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir 

        super().__init__(
            grid_size=size,
            max_steps=4*size*size,
            # Set this to True for maximum speed
            see_through_walls=True
        )
    
    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place a goal square in the bottom-right corner
        #self.put_obj(Goal(), width - 2, height - 2)
        for obj in range(0, random.randint(0, 5)):
            self.place_obj(Key())
        
        for obj in range(0, random.randint(0, 5)):
            self.place_obj(Box(color='green'))

        # Place the agent
        if self.agent_start_pos is not None:
            self.agent_pos = self.agent_start_pos
            self.agent_dir = self.agent_start_dir
        else:
            self.place_agent()

        #TODO CHANGE
        self.mission = 'you must fetch a box'

    def step(self, action):
        obs, reward, done, info = MiniGridEnv.step(self, action)

        if self.carrying:
            if self.carrying.color == self.targetColor and \
               self.carrying.type == self.targetType:
                reward = self._reward()
                done = True
            else:
                reward = 0
                done = True

        return obs, reward, done, info
        
class SimpleGrid5x5(SimpleGrid):
    def __init__(self, **kwargs):
        super().__init__(size=7, **kwargs)

class SimpleRandomGrid5x5(SimpleGrid):
    def __init__(self):
        super().__init__(size=7, agent_start_pos=None)

class SimpleGrid7x7(SimpleGrid):
    def __init__(self, **kwargs):
        super().__init__(size=9, **kwargs)

class SimpleRandomGrid7x7(SimpleGrid):
    def __init__(self):
        super().__init__(size=9, agent_start_pos=None)

register(
    id='MiniGrid-SimpleGrid-5x5-v0',
    entry_point='gym_minigrid.envs:SimpleGrid5x5'
)

register(
    id='MiniGrid-SimpleGrid-Random-5x5-v0',
    entry_point='gym_minigrid.envs:SimpleRandomGrid5x5'
)

register(
    id='MiniGrid-SimpleGrid-7x7-v0',
    entry_point='gym_minigrid.envs:SimpleGrid7x7'
)

register(
    id='MiniGrid-SimpleGrid-Random-7x7-v0',
    entry_point='gym_minigrid.envs:SimpleRandomGrid7x7'
)