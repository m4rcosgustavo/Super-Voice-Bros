import pygame
import os
from typing import List, Tuple

# --------- Configurações da Cena ---------
class SceneConfig:
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 800
    FPS = 60
    GRAVITY = 0.8
    PLAYER_SPEED = 5
    JUMP_POWER = -15

# --------- Classe do Player com Sprite Real ---------
class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        
        # Carregar sprite do personagem
        try:
            self.image = pygame.Surface((50, 80), pygame.SRCALPHA)
            # Desenhar personagem simples (substituir por sprite real depois)
            pygame.draw.rect(self.image, (255, 0, 0), (0, 0, 50, 80), border_radius=10)  # Corpo
            pygame.draw.rect(self.image, (255, 255, 0), (10, 10, 30, 20), border_radius=5)  # Rosto
            pygame.draw.rect(self.image, (0, 0, 255), (5, 30, 40, 50), border_radius=8)  # Roupa
        except:
            # Fallback se não carregar
            self.image = pygame.Surface((50, 80))
            self.image.fill((255, 0, 0))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Física do personagem
        self.vel_x = 0
        self.vel_y = 0
        self.speed = SceneConfig.PLAYER_SPEED
        self.jump_power = SceneConfig.JUMP_POWER
        self.gravity = SceneConfig.GRAVITY
        self.on_ground = False
        self.facing_right = True
        
    def update(self, platforms: List[pygame.Rect]):
        # Aplicar gravidade
        self.vel_y += self.gravity
        
        # Movimento horizontal
        self.rect.x += self.vel_x
        
        # Colisão com plataformas (horizontal)
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_x > 0:  # Movendo para direita
                    self.rect.right = platform.left
                elif self.vel_x < 0:  # Movendo para esquerda
                    self.rect.left = platform.right
        
        # Movimento vertical
        self.rect.y += self.vel_y
        self.on_ground = False
        
        # Colisão com plataformas (vertical)
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_y > 0:  # Caindo
                    self.rect.bottom = platform.top
                    self.on_ground = True
                    self.vel_y = 0
                elif self.vel_y < 0:  # Pulando
                    self.rect.top = platform.bottom
                    self.vel_y = 0
        
        # Limitar à tela (horizontal)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SceneConfig.SCREEN_WIDTH:
            self.rect.right = SceneConfig.SCREEN_WIDTH
            
        # Limitar à tela (vertical - chão)
        if self.rect.bottom > SceneConfig.SCREEN_HEIGHT:
            self.rect.bottom = SceneConfig.SCREEN_HEIGHT
            self.on_ground = True
            self.vel_y = 0
            
        # Direção do personagem
        if self.vel_x > 0:
            self.facing_right = True
        elif self.vel_x < 0:
            self.facing_right = False
    
    def move_left(self):
        self.vel_x = -self.speed
    
    def move_right(self):
        self.vel_x = self.speed
    
    def stop(self):
        self.vel_x = 0
    
    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

# --------- Classe Obstáculos ---------
class Obstacle:
    def __init__(self, x: int, y: int, width: int, height: int, color: Tuple[int, int, int], obs_type: str = "platform"):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.type = obs_type
    
    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.rect)
        # Adicionar detalhes baseados no tipo
        if self.type == "platform":
            pygame.draw.rect(surface, (self.color[0]-30, self.color[1]-30, self.color[2]-30), 
                           self.rect, 2)
        elif self.type == "enemy":
            pygame.draw.rect(surface, (255, 0, 0), 
                           (self.rect.x + 5, self.rect.y + 5, self.rect.width - 10, self.rect.height - 10))

