from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from PodSixNet.EndPoint import EndPoint

logging = True

class RPSChannel(Channel):
	def __init__(self, *args, **kwargs):
		Channel.__init__(self, *args, **kwargs)

	def Close(self):
		if logging:
			print(self, "Client disconnected")
		self._server.channel = None

	def Network_change_state(self, data):
		if logging:
			print("Got", data)
		self._server.competitor_state = data["message"]

	def Network_change_selection(self, data):
		if logging:
			print("Got", data)
		self._server.competitor_selection = data["message"]

	def Network_query(self, data):
		self.Send(
			{"action": "change_selection", "message": str(self._server.selection)}
		)
		self.Send({"action": "change_state", "message": str(self._server.state)})


class RPSServer(Server):
	channelClass = RPSChannel

	def __init__(self, *args, **kwargs):
		Server.__init__(self, *args, **kwargs)
		self.state = ""
		self.competitor_state = ""
		self.selection = ""
		self.competitor_selection = ""
		self.channel = None
		if logging:
			print("Server launched")

	def Connected(self, channel, addr):
		self.channel = channel
		if logging:
			print(channel, "Channel connected")

	def handle_accept(self):
		"""Taken from PodSixNet, because THEY PUT A PRINT STATEMENT IN HERE????"""
		try:
			conn, addr = self.accept()
		except Exception as e:
			return
		self.channels.append(self.channelClass(conn, addr, self, self._map))
		self.channels[-1].Send({"action": "connected"})
		if hasattr(self, "Connected"):
			self.Connected(self.channels[-1], addr)

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
		self.state = ""
		self.competitor_state = ""
		self.selection = ""
		self.competitor_selection = ""
		if logging:
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
		if logging:
			print("RPSClient closed")
		if self.connection != None:
			self.connection.Close()
			self.connection = None

	def Network_connected(self, data):
		if logging:
			print("Connected to the server")

	def Network_error(self, data):
		self.close()

	def Network_disconnected(self, data):
		self.close()

	def Network_change_state(self, data):
		if logging:
			print("Got", data)
		self.competitor_state = data["message"]

	def Network_change_selection(self, data):
		if logging:
			print("Got", data)
		self.competitor_selection = data["message"]

	def submit(self):
		if self.connection == None:
			return
		self.Send({"action": "change_selection", "message": str(self.selection)})
		self.Send({"action": "change_state", "message": str(self.state)})

	def query(self):
		self.Send({"action": "query"})
