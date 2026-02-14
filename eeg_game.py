# game.py
import pygame

class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.hover = False

    def update_hover(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

    def clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen, font):
        bg = (110, 200, 255) if self.hover else (70, 140, 220)
        pygame.draw.rect(screen, bg, self.rect, border_radius=10)
        pygame.draw.rect(screen, (20, 20, 20), self.rect, width=2, border_radius=10)
        label = font.render(self.text, True, (10, 10, 10))
        screen.blit(label, label.get_rect(center=self.rect.center))

def game_process(event_q_game, control_q):
    pygame.init()
    W, H = 900, 500
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("EEG Runner (click BLINK to jump)")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 28)
    big_font = pygame.font.SysFont(None, 36)

    ground_y = 380
    player = pygame.Rect(120, ground_y - 60, 50, 60)
    vy = 0.0
    gravity = 0.9
    on_ground = True

    obstacles = []
    spawn_timer = 0
    speed = 300
    score = 0.0

    blink_flash = 0
    blink_btn = Button((W - 170, 80, 140, 55), "BLINK")

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        mouse_pos = pygame.mouse.get_pos()
        blink_btn.update_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if blink_btn.clicked(event.pos):
                    control_q.put("BLINK")  # <-- only source of blink

        # Read blink events (non-blocking)
        blink_event = False
        try:
            while True:
                msg = event_q_game.get_nowait()
                if msg == "BLINK":
                    blink_event = True
        except Exception:
            pass

        # Jump on blink
        if blink_event and on_ground:
            vy = -18.0
            on_ground = False
            blink_flash = 12

        # Spawn obstacles
        spawn_timer -= 1
        if spawn_timer <= 0:
            obstacles.append(pygame.Rect(W + 30, ground_y - 40, 35, 40))
            spawn_timer = 55

        # Move obstacles
        dx = speed * dt
        for obs in obstacles:
            obs.x -= int(dx)
        obstacles = [o for o in obstacles if o.right > 0]

        # Player physics
        vy += gravity
        player.y += int(vy)
        if player.bottom >= ground_y:
            player.bottom = ground_y
            vy = 0
            on_ground = True

        # Collision / score
        if any(player.colliderect(o) for o in obstacles):
            score = 0.0
            obstacles.clear()
        else:
            score += dt * 10.0

        # Draw
        screen.fill((20, 22, 26))
        pygame.draw.rect(screen, (60, 60, 60), (0, ground_y, W, H - ground_y))
        pygame.draw.rect(screen, (120, 200, 255), player)
        for obs in obstacles:
            pygame.draw.rect(screen, (255, 120, 120), obs)

        screen.blit(font.render(f"Score: {int(score)}", True, (230, 230, 230)), (20, 20))
        screen.blit(font.render("Click BLINK to create EEG spike → Jump", True, (230, 230, 230)), (20, 50))

        if blink_flash > 0:
            blink_flash -= 1
            pygame.draw.circle(screen, (255, 255, 120), (W - 40, 40), 14)

        blink_btn.draw(screen, big_font)
        pygame.display.flip()

    pygame.quit()
    control_q.put("STOP")
