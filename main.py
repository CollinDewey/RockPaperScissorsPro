from sys import exit
import os
import b64font

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
	return b64font.init_font()


# Same font for all systems (Because Linux/macOS/Windows ship with different fonts)
def render_text(text: str, color: tuple, font_size: int, font_name: str):
	"""Load the needed font and return the rendered text object"""
	rendered_font = pygame.font.Font(font_name, font_size)
	rendered_text = rendered_font.render(text, True, color)
	return rendered_text


def deinit(font_name: str):
	"""De-initializes the game properly"""
	pygame.quit()
	os.remove(font_name)
	exit()


def game_screen(screen: pygame.Surface, font_name: str, host: bool):
	"""Game screen and logic"""
	if host:
		server = networking.RPSServer(localaddr=("127.0.0.1", int(25565)))
	else:
		client = networking.RPSClient("127.0.0.1", int(25565))

	# TODO: Check if the connection is closed
	first_run = True
	while True:
		pygame.Surface.fill(screen, (255, 255, 255))  # Blank out screen with White
		session = server if host else client
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
		if (
			session.state == networking.GameState.READY
			and session.competitior_state == networking.GameState.READY
		):
			print("BOTH READY")
			print("User:", session.selection)
			print("Opponent:", session.competitior_selection)

			session.close()
			return

		# Graphics Junk
		hover_color = (118, 181, 197)
		idle_color = (171, 219, 227)

		# Bounding Boxes
		rock_rect = pygame.Rect((WINDOW_SIZE[0] - 480) / 2, 456, 480, 80)
		paper_rect = pygame.Rect((WINDOW_SIZE[0] - 480) / 2, 456 + 100, 480, 80)
		scissors_rect = pygame.Rect((WINDOW_SIZE[0] - 480) / 2, 456 + 200, 480, 80)

		# Cursor logic
		mouse_pos = pygame.mouse.get_pos()
		collide_rock = mouse_pos[0] in range(
			rock_rect.left, rock_rect.right
		) and mouse_pos[1] in range(rock_rect.top, rock_rect.bottom)
		collide_paper = mouse_pos[0] in range(
			paper_rect.left, paper_rect.right
		) and mouse_pos[1] in range(paper_rect.top, paper_rect.bottom)
		collide_scissors = mouse_pos[0] in range(
			scissors_rect.left, scissors_rect.right
		) and mouse_pos[1] in range(scissors_rect.top, scissors_rect.bottom)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				deinit(font_name)
			if event.type == pygame.MOUSEBUTTONDOWN:
				if collide_rock:
					session.selection = networking.RPSSelection.ROCK
					session.state = networking.GameState.READY
					session.submit()
				elif collide_paper:
					session.selection = networking.RPSSelection.PAPER
					session.state = networking.GameState.READY
					session.submit()
				elif collide_scissors:
					session.selection = networking.RPSSelection.SCISSORS
					session.state = networking.GameState.READY
					session.submit()

		# Assets
		rock_text = render_text("ROCK", (0, 0, 0), 45, font_name)
		paper_text = render_text("PAPER", (0, 0, 0), 45, font_name)
		scissors_text = render_text("SCISSORS", (0, 0, 0), 45, font_name)

		# Draw/Blit
		pygame.draw.rect(
			screen, hover_color if collide_rock else idle_color, rock_rect, 0, 15
		)  # ROCK
		pygame.draw.rect(
			screen, hover_color if collide_paper else idle_color, paper_rect, 0, 15
		)  # PAPER
		pygame.draw.rect(
			screen,
			hover_color if collide_scissors else idle_color,
			scissors_rect,
			0,
			15,
		)  # SCISSORS
		screen.blit(
			rock_text,
			(
				rock_rect.centerx - rock_text.get_width() / 2,
				rock_rect.centery - rock_text.get_height() / 2,
			),
		)
		screen.blit(
			paper_text,
			(
				paper_rect.centerx - paper_text.get_width() / 2,
				paper_rect.centery - paper_text.get_height() / 2,
			),
		)
		screen.blit(
			scissors_text,
			(
				scissors_rect.centerx - scissors_text.get_width() / 2,
				scissors_rect.centery - scissors_text.get_height() / 2,
			),
		)

		pygame.time.Clock().tick(FRAME_RATE)
		pygame.display.update()


def main_menu(screen: pygame.Surface, font_name: str):
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
		collide_client = mouse_pos[0] in range(
			client_rect.left, client_rect.right
		) and mouse_pos[1] in range(client_rect.top, client_rect.bottom)
		collide_server = mouse_pos[0] in range(
			server_rect.left, server_rect.right
		) and mouse_pos[1] in range(server_rect.top, server_rect.bottom)
		collide_quit = mouse_pos[0] in range(
			quit_rect.left, quit_rect.right
		) and mouse_pos[1] in range(quit_rect.top, quit_rect.bottom)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			if event.type == pygame.MOUSEBUTTONDOWN:
				if collide_client:
					# Bring up menu for IP entry
					game_screen(screen, font_name, False)
					break
				elif collide_server:
					# Bring up menu for waiting (show IP on screen)
					game_screen(screen, font_name, True)
					# Run server code
					break
				elif collide_quit:
					return

		# Assets
		client_text = render_text("Join a Game", (0, 0, 0), 45, font_name)
		server_text = render_text("Host a Game", (0, 0, 0), 45, font_name)
		quit_text = render_text("Exit", (0, 0, 0), 45, font_name)
		menu_logo = pygame.image.load("logo.png")

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
	FRAME_RATE = 30

	# Init
	font_name = init()
	screen = pygame.display.set_mode(WINDOW_SIZE, vsync=1)  # VSYNC isn't guaranteed
	pygame.display.set_caption("Rock Paper Scissors Pro")
	main_menu(screen, font_name)

	# Deinit
	deinit(font_name)
