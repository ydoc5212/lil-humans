from enum import Enum
import math
import random
from scipy.stats import norm
from scipy.spatial import cKDTree
import numpy as np
from typing import Optional
import matplotlib.pyplot as plt
# 1 tick is 1 year

MALE_PUBERTY_MEAN = 12
FEMALE_PUBERTY_MEAN = 10
OTHER_PUBERTY_MEAN = (MALE_PUBERTY_MEAN+FEMALE_PUBERTY_MEAN)/2


class Gender(Enum):
    FEMALE = 0
    MALE = 1
    OTHER = 2
sub_pronouns={Gender.MALE: 'He', Gender.FEMALE: 'She', Gender.OTHER: 'They'}
obj_pronouns={Gender.MALE: 'Him', Gender.FEMALE: 'Her', Gender.OTHER: 'Them'}


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


class Job(Enum):
    FARMER = 0
    INVENTOR = 1
    ARTIST = 2
    LEADER = 3
    LEARNER = 4
    WARRIOR = 5
    MERCHANT = 6


class Human:
    def __init__(self, id: int, age: int, birth_tick: int, gender: Gender, is_alive_bool: bool, puberty_bool: bool, parents: Optional[list["Human"]], children: Optional[list["Human"]], spouse: Optional["Human"], job: Optional[str], x:int, y:int, personality:dict, relationships:dict):
        self.id = id
        self.age = age
        self.birth_tick = birth_tick
        self.gender = gender
        self.is_alive_bool = is_alive_bool
        self.puberty_bool = puberty_bool
        self.parents = parents
        self.children = children
        self.spouse = spouse
        self.job = job
        self.x = x
        self.y = y
        self.personality = personality
        self.relationships = relationships

    # combine self and partner genetics into a new human
    # args: partner (Human), current time in ticks, the id of the new human in the list
    def give_birth(self, partner, time_ticks, id) -> "Human":
        gender = random.choices(list(Gender), [0.45, 0.45, 0.1], k=1)[0]
        personality = {trait: (self.personality[trait] + partner.personality[trait]) / 2 for trait in self.personality}
        return Human(id=id, age=0, birth_tick=time_ticks, gender=gender, is_alive_bool=True, puberty_bool=False, parents=[self, partner], children=None, spouse=None, job=None, x=self.x, y=self.y, personality=personality, relationships={self:50, partner:50})

    def interact(self, other):
        # print(f'human of age {self.age} is interacting with a human of age {other.age} at {self.x},{self.y}!!')
        # consequences: big or small change in their relationship
        # should utilize a compbination of the OCEAN traits dict each human has, as well as their current relationship status

        # if human extroverted enough to interact
        if random.random() < self.personality['E']:
            # current dummy interaction is solely based off perpetuating previous interactions
            if other in self.relationships:
                if self.relationships[other] < 0:
                    self.relationships[other] = max(self.relationships[other] - 10, -100)
                    other.relationships[self] = max(other.relationships.get(self,0) - 10, -100)

                elif self.relationships[other] > 0:
                    self.relationships[other] = min(self.relationships[other] + 10, 100)
                    other.relationships[self] = min(other.relationships.get(self,0) + 10, 100)
            else:
                self.relationships[other] = random.randrange(-5,int(10*self.personality['A']))  
                other.relationships[self] = other.relationships.get(self, 0) + random.randint(-10,10)  

        # print(f"After interaction, human {self.id} feels {self.relationships.get(other,0)} about human {other.id}.")

    def print_relationship(self, other):
        relationship = self.relationships.get(other,0)
        self_pronoun = sub_pronouns[self.gender]
        self_obj_pronoun = obj_pronouns[self.gender]
        other_pronoun = obj_pronouns[other.gender]

        if other is self.spouse:
            print(f'{other.id} is {self.id}\'s spouse.')
            if relationship > 99:
                relation_text = random.choice(['absolutely loves to the end of the earth ', f'has found {self_pronoun} second half in '])
            elif relationship > 75:
                relation_text = random.choice(['truly loves ', 'simply adores ', 'thinks is very special '])
            elif relationship > 50:
                relation_text = random.choice(['loves ', 'really enjoys ', 'is falling in love with '])
            elif relationship > 25:
                relation_text = random.choice(['is happily married to '])
            elif relationship >= 0:
                relation_text = random.choice(['likes ', 'is still getting to know ', 'cares about '])
            elif relationship >= -25:
                relation_text = random.choice(['isn\'t quite having a good time with ', 'is peeved with '])
            elif relationship >= -50:
                relation_text = random.choice(['is quite unhappy in {self_pronoun} marriage with ', 'loathes '])
            elif relationship >= -75:
                relation_text = random.choice(['despises ', 'hates '])
            elif relationship > -99:
                relation_text = random.choice(['absolutely despises ', 'is disgusted by ', 'is enemies with'])
            elif relationship <= -100:
                relation_text = random.choice(['is interested in spousicide as a means to resolving their tension with ',f'feels the cold breeze from the echoes of the retribution of abandoned morality calling out to {self_obj_pronoun} to take action against '])
        else:
            if relationship > 99:
                relation_text = random.choice(['is inseparable from '])
            elif relationship > 75:
                relation_text = random.choice(['is best friends with ', 'loves hanging out with '])
            elif relationship > 50:
                relation_text = random.choice(['thinks is great ', 'is good friends with '])
            elif relationship > 25:
                relation_text = random.choice(['is friends with ', 'thinks is cool '])
            elif relationship >= 0:
                relation_text = random.choice(['feels ambivalent towards ', 'mildly appreciates '])
            elif relationship >= -25:
                relation_text = random.choice(['doesn\'t care for ', 'is peeved with ', 'has a slight dislike towards '])
            elif relationship >= -50:
                relation_text = random.choice(['is quite unhappy with ', 'loathes '])
            elif relationship >= -75:
                relation_text = random.choice(['despises ', 'hates '])
            elif relationship > -99:
                relation_text = random.choice(['absolutely despises ', 'is disgusted by '])
            elif relationship <= -100:
                relation_text = random.choice(['is interested in murdering ', 'deeply hates with every fiber of their being ', 'is truly disgusted with on a moral level '])
        print(f"{self_pronoun} {relation_text} {other_pronoun}.")

    def print(self):
        print(f'HUMAN #{self.id}:')
        is_was = 'Is' if self.is_alive_bool else 'Was'
        has_had = 'Has' if self.is_alive_bool else 'Had'
        does_did = 'Does' if self.is_alive_bool else 'Did'
        print(f'Was born in the year {self.birth_tick}, of the Human Era')
        print(f'Is {self.age} years old.' if self.is_alive_bool else f'Died at {self.age} years of age, in the year {self.birth_tick+self.age}.')
        print(f'{is_was} {self.gender}.')
        if not self.puberty_bool:
            print('Has not gone through puberty.' if self.is_alive_bool else 'Did not go through puberty.')
        else:
            print(f'{has_had} the following children: {[child.id for child in self.children]}' if self.children else f'{has_had} no children of record.')
            if self.spouse:
                print(f'{has_had} a spouse: {self.spouse.id}.' )
                self.print_relationship(self.spouse)
            else:
                print(f"{does_did} not have a spouse.")
        print(f'{has_had} the following parents: {[parent.id for parent in self.parents]}' if self.parents else f'{has_had} no parents of record.')
        print((f'{is_was} a {self.job}') if self.job else f'{has_had} no designated occupation.')
        print(f'{has_had} the following OCEAN traits: {", ".join(map(str, self.personality.values()))}')
        print(' ')
        print(' ')

