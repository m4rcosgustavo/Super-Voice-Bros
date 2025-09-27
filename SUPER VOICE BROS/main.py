import pygame
import sys
import datetime
from typing import Callable, List, Optional, Tuple
from game.scene import TestScene

# --------- Configurações Globais ---------
class Config:
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 800
    FPS = 60
    
    # Cores
    PRIMARY = (230, 57, 70)
    PRIMARY_HOVER = (255, 75, 92)
    SHADOW = (153, 32, 32)
    ACCENT = (255, 204, 0)
    TEXT = (255, 255, 255)
    BG_OVERLAY = (0, 0, 0, 180)
    
    # Caminhos dos assets
    BG_IMAGE_PATH = "src/assets/images/fundo1.png"
    LOGO_IMAGE_PATH = "src/assets/images/logo00.png"
    FONT_PATH = "PressStart2P.ttf"
    MUSIC_PATH = "src/assets/sounds/super_mario_theme.mp3"

# --------- Classe Button Aprimorada ---------
class Button:
    def __init__(self, text: str, pos: Tuple[int, int], callback: Callable, width: int = 300, height: int = 50):
        self.text = text
        self.callback = callback
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.hovered = False
        self._create_surfaces()
    
    def _create_surfaces(self):
        """Pré-renderiza as superfícies para melhor performance"""
        self.normal_text = Config.FONT_BTN.render(self.text, True, Config.TEXT)
        self.hover_text = Config.FONT_BTN.render(self.text, True, Config.TEXT)
        
        self.normal_surface = self._create_button_surface(Config.PRIMARY)
        self.hover_surface = self._create_button_surface(Config.PRIMARY_HOVER)
    
    def _create_button_surface(self, color: Tuple[int, int, int]) -> pygame.Surface:
        """Cria uma superfície para o botão com estilo"""
        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, color, (0, 0, self.rect.width, self.rect.height), border_radius=10)
        pygame.draw.rect(surface, Config.SHADOW, (0, 0, self.rect.width, self.rect.height), 5, border_radius=10)
        return surface
    
    def draw(self, surface: pygame.Surface):
        """Desenha o botão na superfície especificada"""
        current_surface = self.hover_surface if self.hovered else self.normal_surface
        current_text = self.hover_text if self.hovered else self.normal_text
        
        surface.blit(current_surface, self.rect)
        text_pos = (
            self.rect.centerx - current_text.get_width() // 2,
            self.rect.centery - current_text.get_height() // 2
        )
        surface.blit(current_text, text_pos)
    
    def update(self, mouse_pos: Tuple[int, int], mouse_click: bool) -> bool:
        """Atualiza o estado do botão e retorna se foi clicado"""
        self.hovered = self.rect.collidepoint(mouse_pos)
        return self.hovered and mouse_click
    
    def center_x(self, x: int):
        """Centraliza o botão horizontalmente"""
        self.rect.x = x - self.rect.width // 2

