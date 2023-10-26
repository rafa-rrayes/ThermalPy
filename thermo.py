import numpy as np
import matplotlib.pyplot as plt
import pygame
import random

global TIPOS
TIPOS = {'play': {'gradiente': [[201, 236, 254],[255, 153, 72]]},
        'clear': {'gradiente': [[255,255, 0],[165, 0, 85]]},
        'temp': {'gradiente': [[255, 95, 115], [255, 0, 0]]},
        'ar': {'condutividade': 0.022,
                'calor_especifico': 1.005,
                'convectividade': 0.26,
                'densidade': 1.225,
                'tempMax': 100,
                'gradiente': [[201, 236, 254],[255, 153, 72]]},
        'agua': {'condutividade': 0.58,
                'calor_especifico': 4.181,
                'convectividade': 0.58,
                'densidade': 1000,
                'tempMax': 200,
                'gradiente': [[0, 0, 255],[165, 0, 85]]},
        'ferro': {'condutividade': 80,
                'calor_especifico': 450,
                'convectividade': 0,
                'densidade': 7860,
                'tempMax': 1500,
                'gradiente': [[136, 140, 140], [255, 0, 0]]},
        'pedra': {'condutividade': 1.8,
                'calor_especifico': 1000,
                'convectividade': 0,
                'densidade': 2500,
                'tempMax': 2000,
                'gradiente': [[90, 100, 100], [255, 0, 0]]}}

# Funcoes
def gradiente(cell):
    temp = cell.temperatura
    if temp == 0:
        return (cell.tipo['gradiente'][0])
    elif temp >= cell.tipo['tempMax']:
        return (cell.tipo['gradiente'][1])
    multiplicador = temp/cell.tipo['tempMax']
    start, finnish = cell.tipo['gradiente']
    cor = [(1 - multiplicador) * start[i] + multiplicador * finnish[i] for i in range(3)]
    return cor
def generateGrid(size):
    coords = [[Cell((i, j), 0, 'ar', 0.01) for i in range(size)] for j in range(size)]
    for row in coords:
        for cell in row:
            cell.coords = coords
    return coords
def draw_maze(coords):
    x =0 
    y = 0
    for row in coords:
        x = 0
        for cell in row:
            pygame.draw.rect(screen, gradiente(cell), (y * cell_size, x * cell_size, cell_size, cell_size))
            x+=1
        y +=1
def atualizar(coords, coords2):
    for row in coords:
        for cell in row:
            try:
                cell.update(coords, coords2)
            except IndexError:
                pass
    return coords2
def calcularEnergia(coords):
    energia = 0
    for row in coords:
        for cell in row:
            energia += cell.temperatura*cell.capacidadeTermica
    return energia
# Cell class
class Cell:
    def __init__(self, pos , temperatura, tipo, dt):
        self.tipo = TIPOS[tipo]
        self.pos = pos
        self.capacidadeTermica = self.tipo['calor_especifico'] * self.tipo['densidade']
        self.temperatura = temperatura
        self.coords = None
        self.dt = dt
        self.size = 1
    def update(self, coords, coords2):
        proprio = coords2[self.pos[1]][self.pos[0]]
        vizinhoProprio = coords2[self.pos[1]][self.pos[0]+1]
        vizinho = coords[self.pos[1]][self.pos[0]+1]
        k2 = vizinho.tipo['condutividade']
        k1 = self.tipo['condutividade']
        U = 1/(((self.size/2)/k1) + ((self.size/2)/k2))
        Qcond = U*(self.temperatura - vizinho.temperatura)*self.dt
        proprio.temperatura -= Qcond/(self.capacidadeTermica)
        vizinhoProprio.temperatura += Qcond/(vizinho.capacidadeTermica)
        #vizinho 2
        vizinho2 = coords[self.pos[1]+1][self.pos[0]]
        vizinhoProprio2 = coords2[self.pos[1]+1][self.pos[0]]
        k2 = vizinho2.tipo['condutividade']
        U = 1/(((self.size/2)/k1) + ((self.size/2)/k2))
        Qcond = U*(self.temperatura - vizinho2.temperatura)*self.dt
        proprio.temperatura -= Qcond/(self.capacidadeTermica)
        vizinhoProprio2.temperatura += Qcond/(vizinho2.capacidadeTermica)
        #Convecção
        if self.tipo['convectividade'] != 0:
            chance = self.tipo['convectividade']*self.temperatura*self.dt
            if random.random() < chance:
                escolhida = random.choice([[self.pos[0], self.pos[1]-1], [self.pos[0], self.pos[1]+1],[self.pos[0]-1, self.pos[1]], [self.pos[0]+1, self.pos[1]], [self.pos[0]-1, self.pos[1]], [self.pos[0]-1, self.pos[1]]])
                escolhida = coords2[escolhida[1]][escolhida[0]]
                if escolhida.tipo == self.tipo:
                    proprio.temperatura, escolhida.temperatura = escolhida.temperatura+(self.temperatura-escolhida.temperatura)/10, self.temperatura-(self.temperatura-escolhida.temperatura)/10
