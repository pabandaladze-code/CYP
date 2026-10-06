# note.py
import pygame
import math
from constants import *

class Note:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target_radius = TARGET_RADIUS
        self.current_ring_radius = RING_MAX_RADIUS
        self.alive = True

    def update(self, dt):
        """
        Обновление состояния кольца.
        dt - время с прошлого кадра (в секундах).
        Кольцо сужается с такой скоростью, чтобы достичь радиуса мишени
        ровно за BEAT_INTERVAL секунд.
        """
        # Рассчитываем, сколько пикселей должно сузиться кольцо за dt
        shrink_speed = (RING_MAX_RADIUS - self.target_radius) / BEAT_INTERVAL
        self.current_ring_radius -= shrink_speed * dt
        
        # Не даем кольцу стать меньше мишени
        if self.current_ring_radius < self.target_radius:
            self.current_ring_radius = self.target_radius

    def draw(self, screen):
        """Отрисовка мишени и кольца."""
        # Рисуем мишень (заполненный круг)
        pygame.draw.circle(screen, COLORS["target"], (int(self.x), int(self.y)), self.target_radius)
        
        # Рисуем сужающееся кольцо (только контур)
        pygame.draw.circle(screen, COLORS["ring"], (int(self.x), int(self.y)), int(self.current_ring_radius), 3)

    def check_click(self, mouse_x, mouse_y):
        """
        Проверка попадания клика.
        Возвращает True, если клик был точным.
        """
        # Расстояние от клика до центра мишени
        dist = math.hypot(mouse_x - self.x, mouse_y - self.y)
        
        # Если клик внутри мишени (с небольшим запасом)
        if dist <= self.target_radius + HIT_TOLERANCE:
            # Вычисляем дельту между радиусом кольца и мишени
            delta = abs(self.current_ring_radius - self.target_radius)
            
            # Если дельта меньше 10 пикселей - попадание!
            if delta < HIT_TOLERANCE:
                return True
        return False