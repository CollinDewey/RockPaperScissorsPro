import sys
import os
import b64font

try:
	import pygame

	# import pygase
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
			result = (
				7  # Same as MessageBoxW no on Win32, but it could really be anything
			)

	if result == 6:  # User agreed to installation
		print("Please wait a moment while modules are being installed")
		# https://pip.pypa.io/en/latest/user_guide/#using-pip-from-your-program
		subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
		# subprocess.check_call([sys.executable, "-m", "pip", "install", "pygase"])
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
		ctypes.windll.kernel32.SetConsoleMode(
			ctypes.windll.kernel32.GetStdHandle(-11), 7
		)
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
	while True:
		# Cursor logic
		mouse_pos = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
		pygame.Surface.fill(screen, (255, 255, 255))  # Blank out screen with White

		# Assets
		text_start = render_text("Title", (0, 0, 0), 35, font_name)
		menu_logo = pygame.image.load("logo.png")

		# Blit
		screen.blit(text_start, (0, 0))
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
	deinit()