# --------- Cena de Teste Aprimorada ---------
class TestScene:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Carregar fundo
        self.background = self._create_background()
        
        # Criar player
        self.player = Player(100, SceneConfig.SCREEN_HEIGHT - 200)
        
        # Criar plataformas e obstáculos
        self.platforms = self._create_platforms()
        self.obstacles = self._create_obstacles()
        
        # Juntar todas as colisões
        self.all_colliders = [obs.rect for obs in self.obstacles]
        
        # Fonte para informações
        self.font = pygame.font.SysFont("Arial", 20)
        self.small_font = pygame.font.SysFont("Arial", 16)
        
        # Controle de câmera
        self.camera_x = 0
        
    def _create_background(self) -> pygame.Surface:
        """Cria um fundo parallax simples"""
        bg = pygame.Surface((SceneConfig.SCREEN_WIDTH, SceneConfig.SCREEN_HEIGHT))
        
        # Céu gradiente
        for y in range(SceneConfig.SCREEN_HEIGHT):
            # Gradiente azul para verde
            blue = max(100, 200 - y // 8)
            green = min(200, 100 + y // 6)
            pygame.draw.line(bg, (50, blue, green), (0, y), (SceneConfig.SCREEN_WIDTH, y))
        
        # Nuvens
        cloud_color = (240, 240, 255)
        pygame.draw.ellipse(bg, cloud_color, (100, 80, 120, 40))
        pygame.draw.ellipse(bg, cloud_color, (400, 120, 150, 35))
        pygame.draw.ellipse(bg, cloud_color, (700, 60, 100, 30))
        
        # Sol
        pygame.draw.circle(bg, (255, 255, 100), (900, 100), 40)
        
        return bg
    
    def _create_platforms(self) -> List[pygame.Rect]:
        """Cria as plataformas do cenário"""
        platforms = [
            # Chão principal
            pygame.Rect(0, SceneConfig.SCREEN_HEIGHT - 50, SceneConfig.SCREEN_WIDTH, 50),
            
            # Plataformas flutuantes
            pygame.Rect(200, SceneConfig.SCREEN_HEIGHT - 200, 150, 20),
            pygame.Rect(450, SceneConfig.SCREEN_HEIGHT - 300, 120, 20),
            pygame.Rect(700, SceneConfig.SCREEN_HEIGHT - 150, 100, 20),
            pygame.Rect(300, SceneConfig.SCREEN_HEIGHT - 400, 200, 20),
        ]
        return platforms
    
    def _create_obstacles(self) -> List[Obstacle]:
        """Cria obstáculos e plataformas coloridas"""
        obstacles = [
            # Chão principal (verde)
            Obstacle(0, SceneConfig.SCREEN_HEIGHT - 50, SceneConfig.SCREEN_WIDTH, 50, (100, 200, 100), "platform"),
            
            # Plataformas flutuantes (marrom)
            Obstacle(200, SceneConfig.SCREEN_HEIGHT - 200, 150, 20, (150, 100, 50), "platform"),
            Obstacle(450, SceneConfig.SCREEN_HEIGHT - 300, 120, 20, (160, 110, 60), "platform"),
            Obstacle(700, SceneConfig.SCREEN_HEIGHT - 150, 100, 20, (140, 90, 40), "platform"),
            Obstacle(300, SceneConfig.SCREEN_HEIGHT - 400, 200, 20, (170, 120, 70), "platform"),
            
            # Obstáculos vermelhos (inimigos simples)
            Obstacle(350, SceneConfig.SCREEN_HEIGHT - 70, 30, 30, (255, 0, 0), "enemy"),
            Obstacle(600, SceneConfig.SCREEN_HEIGHT - 220, 25, 25, (255, 50, 50), "enemy"),
            Obstacle(800, SceneConfig.SCREEN_HEIGHT - 170, 35, 35, (255, 30, 30), "enemy"),
        ]
        return obstacles
    
    def handle_events(self):
        """Processa eventos de entrada"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return "quit"
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()
                elif event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_ESCAPE:
                    return "menu"
                elif event.key == pygame.K_r:  # Reset para teste
                    self.player.rect.x = 100
                    self.player.rect.y = SceneConfig.SCREEN_HEIGHT - 200
                    self.player.vel_x = 0
                    self.player.vel_y = 0
                    
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    self.player.stop()
        
        return None
    
    def update_camera(self):
        """Atualiza a câmera para seguir o player"""
        # Câmera simples que segue o player
        target_x = self.player.rect.centerx - SceneConfig.SCREEN_WIDTH // 2
        self.camera_x = max(0, min(target_x, SceneConfig.SCREEN_WIDTH * 2 - SceneConfig.SCREEN_WIDTH))
    
    def update(self):
        """Atualiza a lógica do jogo"""
        self.player.update(self.all_colliders)
        self.update_camera()
    
    def draw_with_camera(self, surface: pygame.Surface, rect: pygame.Rect, color: Tuple[int, int, int]):
        """Desenha um retângulo considerando a câmera"""
        adjusted_rect = rect.move(-self.camera_x, 0)
        pygame.draw.rect(surface, color, adjusted_rect)
    
    def render(self):
        """Renderiza a cena completa"""
        # Fundo
        self.screen.blit(self.background, (-self.camera_x // 3, 0))  # Efeito parallax
        
        # Desenhar obstáculos
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Desenhar player (ajustado pela câmera)
        player_pos = (self.player.rect.x - self.camera_x, self.player.rect.y)
        self.screen.blit(self.player.image, player_pos)
        
        # Informações na tela
        info_text = [
            "CENA DE TESTE - SUPER VOICE BROS",
            "Controles: ← → mover, ESPAÇO pular, R reset, ESC voltar",
            f"Posição: ({self.player.rect.x}, {self.player.rect.y})",
            f"Velocidade: ({self.player.vel_x:.1f}, {self.player.rect.y:.1f})",
            f"No chão: {'SIM' if self.player.on_ground else 'NÃO'}",
            f"Direção: {'DIREITA' if self.player.facing_right else 'ESQUERDA'}",
            f"Plataformas: {len(self.platforms)} obstáculos: {len(self.obstacles)}"
        ]
        
        for i, text in enumerate(info_text):
            color = (255, 255, 0) if i == 0 else (255, 255, 255)
            font = self.font if i == 0 else self.small_font
            rendered = font.render(text, True, color)
            self.screen.blit(rendered, (10, 10 + i * 25))
        
        # Dicas de controle
        tips = [
            "DICA: Pule nas plataformas marrons!",
            "Cuidado com os obstáculos vermelhos!",
            "Objetivo: Explore todo o cenário"
        ]
        
        for i, tip in enumerate(tips):
            rendered = self.small_font.render(tip, True, (200, 255, 200))
            self.screen.blit(rendered, (10, SceneConfig.SCREEN_HEIGHT - 80 + i * 20))
    
    def run(self):
        """Executa o loop da cena de teste"""
        while self.running:
            result = self.handle_events()
            if result:
                return result
                
            self.update()
            self.render()
            pygame.display.flip()
            self.clock.tick(SceneConfig.FPS)
        
        return "menu"
