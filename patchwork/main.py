import pygame
from PatchworkController import PatchworkController

def main(args):
	try:
		gamemain(args)
	except KeyboardInterrupt:
		print("Exiting, keyboard interrupt")

def gamemain(args):
	PatchworkController().mainloop()