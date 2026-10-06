# game.py
import pygame
import sys
import random
from constants import *
from note import Note
from ui import UI

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Ритм-Автомат (Beat Clicker) - ЛР 1")
        self.clock = pygame.time.Clock()
        self.ui = UI(self.screen)
        self.reset()

    def reset(self):
        """Сброс состояния игры."""
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.notes = []
        self.spawn_timer = 0
        self.running = True

    def spawn_note(self):
        """Генерация новой мишени в случайном месте."""
        # Отступы от краев, чтобы мишень не уходила за экран
        margin = RING_MAX_RADIUS + 20
        x = random.randint(margin, WINDOW_WIDTH - margin)
        y = random.randint(margin, WINDOW_HEIGHT - margin)
        self.notes.append(Note(x, y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Обработчик клика мыши (требование ЛР 1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                hit = False
                
                # Проверяем попадание по всем мишеням
                for note in self.notes[:]:
                    if note.check_click(mouse_x, mouse_y):
                        self.score += 10
                        self.combo += 1
                        if self.combo > self.max_combo:
                            self.max_combo = self.combo
                        self.notes.remove(note)
                        hit = True
                        break  # Один клик - одна мишень
                
                # Если промахнулись, сбрасываем комбо
                if not hit:
                    self.combo = 0

    def update(self, dt):
        """Обновление логики игры."""
        # Таймер для генерации нот в такт BPM
        self.spawn_timer += dt
        if self.spawn_timer >= BEAT_INTERVAL:
            self.spawn_timer -= BEAT_INTERVAL
            self.spawn_note()

        # Обновление всех нот
        for note in self.notes[:]:
            note.update(dt)
            
            # Если кольцо дошло до мишени, а клика не было - нота исчезает (промах)
            if note.current_ring_radius <= note.target_radius:
                self.notes.remove(note)
                self.combo = 0  # Сброс комбо при промахе

    def draw(self):
        """Отрисовка всех элементов."""
        self.screen.fill(COLORS["bg"])
        
        for note in self.notes:
            note.draw(self.screen)
            
        self.ui.draw_hud(self.score, self.combo)
        pygame.display.flip()

    def run(self):
        """Главный цикл игры."""
        while self.running:
            # dt - время кадра в секундах
            dt = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.draw()

if __name__ == "__main__":
    game = Game()
    game.run()