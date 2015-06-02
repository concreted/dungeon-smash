import sys, pygame, random, math
from pygame.locals import *

pygame.init()

tile_size = 36		# Should be multiple of two

visible_rows = 8

size = width, height = tile_size*5, tile_size*10
#size = width, height = 500, 500

black = 0,0,0
grey = 25,25,25

ticks_per_second = 1000.0
global_framerate = 60.0
global_interval = int(math.ceil(ticks_per_second/global_framerate))

game_start_time = pygame.time.get_ticks()
game_draw_time = game_start_time

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Dungeon Smash')

#myfont = pygame.font.SysFont("monospace", 20, True)
myfont = pygame.font.Font("Magic Forest.ttf", 16)

showinfo = True

def load_sliced_sprites(w, h, filename):
	images = []
	master_image = pygame.image.load(filename)
	
	master_width, master_height = master_image.get_size()
	
	for i in xrange(int(master_width/w)):
		images.append(master_image.subsurface((i*w,0,w,h)))
	return images

title_card = pygame.image.load("title.png")
button_storymode = pygame.image.load("button_storymode.png")
button_endlessmode = pygame.image.load("button_endlessmode.png")
button_howto = pygame.image.load("button_howto.png")
	
aggro_overlay = pygame.image.load("aggro.png")
stun_overlay = pygame.image.load("stun_1.png")
defend_overlay = pygame.image.load("defending.png")
selection_overlay = pygame.image.load("selection.png")
action_select_overlay = pygame.image.load("action_select.png")
skill_inactive_overlay = pygame.image.load("inactive.png")
equip_overlay = pygame.image.load("equip.png")
broken_overlay = pygame.image.load("broken.png")

attack_images = load_sliced_sprites(32, 32, "DS_Attack.png")
fireball_images = load_sliced_sprites(32, 32, "DS_Fireball.png")

def fps_limited_draw(items):
	global game_draw_time, global_interval
	
	while (pygame.time.get_ticks() < game_draw_time + global_interval):
		pygame.time.wait(1)
		
	game_draw_time = pygame.time.get_ticks()
	
	# Blank de screen
	screen.fill(grey)
	
	# Draw item
	for item in items:
		item.draw()
	
	# Flippit
	pygame.display.flip()

class DS_Keyframe():
	def __init__(self, p, r):
		self.pos = p
		self.rate = r

# Surface manager class that returns surfaces as needed
		
class DS_SurfaceManager:
	player_surfaces = []

	player_surfaces.append(pygame.image.load("sprite\player.png"))
	
	heart_surfaces = []
	heart_surfaces.append(pygame.image.load("sprite\heart_1.png"))
	heart_surfaces.append(pygame.image.load("sprite\heart_2.png"))
	heart_surfaces.append(pygame.image.load("sprite\heart_3.png"))
	heart_surfaces.append(pygame.image.load("sprite\heart_4.png"))
	
	blankheart_surfaces = []
	blankheart_surfaces.append(pygame.image.load("sprite\\blankheart_1.png"))
	blankheart_surfaces.append(pygame.image.load("sprite\\blankheart_2.png"))
	blankheart_surfaces.append(pygame.image.load("sprite\\blankheart_3.png"))
	blankheart_surfaces.append(pygame.image.load("sprite\\blankheart_4.png"))
	
	# Enemy Surfaces
	#-------------------------------------------------------------------#
	enemy_spider = []
	enemy_spider.append(pygame.image.load("sprite\enemy_spider_1.png"))
	enemy_spider.append(pygame.image.load("sprite\enemy_spider_2.png"))
	enemy_spider.append(pygame.image.load("sprite\enemy_spider_3.png"))
	
	enemy_snake = []
	enemy_snake.append(pygame.image.load("sprite\enemy_snake_1.png"))
	enemy_snake.append(pygame.image.load("sprite\enemy_snake_2.png"))
	enemy_snake.append(pygame.image.load("sprite\enemy_snake_3.png"))
	
	enemy_crab = []
	enemy_crab.append(pygame.image.load("sprite\enemy_crab_1.png"))
	enemy_crab.append(pygame.image.load("sprite\enemy_crab_2.png"))
	
	enemy_slime = []
	enemy_slime.append(pygame.image.load("sprite\enemy_slime_1.png"))
	enemy_slime.append(pygame.image.load("sprite\enemy_slime_2.png"))
	enemy_slime.append(pygame.image.load("sprite\enemy_slime_3.png"))
	
	enemy_jelly = []
	enemy_jelly.append(pygame.image.load("sprite\enemy_jelly_1.png"))
	enemy_jelly.append(pygame.image.load("sprite\enemy_jelly_2.png"))
	enemy_jelly.append(pygame.image.load("sprite\enemy_jelly_3.png"))
	
	enemy_wolf = []
	enemy_wolf.append(pygame.image.load("sprite\enemy_wolf_1.png"))
	enemy_wolf.append(pygame.image.load("sprite\enemy_wolf_2.png"))
	enemy_wolf.append(pygame.image.load("sprite\enemy_wolf_3.png"))
	
	enemy_orc = []
	enemy_orc.append(pygame.image.load("sprite\enemy_orc_1.png"))
	enemy_orc.append(pygame.image.load("sprite\enemy_orc_2.png"))
	enemy_orc.append(pygame.image.load("sprite\enemy_orc_3.png"))
	
	enemy_stalker = []
	enemy_stalker.append(pygame.image.load("sprite\enemy_stalker_1.png"))
	enemy_stalker.append(pygame.image.load("sprite\enemy_stalker_2.png"))
	enemy_stalker.append(pygame.image.load("sprite\enemy_stalker_3.png"))

	enemy_horror = []
	enemy_horror.append(pygame.image.load("sprite\enemy_horror_1.png"))
	enemy_horror.append(pygame.image.load("sprite\enemy_horror_2.png"))
	enemy_horror.append(pygame.image.load("sprite\enemy_horror_3.png"))
	
	enemy_undead = []
	enemy_undead.append(pygame.image.load("sprite\enemy_undead_1.png"))
	enemy_undead.append(pygame.image.load("sprite\enemy_undead_2.png"))
	enemy_undead.append(pygame.image.load("sprite\enemy_undead_3.png"))
	
	enemy_demon = []
	enemy_demon.append(pygame.image.load("sprite\enemy_demon_1.png"))
	enemy_demon.append(pygame.image.load("sprite\enemy_demon_2.png"))
	enemy_demon.append(pygame.image.load("sprite\enemy_demon_3.png"))
	
	enemy_dragon = []
	enemy_dragon.append(pygame.image.load("sprite\enemy_dragon_1.png"))
	enemy_dragon.append(pygame.image.load("sprite\enemy_dragon_2.png"))
	enemy_dragon.append(pygame.image.load("sprite\enemy_dragon_3.png"))
	#-------------------------------------------------------------------#
	
	# Boss surfaces
	#-------------------------------------------------------------------#
	boss = []
	boss.append(pygame.image.load("sprite\\boss_1_troll.png"))
	boss.append(pygame.image.load("sprite\\boss_2_beholder.png"))
	boss.append(pygame.image.load("sprite\\boss_3_mindflayer.png"))
	boss.append(pygame.image.load("sprite\\boss_4_greendragon.png"))
	boss.append(pygame.image.load("sprite\\boss_5_towerknight.png"))
	boss.append(pygame.image.load("sprite\\boss_6_deathknight.png"))
	boss.append(pygame.image.load("sprite\\boss_7_dreadknight.png"))
	boss.append(pygame.image.load("sprite\\boss_8_necromancer.png"))
	#-------------------------------------------------------------------#
	
	# Weapon surfaces
	#-------------------------------------------------------------------#
	weapon_fist = pygame.image.load("sprite\weapon_fist.png")
	weapon_melee = []
	weapon_melee.append(pygame.image.load("sprite\weapon_melee_1.png"))
	weapon_melee.append(pygame.image.load("sprite\weapon_melee_2.png"))
	weapon_melee.append(pygame.image.load("sprite\weapon_melee_3.png"))
	weapon_melee.append(pygame.image.load("sprite\weapon_melee_4.png"))
	weapon_melee.append(pygame.image.load("sprite\weapon_melee_5.png"))
	
	weapon_ranged = []
	weapon_ranged.append(pygame.image.load("sprite\weapon_ranged_1.png"))
	weapon_ranged.append(pygame.image.load("sprite\weapon_ranged_2.png"))
	weapon_ranged.append(pygame.image.load("sprite\weapon_ranged_3.png"))
	weapon_ranged.append(pygame.image.load("sprite\weapon_ranged_4.png"))
	weapon_ranged.append(pygame.image.load("sprite\weapon_ranged_5.png"))
	
	weapon_stunner = []
	weapon_stunner.append(pygame.image.load("sprite\weapon_stunner_1.png"))
	weapon_stunner.append(pygame.image.load("sprite\weapon_stunner_2.png"))
	weapon_stunner.append(pygame.image.load("sprite\weapon_stunner_3.png"))
	weapon_stunner.append(pygame.image.load("sprite\weapon_stunner_4.png"))
	
	#-------------------------------------------------------------------#

	skill_surfaces = []

	skill_surfaces.append(pygame.image.load("sprite\skill_defend.png"))
	skill_surfaces.append(pygame.image.load("sprite\skill_divine_shield.png"))
	
	
	pickup_surfaces = []
	
	pickup_surfaces.append(pygame.image.load("sprite\pickup_treasure.png"))
	pickup_surfaces.append(pygame.image.load("sprite\pickup_weapon_chest.png"))
	pickup_surfaces.append(pygame.image.load("sprite\pickup_cross.png"))
	
	
	item_surfaces = []
	
	item_surfaces.append(pygame.image.load("sprite\spell_heal.png"))
	item_surfaces.append(pygame.image.load("sprite\spell_magicmissile.png"))
	
	spell_surfaces = {}
	spell_surfaces['aura'] = pygame.image.load("sprite\spell_aura.png")
	spell_surfaces['coldblast'] = pygame.image.load("sprite\spell_coldblast.png")
	spell_surfaces['deathscroll'] = pygame.image.load("sprite\spell_deathscroll.png")
	spell_surfaces['holyscroll'] = pygame.image.load("sprite\spell_holyscroll.png")
	spell_surfaces['invisibility'] = pygame.image.load("sprite\spell_invisibility.png")
	spell_surfaces['magicmissile'] = pygame.image.load("sprite\spell_magicmissile.png")
	spell_surfaces['heal'] = pygame.image.load("sprite\spell_heal.png")
	spell_surfaces['petrify'] = pygame.image.load("sprite\spell_petrify.png")
	spell_surfaces['petrify'] = pygame.image.load("sprite\spell_petrify.png")
	spell_surfaces['drain'] = pygame.image.load("sprite\spell_drain.png")
	spell_surfaces['fireball'] = pygame.image.load("sprite\spell_fireball.png")
	spell_surfaces['forceblast'] = pygame.image.load("sprite\spell_forceblast.png")
	
	barrier_surfaces = []
	
	barrier_surfaces.append(pygame.image.load("sprite\\barrier_column.png"))
	barrier_surfaces.append(pygame.image.load("sprite\\barrier_divine_shield_left.png"))
	barrier_surfaces.append(pygame.image.load("sprite\\barrier_divine_shield_right.png"))
	barrier_surfaces.append(pygame.image.load("sprite\\barrier_divine_shield_up.png"))
	
	exit_surfaces = []
	
	exit_surfaces.append(pygame.image.load("sprite\location_exit.png"))
	
	def getPlayerSurface(self, num):
		return self.player_surfaces[num]
		
	def getSkillSurface(self, num):
		return self.skill_surfaces[num]
		
	def getPickupSurface(self, num):
		return self.pickup_surfaces[num]
	
	def getItemSurface(self, num):
		return self.item_surfaces[num]
		
	def getBarrierSurface(self, num):
		return self.barrier_surfaces[num]
		
	def getExitSurface(self, num):
		return self.exit_surfaces[num]
	
# Initialize Surface Manager
SurfaceManager = DS_SurfaceManager()


