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

# --------- Classe do Inimigo ---------
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int = 40, height: int = 40, move_range: int = 100, speed: int = 2):
        super().__init__()
        
        # Criar sprite do inimigo
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, width, height), border_radius=8)
        pygame.draw.rect(self.image, (200, 0, 0), (5, 5, width-10, height-10), border_radius=5)
        # Olhos do inimigo
        pygame.draw.rect(self.image, (255, 255, 255), (8, 10, 8, 8))
        pygame.draw.rect(self.image, (255, 255, 255), (24, 10, 8, 8))
        pygame.draw.rect(self.image, (0, 0, 0), (10, 12, 4, 4))
        pygame.draw.rect(self.image, (0, 0, 0), (26, 12, 4, 4))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movimento do inimigo
        self.start_x = x
        self.move_range = move_range
        self.speed = speed
        self.direction = 1  # 1 para direita, -1 para esquerda
        
    def update(self):
        # Movimento horizontal simples (vai e volta)
        self.rect.x += self.speed * self.direction
        
        # Inverter direção se atingir o limite do movimento
        if self.rect.x > self.start_x + self.move_range:
            self.direction = -1
        elif self.rect.x < self.start_x - self.move_range:
            self.direction = 1

# --------- Classe do Player com Sprite Real ---------
class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        
        # Carregar sprite do personagem
        try:
            self.image = pygame.Surface((50, 80), pygame.SRCALPHA)
            # Desenhar personagem simples (substituir por sprite real depois)
            pygame.draw.rect(self.image, (0, 100, 255), (0, 0, 50, 80), border_radius=10)  # Corpo
            pygame.draw.rect(self.image, (255, 200, 150), (10, 10, 30, 20), border_radius=5)  # Rosto
            pygame.draw.rect(self.image, (0, 0, 200), (5, 30, 40, 50), border_radius=8)  # Roupa
            # Olhos
            pygame.draw.rect(self.image, (255, 255, 255), (15, 15, 6, 6))
            pygame.draw.rect(self.image, (255, 255, 255), (29, 15, 6, 6))
        except:
            # Fallback se não carregar
            self.image = pygame.Surface((50, 80))
            self.image.fill((0, 100, 255))
        
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
        
        # Sistema de vidas
        self.lives = 3
        self.invincible = False
        self.invincible_timer = 0
        
    def update(self, platforms: List[pygame.Rect], enemies: pygame.sprite.Group):
        # Atualizar temporizador de invencibilidade
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
        
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
        
        # Verificar colisão com inimigos
        if not self.invincible:
            enemy_hits = pygame.sprite.spritecollide(self, enemies, False)
            if enemy_hits:
                self.lose_life()
        
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
    
    def lose_life(self):
        """Perde uma vida e ativa invencibilidade temporária"""
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            self.invincible_timer = 60  # 1 segundo de invencibilidade (60 frames)
            
            # Efeito visual - piscar
            if self.lives > 0:
                print(f"Vidas restantes: {self.lives}")
            else:
                print("Game Over!")
    
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
        
        # Criar grupo de inimigos
        self.enemies = pygame.sprite.Group()
        self._create_enemies()
        
        # Criar plataformas e obstáculos
        self.platforms = self._create_platforms()
        self.obstacles = self._create_obstacles()
        
        # Juntar todas as colisões
        self.all_colliders = [obs.rect for obs in self.obstacles]
        
        # Fonte para informações
        self.font = pygame.font.SysFont("Arial", 20)
        self.small_font = pygame.font.SysFont("Arial", 16)
        self.life_font = pygame.font.SysFont("Arial", 24, bold=True)
        
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
    
    def _create_enemies(self):
        """Cria os inimigos no cenário"""
        enemies_data = [
            # x, y, move_range, speed
            (350, SceneConfig.SCREEN_HEIGHT - 80, 80, 2),
            (600, SceneConfig.SCREEN_HEIGHT - 230, 60, 3),
            (800, SceneConfig.SCREEN_HEIGHT - 180, 100, 1),
            (200, SceneConfig.SCREEN_HEIGHT - 220, 50, 2),
        ]
        
        for x, y, move_range, speed in enemies_data:
            enemy = Enemy(x, y, 40, 40, move_range, speed)
            self.enemies.add(enemy)
    
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
        ]
        return obstacles
    
    def _draw_lives_hud(self):
        """Desenha o HUD de vidas"""
        life_text = self.life_font.render(f"VIDAS: {self.player.lives}", True, (255, 255, 255))
        life_bg = pygame.Rect(10, 10, life_text.get_width() + 20, life_text.get_height() + 10)
        
        # Fundo semi-transparente
        pygame.draw.rect(self.screen, (0, 0, 0, 128), life_bg, border_radius=5)
        pygame.draw.rect(self.screen, (255, 255, 255), life_bg, 2, border_radius=5)
        
        self.screen.blit(life_text, (20, 15))
        
        # Indicador de invencibilidade
        if self.player.invincible:
            inv_text = self.small_font.render("INVENCIVEL!", True, (255, 255, 0))
            self.screen.blit(inv_text, (20, 50))
    
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
                    self.player.lives = 3
                    self.player.invincible = False
                    
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
        self.player.update(self.all_colliders, self.enemies)
        self.enemies.update()
        self.update_camera()
        
        # Game Over check
        if self.player.lives <= 0:
            print("Game Over - Retornando ao menu...")
            return "menu"
    
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
        
        # Desenhar inimigos (ajustados pela câmera)
        for enemy in self.enemies:
            enemy_pos = (enemy.rect.x - self.camera_x, enemy.rect.y)
            self.screen.blit(enemy.image, enemy_pos)
        
        # Desenhar player (ajustado pela câmera)
        player_pos = (self.player.rect.x - self.camera_x, self.player.rect.y)
        
        # Efeito de piscar quando invencível
        if not self.player.invincible or (self.player.invincible and self.player.invincible_timer % 6 < 3):
            self.screen.blit(self.player.image, player_pos)
        
        # HUD de vidas
        self._draw_lives_hud()
        
        # Informações na tela
        info_text = [
            "SUPER VOICE BROS - FASE DE TESTE",
            "Controles: ← → mover, ESPAÇO pular, R reset, ESC voltar",
            f"Posição: ({self.player.rect.x}, {self.player.rect.y})",
            f"Velocidade: ({self.player.vel_x:.1f}, {self.player.vel_y:.1f})",
            f"No chão: {'SIM' if self.player.on_ground else 'NÃO'}",
            f"Inimigos: {len(self.enemies)}",
        ]
        
        for i, text in enumerate(info_text):
            color = (255, 255, 0) if i == 0 else (255, 255, 255)
            font = self.font if i == 0 else self.small_font
            rendered = font.render(text, True, color)
            self.screen.blit(rendered, (10, 80 + i * 25))
        
        # Dicas de controle
        tips = [
            "💡 DICA: Pule nas plataformas marrons!",
            "⚠️ Cuidado com os inimigos vermelhos!",
            "❤️ Evite tocar nos inimigos para não perder vidas!",
            "🎯 Objetivo: Explore todo o cenário"
        ]
        
        for i, tip in enumerate(tips):
            rendered = self.small_font.render(tip, True, (200, 255, 200))
            self.screen.blit(rendered, (10, SceneConfig.SCREEN_HEIGHT - 100 + i * 20))
    
    def run(self):
        """Executa o loop da cena de teste"""
        while self.running:
            result = self.handle_events()
            if result:
                return result
                
            update_result = self.update()
            if update_result:
                return update_result
                
            self.render()
            pygame.display.flip()
            self.clock.tick(SceneConfig.FPS)
        
        return "menu"