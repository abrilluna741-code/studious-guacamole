# Integración del menú con el gameplay

import pygame
import sys
import time
import random
from enum import Enum
from fractions import Fraction
import json
import os

pygame.init()
pygame.mixer.init()

# =====================================================
# PANTALLA
# =====================================================
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ecuaciones")

# =====================================================
# COLORES
# =====================================================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (100, 100, 100)
DARK_BLUE = (0, 0, 35)
GREEN = (0, 255, 0)
RED = (255, 80, 80)
LIGHT_BLUE = (180, 180, 255)

# =====================================================
# FUENTES
# =====================================================
font = pygame.font.SysFont(None, 30)
font_big = pygame.font.Font(None, 60)
font_med = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)

# =====================================================
# ENUMS
# =====================================================
class EstadoMenu(Enum):
    PRINCIPAL = 0
    MODOS = 1
    DIFICULTAD = 2
    ESTADISTICAS = 3
    GAMEPLAY = 4

class ModoJuego(Enum):
    MODO1 = 0
    MODO2 = 1

# =====================================================
# VARIABLES GLOBALES
# =====================================================
estado = EstadoMenu.PRINCIPAL
modo_actual = None

dificultad = "facil"
# =====================================================
# ESTADISTICAS
# =====================================================

estadisticas = []

archivo_estadisticas = "estadisticas.json"

def cargar_estadisticas():

    global estadisticas

    if os.path.exists(archivo_estadisticas):

        with open(archivo_estadisticas, "r") as archivo:

            estadisticas = json.load(archivo)

def guardar_estadisticas():

    with open(archivo_estadisticas, "w") as archivo:

        json.dump(estadisticas, archivo, indent=4)

def guardar_partida(
    modo,
    score,
    aciertos,
    errores,
    racha_max,
    tiempo
):

    partida = {

        "modo": modo,
        "score": score,
        "aciertos": aciertos,
        "errores": errores,
        "racha_max": racha_max,
        "tiempo": tiempo
    }

    estadisticas.append(partida)

    if len(estadisticas) > 5:
        estadisticas.pop(0)

    guardar_estadisticas()

cargar_estadisticas()


# =====================================================
# GENERADOR DE PREGUNTAS
# =====================================================
def creador_preguntas(dificultad="facil"):

    if dificultad == "facil":

        x = random.randint(-10, 10)
        a = random.randint(1, 10)
        c = random.randint(1, 10)

        while a == c:
            c = random.randint(1, 10)

        b = random.randint(-20, 20)
        d = a * x + b - c * x

    elif dificultad == "medio":

        x = random.randint(-10, 10) / random.randint(2, 5)

        a = random.randint(1, 10)
        c = random.randint(1, 10)

        while a == c:
            c = random.randint(1, 10)

        b = random.randint(-20, 20)
        d = a * x + b - c * x

    else:

        x = round(random.uniform(-10, 10), 2)

        a = round(random.uniform(0.5, 10), 2)
        c = round(random.uniform(0.5, 10), 2)

        while abs(a - c) < 0.1:
            c = round(random.uniform(0.5, 10), 2)

        b = round(random.uniform(-20, 20), 2)
        d = round(a * x + b - c * x, 2)

    return [a, b, c, d, x]

# =====================================================
# CONFIG MODOS
# =====================================================
def setMode_setDifficulty_Balance(dif="facil", modo='1'):

    time_duration = 90
    attempt_limit = 5

    if modo == '1':
        return time_duration

    elif modo == '2':

        if dif == "facil":
            attempt_limit = 8

        elif dif == "medio":
            attempt_limit = 6

        elif dif == "dificil":
            attempt_limit = 4

        return attempt_limit

    return False

