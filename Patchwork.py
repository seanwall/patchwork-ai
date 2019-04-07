import pygame
import argparse
from patchwork.controller.PatchworkControllerPvP import PatchworkControllerPvP
from patchwork.controller.PatchworkControllerPvAI import PatchworkControllerPvAI
from patchwork.controller.PatchworkControllerAIvAI import PatchworkControllerAIvAI

def main():
	parser = argparse.ArgumentParser(description='Select play mode and configure learning for patchwork')
	parser.add_argument("-m", "--mode", choices=["pp", "pa", "aa"], help="Select the run mode for Patchwork (PvP: pp, PvAI: pa, AIvAI: aa). If not specified game will be PvAI")
	parser.add_argument("-g", "--graphical", action='store_true', help="Designate if the game should run in gui - only matters for AIvAI, any player mode will always run graphically")
	parser.add_argument("-s", "--sample", type=int,  help="Runs ai v ai the given number of times, and calculates the win \% for p1 and p2")

	args = parser.parse_args()
	if args.mode:
		if args.mode == "aa":
			if args.graphical:
				print("AI v AI Graphical Placeholder")
			else:
				if args.sample:
					PatchworkControllerAIvAI().mainloop_learning(args.sample)
				else:
					PatchworkControllerAIvAI().mainloop(1)
		elif args.mode == "pp":
			PatchworkControllerPvP().mainloop()
		else:
			PatchworkControllerPvAI().mainloop()
	else:
		PatchworkControllerPvAI().mainloop()

if __name__ == "__main__":
	main()