import random
import argparse

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
	table = [['Name','Birthdate','DNA','Children','Parents','Height']]
	for human in human_list:
		# vars() is a nifty func that takes an object's attributes and prints them
		table += [vars(human).values()]
	put_table(table)

# outputs current state of sim at the end of a tick
def sim_output(tick, humans):
	output_text(f"\nTick: {tick}")
	print_humans(humans)

class Human():
	def __init__(self, name="", birthdate=0, height=0, dna={'sex' : '', 'temperament': {}, 'height': 0}, children=[], parents=[]):
		self.name = name
		self.birthdate = birthdate
		self.dna = dna
		self.children = children
		self.parents = parents
		self.height = height
	
	def create_child(self, parent2, curr_tick):
		if(self.dna['sex'] != parent2.dna['sex']):
			# genetic stuff
			name = self.name + parent2.name
			split_dna = {'sex': [self.dna['sex'], parent2.dna['sex']], 'temperament': [self.dna['temperament'], parent2.dna['temperament']], 'height': [self.dna['height'], parent2.dna['height']]}
			dna = recombine_dna(split_dna)

			# linked-list housekeeping (want to be able to navigate the tree of humans)
			child = Human(name=name, birthdate=curr_tick, dna=dna, children=[], parents=[self, parent2])
			self.children.append(child)
			parent2.children.append(child)
			return child
		return None  # abort func

	# this function shows you a human
	# stand-in for future dataviz pop-up, or a more complex UI
	def printme(self, tick):
		output_text(f"You are looking at {self.name}")
		output_text(f"Age: {self.get_age(tick)}")
		output_text(f"Height: {self.height}")
		output_text(f"DNA: {self.dna}")
		output_text(f"Children: {[i.name for i in self.children]}")
		output_text(f"Parents: {[i.name for i in self.parents]}")

	# this func dynamically calculates age as-needed so we dont have to manually update per tick
	def get_age(self, curr_tick):
		return curr_tick - self.birthdate

class Simulation():
	# initialize the sim		
	# passing in a year parameter will simulate X years immediately after startup
	def __init__(self, tick=0, num_init_humans=0, humans=[]):
		self.tick = 0  # we will iterate this using the arg tick
		self.humans = humans
		self.num_init_humans = num_init_humans
		self.make_starter_humans(num_init_humans)
		if tick != 0:
			self.simulate(tick)
		pass


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
						baby = a.create_child(e, self.tick)
						self.humans.append(baby)
		return


	# run the simulation for the specified duration of time
	# 1 tick = 1 year
	def simulate(self, ticks = 1):
		if ticks >= 1:
			for i in range(ticks):
				self.grow_humans(self.tick)
				self.tick += 1
				sim_output(self.tick, self.humans)

	# increase everyones age by 1
	def grow_humans(self, curr_tick):
		for human in self.humans:
			age = human.get_age(curr_tick)
			# all humans grow linearly towards their genetic max at 18 y.o.
			if age < 18:	
				age_delta = 18 - human.get_age(curr_tick)
				height_delta = human.dna['height'] - human.height
				human.height += height_delta/age_delta
		pass


if __name__ == "__main__":

	ticks = input('Ticks to run:', type=NUMBER)
	humans = input('Initial Humans:', type=NUMBER)

	sim = Simulation(ticks, humans)

