import pygame
import sys
import datetime

# --------- Configurações ---------
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FPS = 60

# Cores
PRIMARY_COLOR = (230, 57, 70)
PRIMARY_HOVER = (255, 75, 92)
SHADOW_COLOR = (153, 32, 32)
ACCENT_COLOR = (255, 204, 0)
TEXT_COLOR = (255, 255, 255)
BG_OVERLAY = (0, 0, 0, 180)

pygame.init()
pygame.display.set_caption("Super Voice Bros | Jogo de Aventura com Voz")

# Fontes
try:
    font_main = pygame.font.Font("PressStart2P.ttf", 24)  # Baixe a fonte se quiser igual ao HTML
except:
    font_main = pygame.font.SysFont("arial", 24, bold=True)
font_small = pygame.font.SysFont("arial", 14)
font_btn = pygame.font.SysFont("arial", 20, bold=True)

class Button:
    def __init__(self, text, y, callback):
        self.text = text
        self.y = y
        self.callback = callback
        self.rect = pygame.Rect(0, y, 300, 50)
        self.hovered = False

    def draw(self, surf):
        color = PRIMARY_HOVER if self.hovered else PRIMARY_COLOR
        pygame.draw.rect(surf, color, self.rect, border_radius=10)
        pygame.draw.rect(surf, SHADOW_COLOR, self.rect, 5, border_radius=10)
        txt = font_btn.render(self.text, True, TEXT_COLOR)
        surf.blit(txt, (self.rect.centerx - txt.get_width() // 2, self.rect.centery - txt.get_height() // 2))

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.callback()

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        
        # Carrega assets
        try:
            self.bg_img = pygame.image.load("fundo.jpg").convert()
            self.bg_img = pygame.transform.scale(self.bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.bg_img = None
            
        try:
            self.logo_img = pygame.image.load("logo00.png").convert_alpha()
            self.logo_img = pygame.transform.smoothscale(self.logo_img, (400, 200))
        except:
            self.logo_img = None
            
        # Define container
        self.container_rect = pygame.Rect(SCREEN_WIDTH//2 - 400, SCREEN_HEIGHT//2 - 250, 800, 500)
        
        # Cria botões
        self.buttons = [
            Button("JOGAR", self.container_rect.y + 200, self.start_game),
            Button("PERSONAGENS", self.container_rect.y + 260, self.open_characters),
            Button("CONFIGURAÇÕES", self.container_rect.y + 320, self.open_settings),
            Button("CRÉDITOS", self.container_rect.y + 380, self.open_credits),
        ]
        
        # Centraliza botões
        for btn in self.buttons:
            btn.rect.x = SCREEN_WIDTH//2 - btn.rect.width//2

    def show_message(self, msg):
        """Mostra uma mensagem temporária na tela"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,180))
        self.screen.blit(overlay, (0,0))
        txt = font_main.render(msg, True, ACCENT_COLOR)
        self.screen.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, SCREEN_HEIGHT//2 - txt.get_height()//2))
        pygame.display.flip()
        pygame.time.wait(1500)

    def start_game(self):
        print("Iniciando o jogo...")
        self.show_message("Iniciando o jogo...")
        self.running = False  # Sai do menu para iniciar o jogo

    def open_characters(self):
        print("Abrindo seleção de personagens")
        self.show_message("Veja os personagens disponíveis!")

    def open_settings(self):
        print("Abrindo configurações")
        self.show_message("Abrindo configurações...")

    def open_credits(self):
        print("Mostrando créditos")
        self.show_message("Desenvolvido por Marcos com amor pelo clássico!")

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    for btn in self.buttons:
                        btn.check_hover(mouse_pos)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for btn in self.buttons:
                        btn.check_click(mouse_pos)

            # Renderização
            # Fundo
            if self.bg_img:
                self.screen.blit(self.bg_img, (0,0))
            else:
                self.screen.fill((30,30,30))

            # Container
            overlay = pygame.Surface((self.container_rect.width, self.container_rect.height), pygame.SRCALPHA)
            overlay.fill(BG_OVERLAY)
            self.screen.blit(overlay, (self.container_rect.x, self.container_rect.y))

            # Logo
            if self.logo_img:
                self.screen.blit(self.logo_img, (SCREEN_WIDTH//2 - self.logo_img.get_width()//2, self.container_rect.y + 20))

            # Título
            title = font_main.render("Super Voice Bros", True, ACCENT_COLOR)
            # Sombra
            shadow = font_main.render("Super Voice Bros", True, (0,0,0))
            self.screen.blit(shadow, (SCREEN_WIDTH//2 - title.get_width()//2 + 3, self.container_rect.y + 180 + 3))
            self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, self.container_rect.y + 180))

            # Botões
            for btn in self.buttons:
                btn.draw(self.screen)

            # Rodapé
            year = datetime.datetime.now().year
            footer = font_small.render(f"© {year} Marcos Gustavo — IFRN CAICÓ", True, (220,220,220))
            self.screen.blit(footer, (SCREEN_WIDTH//2 - footer.get_width()//2, self.container_rect.y + self.container_rect.height - 30))

            pygame.display.flip()
            clock.tick(FPS)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def run(self):
        menu = Menu(self.screen)
        menu.run()
        # Quando sair do menu, inicia o jogo principal
        self.game_loop()

    def game_loop(self):
        # Exemplo de loop principal do jogo
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Aqui viria a lógica do jogo
            self.screen.fill((30, 30, 30))
            
            # Exemplo: desenhar algo
            text = font_main.render("Jogo Principal", True, (255, 255, 255))
            self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
            
            pygame.display.flip()
            clock.tick(FPS)


if __name__ == "__main__":
    Game().run()