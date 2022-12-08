from sys import exit
from items import items
import os

try:
	os.environ[
		"PYGAME_HIDE_SUPPORT_PROMPT"
	] = "hide"  # Hide "Hello from pygame community" text
	import pygame
	import networking  # Local file
except ImportError:
	import subprocess
	import sys

	# Check if the user has the required dependencies, if not, ask to install them
	if os.name == "nt":  # Windows
		import ctypes

		message_box = ctypes.windll.user32.MessageBoxW
		result = message_box(
			None,
			"Missing required modules, do you want to install these?\nThis will take a minute",
			"Missing Pygame/Numpy",
			4,
		)
	else:  # Assume POSIX
		print("Install missing numpy/pygame libraries? [(Y)es/No]")
		if input().lower() in {"yes", "ye", "y", ""}:
			result = 6  # Same as MessageBoxW yes on Win32
		else:
			result = 7  # Same as MessageBoxW no on Win32

	if result == 6:  # User agreed to installation
		print("Please wait a moment while modules are being installed")
		# https://pip.pypa.io/en/latest/user_guide/#using-pip-from-your-program
		subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
		subprocess.check_call([sys.executable, "-m", "pip", "install", "PodSixNet"])
		print("Done")
		print("-------------")
		subprocess.check_call([sys.executable, sys.argv[0]])
	sys.exit()


def init():
	"""Initialize pygame, apply some tweaks, and return the file path to a font"""
	# Windows tweaks for ANSI escape codes and DPI scaling
	if os.name == "nt":
		ctypes = __import__("ctypes")
		ctypes.windll.shcore.SetProcessDpiAwareness(1)
		# ctypes.windll.kernel32.SetConsoleMode(
		# 	ctypes.windll.kernel32.GetStdHandle(-11), 7
		# )
		del ctypes

	# Init
	pygame.init()
	return


# Use same font for all systems (Because Linux/macOS/Windows ship with different fonts)
def render_text(text: str, color: tuple, font_size: int, font_name: str):
	"""Load the needed font and return the rendered text object"""
	rendered_font = pygame.font.Font(font_name, font_size)
	rendered_text = rendered_font.render(text, True, color)
	return rendered_text


def deinit():
	"""De-initializes the game properly"""
	pygame.quit()
	exit()


def draw_message(message, background_color, foreground_color, duration):
	"""Uses pygame's rect and label functionality to create a rectangle with the desired message for the user"""
	initial_time = pygame.time.get_ticks()

	while pygame.time.get_ticks() < initial_time + duration:
		message_text = render_text(message, foreground_color, 55, FONT_NAME)
		background_rect = pygame.Rect(
			(WINDOW_SIZE[0] / 2 - message_text.get_width() / 2 - 50),
			550,
			message_text.get_width() + 100,
			200,
		)

		pygame.draw.rect(screen, background_color, background_rect, 0, 15)
		screen.blit(
			message_text, (WINDOW_SIZE[0] / 2 - (message_text.get_rect()[2] / 2), 620)
		)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				deinit()

		pygame.time.Clock().tick(FRAME_RATE)
		pygame.display.update()


def ip_selection_screen(screen: pygame.Surface):
	"""Uses pygame to ask the user for an IP address and returns the IP. Returns string with IP"""

	# Stub until I can get to it tomorrow, just so it sorta works right now
	return "127.0.0.1"

	#import socket
	#host = socket.gethostname()
	#local_IP = socket.gethostbyname(host)
	#print("Your IP: ", local_IP)
	#user_text = input("Please enter your opponents IP address: ")

	addressbox = pygame.Rect((1024/3,768/2), (1024/3,30))
	#locating and sizing box
	#choosing font for box
	font = pygame.font.SysFont(FONT_NAME, 25)
	ipaddress = ''
	active = False
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				deinit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if addressbox.collidepoint(event.pos):
					active = True
				else:
					active = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_BACKSPACE:
					ipaddress = ipaddress[:-1]
				else:
					ipaddress += event.unicode
			screen.fill('white')
		if active:
			color = pygame.Color('black')
		else:
			color = pygame.Color('gray')

		pygame.draw.rect(screen,color, addressbox,1)
		surface = font.render(ipaddress, True, 'black')
		screen.blit(surface, (addressbox.x +5, addressbox.y +10))
		pygame.time.Clock().tick(FRAME_RATE)
		pygame.display.update()


