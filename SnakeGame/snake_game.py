
import pygame
import random


class SnakeGame:
    # Dimensiones de la ventana del juego
    width = 640
    height = 480

    # Colores
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)

    # Instancia Singleton
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SnakeGame, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # Inicializar Pygame
        pygame.init()
        pygame.font.init()  # Inicializar el módulo de fuentes

        # Crear la fuente
        self.font = pygame.font.SysFont("comicsansms", 20)

        # Crear la ventana del juego
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")

        # Variables del juego
        self.snake_position = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.food_position = [random.randrange(
            1, self.width // 10) * 10, random.randrange(1, self.height // 10) * 10]
        self.food_spawn = True
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.score = 0

    # Función para mostrar el puntaje en la ventana
    def show_score(self):
        score_surface = self.font.render(
            "Puntuación : " + str(self.score), True, self.white)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (self.width / 2, 10)  # type: ignore
        self.window.blit(score_surface, score_rect)

    # Función principal del juego
    def game_over(self):
        game_over_surface = self.font.render(
            "¡Juego terminado! Tu puntuación es: " + str(self.score), True, self.white)
        game_over_surface_2 = self.font.render(
            "Presiona R para reiniciar el juego y Q para salir", True, self.white)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = ( # type: ignore
            self.width / 2, self.height / 4)  # type: ignore
        self.window.fill(self.black)
        self.window.blit(game_over_surface, game_over_rect)
        self.window.blit(game_over_surface_2, (self.width /
                         2 - 200, self.height / 2))  # type: ignore
        pygame.display.flip()

        # Esperar a que se presione la tecla R o Q
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart_game()
                        return
                    if event.key == pygame.K_q:
                        pygame.quit()
                        return

    # Funcion para reiniciar el juego cuando se pierde
    def restart_game(self):
        self.snake_position = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.food_position = [random.randrange(
            1, self.width // 10) * 10, random.randrange(1, self.height // 10) * 10]
        self.food_spawn = True
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.score = 0

    # Método para ejecutar el juego
    def run(self):
        # Bucle principal del juego
        while True:
            # Gestión de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                # Captura de teclas presionadas
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == ord("d"):
                        self.change_to = "RIGHT"
                    if event.key == pygame.K_LEFT or event.key == ord("a"):
                        self.change_to = "LEFT"
                    if event.key == pygame.K_UP or event.key == ord("w"):
                        self.change_to = "UP"
                    if event.key == pygame.K_DOWN or event.key == ord("s"):
                        self.change_to = "DOWN"

            # Verificar cambios válidos de dirección
            if self.change_to == "RIGHT" and self.direction != "LEFT":
                self.direction = "RIGHT"
            if self.change_to == "LEFT" and self.direction != "RIGHT":
                self.direction = "LEFT"
            if self.change_to == "UP" and self.direction != "DOWN":
                self.direction = "UP"
            if self.change_to == "DOWN" and self.direction != "UP":
                self.direction = "DOWN"

            # Actualizar la posición de la serpiente
            if self.direction == "RIGHT":
                self.snake_position[0] += 10
            if self.direction == "LEFT":
                self.snake_position[0] -= 10
            if self.direction == "UP":
                self.snake_position[1] -= 10
            if self.direction == "DOWN":
                self.snake_position[1] += 10

            # Cuerpo de la serpiente
            self.snake_body.insert(0, list(self.snake_position))
            if self.snake_position[0] == self.food_position[0] and self.snake_position[1] == self.food_position[1]:
                self.score += 1
                self.food_spawn = False
            else:
                self.snake_body.pop()

            if not self.food_spawn:
                self.food_position = [random.randrange(
                    1, self.width // 10) * 10, random.randrange(1, self.height // 10) * 10]
                self.food_spawn = True

            self.window.fill(self.black)

            for pos in self.snake_body:
                pygame.draw.rect(self.window, self.green,
                                 pygame.Rect(pos[0], pos[1], 10, 10))

            pygame.draw.rect(self.window, self.red, pygame.Rect(
                self.food_position[0], self.food_position[1], 10, 10))

            # Verificar colisiones con los bordes de la ventana
            if self.snake_position[0] >= self.width or self.snake_position[0] < 0:
                self.game_over()
            if self.snake_position[1] >= self.height or self.snake_position[1] < 0:
                self.game_over()

            # Verificar colisiones con el cuerpo de la serpiente
            for block in self.snake_body[1:]:
                if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                    self.game_over()

            self.show_score()
            pygame.display.flip()
            pygame.time.Clock().tick(20)
