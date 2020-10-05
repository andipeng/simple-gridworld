from gym_minigrid.minigrid import *
from gym_minigrid.register import register

class SimpleGrid(MiniGridEnv):
    """
    Simple 5x5, 7x7 grid environment, no obstacles
    """
    
    def __init__(
        self,
        size=8,
        agent_start_pos=(1,1),
        agent_start_dir=0,
        # Number of keys generated in env
        numObjs = 0,
        
    ):
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir
        self.numObjs = numObjs

        super().__init__(
            grid_size=size,
            max_steps=500,
            # Set this to True for maximum speed
            see_through_walls=True
        )
    
    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)
        
        # Generated random keys, up to maximum number to fill grid
        self.numObjs = self._rand_int(1, (width*height)/4)
        objs = []
        objPos = []
        
        # Until we have generated all the keys and placed randomly
        while len(objs) < self.numObjs:
            objColor = 'green'
            pos = self.place_obj(Key(objColor))
            objs.append(('key', objColor))
            objPos.append(pos)

        # Randomize the agent start position and orientation
        self.place_agent()
        self.reward_range = (0, len(objs))

        #TODO CHANGE
        self.mission = 'you must fetch the green keys'

    def step(self, action):
        obs, reward, done, info = MiniGridEnv.step(self, action)

        # loops until done collecting all objects
        if len(self.collected) == self.numObjs:
            done = True

        return obs, reward, done, info
    
    def _reward(self):
        return len(self.collected)
        
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
