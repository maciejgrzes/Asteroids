import pygame
from constants import *
from player import Player, Shot
from asteroids import Asteroid
from asteroidfield import AsteroidField


def main():
    player_health = 15
    collision_time = 0
    collision_immune = False
    dt = 0
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    font = pygame.font.Font('freesansbold.ttf', 40)
    game_over = font.render('GAME OVER', True, 'red', 'black')
    game_over_rect = game_over.get_rect()
    game_over_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    
    health_text = font.render('Lives: ' + str(player_health//3), True, 'white', 'black')
    health_text_rect = health_text.get_rect()
    health_text_rect.center = (80, SCREEN_HEIGHT - 30)
    
    explosion = pygame.mixer.Sound('assets/explosion.mp3')
    death = pygame.mixer.Sound('assets/death.mp3')

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (bullets, updatable, drawable)
    Player.containers = (updatable, drawable)

    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)


    while True:
        if collision_immune and  (pygame.time.get_ticks() - collision_time > 2000):
            collision_immune = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)
        
        for obj in asteroids:
            if obj.colision(player) and collision_immune == False:
                player_health -= 3
                health_text = font.render('Lives: ' + str(player_health//3), True, 'white', 'black')
                collision_immune = True
                collision_time = pygame.time.get_ticks()
                player.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                if player_health <= 0:
                    screen.blit(game_over, game_over_rect)
                    death.play()
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    return
        
        for ass in asteroids:
            for shot in bullets:
                if ass.colision(shot):
                    explosion.play()
                    ass.split()
                    shot.kill()

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen, 'white')
        
        for bullet in bullets:
            if bullet.position.x < 0 or bullet.position.x > SCREEN_WIDTH or bullet.position.y < 0 or bullet.position.y > SCREEN_HEIGHT:
                bullet.kill()

        screen.blit(health_text, health_text_rect)
        pygame.display.flip()

        dt = clock.tick(TARGET_FRAMERATE) / 1000


if __name__ == "__main__":
    main()