# Basic Dungeon Smash Tile class
class DS_Tile(pygame.sprite.Sprite):
	
	power = 0
	deleted = False
	description = ""
	animated = False
	start_time = 0
	frame = 0
	total_frames = 0
	image = None
	images = []
	framerate = 10.0
	
	# To be used for setting animation keyframes
	# Use global framerate
	keyframes = []		
	dest_pos = [0,0]
	tween_count = 0
	vector = [0,0]
	playing_animation = False
	anim_update_time = 0
	between_keyframes = False
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.keyframes = []
		
	def draw(self):
		screen.blit(self.image, self.rect)
		
	def get_info(self):
		pass
		
	def gone(self):
		return self.deleted
		
	def delete(self):
		self.deleted = True
		
	def copy(self, target):
		if type(self) == type(target):
			self.health = target.health
			self.power = target.power
			self.state = target.state
			self.level = target.level
			return True
		else:
			return False
			
	def replace(self, target):
		if self.copy(target):
			target.delete()
		
	def tap(self, target):
		return True
		
	def clicked(self, pos):
		return self.rect.collidepoint(pos)
		
	def get_description(self):
		return self.description
		
	# Animation-related
	#-------------------------------------------------------------------------#
	# Animation update
	def update(self):
		self.update_animation()
		
		if len(self.images) > 1:
			current_time = pygame.time.get_ticks()
			interval = int(math.ceil(ticks_per_second/self.framerate))

			while self.start_time < current_time:
				self.frame += 1
				self.start_time += interval
				
			self.image = self.images[self.frame % self.total_frames]
			
	# Load next keyframe from queue
	def get_next_keyframe(self):
		# If keyframes in queue, get the next one and 
		if len(self.keyframes) > 0:
			self.playing_animation = True
			# Pop target keyframe into self.dest_pos, harvest information
			keyframe = self.keyframes.pop(0)
			self.dest_pos = keyframe.pos
			self.tween_count = keyframe.rate
			
			# Get vector to dest_pos
			dest_vector_x = abs(self.dest_pos[0] - self.rect.center[0])
			if self.rect.center[0] > self.dest_pos[0]:
				dest_vector_x = -dest_vector_x
			
			dest_vector_y = abs(self.dest_pos[1] - self.rect.center[1])
			if self.rect.center[1] > self.dest_pos[1]:
				dest_vector_y = -dest_vector_y
				
			tween_vector_x = dest_vector_x / float(self.tween_count)
			tween_vector_y = dest_vector_y / float(self.tween_count)
			
			
			self.vector = [tween_vector_x, tween_vector_y]
			
			self.between_keyframes = True
			return True
		else:	# keyframe queue is empty
			# Turn off animation playing
			self.playing_animation = False
			return False
	# Start playing animation
	def update_animation(self):
		if self.playing_animation:
			# Get current time
			current_time = pygame.time.get_ticks()
			# If current_time >= anim_update_time + global_interval, increment position using vector
			if current_time >= self.anim_update_time + global_interval:
				new_pos = [self.rect.center[0] + self.vector[0], self.rect.center[1] + self.vector[1]]
				self.rect.center = new_pos
				self.anim_update_time = pygame.time.get_ticks()
				self.tween_count -= 1
			if self.tween_count == 0:
				self.hit_keyframe()
				
	# Reached keyframe destination - correct position and load next keyframe			
	def hit_keyframe(self):
		# Set position to expected destination position
		self.between_keyframes = False
		
		self.rect.center = self.dest_pos
		self.get_next_keyframe()
		
		
	# Start playing animation if keyframes in queue	
	def play_animation(self):
		if len(self.keyframes) > 0 and self.between_keyframes == False:
			self.get_next_keyframe()
			self.playing_animation = True
			return True
		else:
			return False
			
	def new_keyframe(self, pos):
		self.keyframes.append(DS_Keyframe(pos, 10))
		
	def add_keyframe(self, pos):
		self.keyframes.append(DS_Keyframe(pos, 10))
		
		#self.play_animation()
		
	def set_keyframe(self, index, pos):
		if len(self.keyframes) == 0:
			self.keyframes.append(DS_Keyframe(pos, 20))
		elif len(self.keyframes) > 0 and index >= 0 and index < len(self.keyframes):
			self.keyframes[index].pos = pos
			#self.keyframes[index].rate /= 2.0
		
	def add_keyframe_topleft(self, pos):
		corrected_pos = [pos[0] + self.rect.width/2, pos[1] + self.rect.width/2]
		self.keyframes.append(DS_Keyframe(corrected_pos, 10))
		self.play_animation()
		
	def shake_left(self):
		#if not self.playing_animation:
		original_pos = self.rect.center
		self.keyframes.append(DS_Keyframe([original_pos[0] + self.rect.width/3, original_pos[1]], 3))
		self.keyframes.append(DS_Keyframe([original_pos[0] - self.rect.width/3, original_pos[1]], 3))
		
		self.keyframes.append(DS_Keyframe(original_pos, 3))
		
		self.play_animation()
		
	def shake_right(self):
		original_pos = self.rect.center
		self.keyframes.append(DS_Keyframe([original_pos[0] - self.rect.width/3, original_pos[1]], 3))
		self.keyframes.append(DS_Keyframe([original_pos[0] + self.rect.width/3, original_pos[1]], 3))
		
		self.keyframes.append(DS_Keyframe(original_pos, 3))
		
		self.play_animation()
		
	def shake_down(self):
		original_pos = self.rect.center
		self.keyframes.append(DS_Keyframe([original_pos[0], original_pos[1] + self.rect.width/3], 3))
		self.keyframes.append(DS_Keyframe([original_pos[0], original_pos[1] - self.rect.width/3], 3))
		
		self.keyframes.append(DS_Keyframe(original_pos, 3))
		
		self.play_animation()
		
	def shake_up(self):
		original_pos = self.rect.center
		self.keyframes.append(DS_Keyframe([original_pos[0], original_pos[1] - self.rect.width/3], 3))
		self.keyframes.append(DS_Keyframe([original_pos[0], original_pos[1] + self.rect.width/3], 3))
		
		self.keyframes.append(DS_Keyframe(original_pos, 3))
		
		self.play_animation()
		
	def shake(self):
		self.shake_left()
	
			
	def juke_right(self):
		if not self.playing_animation:
			self.keyframes.append(DS_Keyframe([self.rect.center[0] + self.rect.width/2, self.rect.center[1]], 5))
			self.keyframes.append(DS_Keyframe([self.rect.center[0], self.rect.center[1]], 5))
			self.play_animation()
			
	def juke_left(self):
		if not self.playing_animation:
			self.keyframes.append(DS_Keyframe([self.rect.center[0] - self.rect.width/2, self.rect.center[1]], 5))
			self.keyframes.append(DS_Keyframe([self.rect.center[0], self.rect.center[1]], 5))
			self.play_animation()
			
	def juke_down(self):
		if not self.playing_animation:
			self.keyframes.append(DS_Keyframe([self.rect.center[0], self.rect.center[1] + self.rect.width/2], 5))
			self.keyframes.append(DS_Keyframe([self.rect.center[0], self.rect.center[1]], 5))
			self.play_animation()
			
	def juke_up(self):
		if not self.playing_animation:
			self.keyframes.append(DS_Keyframe([self.rect.center[0], self.rect.center[1] - self.rect.width/2], 5))
			self.keyframes.append(DS_Keyframe([self.rect.center[0], self.rect.center[1]], 5))
			self.play_animation()
		
	def move_right(self):
		if not self.playing_animation:
			self.keyframes.append(DS_Keyframe([self.rect.center[0] + self.rect.width, self.rect.center[1]], 10))
			self.play_animation()
		
	def move_left(self):
		if not self.playing_animation:
			self.keyframes.append(DS_Keyframe([self.rect.center[0] - self.rect.width, self.rect.center[1]], 10))
			self.play_animation()
			
	def move_down(self):
		if not self.playing_animation:
			self.keyframes.append(DS_Keyframe([self.rect.center[0], self.rect.center[1] + self.rect.width], 10))
			self.play_animation()
			
	def move_leftdown(self):
		if not self.playing_animation:
			self.keyframes.append(DS_Keyframe([self.rect.center[0] - self.rect.width, self.rect.center[1]], 10))
			self.keyframes.append(DS_Keyframe([self.rect.center[0], self.rect.center[1] + self.rect.width], 10))
			self.play_animation()
		
class DS_Action(DS_Tile):

	required_targets = 0
	range = 0
	type = 0
	
	def __init__(self):
		DS_Tile.__init__(self)
		
	def get_info(self):
		return "T:" + str(required_targets) + " R:" + str(range)
		
	def get_type(self):
		return self.type
		
	def get_required_targets(self):	
		return self.required_targets
		
	def get_range(self):
		return self.range
		
	def action(self, target):
		pass
		
	def multi_action(self, user, targets):
		pass
		
	def use(self):
		pass

# Weapon class and subclasses
class DS_Weapon(DS_Action):		
	def __init__(self, user):
		DS_Action.__init__(self)
		self.user = user
		self.required_targets = 1
		
		self.power = 1.0
		self.durability = 1
		self.range = 2
		self.type = 0 	# Can be Melee, Ranged, Stun
		
	def get_info(self):
		return "D:" + str(self.durability) + "R:" + str(self.range) + "P:" + str(self.power)
		
	def get_power(self):
		return self.power
		
	def get_type(self):
		return self.type
		
	def broken(self):
		if self.durability <= 0:
			return True
		else:
			return False
	
	def is_ranged(self):
		if self.type != 0:
			return True
		else:
			return False
			
	def degrade(self):
		if self.durability > 0:
			self.durability -= 1
		if self.broken():
			self.break_it()
		
			
	def break_it(self):
		roll = random.randint(0,1)
		if roll == 0:
			self.deleted = True
		
	def use_on(self, target):
		target.take_damage_from_target(self)
		self.use()
			
	def use(self):
		self.degrade()
		return True
		
	def draw(self):
		DS_Action.draw(self)
		
		info_string = str(self.durability)
		info = myfont.render(info_string, 1, (255,255,0))
		screen.blit(info, self.rect.midleft)
		
	def blocked(self):
		pass
		
class DS_Weapon_Melee(DS_Weapon):
	def __init__(self, level, user):
		DS_Weapon.__init__(self, user)
		self.level = level
		
		self.image = SurfaceManager.weapon_melee[level]
		self.rect = self.image.get_rect()
		
		self.type = 0
		
		if level == 0:
			self.description = "Short Sword"
		
			self.power = 2.0
			self.durability = 10
		elif level == 1:
			self.description = "Sword"
		
			self.power = 4.0
			self.durability = 10
		elif level == 2:
			self.description = "Long Sword"
		
			self.power = 6.0
			self.durability = 15
		elif level == 3:
			self.description = "Broad Sword"
		
			self.power = 8.0
			self.durability = 10
		elif level == 4:
			self.description = "Holy Sword"
		
			self.power = 10.0
			self.durability = 10
			
	def use_on(self, target):
		DS_Weapon.use_on(self, target)
		self.user.anim_attack(target)
			
	def blocked(self):
		self.user.blocked()
		
	def multi_action(self, user, targets):
		for target in targets:
		# Attack target
			target.tile().take_damage_direct(self.power * 2)
			#target.provoke()
		self.deleted = True
		
class DS_Weapon_Fist(DS_Weapon):
	def __init__(self, user):
		DS_Weapon.__init__(self, user)
		
		self.image = SurfaceManager.weapon_fist
		self.rect = self.image.get_rect()
		
		self.type = 0
		
		self.power = 0.5
		self.durability = 1
		self.range = 1
		
		self.description = "Fist"
		
	def use_on(self, target):
		target.take_damage_from_target(self)
		self.user.anim_attack(target)
		
	def blocked(self):
		self.user.blocked()
		self.user.take_damage_direct(0.5)
		
	def degrade(self):
		pass
		
	def draw(self):
		DS_Action.draw(self)
		
	def multi_action(self, user, targets):
		for target in targets:
		# Attack target
			target.tile().take_damage_from_target(self)
		
		
class DS_Weapon_Ranged(DS_Weapon):
	def __init__(self, level, user):
		DS_Weapon.__init__(self, user)
		self.level = level
		
		self.image = SurfaceManager.weapon_ranged[level]
		self.rect = self.image.get_rect()
		
		self.required_targets = 1
		
		self.type = 1
		
		if level == 0:
			self.description = "Shortbow"

			self.power = 2.0
			self.durability = 10
			self.range = 2
		elif level == 1:
			self.description = "Bow"

			self.power = 2.0
			self.durability = 10
			self.range = 3
		elif level == 2:
			self.description = "Longbow"

			self.power = 3.0
			self.durability = 10
			self.range = 4
		elif level == 3:
			self.description = "Steel Longbow"

			self.power = 3.0
			self.durability = 20
			self.range = 4
		elif level == 4:
			self.description = "Holy Bow"

			self.power = 4.0
			self.durability = 20
			self.range = 5

	def break_it(self):
		self.power = 0
		self.deleted = True
	
	def use(self):
		if not self.broken():
			self.degrade()
			return True
		else:
			return False
			
	def use_on(self, target):
		target.take_damage_from_target_direct(self)
		#target.provoke()
		self.use()
	
	def multi_action(self, user, targets):
		for target in targets:
		# Attack target
			self.use_on(target.tile())
			
class DS_Weapon_Stunner(DS_Weapon_Ranged):
	def __init__(self, level, user):
		DS_Weapon.__init__(self, user)
		self.level = level
		
		self.image = SurfaceManager.weapon_stunner[level]
		self.rect = self.image.get_rect()
		
		self.required_targets = 1
		self.type = 2
		
		if level == 0:
			self.description = "Rock"
			self.power = 0.5
			self.durability = 10
			self.range = 2
		elif level == 1:
			self.description = "Sling"
			self.power = 1.0
			self.durability = 10
			self.range = 2
		elif level == 2:
			self.description = "War Sling"
			self.power = 1.5
			self.durability = 15
			self.range = 3
		elif level == 3:
			self.description = "Holy Sling"
			self.power = 2.0
			self.durability = 20
			self.range = 3
	
	def use_on(self, target):
		DS_Weapon_Ranged.use_on(self, target)
		
		target.set_stun()
		
		target.set_stun_timer(self.level)
			
	def multi_action(self, user, targets):
		for target in targets:
			self.use_on(target.tile())

# Item class and subclasses
class DS_Item(DS_Action):
	level = 0
	uses = 1
	type = 0 	# can be defensive, offensive, field

	def __init__(self):
		DS_Action.__init__(self)
		self.level = 0
		self.uses = 1
		self.type = 0
		
	
	def gone(self):
		if self.deleted:
			return True
		if self.uses > 0:
			return False
		else:
			return True
	
			
	def use(self):
		if not self.gone():
			self.uses -= 1
			return True
		else:
			return False
			
	def draw(self):
		DS_Tile.draw(self)
		
		level_string = str(self.level + 1)
		level_info = myfont.render(level_string, 1, (255,255,0))
		screen.blit(level_info, self.rect.center)
			
class DS_Spell_Heal(DS_Item):
	def __init__(self, level):
		if level < 0: 
			return False
			
		DS_Item.__init__(self)
		
		self.level = level
		
		self.description = "Heal " + str(self.level + 1)
		
		self.image = SurfaceManager.spell_surfaces['heal']
		self.rect = self.image.get_rect()
		self.type = 0
		
	def tap(self, target):
		if self.use():
			self.action(target)
		
	def action(self, target):
		# Heal player
		target.increase_health(4 * (self.level + 1))
		self.use()
		
class DS_Spell_MagicMissile(DS_Item):
	def __init__(self, level):
		if level < 0: 
			return False
			
		DS_Item.__init__(self)

		self.level = level
		
		self.description = "Magic Missile " + str(self.level + 1)
		
		self.image = SurfaceManager.spell_surfaces['magicmissile']
		self.rect = self.image.get_rect()
		
		self.type = 1
		self.required_targets = self.level + 1
		self.range = 4
	
	def multi_action(self, user, targets):
		# Heal player
		for target in targets:
			AnimManager.queue.append(DS_Anim_Fireball(target.tile().rect.center))
			target.tile().take_damage_direct(4)
		self.use()
		
