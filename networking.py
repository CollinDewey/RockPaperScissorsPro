from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from PodSixNet.EndPoint import EndPoint
from enum import Enum


class GameState(Enum):
	WAITING = 0
	READY = 1


class RPSSelection(Enum):
	INVALID = 0
	ROCK = 1
	PAPER = 2
	SCISSORS = 3


class RPSChannel(Channel):
	def __init__(self, *args, **kwargs):
		Channel.__init__(self, *args, **kwargs)

	def Close(self):
		print(self, "Client disconnected")
		self._server.channel = None

	def Network_change_state(self, data):
		print("Got", data)
		self._server.competitior_state = GameState[data["message"].split(".")[1]]

	def Network_change_selection(self, data):
		print("Got", data)
		self._server.competitior_selection = RPSSelection[data["message"].split(".")[1]]

	def Network_query(self, data):
		self.Send(
			{"action": "change_selection", "message": str(self._server.selection)}
		)
		self.Send({"action": "change_state", "message": str(self._server.state)})


class RPSServer(Server):
	channelClass = RPSChannel

	def __init__(self, *args, **kwargs):
		Server.__init__(self, *args, **kwargs)
		self.state = GameState.WAITING
		self.competitior_state = GameState.WAITING
		self.selection = RPSSelection.INVALID
		self.competitior_selection = RPSSelection.INVALID
		self.channel = None
		print("Server launched")

	def Connected(self, channel, addr):
		self.channel = channel
		print(channel, "Channel connected")

	def submit(self):
		if self.channel == None:
			return
		self.channel.Send(
			{"action": "change_selection", "message": str(self.selection)}
		)
		self.channel.Send({"action": "change_state", "message": str(self.state)})


class RPSClient:
	def __init__(self, host, port):
		self.connection = None
		self.Connect((host, port))
		self.state = GameState.WAITING
		self.competitior_state = GameState.WAITING
		self.selection = RPSSelection.INVALID
		self.competitior_selection = RPSSelection.INVALID
		print("RPSClient started")

	def Connect(self, *args, **kwargs):
		self.connection = EndPoint()
		self.connection.DoConnect(*args, **kwargs)
		self.Pump()

	def Pump(self):
		self.connection.Pump()
		for data in self.connection.GetQueue():
			[
				getattr(self, n)(data)
				for n in ("Network_" + data["action"], "Network")
				if hasattr(self, n)
			]

	def Send(self, data):
		self.connection.Send(data)

	def close(self):
		print("RPSClient closed")
		if self.connection != None:
			self.connection.Close()
			self.connection = None

	def Network_connected(self, data):
		print("Connected to the server")

	def Network_error(self, data):
		self.close()

	def Network_disconnected(self, data):
		self.close()

	def Network_change_state(self, data):
		print("Got", data)
		self.competitior_state = GameState[data["message"].split(".")[1]]

	def Network_change_selection(self, data):
		print("Got", data)
		self.competitior_selection = RPSSelection[data["message"].split(".")[1]]

	def submit(self):
		if self.connection == None:
			return
		self.Send({"action": "change_selection", "message": str(self.selection)})
		self.Send({"action": "change_state", "message": str(self.state)})

	def query(self):
		self.Send({"action": "query"})
