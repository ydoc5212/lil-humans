import random

from pywebio.input import *
from pywebio.output import *

def rand_from_list(list):
	return list[random.randrange(len(list))]

def rand_bool():
	return bool(random.getrandbits(1))

# current dna works by choosing randomly between the *phenotypes* of your parents
# eventually dna will store genotypes
def recombine_dna(dna):
	combined_dna = {}
	for key, value in dna.items():
		combined_dna[key] = rand_from_list(value)
	return combined_dna

# this function handles the front-end
def output_text(text):
	print(text)
	put_text(text)

def print_humans(human_list):
	table = []
	for num, human in enumerate(human_list):
		# add header row
		if num == 0:
			table += [vars(human).keys()]
		# vars() is a nifty func that takes an object's attributes and prints them
		table += [vars(human).values()]
	put_table(table)

# outputs current state of sim at the end of a tick
def sim_output(tick, humans):
	output_text(f"\nTick: {tick}")
	print_humans(humans)

class Human():
	def __init__(self, name="", birthdate=0, height=0, food_need = 2, dna={'sex' : '', 'temperament': {}, 'height': 0}, parents=[]):
		self.name = name
		self.birthdate = birthdate
		self.dna = dna
		self.height = height
		self.food_need = food_need
		self.parents = parents

		self.inventory = dict()
		self.children = list()
	
	def create_child(self, parent2, curr_tick):
		if(self.dna['sex'] != parent2.dna['sex']):
			# genetic stuff
			name = self.name + parent2.name
			split_dna = {'sex': [self.dna['sex'], parent2.dna['sex']], 'temperament': [self.dna['temperament'], parent2.dna['temperament']], 'height': [self.dna['height'], parent2.dna['height']]}
			dna = recombine_dna(split_dna)

			# linked-list housekeeping (want to be able to navigate the tree of humans)
			child = Human(name=name, birthdate=curr_tick, dna=dna, parents=[self, parent2])
			self.children.append(child)
			parent2.children.append(child)
			return child
		return None  # abort func

	# this function shows you a human
	# stand-in for future dataviz pop-up, or a more complex UI
	def printme(self, tick):
		print_humans([self])

	# this func dynamically calculates age as-needed so we dont have to manually update per tick
	def get_age(self, curr_tick):
		return curr_tick - self.birthdate

class Planet():
	day_night_time = (14, 10)  # for now, 1 day = 1 tick
	time_per_lemon = 2


class Simulation():
	# initialize the sim		
	# passing in a year parameter will simulate X years immediately after startup
	def __init__(self, ticks_to_run=0, num_init_humans=0, humans=[]):
		self.humans = humans
		self.num_init_humans = num_init_humans
		self.curr_tick = 0

		planet = Planet()
		self.make_starter_humans(num_init_humans)
		while ticks_to_run != 0:
			self.simulate(ticks_to_run)
			ticks = input('Ticks to run:', type=NUMBER)


	def make_starter_humans(self, num_humans):
		# create the specified # of humans, w random attributes
		for i in range(int(num_humans)):
			is_male = rand_bool() 
			name, sex = ("Adam", "M") if is_male else ("Eve", "F")
			new_human = Human(name=name, height=6, birthdate=-25, dna={'sex':sex, 'temperament':'', 'height': 6})
			self.humans.append(new_human)

		# make a bunch of babies as a debug
		for a in self.humans:
			if a.name == 'Adam':
				for e in self.humans:
					if e.name == 'Eve':	
						baby = a.create_child(e, self.curr_tick)
						self.humans.append(baby)
		return


	# this function does the dirty work of the sim
	# 1 tick = 1 year
	def simulate(self, ticks = 1):
		if ticks >= 1:
			for i in range(ticks):
				# update states
				self.age_humans()
				# simulate decisions
				self.forage()
				# check on states
				self.check_nutrition()
				# wrap up the tick and output relevant data
				self.curr_tick += 1
				sim_output(self.curr_tick, self.humans)

	# increase everyones age and height
	def age_humans(self):
		for human in self.humans:
			age = human.get_age(self.curr_tick)
			# all humans grow linearly towards their genetic max at 18 y.o.
			if age < 18:	
				age_delta = 18 - human.get_age(self.curr_tick)
				height_delta = human.dna['height'] - human.height
				human.height += height_delta/age_delta

	# arguments: a human, an object string, and a negative/positive quantity to change
	# manipulates teh human's inventory, and returns False if human had insufficient items when quantity negative
	# if using a large quantity, consider calling the function in a loop if returning as False is unwanted behavior
	def edit_inventory(self, human, object, quantity=1):
		obj_check = human.inventory.get(object)  # should be None if not present, or the quantity of the object in inventory
		if quantity < 1:
			if obj_check is None or not obj_check - quantity >= 0:
				# insufficient items for check
				sufficient_quantity = False
			else:
				human.inventory[object] += quantity  # quantity is negative
				sufficient_quantity = True
		elif quantity > 1:
			sufficient_quantity = True
			# use .get to initialize inventory quantity of object to 0 then add quantity
			human.inventory[object] = human.inventory.get(object,0) + quantity
		# remove item from inventory if none of it is left!
		# this may be inefficient, but makes for a clearer display
		if human.inventory.get(object) == 0:
			del human.inventory[object]
		return sufficient_quantity

	# every human forages 2 lemons per day
	# TODO only adults? + who forages lemons? can familial systems out-source lemon gathering to one parent?
	def forage(self):
		for human in self.humans:
			self.edit_inventory(human, 'lemon', 3)
		pass

	# TODO manage dead humans (put in separate list? then how will i handle parent/child checking?)
	def kill_human(self, human, reason="unknown causes"):
		output_text(f"{human.name} died of {reason}... but we gave them a second chance!")
		pass

	def check_nutrition(self):
		for human in self.humans:
			for i in range(human.food_need):
				if self.edit_inventory(human, 'lemon', -1):
					output_text(f"{human.name} ate a lemon.")
				else:
					# if youre even one lemon too short, youre not gonna make it...
					self.kill_human(human, reason="starvation")
		pass


if __name__ == "__main__":
	ticks = input('Ticks to run:', type=NUMBER)
	humans = input('Initial Humans:', type=NUMBER)

	sim = Simulation(ticks, humans)