class DS_Spell_Drain(DS_Item):
	def __init__(self, level):
		if level < 0: 
			return False
			
		DS_Item.__init__(self)

		self.level = level
		
		self.description = "Drain " + str(self.level + 1)
		
		self.image = SurfaceManager.spell_surfaces['drain']
		self.rect = self.image.get_rect()
		
		self.type = 1
		self.required_targets = self.level + 1
		self.range = 4
	
	def multi_action(self, user, targets):
		# Heal player
		for target in targets:
			target.tile().take_damage_direct(2)
			user.increase_health(2)
			
		self.use()
		
class DS_Spell_Petrify(DS_Item):
	def __init__(self, level):
		if level < 0: 
			return False
			
		DS_Item.__init__(self)

		self.level = level
		
		self.description = "Petrify " + str(self.level + 1)
		
		self.image = SurfaceManager.spell_surfaces['petrify']
		self.rect = self.image.get_rect()
		
		self.type = 1
		self.required_targets = self.level + 1
		self.range = 4
	
	def multi_action(self, user, targets):
		
		for pair in targets:
			new_barrier = DS_Barrier_Column()
			new_barrier.health = pair.tile().health
			new_barrier.max_health = pair.tile().max_health
			new_barrier.rect.center = pair.tile().rect.center
			
			#target = new_barrier
			#target.tile() = DS_Barrier_Column()
			pair.stream[pair.index] = new_barrier

		self.use()
		
class DS_Spell_Fireball(DS_Item):
	def __init__(self, level):
		if level < 0: 
			return False
			
		DS_Item.__init__(self)

		self.level = level
		
		self.description = "Fireball " + str(self.level + 1)
		
		self.image = SurfaceManager.spell_surfaces['fireball']
		self.rect = self.image.get_rect()
		
		self.type = 1
		self.required_targets = 1
		self.range = 2
	
	def multi_action(self, user, targets):
		
		for pair in targets:
			damage = (self.level + 1) * 8
			for i in range(len(pair.stream)):
				if damage > 0:
					AnimManager.queue.append(DS_Anim_Fireball(pair.stream[i].rect.center))
					if pair.stream[i].health <= damage:
						damage -= pair.stream[i].health
						pair.stream[i].take_damage_direct(pair.stream[i].health)
					else:
						pair.stream[i].take_damage_direct(damage)
						damage = 0
				if damage == 0:
					break

		self.use()

class DS_Spell_ForceBlast(DS_Item):
	def __init__(self, level):
		if level < 0: 
			return False
			
		DS_Item.__init__(self)

		self.level = level
		
		self.description = "Force Blast " + str(self.level + 1)
		
		self.image = SurfaceManager.spell_surfaces['forceblast']
		self.rect = self.image.get_rect()
		
		self.type = 2
		self.required_targets = 1
		self.range = 2
	
	def multi_action(self, user, streams):
		
		for stream in streams:
			if isinstance(stream[0], DS_Enemy):
				stream[0].set_stun()
				stream[0].stun_timer = self.level

		self.use()		

		
# Skill class and subclasses
class DS_Skill(DS_Action):
	
	charge = 0
	full_charge = 0
	type = 0

	def __init__(self):
		DS_Action.__init__(self)
		
	def get_info(self):
		return "Skill"
		
	def active(self):
		if self.charge == self.full_charge:
			return True
		else:
			return False
			
	def activate(self):
		if self.active():
			self.charge = 0
			return True
		else:
			return False
			
	def recharge(self):
		if self.charge < self.full_charge:
			self.charge += 1
			
	def full_recharge(self):
		self.charge = self.full_charge
			
	def tap(self, target): 
		return self.action(target)
		
	def draw(self):
		DS_Tile.draw(self)
		if not self.active():
			screen.blit(skill_inactive_overlay, self.rect)
		
class DS_Skill_Defend(DS_Skill):
	def __init__(self):
		DS_Skill.__init__(self)
		
		self.image = SurfaceManager.getSkillSurface(0)
		self.rect = self.image.get_rect()
		
		self.charge = 3
		self.full_charge = 3
		
		self.type = 0
		
	def action(self, target):
		if self.activate():
			target.set_defend()
			return True
		else:
			return False
		
class DS_Skill_DivineShield(DS_Skill):
	def __init__(self):
		DS_Skill.__init__(self)
		
		self.image = SurfaceManager.getSkillSurface(1)
		self.rect = self.image.get_rect()
		
		self.charge = 20
		self.full_charge = 20
		
		self.type = 2
		
	def act_on_streams(self, streams):
		if self.activate():
			streams[0].add_tile(0, DS_Barrier_DivineShieldLeft())
			streams[2].add_tile(0, DS_Barrier_DivineShieldUp())
			streams[4].add_tile(0, DS_Barrier_DivineShieldRight())
			return True
		return False
		
# Actor class - for live game board tiles
class DS_Actor(DS_Tile):
	def __init__(self):
		DS_Tile.__init__(self)
		self.max_health = 1
		self.health = 1
		self.power = 0
		self.state = 0	# Can be neutral, defend, aggro, or stun
		self.stun_time = 1
		self.stun_timer = 0
		self.level = 0
		
	def copy(self, target):
		if DS_Tile.copy(self, target):
			self.stun_time = target.stun_time
			self.stun_timer = target.stun_timer
			return True
		else:
			return False
		
	def anim_attack(self, target):
		if target.rect.center[0] < self.rect.center[0]:
			self.juke_left()
		elif target.rect.center[0] > self.rect.center[0]:
			self.juke_right()
		elif target.rect.center[1] < self.rect.center[1]:
			self.juke_up()
		elif target.rect.center[1] > self.rect.center[1]:
			self.juke_down()
			
	def kill(self):
		self.shake_left()
		self.health = 0
		
	def take_damage_direct(self, damage):
		self.shake_left()
		self.health -= damage
		
	def take_damage_from_target_direct(self, target):
		self.shake_left()
		damage = target.get_power() - (0.1 * self.level)
		self.health -= damage
		
	def take_damage(self, damage):		
		damage -= (0.1 * self.level)
		if damage < 0.1:
			damage = 0.1
		if self.state == 0:
			self.health -= damage
		elif self.state == 1:
			pass
		elif self.state == 2:
			self.health -= damage / 2.0
		elif self.state == 3:
			self.health -= damage * 2
		
	def take_damage_from_target(self, target):
		if self.state != 1:
			if target.rect.center[0] < self.rect.center[0]:
				self.shake_right()
			elif target.rect.center[0] > self.rect.center[0]:
				self.shake_left()
			elif target.rect.center[1] < self.rect.center[1]:
				self.shake_down()
			elif target.rect.center[1] > self.rect.center[1]:
				self.shake_up()
		
		damage = target.get_power() - (0.1 * self.level)
		
		if damage < 0.1:
			damage = 0.1
		if self.state == 0:
			self.health -= damage
		elif self.state == 1:
			target.blocked()
		elif self.state == 2:
			self.health -= damage / 2.0
		elif self.state == 3:
			self.health -= damage * 2
		
	# prototype for reaction to getting blocked
	def blocked(self):
		self.set_stun()
		self.stun_timer = self.stun_time
		
	def stun_recover(self):
		if self.stun_timer <= 0:
			self.set_neutral()
		elif self.stun_timer > 0:
			self.stun_timer -= 1
		
	def attack(self, target):
		pass
		
	def react(self):
		pass
	
	def reset(self):
		self.health = self.max_health
		self.state = 0
		
	def killed(self):
		if self.health <= 0:
			return True
		else:
			return False
		
	def get_health(self):
		return self.health
		
	def get_max_health(self):
		return self.max_health
		
	def get_power(self):
		return self.power
		
	def get_level(self):
		return self.level
		
	def get_state(self):
		return self.state
		
	def set_neutral(self):
		self.state = 0
		
	def set_defend(self):
		if not self.is_stun():
			self.state = 1
		
	def set_aggro(self):
		if not self.is_stun():
			self.state = 2
		
	def set_stun(self):
		self.state = 3
		
	def set_stun_timer(self, time):
		self.state = 3
		self.stun_timer = time
		
	def provoke(self):
		if not self.is_defend():
			self.set_aggro()
		
	def is_neutral(self):
		if self.state == 0:
			return True
		else:
			return False
			
	def is_defend(self):
		if self.state == 1:
			return True
		else:
			return False
			
	def is_aggro(self): 
		if self.state == 2:
			return True
		else:
			return False
			
	def is_stun(self):
		if self.state == 3:
			return True
		else:
			return False
		
	def get_info(self):
		return "HP:" + str(self.health) + "/" + str(self.max_health) + " P:" + str(self.power)
		
	def merge(self, target):
		self.max_health += target.max_health
		self.health += target.health
		target.delete()
	
	def increase_health(self, num):
		self.health += num
		if self.health > self.max_health:
			self.health = self.max_health
		
	def increase_max_health(self, num):
		self.max_health += num
		
	def gone(self):
		if self.health <= 0:
			return True
		else:
			return self.deleted
	
	def draw(self):
		global aggro_overlay
		
		DS_Tile.draw(self)
		
		if self.state == 1:
			screen.blit(defend_overlay, self.rect)
		if self.state == 2:
			screen.blit(aggro_overlay, self.rect)
		if self.state == 3:
			screen.blit(stun_overlay, self.rect)
		
# Player class - subclass of Actor
class DS_Player(DS_Actor):
	def __init__(self):
		global SurfaceManager
		DS_Actor.__init__(self)
		
		self.image = SurfaceManager.getPlayerSurface(0)
		self.rect = self.image.get_rect()
		
		self.max_health = 12
		self.health = 12
		self.power = 1
		
		self.state = 0 # Can be neutral, defend, or stun
		
		self.level = 0
		
	def reset(self):
		DS_Actor.reset(self)
		
	def gone(self):
		if self.health <= 0:
			return True
		else:
			return False
		