# has: list of human objs,
class Simulation():
    def __init__(self, time_ticks=0, tick_to_stop=0):
        self.time_ticks: int = 0
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
            age = random.randrange(15, 35)
            gender = random.choices(list(Gender), [0.45, 0.45, 0.1], k=1)[0]
            personality = {'O':random.uniform(0,1),'C':random.uniform(0,1),'E':random.uniform(0,1),'A':random.uniform(0,1),'N':random.uniform(0,1)}
            self.humans.append(Human(i, age, birth_tick=0-age, gender=gender, is_alive_bool=True, puberty_bool=True, parents=None, children=None, spouse=None, job=None, x=(np.random.uniform(0, 100)), y=(np.random.uniform(0, 100)), personality=personality, relationships={}))
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

        self.determine_births()
        self.determine_ages()
        self.determine_puberty()
        self.determine_marriages()
        self.determine_jobs()

        self.simulate_interactions(n_steps=100, dt=0.01, delta=0.5, interaction_radius=1.0)

        # show readout
        self.print_sim_readout()

        # mark tick completed, raise counter
        self.time_ticks += 1

    
    def determine_births(self):
        # birth children
        # find married (living) women
        # (would it be cheaperr to have a re-usable 'list of married women')? deal with deaths/remarriages also
        for human in self.humans:
            # if eligible for birthing (married, all partners alive)
            if human.gender == Gender.FEMALE and human.spouse and human.is_alive_bool and human.spouse.is_alive_bool:
                # likelihood of pregnancy in a married couple
                if random.random() > 0.3:
                    self.humans.append(human.give_birth(human.spouse, self.time_ticks, len(self.humans)))
                    self.events['births'][self.time_ticks] += 1

    def determine_ages(self):
        # age out humans
        for human in self.humans:
            # determine whether human dies
            # normal distribution around LIFE_EXPECTANCY
            if dies_this_year(human.age, self.LIFE_EXPECTANCY):
                human.is_alive_bool = False
                self.events['deaths'][self.time_ticks] += 1  
            # increase everyone's age by 1
            # this is non-lossy because we store the birth tick
            if human.is_alive_bool:
                human.age += 1

    def determine_puberty(self):
        # determine puberty
        for human in self.humans:
            if not human.puberty_bool:
                if (human.gender == Gender.FEMALE and event_happens_gaussian(human.age, FEMALE_PUBERTY_MEAN, 1.5)) or (human.gender == Gender.MALE and event_happens_gaussian(human.age, MALE_PUBERTY_MEAN, 1.5) or (human.gender == Gender.OTHER and event_happens_gaussian(human.age, OTHER_PUBERTY_MEAN, 1.5))):
                    human.puberty_bool = True
                    self.events['pubescences'][self.time_ticks] += 1

    def determine_marriages(self):
        # pair spouses (O(n))
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
                        self.events['marriages'][self.time_ticks] += 1

    def determine_jobs(self):
        for human in self.humans:
            # could segment by age (eg 16) but am choosing to segment by puberty
            if human.job or not human.puberty_bool:
                break
            
            # TODO OCEAN traits should affect job probabilities

            # high O makes much more likely to become inventor/artist
            # hihg o = moderately more likely to be learner
            # extraversion -> much more likely ot be politician
            # high C -> warrior, leader
            # low O -> love of routine. farmer likely

            assignment = random.choices(
                [Job.FARMER, Job.INVENTOR, Job.ARTIST, Job.LEARNER, Job.LEADER, Job.WARRIOR, Job.MERCHANT],
                [0.5,0.1,0.1,0.1,0.1,0.1,0.1]
            )[0]
            
            human.job = assignment

