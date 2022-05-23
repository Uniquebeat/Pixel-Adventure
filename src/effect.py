import pygame
from src.debug import debug
from src.support import import_folder


class Collect_effect(pygame.sprite.Sprite):
	def __init__(self, pos, group):
		super().__init__(group)
		self.image = pygame.image.load('graphics/fruits/Collected/0.png').convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)

		# Animations
		self.import_assets()
		self.frame_index = 0
		self.animation_speed = 0.14

	def import_assets(self):
		full_path = 'graphics/fruits/Collected'
		self.frame = import_folder(full_path)

	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frame):
			self.kill()
		else:
			self.image = self.frame[int(self.frame_index)]

	def update(self):
		self.animate()

class Player_effect(pygame.sprite.Sprite):
	def __init__(self, pos, type, group, create_player):
		super().__init__(group)
		self.image = pygame.image.load('graphics/player/Enter_effect/0.png').convert_alpha()
		self.rect = self.image.get_rect(center=pos)
		self.type = type
		self.create_player = create_player

		# Animations
		self.frame_index = 0
		self.animation_speed = 0.14
		if self.type == 'Enter':
			self.frames = import_folder('graphics/player/Enter_effect')
		elif self.type == 'Dead':
			self.frames = import_folder('graphics/player/Dead_effect')

	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames) and self.type == 'Enter':
			self.create_player()
			self.kill()
		elif self.frame_index >= len(self.frames) and self.type == 'Dead':
			self.kill()
		else:
			self.image = self.frames[int(self.frame_index)]

	def update(self):
		self.animate()


class Arrow_effect(pygame.sprite.Sprite):
	def __init__(self, pos, groups):
		super().__init__(groups)
		self.image = pygame.image.load('graphics/Traps/Arrow/Hit/0.png').convert_alpha()
		self.rect = self.image.get_rect(topleft=(pos[0]-2, pos[1]-2))
		# animation
		self.frames = import_folder('graphics/Traps/Arrow/Hit')
		self.animation_speed = 0.14
		self.frame_index = 0

	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.kill()
		else:
			self.image = self.frames[int(self.frame_index)]

	def update(self):
		self.animate()