def battle(screen: pygame.Surface, selection: str, competitor_selection: str):
	"""Uses pygame to display a quick battle animation"""

	# Load assets
	# background_image = pygame.image.load("assets/battle.png")
	# explosion_image = pygame.image.load("assets/explosion.png")
	# explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
	selection_image = pygame.image.load(items[selection].image_path)
	competitor_selection_image = pygame.image.load(
		items[competitor_selection].image_path
	)

	# Animation Loop - Range is duration in seconds * 60
	for i in range(256):
		pygame.Surface.fill(screen, (255, 255, 255))  # Blank out screen with White

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				deinit()

		screen.blit(
			selection_image,
			(
				i * 2 - selection_image.get_width() / 2,
				(WINDOW_SIZE[1] - selection_image.get_height()) / 2,
			),
		)
		screen.blit(
			competitor_selection_image,
			(
				WINDOW_SIZE[0] - competitor_selection_image.get_width() / 2 - i * 2,
				(WINDOW_SIZE[1] - competitor_selection_image.get_height()) / 2,
			),
		)

		pygame.time.Clock().tick(FRAME_RATE)
		pygame.display.update()

	# Draw the explosion image and play the sound

	# pygame.mixer.Sound.play(explosion_sound)
	pygame.Surface.fill(screen, (255, 255, 255))  # Blank out screen with White
	# screen.blit(explosion_image, ((WINDOW_SIZE[0] - explosion_image.get_width()) / 2, (WINDOW_SIZE[1] - explosion_image.get_height()) / 2))

	for i in range(30):  # Wait half a second
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				deinit()

		pygame.time.Clock().tick(FRAME_RATE)
		pygame.display.update()

	# Draw victorious item and display message

	# Win
	if items[selection].defeats(competitor_selection) and not items[
		competitor_selection
	].defeats(selection):
		print("I won")
		screen.blit(
			selection_image,
			(
				(WINDOW_SIZE[0] - selection_image.get_width()) / 2,
				(WINDOW_SIZE[1] - selection_image.get_height()) / 2,
			),
		)
		draw_message(
			selection + " " + items[selection].win + " " + competitor_selection,
			(80, 80, 80),
			(0, 0, 0),
			5000,
		)
	# Lose
	elif not items[selection].defeats(competitor_selection) and items[
		competitor_selection
	].defeats(selection):
		print("I lost")
		screen.blit(
			competitor_selection_image,
			(
				(WINDOW_SIZE[0] - competitor_selection_image.get_width()) / 2,
				(WINDOW_SIZE[1] - competitor_selection_image.get_height()) / 2,
			),
		)
		draw_message(
			selection + " " + items[selection].lose + " " + competitor_selection,
			(80, 80, 80),
			(0, 0, 0),
			5000,
		)
	# Tie
	else:
		print("I tied")
		screen.blit(
			selection_image,
			(
				(WINDOW_SIZE[0] - selection_image.get_width()) / 2
				- selection_image.get_width(),
				(WINDOW_SIZE[1] - selection_image.get_height()) / 2,
			),
		)
		screen.blit(
			competitor_selection_image,
			(
				(WINDOW_SIZE[0] - competitor_selection_image.get_width()) / 2
				+ competitor_selection_image.get_width(),
				(WINDOW_SIZE[1] - competitor_selection_image.get_height()) / 2,
			),
		)
		draw_message(
			selection + " ties " + competitor_selection,
			(80, 80, 80),
			(0, 0, 0),
			5000,
		)


