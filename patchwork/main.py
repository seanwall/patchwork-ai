import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import argparse
from controller.PatchworkControllerPvP import PatchworkControllerPvP
from controller.PatchworkControllerPvAI import PatchworkControllerPvAI
from controller.PatchworkControllerAIvAI import PatchworkControllerAIvAI

def main():
	parser = argparse.ArgumentParser(description='Select play mode and configure learning for patchwork')
	parser.add_argument("-m", "--mode", choices=["pp", "pa", "aa"], help="Select the run mode for Patchwork (PvP: pp, PvAI: pa, AIvAI: aa). If not specified game will be PvAI")
	parser.add_argument("-g", "--graphical", action='store_true', help="Designate if the game should run in gui - only matters for AIvAI, any player mode will always run graphically")

	args = parser.parse_args()
	if args.mode:
		if args.mode == "aa":
			if args.graphical:
				print("AI v AI Graphical Placeholder")
			else:
				PatchworkControllerAIvAI().mainloop()
		elif args.mode == "pp":
			PatchworkControllerPvP().mainloop()
		else:
			PatchworkControllerPvAI().mainloop()
	else:
		PatchworkControllerPvAI().mainloop()

if __name__ == "__main__":
	main()