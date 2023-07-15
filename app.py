import pygame
import random

# Dimensiones de la ventana del juego
width = 640
height = 480

# Colores
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Inicializar Pygame
pygame.init()
pygame.font.init()  # Inicializar el módulo de fuentes

# Ruta de la fuente descargada
font_path = "fonts/Ubuntu/Ubuntu-Medium.ttf"

# Tamaño de la fuente
font_size = 24

# Crear la fuente
font = pygame.font.SysFont("comicsansms", 20)

# Crear la ventana del juego
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Variables del juego
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
food_position = [random.randrange(
    1, width // 10) * 10, random.randrange(1, height // 10) * 10]
food_spawn = True
direction = "RIGHT"
change_to = direction
score = 0

# Variables de los botones
restart_rect = pygame.Rect(0, 0, 0, 0)
quit_rect = pygame.Rect(0, 0, 0, 0)

# Función para mostrar el puntaje en la ventana


def show_score():
    score_surface = font.render("Puntuación : " + str(score), True, white)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (width / 2, 10)  # type: ignore
    window.blit(score_surface, score_rect)

# Función para mostrar los botones en la ventana


def show_buttons():
    restart_surface = font.render("Reiniciar", True, white)
    restart_rect = restart_surface.get_rect()
    restart_rect.center = (width / 2, height / 2 - 20) # type: ignore
    pygame.draw.rect(window, green, restart_rect)
    window.blit(restart_surface, restart_rect)

    quit_surface = font.render("Cerrar", True, white)
    quit_rect = quit_surface.get_rect()
    quit_rect.center = (width / 2, height / 2 + 20) # type: ignore
    pygame.draw.rect(window, red, quit_rect)
    window.blit(quit_surface, quit_rect)

# Función principal del juego


def game_over():
    while True:
        # Gestión de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_rect.collidepoint(mouse_pos):
                    restart()
                    return
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    return

        game_over_surface = font.render("¡Juego terminado!", True, white)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (width / 2, height / 4)  # type: ignore
        window.fill(black)
        window.blit(game_over_surface, game_over_rect)
        show_score()
        show_buttons()
        pygame.display.flip()
        pygame.time.Clock().tick(20)

# Funcion para reiniciar el juego


def restart():
    global snake_position, snake_body, food_position, food_spawn, direction, change_to, score
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    food_position = [random.randrange(
        1, width // 10) * 10, random.randrange(1, height // 10) * 10]
    food_spawn = True
    direction = "RIGHT"
    change_to = direction
    score = 0


# Bucle principal del juego
while True:
    # Gestión de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        # Captura de teclas presionadas
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord("d"):
                change_to = "RIGHT"
            if event.key == pygame.K_LEFT or event.key == ord("a"):
                change_to = "LEFT"
            if event.key == pygame.K_UP or event.key == ord("w"):
                change_to = "UP"
            if event.key == pygame.K_DOWN or event.key == ord("s"):
                change_to = "DOWN"

    # Verificar cambios válidos de dirección
    if change_to == "RIGHT" and direction != "LEFT":
        direction = "RIGHT"
    if change_to == "LEFT" and direction != "RIGHT":
        direction = "LEFT"
    if change_to == "UP" and direction != "DOWN":
        direction = "UP"
    if change_to == "DOWN" and direction != "UP":
        direction = "DOWN"

    # Actualizar la posición de la serpiente
    if direction == "RIGHT":
        snake_position[0] += 10
    if direction == "LEFT":
        snake_position[0] -= 10
    if direction == "UP":
        snake_position[1] -= 10
    if direction == "DOWN":
        snake_position[1] += 10

    # Cuerpo de la serpiente
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_position = [random.randrange(
            1, width // 10) * 10, random.randrange(1, height // 10) * 10]
        food_spawn = True

    window.fill(black)

    for pos in snake_body:
        pygame.draw.rect(window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(window, red, pygame.Rect(
        food_position[0], food_position[1], 10, 10))

    # Verificar colisiones con los bordes de la ventana
    if snake_position[0] >= width or snake_position[0] < 0:
        game_over()
    if snake_position[1] >= height or snake_position[1] < 0:
        game_over()

    # Verificar colisiones con el cuerpo de la serpiente
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    show_score()
    pygame.display.flip()
    pygame.time.Clock().tick(20)