# --------- Tela de Instruções ---------
class InstructionsScreen:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.back_button = Button(
            "VOLTAR", 
            (Config.SCREEN_WIDTH // 2 - 150, Config.SCREEN_HEIGHT - 80),
            self.go_back
        )
        
        # Texto das instruções completo
        self.instructions = [
            "INSTRUÇÕES DO JOGO SUPER VOICE BROS",
            "",
            "OBJETIVO:",
            "Controlar o personagem com comandos de voz para atravessar fases,",
            "derrotar inimigos e completar cada nível.",
            "",
            "COMO JOGAR:",
            "Fale claramente os comandos para o personagem responder:",
            "• 'Pular' - Salto simples",
            "• 'Super salto' - Salto maior e mais longo",
            "• 'Correr' - Move mais rápido",
            "• 'Agachar' - Evita obstáculos baixos",
            "• 'Parar' - Fica imóvel",
            "• 'Ataque' - Ataque giratório contra inimigos",
            "",
            "DETALHES IMPORTANTES:",
            "- Reconhecimento sensível à entonação (gritar = salto maior)",
            "- Fases progressivamente mais difíceis",
            "- Inimigos principais:",
            "  • Glitchy - Inimigo básico no chão",
            "  • Buzzik - Inimigo voador que atrapalha comandos",
            "  • Mutez - Chefe final com ataques especiais",
            "",
        ]
        
        # Configuração de fonte para instruções
        self.title_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.section_font = pygame.font.SysFont("Arial", 22, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 18)
        self.tip_font = pygame.font.SysFont("Arial", 16, italic=True)
    
    def go_back(self):
        """Volta para o menu principal"""
        self.running = False
    
    def handle_events(self):
        mouse_click = False
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True
        
        if self.back_button.update(mouse_pos, mouse_click):
            self.back_button.callback()
    
    def render(self):
        """Renderiza a tela de instruções com formatação"""
        # Fundo semi-transparente
        overlay = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        self.screen.blit(overlay, (0, 0))
        
        # Container principal
        container = pygame.Rect(
            Config.SCREEN_WIDTH // 2 - 450,
            50,
            900, Config.SCREEN_HEIGHT - 150
        )
        pygame.draw.rect(self.screen, (40, 40, 50), container, border_radius=15)
        pygame.draw.rect(self.screen, Config.ACCENT, container, 3, border_radius=15)
        
        # Renderiza cada linha de instrução com formatação apropriada
        y_offset = container.y + 30
        for line in self.instructions:
            if not line:  # Linha vazia para espaçamento
                y_offset += 15
                continue
                
            if line.startswith("INSTRUÇÕES"):
                text = self.title_font.render(line, True, Config.ACCENT)
            elif line.endswith(":"):  # Seções
                text = self.section_font.render(line, True, (100, 200, 255))
            elif line.startswith("-") or line.startswith("•"):  # Itens de lista
                text = self.tip_font.render(line, True, (200, 200, 200))
            else:  # Texto normal
                text = self.text_font.render(line, True, Config.TEXT)
            
            self.screen.blit(text, (container.x + 30, y_offset))
            y_offset += 30 if line.endswith(":") else 25
        
        # Botão de voltar
        self.back_button.draw(self.screen)
    
    def run(self):
        """Executa o loop da tela de instruções"""
        while self.running:
            self.handle_events()
            self.render()
            pygame.display.flip()
            self.clock.tick(Config.FPS)

# --------- Classe Menu Principal ---------
class MainMenu:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self._load_assets()
        self._setup_layout()
    
    def _load_assets(self):
        """Carrega todos os assets necessários"""
        try:
            Config.FONT_MAIN = pygame.font.Font(Config.FONT_PATH, 24)
        except:
            Config.FONT_MAIN = pygame.font.SysFont("Arial", 24, bold=True)
        
        Config.FONT_SMALL = pygame.font.SysFont("Arial", 14)
        Config.FONT_BTN = pygame.font.SysFont("Arial", 20, bold=True)
        
        self.bg_image = self._load_image(Config.BG_IMAGE_PATH, (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.logo_image = self._load_image(Config.LOGO_IMAGE_PATH, (400, 200), alpha=True)
    
    def _load_image(self, path: str, size: Tuple[int, int], alpha: bool = False) -> Optional[pygame.Surface]:
        """Carrega uma imagem com tratamento de erro"""
        try:
            if alpha:
                image = pygame.image.load(path).convert_alpha()
            else:
                image = pygame.image.load(path).convert()
            return pygame.transform.smoothscale(image, size)
        except:
            print(f"Erro ao carregar imagem: {path}")
            # Retorna uma surface padrão se a imagem não carregar
            surface = pygame.Surface(size, pygame.SRCALPHA) if alpha else pygame.Surface(size)
            if not alpha:
                surface.fill((50, 50, 70))
            return surface
    
    def _setup_layout(self):
        """Configura o layout do menu"""
        self.container_rect = pygame.Rect(
            Config.SCREEN_WIDTH // 2 - 400,
            Config.SCREEN_HEIGHT // 2 - 250,
            800, 500
        )
        
        self.buttons = [
            Button("JOGAR", (0, self.container_rect.y + 200), self.start_game),
            Button("TESTE MOVIMENTAÇÃO", (0, self.container_rect.y + 260), self.start_test_scene),
            Button("PERSONAGENS", (0, self.container_rect.y + 320), self.show_characters),
            Button("INSTRUÇÕES", (0, self.container_rect.y + 380), self.show_instructions),
            Button("CRÉDITOS", (0, self.container_rect.y + 440), self.show_credits),
        ]
        
        for btn in self.buttons:
            btn.center_x(Config.SCREEN_WIDTH // 2)
    
    def start_game(self):
        """Inicia o jogo principal"""
        self._show_temp_message("Jogo principal em desenvolvimento!")
    
    def start_test_scene(self):
        """Inicia a cena de teste de movimentação"""
        self.running = False  # Sai do menu para entrar na cena de teste
    
    def show_instructions(self):
        """Mostra a tela de instruções"""
        instructions = InstructionsScreen(self.screen)
        instructions.run()
    
    def show_characters(self):
        self._show_temp_message("Seleção de personagens!")
    
    def show_credits(self):
        year = datetime.datetime.now().year
        self._show_temp_message(f"© {year} Marcos Gustavo - IFRN CAICÓ", 2000)
    
    def _show_temp_message(self, message: str, duration: int = 1500):
        """Exibe uma mensagem temporária"""
        overlay = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(Config.BG_OVERLAY)
        self.screen.blit(overlay, (0, 0))
        
        text = Config.FONT_MAIN.render(message, True, Config.ACCENT)
        text_rect = text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2))
        
        shadow = Config.FONT_MAIN.render(message, True, (0, 0, 0))
        self.screen.blit(shadow, (text_rect.x + 3, text_rect.y + 3))
        self.screen.blit(text, text_rect)
        
        pygame.display.flip()
        pygame.time.wait(duration)
        self.render()  # Redesenha o menu
    
    def handle_events(self):
        """Processa eventos do menu"""
        mouse_click = False
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return "quit"
        
        for btn in self.buttons:
            if btn.update(mouse_pos, mouse_click):
                btn.callback()
        
        return None
    
    def render(self):
        """Renderiza todos os elementos do menu"""
        # Fundo
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill((30, 30, 30))
        
        # Overlay do container
        overlay = pygame.Surface((self.container_rect.width, self.container_rect.height), pygame.SRCALPHA)
        overlay.fill(Config.BG_OVERLAY)
        self.screen.blit(overlay, (self.container_rect.topleft))
        
        # Logo
        if self.logo_image:
            logo_pos = (Config.SCREEN_WIDTH // 2 - self.logo_image.get_width() // 2, 
                        self.container_rect.y + 20)
            self.screen.blit(self.logo_image, logo_pos)
        
        # Título
        title = Config.FONT_MAIN.render("Super Voice Bros", True, Config.ACCENT)
        title_rect = title.get_rect(center=(Config.SCREEN_WIDTH // 2, self.container_rect.y + 180))
        
        shadow = Config.FONT_MAIN.render("Super Voice Bros", True, (0, 0, 0))
        self.screen.blit(shadow, (title_rect.x + 3, title_rect.y + 3))
        self.screen.blit(title, title_rect)
        
        # Botões
        for btn in self.buttons:
            btn.draw(self.screen)
        
        # Rodapé
        year = datetime.datetime.now().year
        footer = Config.FONT_SMALL.render(f"© {year} Marcos Gustavo e Jullyane Sandra — IFRN CAICÓ", True, (220, 220, 220))
        footer_rect = footer.get_rect(center=(Config.SCREEN_WIDTH // 2, self.container_rect.bottom - 30))
        self.screen.blit(footer, footer_rect)
    
    def run(self):
        """Executa o loop principal do menu"""
        while self.running:
            result = self.handle_events()
            if result == "quit":
                return "quit"
                
            self.render()
            pygame.display.flip()
            self.clock.tick(Config.FPS)
        
        return "test"  # Vai para a cena de teste

# --------- Classe Principal do Jogo ---------
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption("Super Voice Bros | Jogo de Aventura com Voz")
        self.current_scene = "menu"  # Controla a cena atual
        self._load_music()
    
    def _load_music(self):
        """Carrega e configura a música de fundo"""
        try:
            pygame.mixer.music.load(Config.MUSIC_PATH)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Erro ao carregar música: {e}")
    
    def run(self):
        """Loop principal do jogo com gerenciamento de cenas"""
        while True:
            if self.current_scene == "menu":
                menu = MainMenu(self.screen)
                result = menu.run()
                self.current_scene = result if result else "test"
                
            elif self.current_scene == "test":
                test_scene = TestScene(self.screen)
                result = test_scene.run()
                self.current_scene = result if result else "menu"
                
            elif self.current_scene == "quit":
                break
        
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