size = 100
coords, coords2 = generateGrid(size), generateGrid(size)
cell_size = 8

# Pygame screen, buttons and text setup
pygame.init()
screen = pygame.display.set_mode((int(size * cell_size), int(size * cell_size)))
pygame.display.set_caption("Thermo Dynamics")
botaoPlay = pygame.Rect(0, size*cell_size - 50, 100, 50)
textoPlay = pygame.font.SysFont("Arial", 20).render("Play", True, (0, 0, 0))
textoStop = pygame.font.SysFont("Arial", 20).render("Stop", True, (0, 0, 0))
textoTemperatura = pygame.font.SysFont("Arial", 20)
botoes = []
posx = 0
for tipo, info in TIPOS.items():
        botao = pygame.Rect(posx, size*cell_size -50, 100, 50)
        texto = pygame.font.SysFont("Arial", 20).render(tipo, True, (0, 0, 0))
        botoes.append([botao, info, texto, tipo])
        posx += 100
brush_type = 'ferro'
Jogando = True
play = False
clock = pygame.time.Clock()
while Jogando:
    if play: # Se a simulação estiver rodando, botão de play vira stop e vermelho
        pygame.draw.rect(screen, (255, 0, 0), botaoPlay) 
        screen.blit(textoStop, (botaoPlay.x+10, botaoPlay.y+10))
    else: # Se a simulação estiver parada, botão de play vira play e verde
        pygame.draw.rect(screen, (0, 255, 0), botaoPlay)
        screen.blit(textoPlay, (botaoPlay.x+10, botaoPlay.y+10))
    # Desenhar Botoes
    for botao in botoes:
        if botao[3] != 'play':
            pygame.draw.rect(screen, botao[1]['gradiente'][0], botao[0])
            screen.blit(botao[2], (botao[0].x+10, botao[0].y+10))

    pos = pygame.mouse.get_pos()
    temp = coords[pos[0]//cell_size][pos[1]//cell_size].temperatura 
    screen.blit(textoTemperatura.render(f'Temperatura:{round(temp, 2)}', True, (0, 0, 255)), (0, 0)) # Mostrar temperatura do mouse
    pygame.display.update()
    if pygame.mouse.get_pressed()[0]:
        if pos[1] < size*cell_size - 50:
            for i in range(-4,4):
                for j in range(-4,4):
                    if brush_type == 'temp':
                        coords[pos[0]//cell_size + i][pos[1]//cell_size + j].temperatura += 10
                        coords2[pos[0]//cell_size + i][pos[1]//cell_size + j].temperatura += 10
                    elif brush_type == 'tempMenos':
                        coords[pos[0]//cell_size + i][pos[1]//cell_size + j].temperatura -= 10
                        coords2[pos[0]//cell_size + i][pos[1]//cell_size + j].temperatura -= 10
                        if coords[pos[0]//cell_size + i][pos[1]//cell_size + j].temperatura < 0:
                            coords[pos[0]//cell_size + i][pos[1]//cell_size + j].temperatura = 0
                            coords2[pos[0]//cell_size + i][pos[1]//cell_size + j].temperatura = 0
                    else:
                        coords[pos[0]//cell_size + i][pos[1]//cell_size + j].tipo = TIPOS[brush_type]
                        coords2[pos[0]//cell_size + i][pos[1]//cell_size + j].tipo = TIPOS[brush_type]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Jogando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                coords = atualizar(coords, coords2)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for botao in botoes:
                if botao[0].collidepoint(pos):
                    if botao[3] == 'clear':
                        coords = generateGrid(size)
                        coords2 = generateGrid(size)
                    elif botao[3] == 'play':
                        play = not play
                    else:
                        brush_type = botao[3]
    if play:
        coords = atualizar(coords, coords2)
    draw_maze(coords)
    clock.tick(60)