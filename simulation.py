from enum import Enum
import math
import random
from scipy.stats import norm
from scipy.spatial import cKDTree
import numpy as np
from typing import Optional
import matplotlib.pyplot as plt
# 1 tick is 1 day

# uses statistics to determine whether or not a particular event happens this year
# in: x, mu, sigma
def event_happens_gaussian(x: int, mu: int, sigma: float = 10) -> bool:
    return random.random() <= norm.pdf(x,mu,sigma)

# gompertz function to model death likelihood increasing exponentially with age
def dies_this_year(age, life_expectancy):
    # values to tweak
    a = 0.0005
    b = 0.085
    mortality_rate = a * math.exp(b * age)
    return random.random() <= mortality_rate

class Gender(Enum):
    FEMALE = 0
    MALE = 1
    NONBINARY = 2


class Human:
    def __init__(self, age: int, gender: Gender, is_alive_bool: bool, puberty_bool: bool, parents: Optional[list["Human"]], children: Optional[list["Human"]], spouse: Optional["Human"], job: Optional[str], x:int, y:int, OCEAN:dict):
        self.age = age
        self.gender = gender
        self.is_alive_bool = is_alive_bool
        self.puberty_bool = puberty_bool
        self.parents = parents
        self.children = children
        self.spouse = spouse
        self.job = job
        self.x = x
        self.y = y
        self.OCEAN = OCEAN

    # combine self and partner genetics into a new human
    def give_birth(self, partner) -> "Human":
        return Human(age=0, gender=random.choices(list(Gender), [0.45, 0.45, 0.1], k=1)[0], is_alive_bool=True, puberty_bool=False, parents=[self, partner], children=None, spouse=None, job=None, x=self.x, y=self.y, OCEAN={trait: (self.OCEAN[trait] + partner.OCEAN[trait]) / 2 for trait in self.OCEAN})

    def interact(self, other):
        # print(f'human of age {self.age} is interacting with a human of age {other.age} at {self.x},{self.y}!!')
        pass

