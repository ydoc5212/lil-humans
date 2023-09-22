import math
import random
from typing import Optional
# 1 tick is 1 day

# uses statistics to determine whether or not a particular event happens this year
# in: x, mu, sigma
def event_happens(x: int, mu: int, sigma: float = 10) -> bool:
    return random.random() <= (1 / (sigma * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - mu) / sigma)**2)

# has: list of human objs, 
class Simulation():
	def __init__(self, time_elapsed_ticks=0, ticks_left_before_stop=0, humans=[]):
		self.time_elapsed_ticks = 0
		self.ticks_left_before_stop = ticks_left_before_stop
		self.humans = humans
		self.LIFE_EXPECTANCY = random.randrange(45,60)

		self.sim_messages:list[str] = []

		self.births_this_tick = 0
		self.deaths_this_tick = 0
		self.pubescenses_this_tick = 0
		self.marriages_this_tick = 0

		# create seed humans
		for i in range(random.randrange(15,40)):
			self.humans.append(Human(age=0, gender=random.choices([0,1,2],[0.45,0.45,0.1], k=1)[0], is_alive_bool = True, puberty_bool=False, parents=None, children=None, spouse=None, job=None))
		self.sim_messages.append(f'You come into awareness of a corner of the world that has {len(self.humans)} humans in it')

	def do_tick(self):
		self.births_this_tick = 0
		self.deaths_this_tick = 0
		self.pubescenses_this_tick = 0
		self.marriages_this_tick = 0


		# birth children
		# find married (living) women
		# (would it be cheaperr to have a re-usable 'list of married women')? deal with deaths/remarriages also
		for human in self.humans:
			# if eligible for birthing (married, all partners alive)
			if human.gender==0 and human.spouse and human.is_alive_bool and human.spouse.is_alive_bool:
				# likelihood of pregnancy in a married couple
				if random.random() > 0.3:
					self.humans.append(human.give_birth(human.spouse))
					self.births_this_tick += 1

		# age out humans
		for human in self.humans:
			# determine whether human dies
			# normal distribution around LIFE_EXPECTANCY
			if event_happens(human.age, self.LIFE_EXPECTANCY, 5):
				human.is_alive_bool = False
				self.deaths_this_tick += 1

			if human.is_alive_bool:
				human.age += 1

		# determine puberty
		for human in self.humans:
			if not human.puberty_bool:
				if (human.gender == 0 and event_happens(human.age, 10, 1.5)) or (human.gender == 1 and event_happens(human.age, 12, 1.5)):
					human.puberty_bool = True
					self.pubescenses_this_tick += 1

		# pair spouses (O(n)!)
		# TODO more efficient way to hide dead humans from list to prevent iterating. how? do i move to a separate list?
		for human in self.humans:
			# female-first matching; will soon have an alt approach
			if human.gender==0 and not human.spouse and human.is_alive_bool:
				if random.random() <= 0.3:
					# pick random living human of appropriate gender
					tries = 0
					rand_human = None
					# matching is currently picking a random human
					while(not rand_human or rand_human.gender!=1 or rand_human.spouse != None or not rand_human.is_alive_bool):					
						if (tries > 256):
							rand_human = None
							break
						rand_human = random.choice(self.humans)
						tries += 1
					# if successful match was found
					if rand_human:
						human.spouse = rand_human
						rand_human.spouse = human 
						self.marriages_this_tick += 1

		# show readout
		self.print_sim_readout()

		# mark tick completed, raise counter
		self.time_elapsed_ticks += 1
		print('Simulated 1 tick.')

	def print_sim_readout(self):
		while self.sim_messages:
			print(self.sim_messages[0])
			self.sim_messages.pop(0)
		print(f'TICK {self.time_elapsed_ticks}:')
		print(f'Total Humans: {len(self.humans)}')

		print(f'Births: {self.births_this_tick}')
		print(f'Marriages: {self.marriages_this_tick}')
		# print(f'Pubescences: ${self.pubescenses_this_tick}')
		print(f'Deaths: {self.deaths_this_tick}')



class Human:
	def __init__(self, age:int, gender:int, is_alive_bool:bool, puberty_bool:bool, parents:Optional[list["Human"]], children:Optional[list["Human"]], spouse:Optional["Human"], job:Optional[str]):
		self.age = age
		self.gender = gender 
		self.is_alive_bool = is_alive_bool
		self.puberty_bool = puberty_bool
		self.parents= parents
		self.children = children
		self.spouse = spouse
		self.job = job

	# combine self and partner genetics into a new human
	def give_birth(self, partner) -> "Human":
		return Human(age=0, gender=random.choices([0,1,2],[0.45,0.45,0.1], k=1)[0], is_alive_bool = True, puberty_bool=False, parents=[self, partner], children=None, spouse=None, job=None)



if __name__ == '__main__':
	ticks_left_before_stop = int(input('Welcome to your world simulation! How many ticks would you like to simulaculate before stopping? Eg. 10:\n'))
	sim = Simulation(0, ticks_left_before_stop)

	while(True):
		while(sim.time_elapsed_ticks < sim.ticks_left_before_stop ):
			sim.do_tick()
		sim.ticks_left_before_stop = int(input('How many ticks would you like to simulaculate before stopping? Eg. 10:\n')) + sim.time_elapsed_ticks
