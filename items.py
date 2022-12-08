global items
items = dict()


class Item:
	def __init__(
		self, name: str, image_path: str, win: str = "beats", lose: str = "loses to"
	):
		self.name = name
		items[self.name] = self
		self.image_path = image_path
		self.win = win
		self.lose = lose
		self.defeat_list = None

	def set_defeats(self, *defeats: object):
		self.defeat_list = list()
		for i in defeats:
			self.defeat_list.append(i.name)

	def defeats(self, item: str):
		"""Checks if the"""
		if item in self.defeat_list:
			return True
		return False


def main():
	rock = Item("Rock", "assets/items/rock.png", "smashes")
	paper = Item("Paper", "assets/items/paper.png")
	scissors = Item("Scissors", "assets/items/scissors.png", "cuts up")
	shield = Item("Shield", "assets/items/shield.png", "protects")
	boom = Item("Boom", "assets/items/boom.png", "destroys")
	pierce = Item("Pierce", "assets/items/pierce.png", "pierces")

	rock.set_defeats(scissors, boom, pierce)
	paper.set_defeats(rock, pierce)
	scissors.set_defeats(paper, pierce)
	shield.set_defeats(boom)
	boom.set_defeats(scissors, pierce, paper)
	pierce.set_defeats(shield)


main()
