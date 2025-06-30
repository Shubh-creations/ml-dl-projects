import pygame
import random
import sys
from pygame.locals import *

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
OBSTACLE_COLOR = (128, 128, 128)

HIGH_SCORE_FILE = 'highscore.txt'
OBSTACLE_COUNT = 10 

def load_high_score():
	try:
		with open(HIGH_SCORE_FILE, 'r') as f:
			return int(f.read())
	except (FileNotFoundError, ValueError):
		return 0

def save_high_score(score):
	with open(HIGH_SCORE_FILE, 'w') as f:
		f.write(str(score))

def collide(x1, x2, y1, y2, w1, w2, h1, h2):
	if x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2:
		return True
	else:
		return False

def draw_grid(surface):
	for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
		for x in range(0, WINDOW_WIDTH, GRID_SIZE):
			rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
			pygame.draw.rect(surface, (40, 40, 40), rect, 1)

def draw_gradient_background(surface, top_color, bottom_color):
	"""Draw a vertical gradient background on the surface."""
	for y in range(WINDOW_HEIGHT):
		ratio = y / WINDOW_HEIGHT
		r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
		g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
		b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
		pygame.draw.line(surface, (r, g, b), (0, y), (WINDOW_WIDTH, y))

def show_game_over(screen, score, high_score):
	font = pygame.font.SysFont('Arial', 50, bold=True)
	title = font.render('Game Over!', True, RED)
	score_text = font.render(f'Score: {score}', True, WHITE)
	high_score_text = font.render(f'High Score: {high_score}', True, BLUE)
	restart_text = font.render('Press R to Restart', True, WHITE)
	
	overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
	overlay.fill((0, 0, 0, 180)) 
	screen.blit(overlay, (0, 0))
	
	screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, WINDOW_HEIGHT // 2 - 90))
	screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2 - 30))
	screen.blit(high_score_text, (WINDOW_WIDTH // 2 - high_score_text.get_width() // 2, WINDOW_HEIGHT // 2 + 30))
	screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2 + 90))
	pygame.display.update()

def show_paused(screen):
	font = pygame.font.SysFont('Arial', 50, bold=True)
	paused_text = font.render('Paused', True, BLUE)
	overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
	overlay.fill((0, 0, 0, 120))
	screen.blit(overlay, (0, 0))
	screen.blit(paused_text, (WINDOW_WIDTH // 2 - paused_text.get_width() // 2, WINDOW_HEIGHT // 2 - 25))
	pygame.display.update()

class SnakeGame:
	def __init__(self):
		self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Snake Game')
		self.clock = pygame.time.Clock()
		self.high_score = load_high_score()
		self.reset()

	def reset(self):
		self.snake_pos = [[GRID_WIDTH//2, GRID_HEIGHT//2]]
		self.snake_direction = [1, 0] 
		self.apple_pos = [random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1)]
		self.score = 0
		self.game_over = False
		self.paused = False
		self.obstacles = self.generate_obstacles()
	
		while self.apple_pos in self.obstacles:
			self.apple_pos = [random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1)]

	def generate_obstacles(self):
		obstacles = set()
		forbidden = set(tuple(pos) for pos in self.snake_pos)
		forbidden.add(tuple(self.apple_pos))
		while len(obstacles) < OBSTACLE_COUNT:
			pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
			if pos not in forbidden:
				obstacles.add(pos)
		return [list(pos) for pos in obstacles]

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if self.game_over:
					if event.key == K_r:
						self.reset()
				elif event.key == K_p:
					self.paused = not self.paused
				elif not self.paused:
					if event.key == K_UP and self.snake_direction != [0, 1]:
						self.snake_direction = [0, -1]
					elif event.key == K_DOWN and self.snake_direction != [0, -1]:
						self.snake_direction = [0, 1]
					elif event.key == K_LEFT and self.snake_direction != [1, 0]:
						self.snake_direction = [-1, 0]
					elif event.key == K_RIGHT and self.snake_direction != [-1, 0]:
						self.snake_direction = [1, 0]

	def update(self):
		if not self.paused and not self.game_over:
			new_head = [self.snake_pos[0][0] + self.snake_direction[0],
					   self.snake_pos[0][1] + self.snake_direction[1]]
		
			if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
				new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
				new_head in self.snake_pos or
				new_head in self.obstacles):
				self.game_over = True
				if self.score > self.high_score:
					self.high_score = self.score
					save_high_score(self.high_score)
				return
			
			self.snake_pos.insert(0, new_head)
		
			if new_head == self.apple_pos:
				self.score += 1
				while self.apple_pos in self.snake_pos or self.apple_pos in self.obstacles:
					self.apple_pos = [random.randint(0, GRID_WIDTH-1),
							   random.randint(0, GRID_HEIGHT-1)]
			else:
				self.snake_pos.pop()

	def draw(self):

		draw_gradient_background(self.screen, (30, 30, 60), (10, 10, 10))
		draw_grid(self.screen)

		for pos in self.obstacles:
			rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2)
			pygame.draw.rect(self.screen, OBSTACLE_COLOR, rect, border_radius=7)

		for i, pos in enumerate(self.snake_pos):
			rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2)
			color = (0, 255, 80) if i == 0 else GREEN
			pygame.draw.rect(self.screen, color, rect, border_radius=8)
	
			if i == 0:
				shadow = pygame.Surface((GRID_SIZE - 2, GRID_SIZE - 2), pygame.SRCALPHA)
				pygame.draw.ellipse(shadow, (0, 0, 0, 40), shadow.get_rect())
				self.screen.blit(shadow, rect.topleft)
	
		apple_rect = pygame.Rect(self.apple_pos[0] * GRID_SIZE, self.apple_pos[1] * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2)
		pygame.draw.rect(self.screen, RED, apple_rect, border_radius=10)

		highlight = pygame.Surface((GRID_SIZE - 6, GRID_SIZE - 10), pygame.SRCALPHA)
		pygame.draw.ellipse(highlight, (255, 255, 255, 60), highlight.get_rect())
		self.screen.blit(highlight, (apple_rect.x + 3, apple_rect.y + 2))
	
		font = pygame.font.SysFont('Arial', 30, bold=True)
		score_text = font.render(f'Score: {self.score}', True, WHITE)
		high_score_text = font.render(f'High Score: {self.high_score}', True, BLUE)
		self.screen.blit(score_text, (10, 10))
		self.screen.blit(high_score_text, (10, 40))
		
		if self.paused:
			show_paused(self.screen)
		elif self.game_over:
			show_game_over(self.screen, self.score, self.high_score)
		else:
			pygame.display.update()

	def run(self):
		while True:
			self.handle_events()
			if not self.paused and not self.game_over:
				self.update()
			self.draw()
			self.clock.tick(10)

if __name__ == '__main__':
	game = SnakeGame()
	game.run()
