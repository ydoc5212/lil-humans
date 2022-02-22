import random

def pick_random_list(list):
	return list[random.randrange(len(list))]

# current dna works by choosing randomly between the *phenotypes* of your parents
# eventually dna will store genotypes
def recombine_dna(dna):
	combined_dna = {}
	for key, value in dna.items():
		combined_dna[key] = pick_random_list(value)
	return combined_dna

class Human():
	def __init__(self, name="", age=0, dna={'sex' : '', 'temperament': {}, 'height': 0}, children=[], parents=[]):
		self.name = name
		self.age = age
		self.dna = dna
		self.children = children
		self.parents = parents
	
	def create_child(self, parent2):
		if(self.dna['sex'] != parent2.dna['sex']):
			# genetic stuff
			name = self.name + parent2.name
			split_dna = {'sex': [self.dna['sex'], parent2.dna['sex']], 'temperament': [self.dna['temperament'], parent2.dna['temperament']], 'height': [self.dna['height'], parent2.dna['height']]}
			dna = recombine_dna(split_dna)

			# linked-list housekeeping (want to be able to navigate the tree of humans)
			child = Human(name=name, age=0, dna=dna, children=[], parents=[self, parent2])
			self.children.append(child)
			parent2.children.append(child)
			return child
		return None  # abort func

	# this function shows you a human
	# stand-in for future dataviz pop-up, or a more complex UI
	def printme(self):
		print(f"You are looking at {self.name}")
		print(f"Age: {self.age}")
		print(f"DNA: {self.dna}")
		print(f"Children: {[i.name for i in self.children]}")
		print(f"Parents: {[i.name for i in self.parents]}")

class Simulation():
	# initialize the sim		
	# passing in a year parameter will simulate X years immediately after startup
	def __init__(self, year=0, humans=[]):
		self.year = year
		self.humans = humans
		self.make_adam_and_eve()
		if year != 0:
			simulate(years)
		pass

	# this debug(?) function creates custom starting parameters for the sim for easy testing
	def make_adam_and_eve(self):
		adam = Human(name="Adam", age=25, dna={'sex':'M', 'temperament':'', 'height': 6})
		eve = Human(name="Eve", age=25, dna={'sex':'F', 'temperament':'', 'height': 6})
		baby = adam.create_child(eve)
		baby.printme()
		self.humans.extend([adam, eve, baby])


	# run the simulation for the specified duration of time
	# 1 tick = 1 year
	def simulate(years = 1):
		if years >= 1:
			for i in range(years):
				grow_humans()
				self.year += 1

	# increase everyones age by 1
	def grow_humans(self):
		for human in self.humans:
			human.age += 1



if __name__ == "__main__":
	sim = Simulation()


