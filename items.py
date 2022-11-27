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
	rock = Item("Rock", "", "smashes")
	paper = Item("Paper", "")
	scissors = Item("Scissors", "", "cuts up")

	rock.set_defeats(scissors)
	paper.set_defeats(rock)
	scissors.set_defeats(paper)


main()