# =====================================================
# BOTON
# =====================================================
class Button:

    def __init__(self, text, x, y, w, h):

        self.text = text

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, screen):

        mouse_pos = pygame.mouse.get_pos()

        hovered = self.rect.collidepoint(mouse_pos)

        if hovered:

            draw_rect = pygame.Rect(
                self.x - 5,
                self.y - 5,
                self.w + 10,
                self.h + 10
            )

            color = DARK_GRAY

        else:

            draw_rect = pygame.Rect(
                self.x,
                self.y,
                self.w,
                self.h
            )

            color = GRAY

        pygame.draw.rect(screen, color, draw_rect)
        pygame.draw.rect(screen, BLACK, draw_rect, 2)

        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=draw_rect.center)

        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# =====================================================
# BOTONES
# =====================================================
btn_modos = Button("Modos de Juego", 280, 150, 240, 50)
btn_stats = Button("Estadisticas", 280, 220, 240, 50)

btn_modo1 = Button("Modo 1", 280, 150, 240, 50)
btn_modo2 = Button("Modo 2", 280, 220, 240, 50)

btn_facil = Button("Facil", 280, 140, 240, 50)
btn_medio = Button("Medio", 280, 210, 240, 50)
btn_dificil = Button("Dificil", 280, 280, 240, 50)

btn_back = Button("Regresar", 10, 10, 120, 40)

# =====================================================
# VARIABLES GAMEPLAY
# =====================================================
start = 0
attempts = 0
correctos = 0
errores = 0
score = 0
racha = 0
racha_max = 0
input_str = ""
feedback = ""
feedback_color = WHITE

problemCurrent = creador_preguntas(dificultad)

a = problemCurrent[0]
b = problemCurrent[1]
c = problemCurrent[2]
d = problemCurrent[3]
result = problemCurrent[4]

eq_text = f"{a}x + {b} = {c}x + {d}"

limit_variable = 90

# =====================================================
# FUNCION INICIAR JUEGO
# =====================================================
def iniciar_juego():

    global start
    global attempts
    global correctos
    global input_str
    global feedback
    global feedback_color
    global problemCurrent
    global a, b, c, d, result
    global eq_text
    global limit_variable
    global errores
    global score
    global racha
    global racha_max

    start = time.time()

    attempts = 0
    correctos = 0
    errores = 0
    score = 0
    racha = 0
    racha_max = 0

    input_str = ""
    feedback = ""
    feedback_color = WHITE

    problemCurrent = creador_preguntas(dificultad)

    a = problemCurrent[0]
    b = problemCurrent[1]
    c = problemCurrent[2]
    d = problemCurrent[3]
    result = problemCurrent[4]

    eq_text = f"{a}x + {b} = {c}x + {d}"

    if modo_actual == ModoJuego.MODO1:
        limit_variable = setMode_setDifficulty_Balance(dificultad, '1')

    elif modo_actual == ModoJuego.MODO2:
        limit_variable = setMode_setDifficulty_Balance(dificultad, '2')

