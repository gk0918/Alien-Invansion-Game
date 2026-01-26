import pygame

class Scoreboard:
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.stats = stats
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 36)

    def draw(self):
        score_img = self.font.render(f"Score: {self.stats.score}", True, self.text_color)
        level_img = self.font.render(f"Level: {self.stats.level}", True, self.text_color)

        self.screen.blit(score_img, (20, 10))
        self.screen.blit(level_img, (20, 40))

