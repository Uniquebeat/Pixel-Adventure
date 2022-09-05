import pygame, json
from src.background import Background


class CharacterNode(pygame.sprite.Sprite):
	def __init__(self, pos, surface, index, groups):
		super().__init__(groups)
		self.image = surface.convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)
		self.index = {'index':index}

class Selected(pygame.sprite.Sprite):
	def __init__(self, index, groups):
		super().__init__(groups)
		self.image = pygame.image.load('graphics/Skinscreen/selected.png').convert_alpha()
		self.index = index
		if self.index == 0:
			self.rect = self.image.get_rect(topleft=(96, 148))
		elif self.index == 1:
			self.rect = self.image.get_rect(topleft=(224, 148))
		elif self.index == 2:
			self.rect = self.image.get_rect(topleft=(352, 148))
		elif self.index == 3:
			self.rect = self.image.get_rect(topleft=(480, 148))

class Select(pygame.sprite.Sprite):
	def __init__(self, index, groups, surface):
		super().__init__(groups)
		self.image = surface.convert_alpha()
		self.pressed = False
		self.index = index
		if self.index == 0:
			self.rect = self.image.get_rect(topleft=(96, 148))
		elif self.index == 1:
			self.rect = self.image.get_rect(topleft=(224, 148))
		elif self.index == 2:
			self.rect = self.image.get_rect(topleft=(352, 148))
		elif self.index == 3:
			self.rect = self.image.get_rect(topleft=(480, 148))

		# movement
		self.direction = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.select_sound = pygame.mixer.Sound('audio/select.wav')
		self.select_sound.set_volume(0.6)

	def get_input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
			if not self.pressed:
				self.select_sound.play()
				self.pressed = True
				self.rect.x += 128
		elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
			if not self.pressed:
				self.select_sound.play()
				self.pressed = True
				self.rect.x -= 128
		elif self.pressed:
			self.pressed = False

	def reset(self):
		if self.rect.x > 480:
			self.rect.x = 96
		elif self.rect.x < 96:
			self.rect.x = 480
			
	def update(self):
		self.get_input()
		self.reset()

class Skinscreen:
	def __init__(self, index, create_titlescreen):
		self.display_surface = pygame.display.get_surface()
		self.index = index
		self.create_titlescreen = create_titlescreen
		self.background_sprite = pygame.sprite.GroupSingle()
		self.node_sprites = pygame.sprite.Group()
		self.select_sprite = pygame.sprite.GroupSingle()
		self.selected_sprite = pygame.sprite.GroupSingle()

		self.setup()
		self.selected_sound = pygame.mixer.Sound('audio/selected.wav')
		self.selected_sound.set_volume(0.6)
		self.pressed = False

	def setup(self):
		Background([self.background_sprite])
		CharacterNode((96, 148), pygame.image.load('graphics/Skinscreen/MaskDude.png'), 0, self.node_sprites)
		CharacterNode((224, 148), pygame.image.load('graphics/Skinscreen/NinjaFrog.png'), 1, self.node_sprites)
		CharacterNode((352, 148), pygame.image.load('graphics/Skinscreen/PinkMan.png'), 2, self.node_sprites)
		CharacterNode((480, 148), pygame.image.load('graphics/Skinscreen/VirtualGuy.png'), 3, self.node_sprites)
		Select(self.index, self.select_sprite, pygame.image.load('graphics/Skinscreen/select.png'))
		Selected(self.index, self.selected_sprite)

	def input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_BACKSPACE]:
			self.selected_sound.play()
			self.create_titlescreen((299, 112))
		elif keys[pygame.K_SPACE]:
			if not self.pressed:
				self.selected_sound.play()
				self.pressed = True
		elif self.pressed:
			self.pressed = False

		select = self.select_sprite.sprite
		selected = self.selected_sprite.sprite
		for node in self.node_sprites.sprites():
			if keys[pygame.K_SPACE] and select.rect.colliderect(node.rect):
				with open('graphics/player/character_index.txt', 'w') as data:
					json.dump(node.index, data)
				selected.rect.topleft = select.rect.topleft

	def run(self, dt):
		self.input()
		self.background_sprite.update(dt)
		self.background_sprite.draw(self.display_surface)
		self.node_sprites.draw(self.display_surface)
		self.select_sprite.update()
		self.select_sprite.draw(self.display_surface)
		if self.selected_sprite:
			self.selected_sprite.draw(self.display_surface)
