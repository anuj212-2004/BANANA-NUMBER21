import pygame
import random
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
FPS = 60
GRAVITY = 0.6
JUMP_SPEED = -12
GAME_SPEED = 5
PLAYER_SPEED = 5  # Speed for horizontal movement

# Colors
RAD_GREEN = (57, 255, 20)  # Radium green color
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Banana Runner Game')
clock = pygame.time.Clock()

# Initialize mixer for sounds
pygame.mixer.init()

# Load sounds
uhh_sound = pygame.mixer.Sound('uhh.mp3')
uhh_sound.set_volume(0.5)

# Load background music
pygame.mixer.music.load('background212.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)  # Loop the music

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('banana.gif').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 130))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = WINDOW_HEIGHT - 100
        self.velocity_y = 0
        self.velocity_x = 0  # Added for horizontal movement
        self.jumping = False
        self.mask = pygame.mask.from_surface(self.image)
        self.rotation = 0
        self.fall_speed = 0
        
    def jump(self):
        if not self.jumping:
            self.velocity_y = JUMP_SPEED
            self.jumping = True
            uhh_sound.play()
    
    def move_left(self):
        self.velocity_x = -PLAYER_SPEED
    
    def move_right(self):
        self.velocity_x = PLAYER_SPEED
    
    def stop(self):
        self.velocity_x = 0
            
    def update(self):
        if game.game_over:
            self.rotation += 5
            self.fall_speed += 0.2
            self.rect.y += self.fall_speed
            rotated_image = pygame.transform.rotate(self.image, self.rotation)
            self.rect = rotated_image.get_rect(center=self.rect.center)
            screen.blit(rotated_image, self.rect)
        else:
            self.velocity_y += GRAVITY
            self.rect.y += self.velocity_y
            self.rect.x += self.velocity_x  # Apply horizontal movement
            
            # Keep player within screen bounds
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > WINDOW_WIDTH:
                self.rect.right = WINDOW_WIDTH
            
            if self.rect.bottom > WINDOW_HEIGHT - 50:
                self.rect.bottom = WINDOW_HEIGHT - 50
                self.velocity_y = 0
                self.jumping = False

class Element(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('objects.webp').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = WINDOW_WIDTH
        self.rect.y = WINDOW_HEIGHT - 100
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self):
        self.rect.x -= GAME_SPEED
        if self.rect.right < 0:
            self.kill()

class Game:
    def __init__(self):
        self.background = pygame.image.load('background21.webp').convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.player = Player()
        self.all_sprites = pygame.sprite.Group()
        self.elements = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.game_over = False
        
        # Load game over sound
        self.game_over_sound = pygame.mixer.Sound('gameover212.mp3')
        self.game_over_sound.set_volume(0.5)
        
    def spawn_element(self):
        if len(self.elements) < 2 and random.randint(1, 150) < 3:
            element = Element()
            self.all_sprites.add(element)
            self.elements.add(element)
            
    def check_collisions(self):
        for element in self.elements:
            if pygame.sprite.collide_mask(self.player, element):
                self.game_over = True
                pygame.mixer.music.stop()
                self.game_over_sound.play()
                break
            
    def update_score(self):
        for element in self.elements:
            if element.rect.right < self.player.rect.left and not hasattr(element, 'counted'):
                self.score += 1
                element.counted = True
                
    def draw_score(self):
        score_text = self.font.render(f'Score: {self.score}', True, RAD_GREEN)
        screen.blit(score_text, (10, 10))
        
    def draw_game_over(self):
        game_over_text = self.font.render('Game Over!', True, RED)
        replay_text = self.font.render('Press R to Replay or Q to Quit', True, BLACK)
        screen.blit(game_over_text, (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 - 50))
        screen.blit(replay_text, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 + 50))
        
    def reset(self):
        self.all_sprites.empty()
        self.elements.empty()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.score = 0
        self.game_over = False
        pygame.mixer.music.play(-1)  # Restart background music
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE and not self.game_over:
                        self.player.jump()
                    elif event.key == K_r and self.game_over:
                        self.reset()
                    elif event.key == K_q and self.game_over:
                        running = False
                    elif event.key == K_LEFT:
                        self.player.move_left()
                    elif event.key == K_RIGHT:
                        self.player.move_right()
                elif event.type == KEYUP:
                    if event.key in (K_LEFT, K_RIGHT):
                        self.player.stop()
                        
            if not self.game_over:
                self.spawn_element()
                self.all_sprites.update()
                self.check_collisions()
                self.update_score()
            else:
                self.player.update()  # Update player even when game is over
                
            screen.blit(self.background, (0, 0))
            self.all_sprites.draw(screen)
            self.draw_score()
            
            if self.game_over:
                self.draw_game_over()
                
            pygame.display.flip()
            clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

# Start the game
if __name__ == "__main__":
    game = Game()
    game.run()