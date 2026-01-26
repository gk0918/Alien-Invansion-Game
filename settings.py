class Settings:
    def __init__(self):
        # Screen
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (0, 0, 0)

        # Ship
        self.ship_speed = 3
        self.ship_limit = 3

        # Bullet
        self.bullet_speed = 6
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)
        self.bullets_allowed = 5

        # Alien
        self.alien_speed = 1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        # Speed increase per level
        self.speedup_scale = 1.2

