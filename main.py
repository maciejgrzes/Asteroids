import pygame
from constants import *
from player import *
from asteroids import *
from asteroidfield import *


def main():
    player_health = 3
    collision_time = 0
    collision_immune = False
    dt = 0
    health_color = 'green'
    score = 0

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    font = pygame.font.Font('freesansbold.ttf', 40)
    game_over = font.render('GAME OVER', True, 'red', 'black')
    game_over_rect = game_over.get_rect()
    game_over_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    health_text = font.render('Lives: ' + str(player_health), True, health_color, 'black')
    health_text_rect = health_text.get_rect()
    health_text_rect.center = (80, SCREEN_HEIGHT - 30)

    score_text = font.render('Score: ' + str(score), True, 'white', 'black')
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (SCREEN_WIDTH // 2, 30)

    explosion = pygame.mixer.Sound('assets/explosion.mp3')
    death = pygame.mixer.Sound('assets/death.mp3')
    hurt = pygame.mixer.Sound('assets/hurt.mp3')
    health_up = pygame.mixer.Sound('assets/heal.mp3')

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    heals = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (bullets, updatable, drawable)
    Player.containers = (updatable, drawable)
    HealPack.containers = (drawable, heals)

    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)


    while True:
        if collision_immune and (pygame.time.get_ticks() - collision_time > 2000):
            collision_immune = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for obj in asteroids:
            if obj.colision(player) and collision_immune == False:
                player_health -= 1
                if player_health < 1:
                    health_color = 'red'
                elif player_health > 0 and health_color != 'green':
                    health_color = 'green'
                health_text = font.render('Lives: ' + str(player_health), True, health_color, 'black')
                collision_immune = True
                collision_time = pygame.time.get_ticks()
                player.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                hurt.play()
                if player_health < 0:
                    screen.blit(game_over, game_over_rect)
                    death.play()
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    return

        for ass in asteroids:
            for shot in bullets:
                if ass.colision(shot):
                    if ass.radius == 60:
                        score += 1
                    elif ass.radius == 40:
                        score += 2
                    elif ass.radius == 20:
                        score += 3
                    score_text = font.render('Score: ' + str(score), True, 'white', 'black')
                    explosion.play()
                    ass.split()
                    if random.random() < 0.15 and player_health < 3 and len(heals) < 3:
                        heal = HealPack(ass.position.x, ass.position.y, ass.radius)
                    shot.kill()

        for h in heals:
            if h.colision(player):
                h.kill()
                player_health += 1
                health_up.play()
                if player_health > 0 and health_color != 'green':
                    health_color = 'green'
                health_text = font.render('Lives: ' + str(player_health), True, health_color, 'black')

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen, 'white')

        for bullet in bullets:
            if bullet.position.x < 0 or bullet.position.x > SCREEN_WIDTH or bullet.position.y < 0 or bullet.position.y > SCREEN_HEIGHT:
                bullet.kill()

        screen.blit(health_text, health_text_rect)
        screen.blit(score_text, score_text_rect)
        pygame.display.flip()

        dt = clock.tick(TARGET_FRAMERATE) / 1000


if __name__ == "__main__":
    main()
