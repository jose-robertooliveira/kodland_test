import pgzrun
from pygame import Rect
import math
import random

# Constantes 
WIDTH: int = 800
HEIGHT: int = 600

GAME_STATE_MENU: int = 0
GAME_STATE_PLAYING: int = 1
game_state: int = GAME_STATE_MENU
sound_on: bool = True
player_lives: int = 3

# Cores
WHITE: tuple[int, int, int] = (255, 255, 255)
CYAN: tuple[int, int, int] = (0, 255, 255)
RED: tuple[int, int, int] = (255, 0, 0)
BLACK: tuple[int, int, int] = (0, 0, 0)
GREEN: tuple[int, int, int] = (0, 255, 0)
ORANGE: tuple[int, int, int] = (255, 165, 0)

delta_time = 1/60  # Assume um valor fixo de tempo entre quadros (60 Framees por segundo)

"""Classe de definição e inicialização do jogador"""
class Avenger:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.rect: Rect = Rect(x, y, 32, 32)
        self.color_idle: tuple[int, int, int] = GREEN
        self.color_walk: list[tuple[int, int, int]] = [GREEN, (0, 200, 0), GREEN, (0, 150, 0)]
        self.animation_timer: float = 0.0
        self.animation_speed: float = 0.1
        self.current_animation_frame: int = 0
        self.damaged: bool = False
        self.damage_timer: float = 0.0
        self.damage_duration: float = 1.0

    def move(self, dx: int, dy: int) -> None:
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x <= WIDTH - self.rect.width and 0 <= new_y <= HEIGHT - self.rect.height:
            self.x = new_x
            self.y = new_y
            self.rect.x = self.x
            self.rect.y = self.y
            if dx != 0 or dy != 0:
                self.animate()

    def animate(self) -> None:
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0.0
            self.current_animation_frame = (self.current_animation_frame + 1) % len(self.color_walk)

    def take_damage(self) -> None:
        global player_lives
        if not self.damaged:
            player_lives -= 1
            self.damaged = True
            self.damage_timer = 0.0

    def update_damage(self) -> None:
        if self.damaged:
            self.damage_timer += delta_time
            if self.damage_timer >= self.damage_duration:
                self.damaged = False

    def draw(self) -> None:
        if self.damaged and int(self.damage_timer * 10) % 2 == 0:
            screen.draw.rect(self.rect, RED)
        elif self.animation_timer > 0:
            screen.draw.rect(self.rect, self.color_walk[self.current_animation_frame])
        else:
            screen.draw.rect(self.rect, self.color_idle)

"""Classe de definição e inicialização do inimigo"""
class Enemy:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.rect: Rect = Rect(x, y, 32, 32)
        self.color_idle: tuple[int, int, int] = ORANGE
        self.color_walk: list[tuple[int, int, int]] = [ORANGE, (200, 100, 0)]
        self.animation_timer: float = 0.0
        self.animation_speed: float = 0.2
        self.current_animation_frame: int = 0
        self.move_speed: int = 1

    def move_towards_avenger(self, avenger: Avenger) -> None:
        if abs(avenger.x - self.x) < 150 and abs(avenger.y - self.y) < 150:
            dx, dy = 0, 0
            if avenger.x > self.x:
                dx = self.move_speed
            elif avenger.x < self.x:
                dx = -self.move_speed
            if avenger.y > self.y:
                dy = self.move_speed
            elif avenger.y < self.y:
                dy = -self.move_speed
            self.x += dx
            self.y += dy
            self.rect.x = self.x
            self.rect.y = self.y
            self.animate()

    def animate(self) -> None:
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0.0
            self.current_animation_frame = (self.current_animation_frame + 1) % len(self.color_walk)

    def draw(self) -> None:
        screen.draw.rect(self.rect, self.color_walk[self.current_animation_frame])

"""Classe de definição e inicialização do botão"""
class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str) -> None:
        self.rect: Rect = Rect(x, y, width, height)
        self.text: str = text
        
    def draw(self) -> None:
        screen.draw.rect(self.rect, CYAN)
        screen.draw.text(self.text, self.rect.center, color=WHITE, fontsize=24, anchor=(0.5, 0.5))

    def is_clicked(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)

"""Inicializa os objetos"""
avenger = Avenger(100, 100)
enemies = [Enemy(random.randint(300, 700), random.randint(200, 500)) for _ in range(3)]
start_button = Button(WIDTH // 2 - 100, 200, 200, 40, "Start Game")
sound_button = Button(WIDTH // 2 - 100, 260, 200, 40, "Sound ON")
exit_button = Button(WIDTH // 2 - 100, 320, 200, 40, "Exit")

"""Função para iniciar o jogo"""
def on_mouse_down(pos: tuple[int, int]) -> None:
    global game_state, sound_on, sound_button
    if game_state == GAME_STATE_MENU:
        if start_button.is_clicked(pos):
            print("Botão Start Game clicado!")
            game_state = GAME_STATE_PLAYING
        elif sound_button.is_clicked(pos):
            print("Botão Sound ON/OFF clicado!")
            sound_on = not sound_on
            sound_button.text = "Sound ON" if sound_on else "Sound OFF"
        elif exit_button.is_clicked(pos):
            print("Botão Exit clicado!")
            exit()

"""Função para lidar com as setas do teclado"""
def on_key_down(key: int) -> None:
    print(f"Tecla pressionada: {key}, estado do jogo: {game_state}")
    if game_state == GAME_STATE_PLAYING:
        if key == keys.LEFT:
            avenger.move(-5, 0)
        elif key == keys.RIGHT:
            avenger.move(5, 0)
        elif key == keys.UP:
            avenger.move(0, -5)
        elif key == keys.DOWN:
            avenger.move(0, 5)

"""Função do desenho na tela"""
def draw() -> None:
    screen.clear()
    if game_state == GAME_STATE_MENU:
        screen.fill(BLACK)
        screen.draw.text("Rogue Game Menu", (WIDTH // 2, 100), color=WHITE, fontsize=24, anchor=(0.5, 0.5))
        start_button.draw() 
        sound_button.draw() 
        exit_button.draw() 
    elif game_state == GAME_STATE_PLAYING:
        screen.fill(RED if avenger.damaged else BLACK)
        avenger.draw()
        for enemy in enemies:
            enemy.draw()
        screen.draw.text(f"Lives: {player_lives}", (20, 20), color=WHITE)
        if player_lives <= 0:
            screen.draw.text("Game Over!", (WIDTH // 2, HEIGHT // 2), color=RED, fontsize=64, anchor=(0.5, 0.5))

"""Função para atualizar o jogo"""
def update():
    global game_state, player_lives, delta_time
    delta_time = 1/60 
    if game_state == GAME_STATE_PLAYING:
        print("Função update() sendo chamada")
        avenger.update_damage()
        print(f"Posição do Avenger: ({avenger.x}, {avenger.y})")
        avenger.move(0, 0)
        for enemy in enemies:
            print(f"Posição do Inimigo: ({enemy.x}, {enemy.y})")
            enemy.move_towards_avenger(avenger)
            if avenger.rect.colliderect(enemy.rect):
                print("Colisão detectada!")
                avenger.take_damage()
        if player_lives <= 0:
            game_state = GAME_STATE_MENU

pgzrun.go()

"""OBS: Não há som no jogo pois isso iria quebrar uma das regras, 
    porque seria necessário copiar uma musica da internet"""