# has: list of human objs,
class Simulation():
    def __init__(self, time_elapsed_ticks=0, tick_to_stop=0):
        self.time_elapsed_ticks: int = 0
        self.tick_to_stop: int = tick_to_stop
        self.humans: list[Human] = []
        self.LIFE_EXPECTANCY: int = random.randrange(45, 60)
        self.events:dict[list] = {'births':[],
                                  'deaths':[],
                                  'pubescences':[],
                                  'interactions':[],
                                  'marriages':[]}

        self.sim_messages: list[str] = []

        # create seed humans
        for i in range(random.randrange(15, 40)):
            self.humans.append(Human(age=random.randrange(15, 35), gender=random.choices(list(Gender), [0.45, 0.45, 0.1], k=1)[0], is_alive_bool=True, puberty_bool=True, parents=None, children=None, spouse=None, job=None, x=(np.random.uniform(0, 100)), y=(np.random.uniform(0, 100)), OCEAN={'O':random.uniform(),'C':random.uniform(),'E':random.uniform(),'A':random.uniform(),'N':random.uniform()}))
        self.sim_messages.append(f'You come into awareness of a corner of the world that has {len(self.humans)} humans in it')
    
    def kill(self):
        humans = []
        print("Terminated.")

    def do_tick(self):
        # prepare event counter for this tick
        self.events['births'].append(0)
        self.events['deaths'].append(0)
        self.events['pubescences'].append(0)
        self.events['interactions'].append(0)
        self.events['marriages'].append(0)

        self.birth_children()
        self.age_humans()
        self.determine_puberty()
        self.marry_humans()

        self.simulate_interactions(n_steps=100, dt=0.01, delta=0.5, interaction_radius=1.0)

        # show readout
        self.print_sim_readout()

        # mark tick completed, raise counter
        self.time_elapsed_ticks += 1

    
    def birth_children(self):
        # birth children
        # find married (living) women
        # (would it be cheaperr to have a re-usable 'list of married women')? deal with deaths/remarriages also
        for human in self.humans:
            # if eligible for birthing (married, all partners alive)
            if human.gender == Gender.FEMALE and human.spouse and human.is_alive_bool and human.spouse.is_alive_bool:
                # likelihood of pregnancy in a married couple
                if random.random() > 0.3:
                    self.humans.append(human.give_birth(human.spouse))
                    self.events['births'][self.time_elapsed_ticks] += 1

    def age_humans(self):
        # age out humans
        for human in self.humans:
            # determine whether human dies
            # normal distribution around LIFE_EXPECTANCY
            if dies_this_year(human.age, self.LIFE_EXPECTANCY):
                human.is_alive_bool = False
                self.events['deaths'][self.time_elapsed_ticks] += 1  
            # increase everyone's age by 1
            if human.is_alive_bool:
                human.age += 1

    def determine_puberty(self):
        # determine puberty
        for human in self.humans:
            if not human.puberty_bool:
                if (human.gender == Gender.FEMALE and event_happens_gaussian(human.age, 10, 1.5)) or (human.gender == Gender.MALE and event_happens_gaussian(human.age, 12, 1.5) or (human.gender == Gender.NONBINARY and event_happens_gaussian(human.age, 11, 1.5))):
                    human.puberty_bool = True
                    self.events['pubescences'][self.time_elapsed_ticks] += 1

    def marry_humans(self):
        # pair spouses (O(n)!)
        # TODO more efficient way to hide dead humans from list to prevent iterating. how? do i move to a separate list?
        for human in self.humans:
            # female-first matching; will soon have an alt approach
            if human.gender == Gender.FEMALE and not human.spouse and human.is_alive_bool and human.puberty_bool:
                if random.random() <= 0.3:
                    # pick random living human of appropriate gender
                    tries = 0
                    rand_human = None
                    # matching is currently picking a random human
                    while(not rand_human or rand_human.gender != Gender.MALE or rand_human.spouse is not None or not rand_human.is_alive_bool or not rand_human.puberty_bool):
                        if (tries > 256):
                            rand_human = None
                            break
                        rand_human = random.choice(self.humans)
                        tries += 1
                    # if successful match was found
                    if rand_human:
                        human.spouse = rand_human
                        rand_human.spouse = human
                        self.events['marriages'][self.time_elapsed_ticks] += 1

    def simulate_interactions(self, n_steps: int, dt: float, delta: float, interaction_radius: float):
        n_agents = len(self.humans)
        
        # Create empty arrays for x, y positions for all agents for all steps
        x = np.zeros((n_agents, n_steps))
        y = np.zeros((n_agents, n_steps))
        
        # Initialize first step to initial position
        x[:, 0] = np.array([human.x for human in self.humans])
        y[:, 0] = np.array([human.y for human in self.humans])
        
        for step in range(1, n_steps):
            # Generate random steps for x, y for each agent
            r_x = norm.rvs(size=(n_agents,), scale=delta * math.sqrt(dt))
            r_y = norm.rvs(size=(n_agents,), scale=delta * math.sqrt(dt))
            
            # Add the random step to the previous position for each agent
            x[:, step] = x[:, step-1] + r_x
            y[:, step] = y[:, step-1] + r_y

            # Create KD-tree for the current positions
            tree = cKDTree(np.stack((x[:, step], y[:, step]), axis=-1))
            
            # Find pairs that are within interaction_radius of each other
            pairs = tree.query_pairs(interaction_radius)
            
            for i, j in pairs:
                self.humans[i].interact(self.humans[j])
                self.humans[j].interact(self.humans[i])
                self.events['interactions'][self.time_elapsed_ticks] += 1

    def print_sim_readout(self):
        while self.sim_messages:
            print(self.sim_messages[0])
            self.sim_messages.pop(0)
        print(f'\nTICK {self.time_elapsed_ticks}:')
        print(f'Living Humans: {len([human for human in self.humans if human.is_alive_bool ])}')

        print(f'Interactions: {self.events["interactions"][self.time_elapsed_ticks]}')
        print(f'Births: {self.events["births"][self.time_elapsed_ticks]}')
        print(f'Marriages: {self.events["marriages"][self.time_elapsed_ticks]}')
        print(f'Pubescenses: {self.events["births"][self.time_elapsed_ticks]}')
        print(f'Deaths: {self.events["deaths"][self.time_elapsed_ticks]}')
        # self.show_ages()

    def show_ages(self):
        [print(f'{human.age}') for human in self.humans]

    def plot(self):
        for k,v in self.events.items():
            first_key = list(self.events.keys())[0]
            time_ticks = list(range(len(self.events[first_key])))
            plt.plot(time_ticks, v, label=k, marker='o')
            plt.title(f'{k} Per Year')
            plt.xlabel('Year')
            plt.ylabel(f'Number of {k}')
            plt.legend()
            plt.show()


if __name__ == '__main__':
    sim = Simulation(0, tick_to_stop=1)

    while(True):
        # run sim
        while(sim.time_elapsed_ticks < sim.tick_to_stop):
            sim.do_tick()

        response = input('How many ticks would you like to simulaculate before stopping? Eg. 10:\n')

        # handle possible input
        if response == "plot":
            sim.plot()
        if response == "kill":
            sim.kill()
        elif response.isdigit():
            sim.tick_to_stop = int(response) + sim.time_elapsed_ticks
