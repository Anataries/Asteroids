import pygame
import sys
from constants import *
from player import *
from circleshape import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

updatable = pygame.sprite.Group()
drawable = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
shots = pygame.sprite.Group()

Asteroid.containers = (asteroids, updatable, drawable)
AsteroidField.containers = (updatable,)
Player.containers = (updatable, drawable)
Shot.containers = (shots, updatable, drawable)


def main():
    pygame.init()
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    player_instance = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    clock = pygame.time.Clock()
    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill((0, 0 ,0))
        
        shot = player_instance.update(dt)
        if shot is not None:
            shots.add(shot)

        for sprite in updatable:
            if sprite != player_instance:
                sprite.update(dt)

        for asteroid in asteroids:
            for shot in shots:
                distance = ((shot.position.x - asteroid.position.x) ** 2 + (shot.position.y - asteroid.position.y) **  2) ** 0.5
                if distance < shot.radius + asteroid.radius:
                    asteroid.split()
                    shot.kill()

        for asteroid in asteroids:
            if player_instance.collision(asteroid):
                print("Game Over!")
                sys.exit()

        for sprite in drawable:
            sprite.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()

