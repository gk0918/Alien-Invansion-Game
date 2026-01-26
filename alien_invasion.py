import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard

def run_game():
    pygame.init()
    pygame.mixer.init()

    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    ship = Ship(ai_settings, screen)

    bullets = pygame.sprite.Group()
    aliens = pygame.sprite.Group()

    create_fleet(ai_settings, screen, ship, aliens)

    shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
    hit_sound = pygame.mixer.Sound("sounds/explosion.wav")

    clock = pygame.time.Clock()

    while True:
        check_events(ai_settings, screen, ship, bullets, shoot_sound)
        if stats.game_active:
            ship.update()
            update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, hit_sound)
            update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets)
        clock.tick(60)

def check_events(ai_settings, screen, ship, bullets, shoot_sound):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                ship.moving_left = True
            elif event.key == pygame.K_SPACE:
                if len(bullets) < ai_settings.bullets_allowed:
                    new_bullet = Bullet(ai_settings, screen, ship)
                    bullets.add(new_bullet)
                    shoot_sound.play()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                ship.moving_left = False

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, hit_sound):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        hit_sound.play()
        stats.score += 10 * len(collisions)

    if not aliens:
        bullets.empty()
        ai_settings.alien_speed *= ai_settings.speedup_scale
        stats.level += 1
        create_fleet(ai_settings, screen, ship, aliens)

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            for a in aliens:
                a.rect.y += ai_settings.fleet_drop_speed
            ai_settings.fleet_direction *= -1
            break

def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height

    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = available_space_x // (2 * alien_width)

    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship.rect.height
    number_rows = available_space_y // (2 * alien_height)

    for row in range(number_rows):
        for alien_number in range(number_aliens_x):
            new_alien = Alien(ai_settings, screen)
            new_alien.x = alien_width + 2 * alien_width * alien_number
            new_alien.rect.x = new_alien.x
            new_alien.rect.y = alien_height + 2 * alien_height * row
            aliens.add(new_alien)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets):
    screen.fill(ai_settings.bg_color)

    for bullet in bullets:
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    sb.draw()

    pygame.display.flip()

if __name__ == "__main__":
    run_game()