# =====================================================
# LOOP PRINCIPAL
# =====================================================
while True:

    screen.fill(DARK_BLUE)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # =====================================================
        # CLICKS MENU
        # =====================================================
        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            if estado == EstadoMenu.PRINCIPAL:

                if btn_modos.is_clicked(mouse_pos):
                    estado = EstadoMenu.MODOS

                if btn_stats.is_clicked(mouse_pos):
                    estado = EstadoMenu.ESTADISTICAS

            elif estado == EstadoMenu.MODOS:

                if btn_modo1.is_clicked(mouse_pos):

                    modo_actual = ModoJuego.MODO1
                    estado = EstadoMenu.DIFICULTAD

                if btn_modo2.is_clicked(mouse_pos):

                    modo_actual = ModoJuego.MODO2
                    estado = EstadoMenu.DIFICULTAD

                if btn_back.is_clicked(mouse_pos):
                    estado = EstadoMenu.PRINCIPAL

            elif estado == EstadoMenu.DIFICULTAD:

                if btn_facil.is_clicked(mouse_pos):

                    dificultad = "facil"
                    iniciar_juego()
                    estado = EstadoMenu.GAMEPLAY

                if btn_medio.is_clicked(mouse_pos):

                    dificultad = "medio"
                    iniciar_juego()
                    estado = EstadoMenu.GAMEPLAY

                if btn_dificil.is_clicked(mouse_pos):

                    dificultad = "dificil"
                    iniciar_juego()
                    estado = EstadoMenu.GAMEPLAY

                if btn_back.is_clicked(mouse_pos):
                    estado = EstadoMenu.MODOS

            elif estado == EstadoMenu.ESTADISTICAS:

                if btn_back.is_clicked(mouse_pos):
                    estado = EstadoMenu.PRINCIPAL

        # =====================================================
        # GAMEPLAY INPUT
        # =====================================================
        if estado == EstadoMenu.GAMEPLAY:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN and input_str != "":

                    try:
                        n1 = float(input_str)

                        attempts += 1

                        lhs = a * n1 + b
                        rhs = c * n1 + d

                        if abs(n1 - result) < 0.01:

                            feedback = f"Correcto | x = {result}"
                            feedback_color = GREEN

                            correctos += 1

                            score += 100

                            racha += 1

                            if racha > racha_max:
                                 racha_max = racha

                            problemCurrent = creador_preguntas(dificultad)

                            a = problemCurrent[0]
                            b = problemCurrent[1]
                            c = problemCurrent[2]
                            d = problemCurrent[3]
                            result = problemCurrent[4]

                            eq_text = f"{a}x + {b} = {c}x + {d}"

                        elif lhs > rhs:
                            errores += 1
                            racha = 0
                            feedback = f"{lhs} > {rhs}"
                            feedback_color = RED

                        else:
                            
                            errores += 1
                            racha = 0
                            feedback = f"{lhs} < {rhs}"
                            feedback_color = RED

                        input_str = ""

                    except ValueError:
                        input_str = ""

                elif event.key == pygame.K_BACKSPACE:
                    input_str = input_str[:-1]

                elif event.unicode in "0123456789.-":
                    input_str += event.unicode

                elif event.key == pygame.K_ESCAPE:
                    estado = EstadoMenu.PRINCIPAL

    # =====================================================
    # CURSOR
    # =====================================================
    hovering = False

    mouse_pos = pygame.mouse.get_pos()

    if estado == EstadoMenu.PRINCIPAL:

        if (
            btn_modos.rect.collidepoint(mouse_pos)
            or btn_stats.rect.collidepoint(mouse_pos)
        ):
            hovering = True

    elif estado == EstadoMenu.MODOS:

        if (
            btn_modo1.rect.collidepoint(mouse_pos)
            or btn_modo2.rect.collidepoint(mouse_pos)
            or btn_back.rect.collidepoint(mouse_pos)
        ):
            hovering = True

    elif estado == EstadoMenu.DIFICULTAD:

        if (
            btn_facil.rect.collidepoint(mouse_pos)
            or btn_medio.rect.collidepoint(mouse_pos)
            or btn_dificil.rect.collidepoint(mouse_pos)
            or btn_back.rect.collidepoint(mouse_pos)
        ):
            hovering = True

    elif estado == EstadoMenu.ESTADISTICAS:

        if btn_back.rect.collidepoint(mouse_pos):
            hovering = True

    if hovering:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    # =====================================================
    # DIBUJAR MENU PRINCIPAL
    # =====================================================
    if estado == EstadoMenu.PRINCIPAL:

        titulo = font_big.render("MENU PRINCIPAL", True, WHITE)
        screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 70))

        btn_modos.draw(screen)
        btn_stats.draw(screen)

    # =====================================================
    # DIBUJAR MODOS
    # =====================================================
    elif estado == EstadoMenu.MODOS:

        titulo = font_big.render("SELECCIONA UN MODO", True, WHITE)
        screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 70))

        btn_modo1.draw(screen)
        btn_modo2.draw(screen)
        btn_back.draw(screen)

    # =====================================================
    # DIBUJAR DIFICULTAD
    # =====================================================
    elif estado == EstadoMenu.DIFICULTAD:

        titulo = font_big.render("SELECCIONA DIFICULTAD", True, WHITE)
        screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 70))

        btn_facil.draw(screen)
        btn_medio.draw(screen)
        btn_dificil.draw(screen)
        btn_back.draw(screen)

    # =====================================================
    # DIBUJAR ESTADISTICAS
    # =====================================================
    elif estado == EstadoMenu.ESTADISTICAS:

        titulo = font_big.render("ESTADISTICAS", True, WHITE)
        screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 30))

        btn_back.draw(screen)

        if len(estadisticas) == 0:
            texto = font_med.render(
                "No hay partidas guardadas",
                True,
                WHITE
            )
            screen.blit(texto, (180, 220))
        else:
            y = 100
            for partida in reversed(estadisticas):
                texto1 = font_small.render(
                    f"{partida['modo']} | Score: {partida['score']}",
                    True,
                    WHITE
                )
                texto2 = font_small.render(
                    f"Aciertos: {partida['aciertos']} | "
                    f"Errores: {partida['errores']}",
                    True,
                    WHITE
                )
                texto3 = font_small.render(
                    f"Racha Max: {partida['racha_max']} | "
                    f"Tiempo: {partida['tiempo']} s",
                    True,
                    WHITE
                )
                screen.blit(texto1, (120, y))
                screen.blit(texto2, (120, y + 30))
                screen.blit(texto3, (120, y + 60))
                y += 100

    # =====================================================
    # GAMEPLAY
    # =====================================================
    elif estado == EstadoMenu.GAMEPLAY:

        if modo_actual == ModoJuego.MODO1:

            tiempo_restante = max(0, int(limit_variable - (time.time() - start)))

            tiempo_text = font_small.render(
                f"Tiempo restante: {tiempo_restante}",
                True,
                WHITE
            )

            screen.blit(tiempo_text, (20, 20))
            score_text = font_small.render(
            f"Score: {score}",
            True,
            WHITE
            )

            screen.blit(score_text, (20, 60))

            if tiempo_restante <= 0:
                guardar_partida(
                "Modo 1",
                score,
                correctos,
                errores,
                racha_max,
                limit_variable
                )

                estado = EstadoMenu.PRINCIPAL

        elif modo_actual == ModoJuego.MODO2:

            intentos_restantes = max(0, limit_variable - attempts)

            intentos_text = font_small.render(
                f"Intentos restantes: {intentos_restantes}",
                True,
                WHITE
            )

            screen.blit(intentos_text, (20, 20))
            score_text = font_small.render(
            f"Score: {score}",
            True,
            WHITE
            )

            screen.blit(score_text, (20, 60))

            if intentos_restantes <= 0:
                tiempo_jugado = int(time.time() - start)
                
                guardar_partida(
                    "Modo 2",
                    score,
                    correctos,
                    errores,
                    racha_max,
                    tiempo_jugado
                )
                estado = EstadoMenu.PRINCIPAL

        eq_surf = font_big.render(eq_text, True, WHITE)
        screen.blit(eq_surf, (400 - eq_surf.get_width() // 2, 150))

        prompt = font_med.render(f"x = {input_str}_", True, LIGHT_BLUE)
        screen.blit(prompt, (400 - prompt.get_width() // 2, 250))

        if feedback:

            fb_surf = font_small.render(feedback, True, feedback_color)
            screen.blit(fb_surf, (400 - fb_surf.get_width() // 2, 340))

        hint = font_small.render(
            f"Intentos = {attempts}. Correctos = {correctos}. ESC para salir",
            True,
            GRAY
        )

        screen.blit(hint, (180, 430))

    pygame.display.flip()
