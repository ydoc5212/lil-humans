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
		return None  # holy shit

	def printme(self):
		print(f"You are looking at {self.name}")
		print(f"Age: {self.age}")
		print(f"DNA: {self.dna}")
		print(f"Children: {[i.name for i in self.children]}")
		print(f"Parents: {[i.name for i in self.parents]}")

def main():
	adam = Human(name="Adam", age=25, dna={'sex':'M', 'temperament':'horny', 'height': 6})
	eve = Human(name="Eve", age=25, dna={'sex':'F', 'temperament':'horny', 'height': 6})
	humans = [adam, eve]
	humans.append(adam.create_child(eve))
	humans[-1].printme()


if __name__ == "__main__":
	main()






# emphasis on modularity (make it easy to revamp systems in the future, accept open-source contributions as new modules that flesh out features)
# emphasis on first-principles (build the sim grounded in real-world data or theories about how the world works. but make simplifying assumptions as necessary)
#  ^ the essence of this project is emergence