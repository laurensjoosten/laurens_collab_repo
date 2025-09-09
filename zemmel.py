import pygame
import sys


pygame.init()


BREEDTE = 800
HOOGTE = 600
FPS = 60
PLAYER_SPEED = 5
ATTACK_DAMAGE = 10
HP_LOSS_PER_HIT = 10 
ATTACK_RANGE = 80  

background_image = pygame.image.load(r"project_pygame\oefenmee\Afbeelding_achtergrond_SF.jpg")
background_image = pygame.transform.scale(background_image, (BREEDTE, HOOGTE))
player1_image = pygame.image.load(r"project_pygame\oefenmee\Samurai_Fighter1.png")
player2_image = pygame.image.load(r"project_pygame\oefenmee\Samurai_Fighter_2.png")
player1_hp_image = pygame.image.load(r"project_pygame\oefenmee\afbeelding_hp_balk_2-removebg-preview.png")  # Verwisseld met speler 2
player2_hp_image = pygame.image.load(r"project_pygame\oefenmee\afbeelding_hp_balk_1-removebg-preview.png")  # Verwisseld met speler 1
win_image_p1 = pygame.image.load(r"project_pygame\oefenmee\Player 1 wins.png")  
win_image_p2 = pygame.image.load(r"project_pygame\oefenmee\Player 2 wins.png")  

win_image_p1 = pygame.transform.scale(win_image_p1, (300, 100))  
win_image_p2 = pygame.transform.scale(win_image_p2, (300, 100))

def scale_image(image, scale_factor=1.2):
    width, height = image.get_size()
    return pygame.transform.scale(image, (int(width * scale_factor), int(height * scale_factor)))

player1_image = scale_image(player1_image)
player2_image = scale_image(player2_image)

player1_hp_image = scale_image(player1_hp_image, 0.5)
player2_hp_image = scale_image(player2_hp_image, 0.5)

player2_image = pygame.transform.flip(player2_image, True, False)

player2_hp_image = pygame.transform.flip(player2_hp_image, True, False)

class Player:
    def __init__(self, image, x, y, hp_image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 100
        self.hp_image = hp_image
        self.hp_width = hp_image.get_width()
        self.can_attack = True
        self.alive = True

    def move(self, dx, dy):
        if self.alive:
            self.rect.x += dx
            self.rect.y += dy
            self.rect.x = max(0, min(self.rect.x, BREEDTE - self.rect.width))
            self.rect.y = max(0, min(self.rect.y, HOOGTE - self.rect.height))

    def take_damage(self):
        self.health -= HP_LOSS_PER_HIT
        if self.health <= 0:
            self.health = 0
            self.alive = False
        self.hp_width = int((self.health / 100) * self.hp_image.get_width())

    def draw(self, surface):
        if self.alive:
            surface.blit(self.image, self.rect.topleft)

    def draw_hp(self, surface, x, y):
        if self.alive:
            surface.blit(self.hp_image, (x, y), (0, 0, self.hp_width, self.hp_image.get_height()))

    def is_within_attack_range(self, opponent):
        return abs(self.rect.centerx - opponent.rect.centerx) <= ATTACK_RANGE

def main():
    screen = pygame.display.set_mode((BREEDTE, HOOGTE))
    pygame.display.set_caption('Fighting Game')
    clock = pygame.time.Clock()

    ground_level = HOOGTE - 100  
    player1 = Player(player1_image, 100, ground_level - player1_image.get_height(), player1_hp_image)
    player2 = Player(player2_image, 600, ground_level - player2_image.get_height(), player2_hp_image)

    game_over = False
    winner_image = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and player1.can_attack and player1.is_within_attack_range(player2):
                        player2.take_damage()
                        player1.can_attack = False
                    if event.key == pygame.K_UP and player2.can_attack and player2.is_within_attack_range(player1):
                        player1.take_damage()
                        player2.can_attack = False
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        player1.can_attack = True
                    if event.key == pygame.K_UP:
                        player2.can_attack = True

        keys = pygame.key.get_pressed()

        if not game_over:   
            if keys[pygame.K_a]:
                player1.move(-PLAYER_SPEED, 0)
            if keys[pygame.K_d]:
                player1.move(PLAYER_SPEED, 0)

            if keys[pygame.K_LEFT]:
                player2.move(-PLAYER_SPEED, 0)
            if keys[pygame.K_RIGHT]:
                player2.move(PLAYER_SPEED, 0)

        screen.blit(background_image, (0, 0))
        player1.draw(screen)
        player2.draw(screen)

        player1.draw_hp(screen, 10, 10)  
        player2.draw_hp(screen, BREEDTE - player2_hp_image.get_width() - 10, 10)  

        if player2.health <= 0:
            player2.alive = False
            winner_image = win_image_p1
            game_over = True
        elif player1.health <= 0:
            player1.alive = False
            winner_image = win_image_p2
            game_over = True

        if winner_image:
            screen.blit(winner_image, ((BREEDTE // 2) - 150, (HOOGTE // 2) - 50))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()