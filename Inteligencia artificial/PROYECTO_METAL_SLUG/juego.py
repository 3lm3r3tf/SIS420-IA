import pygame
import torch
import torch.nn as nn
import numpy as np
import time

# Estructura de la Red DQN
class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, 24),
            nn.ReLU(),
            nn.Linear(24, 24),
            nn.ReLU(),
            nn.Linear(24, output_dim)
        )
    def forward(self, x):
        return self.fc(x)

# Cargar el modelo entrenado
input_dim = 2
output_dim = 3
modelo_cargado = DQN(input_dim, output_dim)
modelo_cargado.load_state_dict(torch.load("PROYECTO_METAL_SLUG/modelo_metal_slug_dqn.pth"))
modelo_cargado.eval()

# Inicializar Pygame
pygame.init()
ANCHO, ALTO = 800, 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("IA Jugando - Estilo Metal Slug (DQN)")
reloj = pygame.time.Clock()

BLANCO = (255, 255, 255)
AZUL = (50, 150, 250)
ROJO = (220, 50, 50)
NEGRO = (20, 20, 20)
VERDE = (50, 200, 100)

def ejecutar_partida_visual():
    jugador_x_pos = 0
    obstaculo_x_pos = 10
    jugador_screen_x = 100
    suelo_y = 300
    jugador_y = suelo_y
    en_aire = False
    salto_contador = 0
    terminado = False
    puntaje = 0
    
    while True:
        pantalla.fill(BLANCO)
        pygame.draw.rect(pantalla, VERDE, (0, suelo_y + 20, ANCHO, 100))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

        if not terminado:
            estado = np.array([jugador_x_pos, obstaculo_x_pos], dtype=np.float32)
            with torch.no_grad():
                q