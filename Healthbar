import pygame as pg, sys
pg.font.init()

RED = (255,0,0)
pg.init()
WIDTH = 1080
HEIGHT = 720
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()

bleeding = pg.image.load('bleed.png')
Default_Size = (1080,720)
bleeding = pg.transform.scale(bleeding, Default_Size)
bleed = bleeding.get_rect(center=(WIDTH/2, HEIGHT/2))



textfont = pg.font.Font("alagard.ttf", 100)
subtext = pg.font.Font("alagard.ttf", 35)
text = textfont.render("GAME OVER", True, RED)
text2 = subtext.render("Press Spacebar to restart or Esc to Quit", True, 'WHITE')
text_lower = text.get_rect(center=(500, 500))
text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))

class Player(pg.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pg.Surface((40,40))
		self.image.fill((200,30,30))
		self.rect = self.image.get_rect(center = (WIDTH/2,HEIGHT/2))
		self.current_health = 200
		self.target_health = 1000
		self.max_health = 1000
		self.health_bar_length = 750
		self.health_ratio = self.max_health / self.health_bar_length
		self.health_change_speed = 5

	def get_damage(self,amount):
		if self.target_health > 0:
			self.target_health -= amount
		if self.target_health < 0:
			self.current_health = 0

	def get_health(self,amount):
		if self.target_health < self.max_health:
			self.target_health += amount
		if self.target_health > self.max_health:
			self.target_health = self.max_health

	def update(self):
		self.advanced_health()
		
	def advanced_health(self):
		transition_width = 0
		transition_color = (255,0,0)

		if self.current_health < self.target_health:
			self.current_health += self.health_change_speed
			transition_width = int((self.target_health - self.current_health) / self.health_ratio)
			transition_color = (0,255,0)

		if self.current_health > self.target_health:
			self.current_health -= self.health_change_speed 
			transition_width = int((self.target_health - self.current_health) / self.health_ratio)
			transition_color = (255,255,0)

		health_bar_width = int(self.current_health / self.health_ratio)
		health_bar = pg.Rect(10,45,health_bar_width,25)
		transition_bar = pg.Rect(health_bar.right,45,transition_width,25)

		pg.draw.rect(screen,(255,0,0),health_bar)
		pg.draw.rect(screen,transition_color,transition_bar)	
		pg.draw.rect(screen,(255,255,255),(10,45,self.health_bar_length,25),4)	

	
	

player = pg.sprite.GroupSingle(Player())

'''pg.init()
WIDTH = 1080
HEIGHT = 720
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()
player = pg.sprite.GroupSingle(Player())'''
healthstate = False


gamestate =1
while True:
	if gamestate == 1:
		screen.fill((30,30,30))
		for event in pg.event.get():
			if event.type == pg.QUIT:
				sys.exit()
				pg.quit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_UP:
					player.sprite.get_health(200)
				if event.key == pg.K_DOWN:
					player.sprite.get_damage(200)
				if player.sprite.current_health <= 1000:
					healthstate = True
				if healthstate:
					screen.blit(bleeding, bleed)
					pg.display.update()
				if player.sprite.current_health == 0:
					
					'''screen.blit(textfont.render("GAME OVER", True, RED), (textfont,text_rect))''' 
					gamestate = 2

					

		player.draw(screen)
		player.update()
		pg.display.update()
		clock.tick(60)

	elif gamestate ==2:
		screen.fill('black')
		for event in pg.event.get():
			screen.blit(text, text_rect)
			screen.blit(text2, text_lower)			
			pg.display.update()	
			gamestate = 3


	elif gamestate == 3:
		screen.fill('black')
		screen.blit(text, text_rect)
		screen.blit(text2, text_lower)

		if event.type == pg.KEYDOWN:
			if event.key == pg.K_SPACE:
				gamestate = "menu"
			if event.key == pg.K_ESCAPE:
				event.type == pg.QUIT
				sys.exit()
			


