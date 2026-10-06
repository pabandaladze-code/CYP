# ui.py
import pygame
from constants import *

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)

    def draw_hud(self, score, combo):
        """Отрисовка очков и комбо."""
        score_text = self.font.render(f"Очки: {score}", True, COLORS["text"])
        combo_text = self.font.render(f"Комбо: {combo}", True, COLORS["combo"])
        
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(combo_text, (20, 60))