# ENEMY CLASSES
#-------------------------------------------------------------------------------------------#
class DS_Enemy(DS_Actor):
	points = 0
	
	def __init__(self):
		DS_Actor.__init__(self)
		self.level = 0
		self.behavior = 0			# aggressor, defender, deullist
		
	def get_info(self):
		return "HP" + str(self.health) + "/" + str(self.max_health) + ":P" + str(self.power) + ":L" + str(self.level)
		
	def get_power(self):
		return self.power + (0.1 * self.power * self.level)
		
	def react(self, player):
		if self.behavior == 0:
			self.set_aggro()
		elif self.behavior == 1:
			if player.is_stun():
				self.set_aggro()
			else:
				self.set_defend()
		elif self.behavior == 2:
			if player.is_defend() or player.is_stun():
				self.set_aggro()
			else:
				self.set_defend()
		
	def attack(self, target):
		self.anim_attack(target)
		
		target.take_damage_from_target(self)
		
	def points_worth(self):
		return int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Spider1(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Brown Spider"
		
		self.image = SurfaceManager.enemy_spider[0]
		self.rect = self.image.get_rect()	
		
		self.max_health = 0.5
		self.health = self.max_health
		
		self.power = 0.5
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Spider2(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Grey Spider"
		
		self.image = SurfaceManager.enemy_spider[1]
		self.rect = self.image.get_rect()	
		
		self.max_health = 0.5
		self.health = self.max_health
		
		self.power = 1.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Spider3(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Dark Spider"
		
		self.image = SurfaceManager.enemy_spider[2]
		self.rect = self.image.get_rect()	
		
		self.max_health = 1.0
		self.health = self.max_health
		
		self.power = 1.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Crab1(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Blue Crab"
		
		self.image = SurfaceManager.enemy_crab[0]
		self.rect = self.image.get_rect()	
		
		self.max_health = 1.5
		self.health = self.max_health
		
		self.power = 1.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
		self.behavior = 1
		
class DS_Enemy_Crab2(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Red Crab"
		
		self.image = SurfaceManager.enemy_crab[1]
		self.rect = self.image.get_rect()	
		
		self.max_health = 2.0
		self.health = self.max_health
		
		self.power = 2.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
		self.behavior = 1
		
class DS_Enemy_Snake1(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Green Snake"
		
		self.image = SurfaceManager.enemy_snake[0]
		self.rect = self.image.get_rect()	
		
		self.max_health = 0.5
		self.health = self.max_health
		
		self.power = 1.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
		self.behavior = 2
		
class DS_Enemy_Snake2(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Blue Snake"
		
		self.image = SurfaceManager.enemy_snake[1]
		self.rect = self.image.get_rect()	
		
		self.max_health = 1.0
		self.health = self.max_health
		
		self.power = 1.5
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
		self.behavior = 2
		
class DS_Enemy_Snake3(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Red Snake"
		
		self.image = SurfaceManager.enemy_snake[2]
		self.rect = self.image.get_rect()	
		
		self.max_health = 1.0
		self.health = self.max_health
		
		self.power = 2.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
		self.behavior = 2
		
class DS_Enemy_Wolf1(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Wolf Pup"
		
		self.image = SurfaceManager.enemy_wolf[0]
		self.rect = self.image.get_rect()	
		
		self.max_health = 2.0
		self.health = self.max_health
		
		self.power = 2.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Wolf2(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Grey Wolf"
		
		self.image = SurfaceManager.enemy_wolf[1]
		self.rect = self.image.get_rect()	
		
		self.max_health = 3.0
		self.health = self.max_health
		
		self.power = 3.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Wolf3(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "White Wolf"
		
		self.image = SurfaceManager.enemy_wolf[2]
		self.rect = self.image.get_rect()	
		
		self.max_health = 4.0
		self.health = self.max_health
		
		self.power = 4.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Slime1(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Green Slime"
		
		self.image = SurfaceManager.enemy_slime[0]
		self.rect = self.image.get_rect()	
		
		self.max_health = 1.0
		self.health = self.max_health
		
		self.power = 1.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Slime2(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Blue Slime"
		
		self.image = SurfaceManager.enemy_slime[1]
		self.rect = self.image.get_rect()	
		
		self.max_health = 2.0
		self.health = self.max_health
		
		self.power = 1.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Slime3(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Red Slime"
		
		self.image = SurfaceManager.enemy_slime[2]
		self.rect = self.image.get_rect()	
		
		self.max_health = 3.0
		self.health = self.max_health
		
		self.power = 1.5
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Orc1(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Orc Grunt"
		
		self.image = SurfaceManager.enemy_orc[0]
		self.rect = self.image.get_rect()
		
		self.max_health = 2.0
		self.health = self.max_health
		
		self.power = 2.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Orc2(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Orc Fighter"
		
		self.image = SurfaceManager.enemy_orc[1]
		self.rect = self.image.get_rect()
		
		self.max_health = 3.0
		self.health = self.max_health
		
		self.power = 3.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
		self.behavior = 2
		
class DS_Enemy_Orc3(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Orc Knight"
		
		self.image = SurfaceManager.enemy_orc[2]
		self.rect = self.image.get_rect()
		
		self.max_health = 4.0
		self.health = self.max_health
		
		self.power = 4.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
		self.behavior = 2
		
class DS_Enemy_Jelly1(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Green Jelly"
		
		self.image = SurfaceManager.enemy_jelly[0]
		self.rect = self.image.get_rect()
		
		self.max_health = 2.0
		self.health = self.max_health
		
		self.power = 1.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Jelly2(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Blue Jelly"
		
		self.image = SurfaceManager.enemy_jelly[1]
		self.rect = self.image.get_rect()
		
		self.max_health = 3.0
		self.health = self.max_health
		
		self.power = 2.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Jelly3(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Red Jelly"
		
		self.image = SurfaceManager.enemy_jelly[2]
		self.rect = self.image.get_rect()
		
		self.max_health = 4.0
		self.health = self.max_health
		
		self.power = 2.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Stalker1(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Green Stalker"
		
		self.image = SurfaceManager.enemy_stalker[0]
		self.rect = self.image.get_rect()
		
		self.max_health = 6.0
		self.health = self.max_health
		
		self.power = 2.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
		self.behavior = 1
		
class DS_Enemy_Stalker2(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Blue Stalker"
		
		self.image = SurfaceManager.enemy_stalker[1]
		self.rect = self.image.get_rect()
		
		self.max_health = 8.0
		self.health = self.max_health
		
		self.power = 2.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
		self.behavior = 1
		
class DS_Enemy_Stalker3(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Red Stalker"
		
		self.image = SurfaceManager.enemy_stalker[2]
		self.rect = self.image.get_rect()
		
		self.max_health = 10.0
		self.health = self.max_health
		
		self.power = 2.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
		self.behavior = 1
		
class DS_Enemy_Horror1(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Green Horror"
		
		self.image = SurfaceManager.enemy_horror[0]
		self.rect = self.image.get_rect()
		
		self.max_health = 4.0
		self.health = self.max_health
		
		self.power = 4.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Horror2(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Blue Horror"
		
		self.image = SurfaceManager.enemy_horror[1]
		self.rect = self.image.get_rect()
		
		self.max_health = 4.0
		self.health = self.max_health
		
		self.power = 6.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Horror3(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Red Horror"
		
		self.image = SurfaceManager.enemy_horror[2]
		self.rect = self.image.get_rect()
		
		self.max_health = 4.0
		self.health = self.max_health
		
		self.power = 8.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Undead1(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Zombie"
		
		self.image = SurfaceManager.enemy_undead[0]
		self.rect = self.image.get_rect()
		
		self.max_health = 3.0
		self.health = self.max_health
		
		self.power = 2.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Undead2(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Skeleton"
		
		self.image = SurfaceManager.enemy_undead[1]
		self.rect = self.image.get_rect()
		
		self.max_health = 2.0
		self.health = self.max_health
		
		self.power = 4.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Undead3(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Wraith"
		
		self.image = SurfaceManager.enemy_undead[2]
		self.rect = self.image.get_rect()
		
		self.max_health = 6.0
		self.health = self.max_health
		
		self.power = 6.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
		self.behavior = 2
		
class DS_Enemy_Demon1(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Lesser Demon"
		
		self.image = SurfaceManager.enemy_demon[0]
		self.rect = self.image.get_rect()
		
		self.max_health = 6.0
		self.health = self.max_health
		
		self.power = 6.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Demon2(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Demon"
		
		self.image = SurfaceManager.enemy_demon[1]
		self.rect = self.image.get_rect()
		
		self.max_health = 9.0
		self.health = self.max_health
		
		self.power = 6.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Demon3(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Greater Demon"
		
		self.image = SurfaceManager.enemy_demon[2]
		self.rect = self.image.get_rect()
		
		self.max_health = 12.0
		self.health = self.max_health
		
		self.power = 9.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Dragon1(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Blue Dragon"
		
		self.image = SurfaceManager.enemy_Dragon[0]
		self.rect = self.image.get_rect()
		
		self.max_health = 20.0
		self.health = self.max_health
		
		self.power = 10.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Dragon2(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Red Dragon"
		
		self.image = SurfaceManager.enemy_Dragon[1]
		self.rect = self.image.get_rect()
		
		self.max_health = 40.0
		self.health = self.max_health
		
		self.power = 11.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Enemy_Dragon3(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Bone Dragon"
		
		self.image = SurfaceManager.enemy_Dragon[2]
		self.rect = self.image.get_rect()
		
		self.max_health = 60.0
		self.health = self.max_health
		
		self.power = 12.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
#-------------------------------------------------------------------------------------------#

# BOSS CLASSES
#-------------------------------------------------------------------------------------------#
class DS_Boss_Troll(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Troll"
		
		self.image = SurfaceManager.boss[0]
		self.rect = self.image.get_rect()
		
		self.max_health = 12.0
		self.health = self.max_health
		
		self.power = 4.0
		
		self.points = int(self.max_health * 100 + self.power * 100)

class DS_Boss_Beholder(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Beholder"
		
		self.image = SurfaceManager.boss[1]
		self.rect = self.image.get_rect()
		
		self.max_health = 18.0
		self.health = self.max_health
		
		self.power = 6.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
	def attack(self, target):
		DS_Enemy.attack(self, target)
		target.set_stun()
		
class DS_Boss_Mindflayer(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Mindflayer"
		
		self.image = SurfaceManager.boss[2]
		self.rect = self.image.get_rect()
		
		self.max_health = 25.0
		self.health = self.max_health
		
		self.power = 8.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Boss_GreenDragon(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Green Dragon"
		
		self.image = SurfaceManager.boss[3]
		self.rect = self.image.get_rect()
		
		self.max_health = 50.0
		self.health = self.max_health
		
		self.power = 10.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
class DS_Boss_TowerKnight(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Tower Knight"
		
		self.image = SurfaceManager.boss[4]
		self.rect = self.image.get_rect()
		
		self.max_health = 66.0
		self.health = self.max_health
		
		self.power = 6.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
		self.behavior = 2
		
class DS_Boss_DeathKnight(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Death Knight"
		
		self.image = SurfaceManager.boss[5]
		self.rect = self.image.get_rect()
		
		self.max_health = 66.0
		self.health = self.max_health
		
		self.power = 6.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
		self.behavior = 2
		
class DS_Boss_DreadKnight(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Dread Knight"
		
		self.image = SurfaceManager.boss[6]
		self.rect = self.image.get_rect()
		
		self.max_health = 66.0
		self.health = self.max_health
		
		self.power = 6.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
		self.behavior = 2
		
class DS_Boss_Necromancer(DS_Enemy):
	def __init__(self):
		DS_Enemy.__init__(self)
		
		self.description = "Necromancer"
		
		self.image = SurfaceManager.boss[7]
		self.rect = self.image.get_rect()
		
		self.max_health = 100
		self.health = self.max_health
		
		self.power = 6.0
		
		self.points = int(self.max_health * 100 + self.power * 100)
		
		self.behavior = 2

#-------------------------------------------------------------------------------------------#

		
# Pickup class
class DS_Pickup(DS_Actor):
	def __init__(self):
		DS_Actor.__init__(self)

class DS_Pickup_ItemChest(DS_Pickup):
	def __init__(self):
		DS_Pickup.__init__(self)
		
		self.image = SurfaceManager.getPickupSurface(0)
		self.rect = self.image.get_rect()
		
class DS_Pickup_WeaponChest(DS_Pickup):
	def __init__(self):
		DS_Pickup.__init__(self)
		
		self.image = SurfaceManager.getPickupSurface(1)
		self.rect = self.image.get_rect()
		
class DS_Pickup_Cross(DS_Pickup):
	def __init__(self):
		DS_Pickup.__init__(self)
		
		self.image = SurfaceManager.getPickupSurface(2)
		self.rect = self.image.get_rect()
		
		
# Barrier class
class DS_Barrier(DS_Actor):
	def __init__(self):
		DS_Actor.__init__(self)
		
	def take_damage_from_target(self, target):
		damage = target.get_power() - (0.1 * self.level)
		if damage < 0.1:
			damage = 0.1
		if self.state == 0:
			self.health -= damage
		elif self.state == 1:
			target.blocked()
		elif self.state == 2:
			self.health -= damage / 2.0
		elif self.state == 3:
			self.health -= damage * 2
			
	def set_stun(self):
		pass
		
	def set_stun_timer(self, time):
		pass
		
class DS_Barrier_Column(DS_Barrier):
	def __init__(self):
		DS_Barrier.__init__(self)
		
		self.image = SurfaceManager.getBarrierSurface(0)
		self.rect = self.image.get_rect()
		
		self.health = 4
		self.max_health = 4
		
class DS_Barrier_FixedColumn(DS_Barrier):
	def __init__(self):
		DS_Barrier.__init__(self)
		
		self.image = SurfaceManager.getBarrierSurface(0)
		self.rect = self.image.get_rect()
		
		self.health = 1000
		self.max_health = 1000
		
	def gone(self):
		return False
		
class DS_Barrier_DivineShieldLeft(DS_Barrier):
	def __init__(self):
		DS_Barrier.__init__(self)
		
		self.image = SurfaceManager.getBarrierSurface(1)
		self.rect = self.image.get_rect()
		
		self.health = 10
		self.max_health = 10
	
class DS_Barrier_DivineShieldRight(DS_Barrier):
	def __init__(self):
		DS_Barrier.__init__(self)
		
		self.image = SurfaceManager.getBarrierSurface(2)
		self.rect = self.image.get_rect()
		
		self.health = 10
		self.max_health = 10
		
class DS_Barrier_DivineShieldUp(DS_Barrier):
	def __init__(self):
		DS_Barrier.__init__(self)
		
		self.image = SurfaceManager.getBarrierSurface(3)
		self.rect = self.image.get_rect()
		
		self.health = 10
		self.max_health = 10
		
class DS_Location(DS_Actor):
	def __init__(self):
		DS_Actor.__init__(self)
		
	def gone(self):
		return False
		
class DS_Location_Exit(DS_Location):
	def __init__(self):
		DS_Location.__init__(self)
		
		self.image = SurfaceManager.getExitSurface(0)
		self.rect = self.image.get_rect()
		
		self.health = 1000
		self.max_health = 1000
		

# Animation classes
class DS_Anim(pygame.sprite.Sprite):
	deleted = False
	start_time = 0
	frame = 0
	total_frames = 0
	image = None
	images = None
	framerate = 10.0
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.start_time = pygame.time.get_ticks()
		
	def update(self):
		if not self.deleted:
			current_time = pygame.time.get_ticks()
			interval = int(math.ceil(ticks_per_second/self.framerate))

			while self.start_time < current_time:
				self.frame += 1
				self.start_time += interval
				
			self.image = self.images[self.frame % self.total_frames]
				
			if self.frame >= self.total_frames:
				self.deleted = True
				
	def draw(self):
		if not self.deleted:
			screen.blit(self.image, self.rect)
			
class DS_Anim_MeleeAttack(DS_Anim):
	def __init__(self, pos):
		DS_Anim.__init__(self)
		self.images = attack_images
		self.image = self.images[self.frame]
		self.rect = self.image.get_rect()
		self.total_frames = len(self.images)
		self.rect.center = pos
		
class DS_Anim_Fireball(DS_Anim):
	def __init__(self, pos):
		DS_Anim.__init__(self)
		self.images = fireball_images
		self.image = self.images[self.frame]
		self.rect = self.image.get_rect()
		self.total_frames = len(self.images)
		self.rect.center = pos
		
# Tile Manager class - superclass of Enemy, Weapon, Item, and Barrier Managers
class DS_TileManager:
	def getTile(tier):
		# Set rules for retrieving tiles from certain tier
		pass
		
# Enemy Manager class used to generate enemies
class DS_EnemyManager(DS_TileManager):
	pass
		
class DS_WeaponManager(DS_TileManager):
	def getShortSword(self):
		return DS_Weapon_ShortSword()
	def getShortbow(self):
		return DS_Weapon_Shortbow()
	def getLongbow(self):
		return DS_Weapon_Longbow()
	def getSling(self):
		return DS_Weapon_Sling()
		
class DS_ItemManager(DS_TileManager):
	pass

class DS_PickupManager(DS_TileManager):
	def getItemChest(self):
		return DS_Pickup_ItemChest()
	def getWeaponChest(self):
		return DS_Pickup_WeaponChest()
	def getCross(self):
		return DS_Pickup_Cross()
		
class DS_BarrierManager(DS_TileManager):
	def getColumn(self):
		return DS_Barrier_Column()
	def getFixedColumn(self):
		return DS_Barrier_FixedColumn()
		
class DS_LocationManager:
	def getExit(self):
		# Placeholder
		return DS_Location_Exit()		
		
# Initialize Enemy Manager
EnemyManager = DS_EnemyManager()

# Initialize Weapon Manager
WeaponManager = DS_WeaponManager()

# Initialize Item Manager
ItemManager = DS_ItemManager()

# Initialize Pickup Manager
PickupManager = DS_PickupManager()

# Initialize Barrier Manager
BarrierManager = DS_BarrierManager()

# Initialize Location Manager
LocationManager = DS_LocationManager()

class DS_Button(pygame.sprite.Sprite):
	def __init__(self, surface):
		pygame.sprite.Sprite.__init__(self)
		self.image = surface
		self.rect = self.image.get_rect()
		
	def draw(self):
		screen.blit(self.image, self.rect)
		
	def clicked(self, pos):
		return self.rect.collidepoint(pos)
		
class DS_Interface:
	def __init__(self):
		self.images = []
		self.buttons = []

	def draw(self):
		pass
		
	def handle_key(self, key):
		pass
		
	def handle_tap(self, pos):
		pass
	
class DS_Interface_MainMenu(DS_Interface):
	def __init__(self):
		DS_Interface.__init__(self)
		self.images.append(DS_Button(title_card))
		self.images[0].rect.center = [width/2.0, self.images[0].rect.height/2.0]
		
		self.buttons.append(DS_Button(button_storymode))
		self.buttons[0].rect.center = [width/2.0, self.images[0].rect.height + self.buttons[0].rect.height/2.0]
		
		self.buttons.append(DS_Button(button_endlessmode))
		self.buttons[1].rect.center = [width/2.0, self.buttons[0].rect.center[1] + self.buttons[1].rect.height]
		
	def draw(self):
		for image in self.images:
			image.draw()
			
		for button in self.buttons:
			button.draw()
		'''
		title = myfont.render("Dungeon", 1, (255,255,0))
		title2 = myfont.render("Smash", 1, (255,255,0))
		
		info = myfont.render("Click", 1, (255,255,0))
		info2 = myfont.render("to Smash!", 1, (255,255,0))
		
		screen.blit(title, (10, tile_size * 2))
		screen.blit(title2, (10, tile_size * 3))
		screen.blit(info, (10, tile_size * 5))
		screen.blit(info2, (10, tile_size * 6))
		'''
		
	def handle_tap(self, pos):
		for i in range(len(self.buttons)):
			if self.buttons[i].clicked(pos):
				return i
	
class DS_Interface_StatScreen(DS_Interface):
	level_score = 0
	bonus = 0
	enemies_killed = []
	got_bonus = False
	
	def getStats(self, gameManager):	
		self.level_score = gameManager.level_score
		self.enemies_killed = gameManager.stat_enemies_killed
		self.bonus = gameManager.bonus / 2
		self.got_bonus = gameManager.clean_sweep()
		
	def draw(self):
		score_info = myfont.render("Level Score:", 1, (255,255,0))
		score = myfont.render(str(self.level_score), 1, (255,255,0))
		
		level_info = myfont.render("Get Ready", 1, (255,255,0))
		level_info2 = myfont.render("Next Level", 1, (255,255,0))
		
		screen.blit(score_info, (10, tile_size * 1))
		screen.blit(score, (10, tile_size * 2))
		screen.blit(level_info, (10, tile_size * 5))
		screen.blit(level_info2, (10, tile_size * 6))
		
		if self.got_bonus:
			bonus_info = myfont.render("Sweep Bonus:", 1, (255,255,0))
			bonus = myfont.render(str(self.bonus), 1, (255,255,0))
			screen.blit(bonus_info, (10, tile_size * 3))
			screen.blit(bonus, (10, tile_size * 4))
	
class DS_Interface_GameOverScreen(DS_Interface):
	total_score = 0
	enemies_killed = []

	def getStats(self, gameManager):	
		self.total_score = gameManager.score
		self.enemies_killed = gameManager.stat_enemies_killed
		
	def draw(self):
		score_info = myfont.render("Total Score:", 1, (255,255,0))
		score = myfont.render(str(self.total_score), 1, (255,255,0))
		level_info = myfont.render("Game Over", 1, (255,255,0))
		
		screen.blit(score_info, (10, tile_size * 3))
		screen.blit(score, (10, tile_size * 4))
		screen.blit(level_info, (10, tile_size * 6))
		
class DS_Interface_GameWonScreen(DS_Interface):
	level_score = 0
	bonus = 0
	enemies_killed = []
	got_bonus = False
	
	def getStats(self, gameManager):	
		self.level_score = gameManager.level_score
		self.enemies_killed = gameManager.stat_enemies_killed
		self.bonus = gameManager.bonus / 2
		self.got_bonus = gameManager.clean_sweep()
		
	def draw(self):
		score_info = myfont.render("Level Score:", 1, (255,255,0))
		score = myfont.render(str(self.level_score), 1, (255,255,0))
		
		level_info = myfont.render("You Won!", 1, (255,255,0))
		level_info2 = myfont.render("Good job!", 1, (255,255,0))
		
		screen.blit(score_info, (10, tile_size * 1))
		screen.blit(score, (10, tile_size * 2))
		screen.blit(level_info, (10, tile_size * 5))
		screen.blit(level_info2, (10, tile_size * 6))
		
		if self.got_bonus:
			bonus_info = myfont.render("Sweep Bonus:", 1, (255,255,0))
			bonus = myfont.render(str(self.bonus), 1, (255,255,0))
			screen.blit(bonus_info, (10, tile_size * 3))
			screen.blit(bonus, (10, tile_size * 4))
		
class DS_Menu:
	state = 0		# Main menu, 

	interfaces = []
	
	def init(self):
		self.addInterface(DS_Interface_MainMenu())
		self.addInterface(DS_Interface_StatScreen())
		self.addInterface(DS_Interface_GameOverScreen())
		self.addInterface(DS_Interface_GameWonScreen())
	
	def setInterface(self, num):
		if num >= 0 and num < len(self.interfaces):
			self.state = num
			return True
		else:
			return False
		
	def addInterface(self, interface):
		self.interfaces.append(interface)
		
	def currentInterface(self):
		return self.interfaces[self.state]
		
	def draw(self):
		self.currentInterface().draw()
		# Flip screen
		pygame.display.flip()
		
	def handle_key(self, key):
		self.currentInterface().handle_key(key)
		
	def handle_tap(self, pos):
		self.currentInterface().handle_tap(pos)
		
	def loop(self, gamemanager, event):
		# Placeholder - Should be handled by each Interface's own GetInput methods
		if isinstance(self.currentInterface(), DS_Interface_MainMenu):
			if event.type == pygame.QUIT:
				sys.exit()
			#if event.type == KEYUP:
			#	pass
			elif event.type == KEYDOWN:
				pass
				'''
				gamemanager.re_init()
				return 1
				'''
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					game_mode = self.currentInterface().handle_tap(event.pos)
					if game_mode == 0 or game_mode == 1:
						gamemanager.mode = game_mode
						gamemanager.re_init()
						return 1
					else:
						pass
		elif isinstance(self.currentInterface(), DS_Interface_StatScreen):
			self.currentInterface().getStats(GameManager)
			if event.type == pygame.QUIT:
				sys.exit()
			#if event.type == KEYUP:
			#	pass
			elif event.type == KEYDOWN:
				gamemanager.next_level()
				return 1
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					gamemanager.next_level()
					return 1
		elif isinstance(self.currentInterface(), DS_Interface_GameOverScreen):
			self.currentInterface().getStats(GameManager)
			if event.type == pygame.QUIT:
				sys.exit()
			#if event.type == KEYUP:
			#	pass
			elif event.type == KEYDOWN:
				#gamemanager.re_init()
				self.setInterface(0)
				return 0
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					#gamemanager.re_init()
					self.setInterface(0)
					return 0
		elif isinstance(self.currentInterface(), DS_Interface_GameWonScreen):
			self.currentInterface().getStats(GameManager)
			if event.type == pygame.QUIT:
				sys.exit()
			#if event.type == KEYUP:
			#	pass
			elif event.type == KEYDOWN:
				self.setInterface(0)
				return 0
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					self.setInterface(0)
					return 0
		# Can return -1 also
		return
		#screen.fill(black)
		#self.draw()
		
# Create and Initialize Menu
Menu = DS_Menu()
Menu.init()

class DS_Stream():
	def __init__(self, pos, orientation):
		self.stream = []
		self.pos = pos					# Center position of first tile
		self.orientation = orientation 	# Can be left, up, right, down
		
	def __getitem__(self, index):
		return self.stream[index]
		
	def __setitem__(self, index, value):
		self.stream[index] = value
		
	def __len__(self):
		return len(self.stream)
		
	def append(self, tile):
		self.stream.append(tile)
		self.stream[-1].rect.center = self.get_index_pos(len(self.stream) - 1)
		
	def insert(self, index, value):
		self.stream.insert(index, value)
		
	def set_position(self, pos):
		self.pos = pos
		
	def set_orientation(self, orientation):
		self.orientation = orientation
		
	def get_index_pos(self, index):
		if self.orientation == 0: 	# Left
			return [self.pos[0] - index * tile_size, self.pos[1]]
		if self.orientation == 1:	# Up
			return [self.pos[0], self.pos[1] - index * tile_size]
		if self.orientation == 2:	# Right
			return [self.pos[0] + index * tile_size, self.pos[1]]
		if self.orientation == 3:	# Down
			return [self.pos[0], self.pos[1] + index * tile_size]
			
	def add_tile(self, index, tile):
		self.stream.insert(index, tile)
		tile.rect.center = self.get_index_pos(index)
		
	def set_positions(self):
		for i in range(len(self.stream)):
			self.stream[i].rect.center = self.get_index_pos(i)
		
	def update_positions(self):
		for i in range(len(self.stream)):
			self.stream[i].add_keyframe(self.get_index_pos(i))
			#self.stream[i].set_keyframe(0, self.get_index_pos(i))
			
class DS_StreamIndexPair():
	def __init__(self, stream, index):
		self.stream = stream
		self.index = index
		
	def tile(self):
		return self.stream[self.index]

# Game Manager class - handles game state
class DS_GameManager:
	mode = 0 	# Story mode, or Endless mode
	
	player = DS_Player()
	
	weapons = []
	equipped_weapon = None
	
	skills = []
	items = []
	
	stream_size = 12
	
	left_stream = DS_Stream([tile_size + tile_size/2, tile_size * 5 + tile_size/2], 0)
	right_stream = DS_Stream([tile_size * 3 + tile_size/2, tile_size * 5 + tile_size/2], 2)
	
	vert_center_stream = DS_Stream([tile_size * 2 + tile_size/2, tile_size * 4 + tile_size/2], 1)
	
	vert_left_stream = DS_Stream([tile_size * 1 + tile_size/2, tile_size * 4 + tile_size/2], 1)
	left_stream_changed = False
	
	vert_right_stream = DS_Stream([tile_size * 3 + tile_size/2, tile_size * 4 + tile_size/2], 1)
	right_stream_changed = False
	
	active_action = None
	action_targets = []
	
	selected_tile = None
	
	center_enemies_killed = []
	
	stat_enemies_killed = []
	stat_items_used = []
	stat_weapons_gotten = []
	
	active_game = True
	
	exit_inplay = False
	
	# reset in init_game(
	enemy_quota_base = 1
	enemy_quota = enemy_quota_base
	
	initial_bonus = 100000
	bonus = initial_bonus
	
	score = 0
	level_score = 0
	multiplier = 1
	
	levels_completed = 0
	
	tile_weights = [2, 1, 1, 5, .2] 	# [barrier, item chest, weapon chest, enemy, cross]
	
	weapon_melee_weights = [5, 4, 3, 2, 0.1]
	
	weapon_ranged_weights = [5, 4, 3, 2, 0.1]
	
	weapon_stunner_weights = [5, 4, 3, 0.2]
	
	spell_level_weights = [5, 4, 3, 1, 0.5]
	
	level_enemy_weights = []
	
	level_1_weights = [[2, DS_Enemy_Slime1], [2, DS_Enemy_Slime2], [4, DS_Enemy_Spider1], [3, DS_Enemy_Spider2], [1, DS_Enemy_Jelly1], [3, DS_Enemy_Snake1], [2, DS_Enemy_Snake2], [1, DS_Enemy_Wolf1], [1, DS_Enemy_Crab1]]
	
	level_2_weights = [[2, DS_Enemy_Spider1], [3, DS_Enemy_Spider2], [2, DS_Enemy_Spider3], [4, DS_Enemy_Slime1], [3, DS_Enemy_Slime2], [2, DS_Enemy_Jelly1], [2, DS_Enemy_Jelly2], [3, DS_Enemy_Snake1], [2, DS_Enemy_Snake2], [2, DS_Enemy_Snake3], [2, DS_Enemy_Wolf1], [1, DS_Enemy_Wolf2], [2, DS_Enemy_Crab1], [1, DS_Enemy_Crab2], [2, DS_Enemy_Orc1]]
	
	level_3_weights = [[2, DS_Enemy_Slime1], [3, DS_Enemy_Slime2], [2, DS_Enemy_Slime3], [4, DS_Enemy_Jelly1], [3, DS_Enemy_Jelly2], [2, DS_Enemy_Jelly3], [2, DS_Enemy_Wolf1], [3, DS_Enemy_Wolf2], [2, DS_Enemy_Wolf3], [2, DS_Enemy_Crab2], [2, DS_Enemy_Orc1], [0.5, DS_Enemy_Stalker1], [0.5, DS_Enemy_Horror1]]
	
	level_4_weights = [[2, DS_Enemy_Slime2], [3, DS_Enemy_Slime3], [3, DS_Enemy_Jelly2], [2, DS_Enemy_Jelly3], [3, DS_Enemy_Wolf1], [2, DS_Enemy_Wolf2], [2, DS_Enemy_Orc1], [1, DS_Enemy_Orc2], [0.5, DS_Enemy_Stalker1], [0.25, DS_Enemy_Stalker2], [0.5, DS_Enemy_Horror1], [1, DS_Enemy_Undead1], [0.5, DS_Enemy_Undead2]]
	
	level_5_weights = [[3, DS_Enemy_Slime3], [3, DS_Enemy_Jelly3], [3, DS_Enemy_Orc1], [3, DS_Enemy_Orc2], [2, DS_Enemy_Orc3], [0.5, DS_Enemy_Stalker1], [0.5, DS_Enemy_Stalker2], [0.25, DS_Enemy_Stalker3], [0.5, DS_Enemy_Horror1], [0.5, DS_Enemy_Horror2], [3, DS_Enemy_Undead1], [2, DS_Enemy_Undead2], [1, DS_Enemy_Undead3], [1, DS_Enemy_Demon1]]
	
	level_6_weights = [[3, DS_Enemy_Orc2], [3, DS_Enemy_Orc3], [0.5, DS_Enemy_Stalker1], [0.5, DS_Enemy_Stalker2], [0.25, DS_Enemy_Stalker3], [0.5, DS_Enemy_Horror1], [0.5, DS_Enemy_Horror2], [0.25, DS_Enemy_Horror3], [3, DS_Enemy_Undead1], [2, DS_Enemy_Undead2], [2, DS_Enemy_Undead3], [2, DS_Enemy_Demon1], [1, DS_Enemy_Demon2]]
	
	level_7_weights = [[3, DS_Enemy_Orc3], [1, DS_Enemy_Stalker2], [0.5, DS_Enemy_Stalker3], [1, DS_Enemy_Horror2], [0.5, DS_Enemy_Horror3], [3, DS_Enemy_Undead1], [3, DS_Enemy_Undead2], [3, DS_Enemy_Undead3], [3, DS_Enemy_Demon1], [2, DS_Enemy_Demon2], [1, DS_Enemy_Demon3]]
	
	level_8_weights = [[1, DS_Enemy_Stalker3], [1, DS_Enemy_Stalker3], [3, DS_Enemy_Undead1], [3, DS_Enemy_Undead2], [3, DS_Enemy_Undead3], [3, DS_Enemy_Demon1], [3, DS_Enemy_Demon2], [3, DS_Enemy_Demon3]]
	
	level_enemy_weights.append(level_1_weights)
	level_enemy_weights.append(level_2_weights)
	level_enemy_weights.append(level_3_weights)
	level_enemy_weights.append(level_4_weights)
	level_enemy_weights.append(level_5_weights)
	level_enemy_weights.append(level_6_weights)
	level_enemy_weights.append(level_7_weights)
	level_enemy_weights.append(level_8_weights)
	
	endless_enemy_weights = [[2, DS_Enemy_Slime1], [2, DS_Enemy_Slime2]]
	
	def __init__(self):
		self.all_streams = []
		self.all_streams.append(self.left_stream)
		self.all_streams.append(self.vert_left_stream)
		self.all_streams.append(self.vert_center_stream)
		self.all_streams.append(self.vert_right_stream)
		self.all_streams.append(self.right_stream)
		
	def playing_animations(self):
		for stream in self.all_streams:
			for item in stream:
				if item.playing_animation:
					return True
		return False
		
	def current_level(self):
		return self.levels_completed + 1
	
	def start(self):
		self.active_game = True
	
	def stop(self):
		self.active_game = False
	
	def active(self):
		return self.active_game
	
	def get_score(self):
		return self.score
		
	def init(self):
		self.end_game()
		self.init_game()
	
	# Initialize game state
	def init_game(self):
		
		self.end_level()
		
		self.init_level()
		
		# Set initial skills
		self.skills.append(DS_Skill_Defend())
		self.skills.append(DS_Skill_DivineShield())
		
		# Set initial weapons - should be empty on regular game start
		self.weapons.append(DS_Weapon_Melee(0, self.player))
		#self.weapons.append(DS_Weapon_Ranged(0, self.player))
		#self.weapons.append(DS_Weapon_Stunner(1, self.player))
		
		self.equipped_weapon = self.weapons[0]
		
		# Set initial items - should be empty on regular game start
		#self.items.append(DS_Spell_Heal(0))
		#self.items.append(DS_Spell_Petrify(0))
		#self.items.append(DS_Spell_Fireball(0))
		#self.items.append(DS_Spell_MagicMissile(2))
		#self.items.append(DS_Spell_ForceBlast(0))
		
		# Set player position
		self.player.rect.center = [tile_size * 2 + tile_size/2, tile_size * 5 + tile_size/2] 
		
		# Set positions
		self.update()
		
		self.reset_enemy_quota()
		
		self.active_game = True
		
	def init_level(self):
		# Fill Streams with enemies/items - should be randomized by calling a method
		self.fill_streams()
		
		self.set_positions()
		
		self.level_score = 0
		
		self.start()
		
	def re_init(self):
		self.levels_completed = 0
		
		self.init()
		
		self.reset_bonus()
		
		self.reset_multiplier()
		
		self.score = 0

		self.clear_stats()
		
	def reset_bonus(self):
		self.bonus = self.initial_bonus
		
	def reset_enemy_quota(self):
		self.enemy_quota = self.enemy_quota_base
		
	def end_game(self):
		# End level
		self.end_level()
		
		# Reset player
		self.player.reset()
		
		# Clear inventory
		self.clear_inventory()
		self.clear_equipped_weapon()
		
	def clean_sweep(self):
		for tile in self.vert_center_stream:
			if isinstance(tile, DS_Enemy):
				return False
		for tile in self.vert_right_stream:
			if isinstance(tile, DS_Enemy):
				return False
		for tile in self.vert_left_stream:
			if isinstance(tile, DS_Enemy):
				return False
		for tile in self.right_stream:
			if isinstance(tile, DS_Enemy):
				return False
		for tile in self.left_stream:
			if isinstance(tile, DS_Enemy):
				return False
		return True
		
	def exit_level(self):
		# Check for Clean Sweep Bonus
		if self.clean_sweep():
			self.score += self.bonus
			self.bonus *= 2
		# Stop level (go to menu)
		if self.mode == 0 and self.current_level() == 8:
			Menu.setInterface(3)
		self.stop()
		
	def end_level(self):
		# Clear game state
		self.clear_streams()
		
		self.clear_actions()
		
		self.clear_selected_tile()
		
		self.active_game = False
		
		self.exit_inplay = False
		
		self.reset_center_enemies_killed()
		
	def next_level(self):
		self.levels_completed += 1
		if self.mode == 1:
			self.enemy_quota += 5
		self.end_level()
		self.init_level()
		
	def reset_multiplier(self):
		self.multiplier = 1
	
	def reset_center_enemies_killed(self):
		del self.center_enemies_killed[:]
	
	# Add to inventory
	def add_item(self, item):
		self.items.insert(0, item)
		if len(self.items) > 3:
			self.items.pop()
	
	# Add a weapon
	def add_weapon(self, weapon):
		self.weapons.insert(0, weapon)
		
		if isinstance(self.equipped_weapon, DS_Weapon_Fist):
			self.equipped_weapon = self.weapons[0]
		
		if len(self.weapons) > 3:
			self.equipped_weapon = self.weapons[2]
			self.weapons.pop()
		'''
		if weapon.get_type() == 0:
			if self.weapons[0].level <= weapon.level or self.weapons[0].broken():
				self.weapons[0] = weapon
				# Need to equip new weapon to prevent issue with broken weapon being kept equipped
				self.equipped_weapon = self.weapons[0]
		elif weapon.get_type() == 1:
			if self.weapons[1].level <= weapon.level or self.weapons[1].broken():
				self.weapons[1] = weapon
		elif weapon.get_type() == 2:
			if self.weapons[2].level <= weapon.level or self.weapons[2].broken():
				self.weapons[2] = weapon
		'''

	# Add to tile stream - randomized
	def add_to_stream(self, stream, mode):	
		# Modes: Fully Random, Random with no barriers, Fixed
		if mode == 0 or mode == 1:
			i = random.randint(0, 10)
			# Randomized add to stream
			if i == 0 or i == 1:
				stream.append(DS_Enemy_RedSlime()) # Placeholder for test
			elif i == 2:
				stream.append(EnemyManager.getJelly())
			elif i == 3:
				stream.append(EnemyManager.getOrc()) # Placeholder for test
			elif i == 4:
				j = random.randint(0, 2)
				if j == 0:
					stream.append(EnemyManager.getGreenHorror())
			elif i == 5:
				j = random.randint(0, 5)
				if j == 0:
					stream.append(EnemyManager.getMindflayer())
			elif i == 7:
				if mode == 0:
					stream.append(BarrierManager.getColumn())
				elif mode == 1:
					stream.append(EnemyManager.getJelly())
			elif i == 8:
				j = random.randint(0, 5)
				if j == 0:
					stream.append(PickupManager.getCross())
			elif i == 9:
				j = random.randint(0, 1)
				if j == 0:
					stream.append(PickupManager.getItemChest())
				elif j == 1: 
					stream.append(PickupManager.getWeaponChest())
		elif mode == 2:
			stream.append(DS_Enemy_RedSlime())
			
	def get_weighted_selection(self, weight_list):
		totals = []
		running_total = 0
		
		for weight in weight_list:
			running_total += weight
			totals.append(running_total)
			
		rnd = random.random() * running_total
		for i, total in enumerate(totals):
			if rnd < total:
				return i
				
	def get_random_weapon_melee(self):
		chosen_tile = self.get_weighted_selection(self.weapon_melee_weights)
		return DS_Weapon_Melee(chosen_tile, self.player)
	def get_random_weapon_ranged(self):
		chosen_tile = self.get_weighted_selection(self.weapon_ranged_weights)
		return DS_Weapon_Ranged(chosen_tile, self.player)	
	def get_random_weapon_stunner(self):
		chosen_tile = self.get_weighted_selection(self.weapon_stunner_weights)
		return DS_Weapon_Stunner(chosen_tile, self.player)
		
	def get_random_tile_endless(self):
		chosen_tile = self.get_weighted_selection(self.tile_weights)
		
		if chosen_tile == 0:
			return DS_Barrier_Column()
		elif chosen_tile == 1:
			return DS_Pickup_ItemChest()
		elif chosen_tile == 2:
			return DS_Pickup_WeaponChest()
		elif chosen_tile == 3:
			return self.get_random_enemy_endless()
		elif chosen_tile == 4:
			return DS_Pickup_Cross()
				
	def get_random_tile_story(self):
		chosen_tile = self.get_weighted_selection(self.tile_weights)
		
		if chosen_tile == 0:
			return DS_Barrier_Column()
		elif chosen_tile == 1:
			return DS_Pickup_ItemChest()
		elif chosen_tile == 2:
			return DS_Pickup_WeaponChest()
		elif chosen_tile == 3:
			return self.get_random_enemy_story()
		elif chosen_tile == 4:
			return DS_Pickup_Cross()
			
	def get_random_enemy_endless(self):
		enemy_weights = [val[0] for val in self.endless_enemy_weights]
		chosen_tile = self.get_weighted_selection(enemy_weights)
		
		return self.endless_enemy_weights[chosen_tile][1]()
			
	def get_random_enemy_story(self):
		enemy_weights = [val[0] for val in self.level_enemy_weights[self.levels_completed]]
		chosen_tile = self.get_weighted_selection(enemy_weights)
		
		return self.level_enemy_weights[self.levels_completed][chosen_tile][1]()
		
	def add_to_stream_endless(self, stream):
		stream.append(self.get_random_tile_endless())
			
	def add_to_stream_story(self, stream):
		stream.append(self.get_random_tile_story())
			
	def add_tile(self, stream, tile):
		stream.append(tile)
		
	def insert_tile(self, stream, tile, index):
		stream.insert(index, tile)
			
	def add_exit_sequence_endless(self):
		self.vert_center_stream.append(DS_Boss_Troll())
		self.vert_center_stream.append(DS_Location_Exit())
		self.vert_center_stream.append(DS_Barrier_Column())
		
		self.vert_right_stream.append(DS_Pickup_ItemChest())
		self.vert_right_stream.append(DS_Barrier_Column())
		self.vert_right_stream.append(DS_Barrier_Column())
		
		self.vert_left_stream.append(DS_Pickup_WeaponChest())
		self.vert_left_stream.append(DS_Barrier_Column())
		self.vert_left_stream.append(DS_Barrier_Column())
		
		self.exit_inplay = True
	
	def add_exit_sequence_story(self):
		if self.current_level() == 1:
			self.vert_center_stream.append(DS_Boss_Troll())
		elif self.current_level() == 2:
			self.vert_center_stream.append(DS_Boss_Beholder())
		elif self.current_level() == 3:
			self.vert_center_stream.append(DS_Boss_Mindflayer())
		elif self.current_level() == 4:
			self.vert_center_stream.append(DS_Boss_GreenDragon())
		elif self.current_level() == 5:
			self.vert_center_stream.append(DS_Boss_TowerKnight())
		elif self.current_level() == 6:
			self.vert_center_stream.append(DS_Boss_DeathKnight())
		elif self.current_level() == 7:
			self.vert_center_stream.append(DS_Boss_DreadKnight())
		elif self.current_level() == 8:
			self.vert_center_stream.append(DS_Boss_Necromancer())
			
		self.vert_center_stream.append(DS_Location_Exit())
		self.vert_center_stream.append(DS_Barrier_Column())
		
		self.vert_right_stream.append(DS_Pickup_ItemChest())
		self.vert_right_stream.append(DS_Barrier_Column())
		self.vert_right_stream.append(DS_Barrier_Column())
		
		self.vert_left_stream.append(DS_Pickup_WeaponChest())
		self.vert_left_stream.append(DS_Barrier_Column())
		self.vert_left_stream.append(DS_Barrier_Column())
		
		self.exit_inplay = True
	
	# Fill tile streams - while tile stream has less than 6 elements
	def fill_stream_random(self, stream):
		while len(stream) < self.stream_size:
			self.add_to_stream(stream, 0)
			
	def fill_stream_random_nobarriers(self, stream):
		while len(stream) < self.stream_size:
			self.add_to_stream(stream, 1)
			
	def fill_stream_fixedbarriers(self, stream):
		while len(stream) < self.stream_size:
			self.add_tile(stream, BarrierManager.getFixedColumn())
			
	def fill_stream_barriers(self, stream):
		while len(stream) < self.stream_size:
			self.add_tile(stream, BarrierManager.getColumn())
			
	def fill_stream_story(self, stream):
		if self.current_level() >= 0 and self.current_level() < 9:
			while len(stream) < self.stream_size:
				self.add_to_stream_story(stream)
			return True
		else:
			return False
			
	def fill_stream_endless(self, stream):
		while len(stream) < self.stream_size:
			self.add_to_stream_endless(stream)
		return True
	
	# Fill all tile streams
	def fill_streams(self):
		if self.mode == 0: 		# story mode
			if self.exit_inplay:
				self.fill_stream_barriers(self.vert_center_stream)
				self.fill_stream_barriers(self.vert_left_stream)
				self.fill_stream_barriers(self.vert_right_stream)
			else:
				self.fill_stream_story(self.vert_center_stream)
				self.fill_stream_story(self.vert_left_stream)
				self.fill_stream_story(self.vert_right_stream)
				
			self.fill_stream_story(self.left_stream)
			self.fill_stream_story(self.right_stream)
			
		elif self.mode == 1:		# endless mode
			self.fill_stream_endless(self.vert_center_stream)
			self.fill_stream_endless(self.vert_left_stream)
			self.fill_stream_endless(self.vert_right_stream)
			self.fill_stream_endless(self.left_stream)
			self.fill_stream_endless(self.right_stream)
		
	def fill_streams_fixedbarriers(self):
		self.fill_stream_fixedbarriers(self.vert_center_stream)
		self.fill_stream_fixedbarriers(self.vert_left_stream)
		self.fill_stream_fixedbarriers(self.vert_right_stream)
		self.fill_stream_fixedbarriers(self.left_stream)
		self.fill_stream_fixedbarriers(self.right_stream)
		
	def fill_streams_barriers(self):
		self.fill_stream_barriers(self.vert_center_stream)
		self.fill_stream_barriers(self.vert_left_stream)
		self.fill_stream_barriers(self.vert_right_stream)
		self.fill_stream_barriers(self.left_stream)
		self.fill_stream_barriers(self.right_stream)
		
	# Update a list, checking for deaths and removing tiles
	# Returns list of descriptions of removed tiles
	def update_list(self, list):
		killed = []
		for tile in list:
			if isinstance(tile, DS_Enemy) and tile.killed():
				self.score += tile.points_worth() * self.multiplier
				self.level_score += tile.points_worth() * self.multiplier
				killed.append(tile.get_description())
				self.multiplier += 1
		list[:] = [tile for tile in list if not tile.gone()]
		return killed
		
	# Update stream conditions using update_list() - DO NOT USE ON CENTER STREAM
	def update_stream_random(self, stream):
		killed = self.update_list(stream)
		# Add list of killed enemies to stat
		self.stat_enemies_killed += killed
		
		#self.fill_stream_random(stream)
		return killed
		
	def update_stream_random_nobarriers(self, stream):
		killed = self.update_list(stream)
		# Add list of killed enemies to stat
		self.stat_enemies_killed += killed
		
		#self.fill_stream_random_nobarriers(stream)
		return killed
		
	# Special update of center (main) stream
	def update_main_stream(self):
		if self.vert_center_stream[0].gone():
			self.drop_tiles()
		self.center_enemies_killed += self.update_stream_random(self.vert_center_stream)
	
			
	def enemy_quota_met(self):
		if len(self.center_enemies_killed) >= self.enemy_quota:
			return True
		else:
			return False
		
		
	# Drop side tiles when first center tile is destroyed
	def drop_tiles(self):
		# Check if first vert left stream element and first left stream element are both barriers
		if isinstance(self.left_stream[0], DS_Barrier): 
			if isinstance(self.vert_left_stream[0], DS_Barrier):
				# If true, merge first left barrier with first vert left barrier
				self.left_stream[0].merge(self.vert_left_stream[0])
			else: 
				self.left_stream.insert(1, type(self.vert_left_stream[0])())
				self.left_stream[1].rect.center = [tile_size + tile_size/2, tile_size * 4 + tile_size/2]
				
				self.left_stream[1].add_keyframe([0 + tile_size/2, tile_size * 4 + tile_size/2])
				
				self.left_stream[1].replace(self.vert_left_stream[0])
		
		else:
			# Else drop to left of player
			self.left_stream.insert(0, type(self.vert_left_stream[0])())
			self.left_stream[0].rect.center = [tile_size + tile_size/2, tile_size * 4 + tile_size/2]
			self.left_stream[0].replace(self.vert_left_stream[0])
		
		# Do the same for vert right/right streams
		if isinstance(self.right_stream[0], DS_Barrier):
			if isinstance(self.vert_right_stream[0], DS_Barrier):
				# If true, merge first right barrier with first vert right barrier
				self.right_stream[0].merge(self.vert_right_stream[0])
			else: 
				self.right_stream.insert(1, type(self.vert_right_stream[0])())
				self.right_stream[1].rect.center = [tile_size * 3 + tile_size/2, tile_size * 4 + tile_size/2]
				
				self.right_stream[1].add_keyframe([tile_size * 4 + tile_size/2, tile_size * 4 + tile_size/2])
				
				self.right_stream[1].replace(self.vert_right_stream[0])
		
		else:
			# Else drop to right of player
			self.right_stream.insert(0, type(self.vert_right_stream[0])())
			self.right_stream[0].rect.center = [tile_size * 3 + tile_size/2, tile_size * 4 + tile_size/2]
			self.right_stream[0].replace(self.vert_right_stream[0])
	
	# Update all streams
	def update(self):
		# Update all lists - remove "gone" tiles
		self.update_main_stream()
		self.vert_left_stream_changed = self.update_stream_random(self.vert_left_stream)
		self.vert_right_stream_changed = self.update_stream_random(self.vert_right_stream)
		self.update_stream_random_nobarriers(self.left_stream)
		self.update_stream_random_nobarriers(self.right_stream)
		
		if self.mode == 0:
			if self.enemy_quota_met():
				if not self.exit_inplay:
					self.add_exit_sequence_story()
				else:
					self.fill_streams()
			elif not self.enemy_quota_met():
				self.fill_streams()
		
		elif self.mode == 1: 	#endless mode
			# Refill streams if enemy quota is not met
			if self.enemy_quota_met():
				if not self.exit_inplay:
					self.add_exit_sequence_endless()
				else:
					self.fill_streams_barriers()
			elif not self.enemy_quota_met():
				self.fill_streams()
		
		self.update_list(self.weapons)
		
		while len(self.weapons) < 3:
			self.weapons.append(DS_Weapon_Fist(self.player))
			
		if self.equipped_weapon.deleted:
			available_weapons = len(self.weapons)
			if available_weapons > 0 and available_weapons <= 3:
				self.equipped_weapon = self.weapons[available_weapons - 1]
			else:
				self.equipped_weapon = None		# Change this to DS_Weapon_Fist?
		self.update_list(self.skills)
		self.update_list(self.items)
		
		self.update_positions()
		
	# SET tile positions, no animation, used during initialization
	def set_positions(self):
		self.set_gametile_positions()
		self.set_menuitem_positions()
		
	def set_gametile_positions(self):
		self.vert_center_stream.set_positions()
		self.vert_left_stream.set_positions()
		self.vert_right_stream.set_positions()
		self.left_stream.set_positions()
		self.right_stream.set_positions()
		
	def set_menuitem_positions(self):
		# Update skills positions
		for i in range(len(self.skills)):
			self.skills[i].rect.center = [tile_size * 2 + tile_size/2, tile_size * 6 + tile_size * i + tile_size/2]
		
		# Update items positions
		for i in range(len(self.items)):
			if i == 0 or i == 1:
				self.items[i].rect.center = [tile_size * 3 + tile_size * i + tile_size/2, tile_size * 6 + tile_size/2]
			elif i == 2:
				self.items[i].rect.center = [tile_size * 3 + tile_size/2, tile_size * 7 + tile_size/2]
				
		# Update weapons positions
		for i in range(len(self.weapons)):
			if i == 0 or i == 1:
				self.weapons[i].rect.center = [tile_size * 1 - tile_size * i + tile_size/2, tile_size * 6 + tile_size/2]
			elif i == 2:
				self.weapons[i].rect.center = [tile_size * 1 + tile_size/2, tile_size * 7 + tile_size/2]
		
	# UPDATE tile positions - with animation, used during gameplay
	def update_positions(self):
		self.update_gametile_positions()
		self.update_menuitem_positions()
	
	# Update game tile positions
	def update_gametile_positions(self):
		self.vert_center_stream.update_positions()
		self.vert_left_stream.update_positions()
		self.vert_right_stream.update_positions()
		self.left_stream.update_positions()
		self.right_stream.update_positions()

	def update_menuitem_positions(self):
		# Update skills positions
		for i in range(len(self.skills)):
			self.skills[i].rect.topleft = [tile_size * 2, tile_size * 6 + tile_size * i]
		
		# Update items positions
		for i in range(len(self.items)):
			if i == 0 or i == 1:
				self.items[i].rect.topleft = [tile_size * 3 + tile_size * i, tile_size * 6]
			elif i == 2:
				self.items[i].rect.topleft = [tile_size * 3, tile_size * 7]
				
		# Update weapons positions
		for i in range(len(self.weapons)):
			if i == 0 or i == 1:
				self.weapons[i].rect.topleft = [tile_size * 1 - tile_size * i, tile_size * 6]
			elif i == 2:
				self.weapons[i].rect.topleft = [tile_size * 1, tile_size * 7]
		
	
	# Clear actions
	def clear_actions(self):
		self.active_action = None
		del self.action_targets[:]
		
	def clear_selected_tile(self):
		self.selected_tile = None
		
	def clear_equipped_weapon(self):
		self.equipped_weapon = None
	
	def clear_stats(self):
		del self.stat_enemies_killed[:]
		del self.stat_items_used[:]
		del self.stat_weapons_gotten[:]
		
		del self.center_enemies_killed[:]
	
	# Clear inventory
	def clear_inventory(self):
		del self.weapons[:]
		del self.skills[:]
		del self.items[:]
	
	# Clear tile streams
	def clear_streams(self):
		del self.left_stream.stream[:]
		del self.right_stream.stream[:]
		del self.vert_center_stream.stream[:]
		del self.vert_left_stream.stream[:]
		del self.vert_right_stream.stream[:]
		
	# Aggro enemy if in range
	def enemy_aggro(self):
		if isinstance(self.left_stream[0], DS_Enemy):
			self.left_stream[0].react(self.player)
		if isinstance(self.right_stream[0], DS_Enemy):
			self.right_stream[0].react(self.player)
		if isinstance(self.vert_center_stream[0], DS_Enemy):
			self.vert_center_stream[0].react(self.player)
			
		# Aggro left/right vert streams immediately when in range
		if isinstance(self.vert_left_stream[0], DS_Enemy):
				self.vert_left_stream[0].react(self.player)
		if isinstance(self.vert_right_stream[0], DS_Enemy):
				self.vert_right_stream[0].react(self.player)

	# De-Aggro enemy if out of range
	def enemy_deaggro(self):
		pass
		'''
		for tile in self.left_stream[3:]:
			if isinstance(tile, DS_Enemy):
				tile.set_neutral()
		for tile in self.right_stream[3:]:
			if isinstance(tile, DS_Enemy):
				tile.set_neutral()
		'''
	
	# Check stream for stunned enemies, set them back to neutral
	def reset_stun(self, stream):
		for tile in stream:
			if isinstance(tile, DS_Enemy) and tile.is_stun():
				tile.stun_recover()
				
	# Reset stunned enemies in all streams
	def reset_stun_allstreams(self):
		self.reset_stun(self.vert_center_stream)
		self.reset_stun(self.vert_right_stream)
		self.reset_stun(self.vert_left_stream)
		self.reset_stun(self.right_stream)
		self.reset_stun(self.left_stream)
		
	# Enemy takes turn
	def enemy_turn(self):
		# Check if first tile in left stream is Enemy
		if isinstance(self.left_stream[0], DS_Enemy):
			# If Enemy is aggro:
			if self.left_stream[0].is_aggro():
				# Attack
				#self.left_stream[0].juke_right()
				self.left_stream[0].attack(self.player)
				
		# Else if Tile on left is barrier
		'''
		elif isinstance(self.left_stream[0], DS_Barrier):
			# If next tile on left is Enemy and Enemy is aggro:
			if isinstance(self.left_stream[1], DS_Enemy) and self.left_stream[1].is_aggro():
				self.left_stream[1].attack(self.left_stream[0])
		'''
		
		# Check if first tile in right stream is Enemy
		if isinstance(self.right_stream[0], DS_Enemy):
			# If Enemy is aggro:
			if self.right_stream[0].is_aggro():
				# Attack
				#self.right_stream[0].juke_left()
				self.right_stream[0].attack(self.player)
		# If first in right stream is Barrier:
		'''
		elif isinstance(self.right_stream[0], DS_Barrier):
			if isinstance(self.right_stream[1], DS_Enemy) and self.right_stream[1].is_aggro():
				self.right_stream[1].attack(self.right_stream[0])
		'''
				
		# Enemy above attacks player or barrier directly next to player (if aggro)
		if isinstance(self.vert_center_stream[0], DS_Enemy):
			# If Enemy is aggro:
			if self.vert_center_stream[0].is_aggro():
				# Attack
				#self.vert_center_stream[0].juke_down()
				self.vert_center_stream[0].attack(self.player)
				
		# If first in right stream is Barrier:
		'''
		elif isinstance(self.vert_center_stream[0], DS_Barrier):
			if isinstance(self.vert_center_stream[1], DS_Enemy) and self.vert_center_stream[1].is_aggro():
				self.vert_center_stream[1].attack(self.vert_center_stream[0])
		'''
		
		for i in range(len(self.vert_center_stream)):
			if i > 0 and isinstance(self.vert_center_stream[i], DS_Enemy) and self.vert_center_stream[i].is_aggro():
				if not isinstance(self.vert_center_stream[i-1], DS_Enemy):
					self.vert_center_stream[i].attack(self.vert_center_stream[i-1])
					
		for i in range(len(self.vert_left_stream)):
			if i > 0 and isinstance(self.vert_left_stream[i], DS_Enemy) and self.vert_left_stream[i].is_aggro():
				if not isinstance(self.vert_left_stream[i-1], DS_Enemy):
					self.vert_left_stream[i].attack(self.vert_left_stream[i-1])
					
		for i in range(len(self.vert_right_stream)):
			if i > 0 and isinstance(self.vert_right_stream[i], DS_Enemy) and self.vert_right_stream[i].is_aggro():
				if not isinstance(self.vert_right_stream[i-1], DS_Enemy):
					self.vert_right_stream[i].attack(self.vert_right_stream[i-1])
					
		for i in range(len(self.left_stream)):
			if i > 0 and isinstance(self.left_stream[i], DS_Enemy) and self.left_stream[i].is_aggro():
				if not isinstance(self.left_stream[i-1], DS_Enemy):
					self.left_stream[i].attack(self.left_stream[i-1])
					
		for i in range(len(self.right_stream)):
			if i > 0 and isinstance(self.right_stream[i], DS_Enemy) and self.right_stream[i].is_aggro():
				if not isinstance(self.right_stream[i-1], DS_Enemy):
					self.right_stream[i].attack(self.right_stream[i-1])
				
		# Check if enemy in range
		# If enemy in range, aggro it
		self.enemy_aggro()
		
		self.enemy_deaggro()
		
	def recharge_skills(self):
		for skill in self.skills:
			skill.recharge()
		
	# End your turn	
	def end_turn(self):
		# Clear active actions and targets/selections
		self.clear_actions()
		
		self.clear_selected_tile()
		
		# Update streams to remove dead tiles
		self.update()
		
		current_time = pygame.time.get_ticks()
		
		while (self.playing_animations() or pygame.time.get_ticks() < current_time + 100):
			fps_limited_draw([self, AnimManager])

		# Enemy takes turn
		self.enemy_turn()
		
		# Check if HP is less than zero
		if self.player.get_health() <= 0:
			self.stop()
			Menu.setInterface(2)
		
		# Update again to remove barriers destroyed during enemy turn
		self.update()
		
		current_time = pygame.time.get_ticks()
		
		while (self.playing_animations() or pygame.time.get_ticks() < current_time + 100):
			fps_limited_draw([self, AnimManager])
		
		# Set player back to neutral state
		self.player.set_neutral()
		
		# Recharge skills
		self.recharge_skills()
		
		# Reset stunned enemies back to neutral
		self.reset_stun_allstreams()
		
		# Uncomment this line to see stats and cause crashes in pythonw :(
		#print self.stat_enemies_killed
	
	
	# Draw all game elements
	def draw(self):
		# Draw player
		self.player.draw()
		self.player.update()
		self.player.play_animation()
		
		# Draw weapons
		for weapon in self.weapons:
			weapon.draw()
		
		# Draw skills
		for skill in self.skills:
			# replace with tile's own draw()
			skill.draw()
		
		# Draw items
		for item in self.items:
			item.draw()
		
		# Draw streams
		for tile in self.vert_center_stream:
			tile.draw()
			tile.update()
			tile.play_animation()
		for tile in self.left_stream:
			tile.draw()
			tile.update()
			tile.play_animation()
		for tile in self.right_stream:
			tile.draw()
			tile.update()
			tile.play_animation()
		for tile in self.vert_right_stream:
			tile.draw()
			tile.update()
			tile.play_animation()
		for tile in self.vert_left_stream:
			tile.draw()
			tile.update()
			tile.play_animation()

		self.draw_gui()
		
	def draw_health(self):
		for i in range(int(self.player.get_max_health())):
			screen.blit(SurfaceManager.blankheart_surfaces[i % 4], (0, tile_size*(int(i/4))))
			
		for i in range(int(self.player.get_health())):
			screen.blit(SurfaceManager.heart_surfaces[i % 4], (0, tile_size*(int(i/4))))
			
	def draw_gui(self):
		# Draw GUI
		'''
		health_info = myfont.render("HP:" + str(self.player.health) + "/" + str(self.player.max_health), 1, (255,255,0))
		screen.blit(health_info, (10, tile_size * 8))
		'''
		
		# Draw score and level
		score_info = myfont.render("S:" + str(self.score) + " L:" + str(self.levels_completed + 1), 1, (255,255,0))
		screen.blit(score_info, (10, tile_size * visible_rows))
		
		# Draw multiplier
		multiplier_string = "x" + str(self.multiplier)
		multiplier_info = myfont.render(multiplier_string, 1, (255,255,0))
		screen.blit(multiplier_info, (tile_size * 4 + 12 - len(multiplier_string) * 5, 10))
		
		# Draw selection box
		if self.selected_tile != None:
			tile_info = myfont.render(self.selected_tile.get_info(), 1, (255,255,0))
			screen.blit(tile_info, (10, tile_size * (visible_rows + 1)))
			screen.blit(selection_overlay, self.selected_tile.rect)
			
		# Draw selection box around active action
		if self.active_action != None:
			screen.blit(action_select_overlay, self.active_action.rect)
			
		
		if len(self.action_targets) > 0:
			for target in self.action_targets:
				screen.blit(action_select_overlay, target.tile().rect)
		
			
		# Draw "broken" overlay
		for weapon in self.weapons:
			if weapon.broken():
				screen.blit(broken_overlay, weapon.rect)
				
		# Draw "equipped" overlay
		if self.equipped_weapon != None:
			screen.blit(equip_overlay, self.equipped_weapon.rect)
			
		# Draw health hearts
		self.draw_health()
	
	# Add item to item list
	def get_item(self):
		i = random.randint(0, 5)
		chosen_level = self.get_weighted_selection(self.spell_level_weights)
		
		if i == 0:
			self.add_item(DS_Spell_Heal(chosen_level))
		elif i == 1:
			self.add_item(DS_Spell_MagicMissile(chosen_level))
		elif i == 2:
			self.add_item(DS_Spell_Fireball(chosen_level))
		elif i == 3:
			self.add_item(DS_Spell_Drain(chosen_level))
		elif i == 4:
			self.add_item(DS_Spell_Petrify(chosen_level))
		elif i == 5:
			self.add_item(DS_Spell_ForceBlast(chosen_level))
		
	# Add weapon to weapon list
	def get_weapon(self):
		i = random.randint(0, 2)
		if i == 0:
			self.add_weapon(self.get_random_weapon_melee())
		elif i == 1:
			self.add_weapon(self.get_random_weapon_ranged())
		elif i == 2:
			self.add_weapon(self.get_random_weapon_stunner())
			
	def get_cross(self):
		self.skills[1].full_recharge()
				
	# Interact with object via keypress
	def interact(self, target):
		# If target is enemy, attack
		if isinstance(target, DS_Enemy):
			self.attack(target)
			AnimManager.queue.append(DS_Anim_MeleeAttack(target.rect.center))
			self.multiplier += 0.1
			
		# If target is pickup, pick up
		elif isinstance(target, DS_Pickup):
			# If item chest:
			if isinstance(target, DS_Pickup_ItemChest):
				self.get_item()
			
			# If weapon chest:
			if isinstance(target, DS_Pickup_WeaponChest):
				self.get_weapon()
			
			# If cross:
			if isinstance(target, DS_Pickup_Cross):
				self.get_cross()
				
			# Mark pickup for deletion
			target.delete()
			
		# If barrier, remove it:
		elif isinstance(target, DS_Barrier):
			target.delete()
			
		# If target is exit, exit
		elif isinstance(target, DS_Location_Exit):
			self.exit_level()

	# Handle click on item 
	def dual_interact(self, item):
		pass
		
	def attack(self, target):
		self.equipped_weapon.use_on(target)
		#target.take_damage(self.equipped_weapon.power * self.multiplier * 0.1)
		#target.take_damage_from_target(self.equipped_weapon)
		
	# Handle Up keypress
	def handle_key(self, key):
		# Examine and act on first element in vert_center_stream
		# 
		
		# Reset
		if event.key == K_r:
			self.re_init()
			return
		
		if event.key == K_ESCAPE:
			sys.exit()
		elif event.key == K_UP:
			# Attack enemy in 
			self.interact(self.vert_center_stream[0])		# Placeholder - should call a function
		elif event.key == K_LEFT:
			self.interact(self.left_stream[0])		# Placeholder - should call a function
		elif event.key == K_RIGHT:
			self.interact(self.right_stream[0])		# Placeholder - should call a function
		elif event.key == K_p:
			print self.action_targets
			return
		else:
			return
		
		current_time = pygame.time.get_ticks()
		
		while self.playing_animations():
			fps_limited_draw([self, AnimManager])
		
		if self.active():
			self.end_turn()
		
	def handle_tap(self, pos):
		valid_move = False
		valid_click = False
		
		# Check item tiles for clicks
		for item in self.items:
			if item.clicked(pos):
				valid_click = True
				# If defensive item, pass player
				if item.get_type() == 0:
					item.tap(self.player)
					valid_move = True
				# If offensive item, set to active action and clear action targets
				if item.get_type() == 1:
					self.active_action = item
					del self.action_targets[:]
				# If field item, pass player and all streams and activate item
				if item.get_type() == 2:
					item.multi_action(self.player, self.all_streams)
					valid_move = True
		
		# Check skill tiles for clicks
		for skill in self.skills:
			if skill.clicked(pos):
				valid_click = True
				# If defensive skill, pass player
				if skill.get_type() == 0:
					# If successfully used, set valid_move and reset multiplier
					if skill.tap(self.player):
						valid_move = True
						self.reset_multiplier()
				# If offensive skill, set to active action and clear action targets
				if skill.get_type() == 1:
					self.active_action = skill
					del self.action_targets[:]
				# If field skill, pass list of streams
				if skill.get_type() == 2:
					if skill.act_on_streams(self.all_streams):
						valid_move = True
						self.reset_multiplier()
						
		# Check weapon tiles for clicks
		for weapon in self.weapons:
			if weapon.clicked(pos):
				valid_click = True
				self.equipped_weapon = weapon
				self.selected_tile = weapon
				# If melee weapon, equip it
				if not weapon.is_ranged():
					self.active_action = weapon
					del self.action_targets[:]
						#valid_move = True
				# If ranged weapon and not broken, set to active action and clear action targets
				elif weapon.is_ranged() and not weapon.broken():
					self.active_action = weapon
					del self.action_targets[:]
		
		# Check all streams for clicks (outside of action targeting)
		if self.active_action == None:
			for tile in self.left_stream:
				if tile.clicked(pos):
					valid_click = True
					self.selected_tile = tile
			for tile in self.right_stream:
				if tile.clicked(pos):
					valid_click = True
					self.selected_tile = tile
			for tile in self.vert_center_stream:
				if tile.clicked(pos):
					valid_click = True
					self.selected_tile = tile
			for tile in self.vert_left_stream:
				if tile.clicked(pos):
					valid_click = True
					self.selected_tile = tile
			for tile in self.vert_right_stream:
				if tile.clicked(pos):
					valid_click = True
					self.selected_tile = tile
			if self.player.clicked(pos):
				valid_click = True
				self.selected_tile = self.player
			for weapon in self.weapons:
				if weapon.clicked(pos):
					valid_click = True
					self.selected_tile = weapon
		# TODO
				
		# If enough action targets for active action, execute active action and delete it
		elif self.active_action != None:
			# Check streams for clicks, depending on range of active action
			# Range 2:
			if self.active_action.get_range() > 0:
				for i in range(self.active_action.get_range()):
					if self.vert_center_stream[i].clicked(pos):
						valid_click = True
						self.action_targets.append(DS_StreamIndexPair(self.vert_center_stream, i))
					elif self.left_stream[i].clicked(pos):
						valid_click = True
						self.action_targets.append(DS_StreamIndexPair(self.left_stream, i))
					elif self.right_stream[i].clicked(pos):
						valid_click = True
						self.action_targets.append(DS_StreamIndexPair(self.right_stream, i))
					
					if i < self.active_action.get_range() - 1:
						if self.vert_left_stream[i].clicked(pos):
							valid_click = True
							self.action_targets.append(DS_StreamIndexPair(self.vert_left_stream, i))
						elif self.vert_right_stream[i].clicked(pos):
							valid_click = True
							self.action_targets.append(DS_StreamIndexPair(self.vert_right_stream, i))
			
			# If enough action targets selected, perform active action	
			if len(self.action_targets) == self.active_action.get_required_targets():
				self.multiplier += 0.1 * self.active_action.get_required_targets()
				self.active_action.multi_action(self.player, self.action_targets)
				
				valid_move = True
					# If was multitarget skill, reset multiplier
				if isinstance(self.active_action, DS_Skill):
					self.reset_multiplier()
					
		current_time = pygame.time.get_ticks()
		
		while self.playing_animations() or AnimManager.playing_animations():
			fps_limited_draw([self, AnimManager])
		
		if valid_move:
			self.end_turn()
			
		if not valid_click:
			self.clear_actions()
			self.clear_selected_tile()
			
	# Handle actions between player and other tiles
	def player_action(self, target):
		self.handle_action(self.player, target)
			
	# Handle actions between tiles
	def handle_action(self, actor, target):
		pass
		
class DS_AnimManager():
	def __init__(self):
		self.queue = []
		
	def cleanup(self):
		self.queue[:] = [item for item in self.queue if not item.deleted]
		
	def draw(self):
		for item in self.queue:
			item.draw()
			item.update()
		
		self.cleanup()
		
	def playing_animations(self):
		if len(self.queue) > 0:
			return True
		return False

def debug():
	GameManager.player.health = 1000
	GameManager.player.max_health = 1000
	
def fps_limited_draw(items):
	global game_draw_time, global_interval
	
	while (pygame.time.get_ticks() < game_draw_time + global_interval):
		pygame.time.wait(1)
		
	game_draw_time = pygame.time.get_ticks()
	
	# Blank de screen
	screen.fill(grey)
	
	# Draw item
	for item in items:
		item.draw()
	
	# Flippit
	pygame.display.flip()
	
# Create and Initialize Animation Manager
AnimManager = DS_AnimManager()
			
# Create and Initialize Game Manager
GameManager = DS_GameManager()
#GameManager.mode = 1						# Enable Endless Mode
GameManager.init()
GameManager.stop()
	
#debug()

# Main Game loop
while 1:
	# Get Input
	
	#event = pygame.event.wait()			# For turn-based non-animated game loop
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		
		if event.type == MOUSEBUTTONDOWN:
			if event.button == 1:
				pass
				#AnimManager.queue.append(DS_Anim_MeleeAttack(event.pos))
				
		if event.type == KEYDOWN:
			if event.key == K_p:
				print "AnimQueue: " + str(AnimManager.queue)
			
		if GameManager.active():
			if event.type == KEYUP:
				pass
			elif event.type == KEYDOWN:
				GameManager.handle_key(event.key)
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					GameManager.handle_tap(event.pos)
					
		else:
			Menu.setInterface(Menu.loop(GameManager, event))
				
	if GameManager.active():
		fps_limited_draw([GameManager, AnimManager])
	else:
		fps_limited_draw([Menu])
	
