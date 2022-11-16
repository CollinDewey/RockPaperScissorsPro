from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from PodSixNet.Connection import connection, ConnectionListener
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

	def Network_change_state(self, data):
		print("Got", data)
		self._server.competitior_state = GameState[data["message"].split(".")[1]]

	def Network_change_selection(self, data):
		print("Got", data)
		self._server.competitior_selection = RPSSelection[data["message"].split(".")[1]]


class RPSServer(Server):
	channelClass = RPSChannel

	def __init__(self, *args, **kwargs):
		Server.__init__(self, *args, **kwargs)
		self.state = GameState.WAITING
		self.competitior_state = GameState.WAITING
		self.selection = RPSSelection.INVALID
		self.competitior_selection = RPSSelection.INVALID
		self.schannel = None
		print("Server launched")

	def Connected(self, channel, addr):
		self.schannel = channel
		print(channel, "Channel connected")

	def submit(self):
		self.schannel.Send(
			{"action": "change_selection", "message": str(self.selection)}
		)
		self.schannel.Send({"action": "change_state", "message": str(self.state)})


class RPSClient(ConnectionListener):
	def __init__(self, host, port):
		self.Connect((host, port))
		self.state = GameState.WAITING
		self.competitior_state = GameState.WAITING
		self.selection = RPSSelection.INVALID
		self.competitior_selection = RPSSelection.INVALID
		print("RPSClient started")

	def Network_connected(self, data):
		print("Connected to the server")

	def Network_error(self, data):
		print("error:", data["error"][1])
		connection.Close()

	def Network_disconnected(self, data):
		connection.Close()

	def Network_change_state(self, data):
		print("Got", data)
		self.competitior_state = GameState[data["message"].split(".")[1]]

	def Network_change_selection(self, data):
		print("Got", data)
		self.competitior_selection = RPSSelection[data["message"].split(".")[1]]

	def submit(self):
		self.Send({"action": "change_selection", "message": str(self.selection)})
		self.Send({"action": "change_state", "message": str(self.state)})