def game_screen(screen: pygame.Surface, host: bool):
	"""Game screen and logic"""
	if host:
		# This is hacky
		socket_lib = __import__('socket')
		socket = socket_lib.socket(socket_lib.AF_INET, socket_lib.SOCK_DGRAM)
		socket.connect(("8.8.8.8", 80)) # Google
		ip = socket.getsockname()[0]
		del socket, socket_lib

		server = networking.RPSServer(localaddr=("127.0.0.1", int(25568)))
	else:
		ip = ip_selection_screen(screen)
		client = networking.RPSClient(ip, int(25568))

	# TODO: Check if the connection is closed
	first_run = True
	session = server if host else client
	while True:
		pygame.Surface.fill(screen, (255, 255, 255))  # Blank out screen with White
		try:
			session.Pump()
		except:
			# Connection failed, go back to the main menu
			session.close()
			return

		#
		# This next section is very temporary
		# Rock, Paper, and Scissors ( + additional ones ) will be classes
		#

		# Query for the host state since the RPS could have already been selected
		if not host and first_run:
			first_run = False
			client.query()

		# Both users have selected their RPS
		if session.state == "ready" and session.competitor_state == "ready":
			print("BOTH READY")
			print("User:", session.selection)
			print("Opponent:", session.competitor_selection)
			session.close()

			battle(screen, session.selection, session.competitor_selection)

			return

		# Graphics Junk
		hover_color = (118, 181, 197)
		idle_color = (171, 219, 227)

		mouse_pos = pygame.mouse.get_pos()
		button_collide = dict()
		for i,j in enumerate(items):

			# Bounding Boxes & Assets
			button_rect = pygame.Rect((WINDOW_SIZE[0] - 480) / 2, 100 + 100*i, 480, 80)
			button_text = render_text(items[j].name.upper(), (0, 0, 0), 45, FONT_NAME)

			# Cursor logic
			button_collide[j] = button_rect.collidepoint(mouse_pos)

			# Draw/Blit
			pygame.draw.rect(
				screen, hover_color if button_collide[j] else idle_color, button_rect, 0, 15
			)
			screen.blit(
				button_text,
				(
					button_rect.centerx - button_text.get_width() / 2,
					button_rect.centery - button_text.get_height() / 2,
				),
			)

		ip_text = render_text(f"Host: {ip}", (0,0,0), 35, FONT_NAME);
		screen.blit(ip_text, ((WINDOW_SIZE[0] - ip_text.get_width()) / 2, 0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				deinit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				for i in items:
					if button_collide[i]:
						session.selection = items[i].name
						session.state = "ready"
						session.submit()

		pygame.time.Clock().tick(FRAME_RATE)
		pygame.display.update()


def main_menu(screen: pygame.Surface):
	"""Displays a menu for selecting gamemode"""
	hover_color = (118, 181, 197)
	idle_color = (171, 219, 227)

	while True:
		pygame.Surface.fill(screen, (255, 255, 255))  # Blank out screen with White

		# Bounding Boxes
		client_rect = pygame.Rect((WINDOW_SIZE[0] - 480) / 2, 456, 480, 80)
		server_rect = pygame.Rect((WINDOW_SIZE[0] - 480) / 2, 456 + 100, 480, 80)
		quit_rect = pygame.Rect((WINDOW_SIZE[0] - 480) / 2, 456 + 200, 480, 80)

		# Cursor logic
		mouse_pos = pygame.mouse.get_pos()
		collide_client = client_rect.collidepoint(mouse_pos)
		collide_server = server_rect.collidepoint(mouse_pos)
		collide_quit = quit_rect.collidepoint(mouse_pos)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			if event.type == pygame.MOUSEBUTTONDOWN:
				if collide_client:
					game_screen(screen, False)
					break
				elif collide_server:
					game_screen(screen, True)
					break
				elif collide_quit:
					return

		# Assets
		client_text = render_text("Join a Game", (0, 0, 0), 45, FONT_NAME)
		server_text = render_text("Host a Game", (0, 0, 0), 45, FONT_NAME)
		quit_text = render_text("Exit", (0, 0, 0), 45, FONT_NAME)
		menu_logo = pygame.image.load("assets/logo.png")

		# Draw/Blit
		pygame.draw.rect(
			screen, hover_color if collide_client else idle_color, client_rect, 0, 15
		)  # Client
		pygame.draw.rect(
			screen, hover_color if collide_server else idle_color, server_rect, 0, 15
		)  # Server
		pygame.draw.rect(
			screen, hover_color if collide_quit else idle_color, quit_rect, 0, 15
		)  # Quit
		screen.blit(
			client_text,
			(
				client_rect.centerx - client_text.get_width() / 2,
				client_rect.centery - client_text.get_height() / 2,
			),
		)
		screen.blit(
			server_text,
			(
				server_rect.centerx - server_text.get_width() / 2,
				server_rect.centery - server_text.get_height() / 2,
			),
		)
		screen.blit(
			quit_text,
			(
				quit_rect.centerx - quit_text.get_width() / 2,
				quit_rect.centery - quit_text.get_height() / 2,
			),
		)
		screen.blit(
			pygame.transform.smoothscale(menu_logo, (640, 360)),
			((WINDOW_SIZE[0] - 640) / 2, 64),
		)
		pygame.time.Clock().tick(FRAME_RATE)
		pygame.display.update()


if __name__ == "__main__":
	"""Main :)"""
	# Window Size
	global WINDOW_SIZE  # Lazy
	global FRAME_RATE
	WINDOW_SIZE = (1024, 768)
	FRAME_RATE = 60
	FONT_NAME = "assets/FreeSans.ttf"

	# Init
	init()
	screen = pygame.display.set_mode(WINDOW_SIZE, vsync=1)  # VSYNC isn't guaranteed
	pygame.display.set_caption("Rock Paper Scissors Pro")
	main_menu(screen)

	# Deinit
	deinit()