# TODO dead humans shouldnt move around
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
                if self.humans[i].is_alive_bool and self.humans[j].is_alive_bool:
                    self.humans[i].interact(self.humans[j])
                    self.humans[j].interact(self.humans[i])
                    self.events['interactions'][self.time_ticks] += 1

    def print_sim_readout(self):
        while self.sim_messages:
            print(self.sim_messages[0])
            self.sim_messages.pop(0)
        print(f'\YEAR {self.time_ticks} of the HUMAN ERA:')
        print(f'Living Humans: {len([human for human in self.humans if human.is_alive_bool ])}')

        print(f'Interactions: {self.events["interactions"][self.time_ticks]}')
        print(f'Births: {self.events["births"][self.time_ticks]}')
        print(f'Marriages: {self.events["marriages"][self.time_ticks]}')
        print(f'Pubescenses: {self.events["births"][self.time_ticks]}')
        print(f'Deaths: {self.events["deaths"][self.time_ticks]}')
        # self.show_ages()
        print(f"\n")

    # prints all available info about the specified human
    # args: takes a start and stop range of humans to print out
    def print_humans(self, start, end):
        for id in range(start,end):
            if 0 <= id < len(self.humans):  # checking if in bounds
                self.humans[id].print()

        # TODO can take any parameter, eg ages, and shows it for specified range of humans. use enum
        # for i, human in enumerate(self.humans[start:end]):
        #     print(f"Human {i + start}: {human.age}")



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
    sim = Simulation(time_ticks=0, tick_to_stop=1)

    while(1<2):
        # run sim
        while(sim.time_ticks < sim.tick_to_stop):
            sim.do_tick()

        response = input('How many ticks would you like to simulaculate before stopping? Eg. 10:\n')

        # handle possible input
        if response == "plot":
            sim.plot()
        elif response == "kill":
            sim.kill()
        elif response.startswith("print_humans"):
            args = response.split()
            start = int(args[1]) if len(args) > 1 else 0
            end = int(args[2]) if len(args) > 2 else len(sim.humans)
            sim.print_humans(start, end)
        elif response.isdigit():
            sim.tick_to_stop = int(response) + sim.time_ticks
