import pygame
from src.background import Background


class Infoscreen:
	def __init__(self, create_titlescreen):
		self.display_surface = pygame.display.get_surface()
		self.create_titlescreen = create_titlescreen
		self.background_sprite = pygame.sprite.GroupSingle()
		self.selected_sound = pygame.mixer.Sound('audio/selected.wav')
		self.selected_sound.set_volume(0.6)
		self.delay = pygame.time.get_ticks()
		self.cooldown = 400
		self.screen_img = pygame.image.load('graphics/Titlescreen/infoscreen.png').convert_alpha()

		self.load()

	def load(self):
		Background(self.background_sprite)

	def input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_BACKSPACE]:
			self.selected_sound.play()
			self.create_titlescreen((299, 304))

	def timer(self):
		current = pygame.time.get_ticks()
		if current - self.delay >= self.cooldown:
			self.input()

	def run(self, dt):
		self.timer()
		self.background_sprite.update(dt)
		self.background_sprite.draw(self.display_surface)
		self.display_surface.blit(self.screen_img, (160, 118))