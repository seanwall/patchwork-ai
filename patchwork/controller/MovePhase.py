import enum

class MovePhase(enum.Enum):
	BUYPHASE = 1
	PLACEPHASE = 2
	GAMEOVER = 3
	SPECIAL_PLACEPHASE = 4