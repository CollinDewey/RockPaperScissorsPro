import sys
import os
import b64font

try:
	import pygame
	import PodSixNet  # We don't actually need this imported yet, this is more just to see if the module exists (TODO: Do this correctly)
	from pygame import gfxdraw  # Unsure as to why this needs to be a separate call
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
	os.environ[
		"PYGAME_HIDE_SUPPORT_PROMPT"
	] = "hide"  # Hide "Hello from pygame community" text
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
	sys.exit()


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
					# Run client code
					break
				elif collide_server:
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
			screen, hover_color if collide_client else idle_color, client_rect, 0, 10
		)  # Client
		pygame.draw.rect(
			screen, hover_color if collide_server else idle_color, server_rect, 0, 10
		)  # Server
		pygame.draw.rect(
			screen, hover_color if collide_quit else idle_color, quit_rect, 0, 10
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
			(WINDOW_SIZE[0] / 2 - 320, 64),
		)
		pygame.display.update()


if __name__ == "__main__":
	"""Main :)"""
	# Window Size
	global WINDOW_SIZE  # Lazy
	WINDOW_SIZE = (1024, 768)

	# Init
	font_name = init()
	screen = pygame.display.set_mode(WINDOW_SIZE, vsync=1)  # VSYNC isn't guaranteed
	pygame.display.set_caption("Rock Paper Scissors Pro")
	main_menu(screen, font_name)

	# Deinit
	deinit(font_name)
