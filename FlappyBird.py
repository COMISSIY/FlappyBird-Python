import pygame, random
pygame.init()

clock = pygame.time.Clock()
height, width = 600, 400
sc = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')
font = pygame.font.Font('Fonts/19783.ttf', 80)
rendering_area = sc.get_rect()
button = pygame.image.load('Sprites/button.png').convert()
button.set_colorkey((255, 255, 255))
cheak_button = button.get_rect(center=(width//2, height//2))
player = pygame.image.load('Sprites/bird.png').convert()
player = pygame.transform.scale(player, (90, 60))
player.set_colorkey((255, 255, 255))
player_collide = player.get_rect(center=(width//2, height//2))
background = pygame.image.load('Sprites/FlappyBG.png').convert()
background = pygame.transform.scale(background, (width, height))
lenght = 160
speed = 4 
score = 0
isjump = False
jump = 10
gravity = 0
    
class Tube:
	def __init__(self, x, n):
		self.width = x + rendering_area.width + 500
		self.num = n
		self.image = pygame.image.load('Sprites/tube.png').convert()
		self.image.set_colorkey((255, 255, 255))
		self.collide = self.image.get_rect(topleft=(self.width, random.randint(-50, -20) * 10))
		self.bottom_tube = pygame.transform.flip(self.image, 0, 1)
		self.bottom_collide = self.bottom_tube.get_rect(topleft=(self.width, self.collide.y + self.collide.height + lenght))

	def draw(self):
		if self.collide.x + self.collide.width >= rendering_area.x:
			if rendering_area.colliderect(self.collide):
				sc.blit(self.image, self.collide)
				sc.blit(self.bottom_tube, self.bottom_collide)
			self.collide.move_ip(-speed, 0)
			self.bottom_collide.move_ip(-speed, 0)

	def generate(self):
		if self.num == 9:
			if self.collide.x < -self.collide.width:
				global tubes
				print(True)
				tubes = [Tube(i*400, i) for i in range(10)]

	def cheak_collide(self):
		global speed
		if self.collide.colliderect(player_collide) or self.bottom_collide.colliderect(player_collide) or not rendering_area.colliderect(player_collide):
			speed = 0

	def take_score(self):
		global score
		if self.collide.x // 4 == player_collide.x // 4 and speed != 0:
			score += 1


def grav():
	global gravity, speed
	if player_collide.y + player_collide.height < height:
		player_collide.move_ip(0, gravity)
		gravity += 0.1 
	else:
		player_collide.y = height - player_collide.height
		speed = 0
tubes = [Tube(i*400, i) for i in range(10)]

def restart():
	if speed == 0:
		sc.blit(button, cheak_button)

while True:
	for ev in pygame.event.get():
		if ev.type == pygame.QUIT:
			exit()
			break
		elif ev.type == pygame.KEYDOWN:
			if ev.key == pygame.K_SPACE and speed != 0:
				isjump = True
				gravity = 0
		elif ev.type == pygame.MOUSEBUTTONDOWN:
			if cheak_button.collidepoint(pygame.mouse.get_pos()) and speed == 0:
				player_collide.y = height // 2
				speed = 4
				gravity = 0
				score = 0
				tubes = [Tube(i*400, i) for i in range(10)]

	clock.tick(60)
	text = font.render(str(score), 1, (255, 255, 255))
	sc.blit(background, (0, 0))
	sc.blit(player, player_collide)
	if isjump:
		if jump > 2:
			jump -= 1
		else:
			isjump = False
			jump = 10
		player_collide.move_ip(0, -jump)
	for i in tubes:
	 	i.draw()
	 	i.generate()
	 	i.cheak_collide()
	 	i.take_score()
	sc.blit(text, (width//2 - 10, 100))
	grav()
	restart()
	
	pygame.display.update()

