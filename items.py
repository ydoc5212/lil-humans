class Good():
	def __init__(self):
		pass
	pass

class Food(Good):
	def __init__(self):
		Good.__init__(self)
	pass

class Lemon(Food)