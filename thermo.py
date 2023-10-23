import numpy as np
import matplotlib.pyplot as plt
import pygame
global TIPOS


TIPOS = {'ar': {'condutividade': 0.022,
                'calor_especifico': 1.005,
                'convectividade': 0.026,
                'densidade': 1.225,
                'cor': 255},
        'agua': {'condutividade': 0.58,
                'calor_especifico': 4.181,
                'convectividade': 0.58,
                'densidade': 1000,
                'cor': 0},
        'ferro': {'condutividade': 80,
                'calor_especifico': 450,
                'convectividade': 0,
                'densidade': 7860,
                'cor': 125}}
import random
class Cell:
    def __init__(self, pos , temperatura, tipo, dt):
        self.tipo = TIPOS[tipo]
        self.pos = pos
        self.capacidadeTermica = self.tipo['calor_especifico'] * self.tipo['densidade']
        self.temperatura = temperatura
        self.newTemp = temperatura
        self.coords = None
        self.dt = dt
        self.size = 1
    def update(self, coords):
        vizinho = coords[self.pos[1]][self.pos[0]+1]
        k2 = vizinho.tipo['condutividade']
        k1 = self.tipo['condutividade']
        U = 1/(((self.size/2)/k1) + ((self.size/2)/k2))
        Qcond = U*(self.temperatura - vizinho.temperatura)*self.dt
        self.temperatura -= Qcond/(self.capacidadeTermica)
        vizinho.temperatura += Qcond/(vizinho.capacidadeTermica)
        # vizinho 2
        vizinho = coords[self.pos[1]+1][self.pos[0]]
        k2 = vizinho.tipo['condutividade']
        U = 1/(((self.size/2)/k1) + ((self.size/2)/k2))
        Qcond = U*(self.temperatura - vizinho.temperatura)*self.dt
        self.temperatura -= Qcond/(self.capacidadeTermica)
        vizinho.temperatura += Qcond/(vizinho.capacidadeTermica)
        if self.tipo['convectividade'] != 0:
            chance = self.tipo['convectividade']*self.temperatura*self.dt
            if random.random() < chance:
                escolhida = random.choice([[self.pos[0], self.pos[1]-1], [self.pos[0], self.pos[1]+1],[self.pos[0]-1, self.pos[1]], [self.pos[0]+1, self.pos[1]], [self.pos[0]-1, self.pos[1]]])
                escolhida = coords[escolhida[1]][escolhida[0]]
                if escolhida.tipo['convectividade'] != 0:
                    self.temperatura, escolhida.temperatura = escolhida.temperatura+(self.temperatura-escolhida.temperatura)/2, self.temperatura-(self.temperatura-escolhida.temperatura)/2
size = 100
def generateGrid(size):
    coords = [[Cell((i, j), 0, 'ar', 0.01) for i in range(size)] for j in range(size)]
    for row in coords:
        for cell in row:
            cell.coords = coords
    return coords
coords = generateGrid(size)
rows, cols = len(coords), len(coords[0])
pygame.init()
cell_size = 8
screen = pygame.display.set_mode((int(cols * cell_size), int(rows * cell_size)))
pygame.display.set_caption("Thermo Dynamics")
def gradiente(cell):
    temp = cell.temperatura
    g = cell.tipo['cor']
    temp = max(0, min(1020, temp))
    temp = temp//4
    return (temp, g, 255-temp)
def draw_maze(coords):
    x =0 
    y = 0
    for row in coords:
        x = 0
        for cell in row:
            pygame.draw.rect(screen, gradiente(cell), (y * cell_size, x * cell_size, cell_size, cell_size))
            x+=1
        y +=1

draw_maze(coords)
botaoPlay = pygame.Rect(0, rows*cell_size - 50, 100, 50)
textoPlay = pygame.font.SysFont("Arial", 20).render("Play", True, (0, 0, 0))
textoStop = pygame.font.SysFont("Arial", 20).render("Stop", True, (0, 0, 0))
botaoClear = pygame.Rect(100, rows*cell_size -50, 100, 50)
textoClear = pygame.font.SysFont("Arial", 20).render("Clear", True, (0, 0, 0))
botaoFerro = pygame.Rect(200, rows*cell_size -50, 100, 50)
textoFerro = pygame.font.SysFont("Arial", 20).render("Ferro", True, (0, 0, 0))
botaoAgua = pygame.Rect(300, rows*cell_size -50, 100, 50)
textoAgua = pygame.font.SysFont("Arial", 20).render("Agua", True, (0, 0, 0))
botaoTemp = pygame.Rect(400, rows*cell_size -50, 100, 50)
textoTemp = pygame.font.SysFont("Arial", 20).render("Temp", True, (0, 0, 0))
botaoAr= pygame.Rect(500, rows*cell_size -50, 100, 50)
textoAr = pygame.font.SysFont("Arial", 20).render("Ar", True, (0, 0, 0))
botaoAnalise= pygame.Rect(600, rows*cell_size -50, 100, 50)
textoAnalise = pygame.font.SysFont("Arial", 20).render("Analise", True, (0, 0, 0))
brush_type = 'ferro'
Jogando = True
play = False

def atualizar(coords):
    Ncoords = coords.copy()
    for row in Ncoords:
        for cell in row:
            try:
                cell.update(Ncoords)
            except IndexError:
                pass
    return Ncoords
while Jogando:
    if play:
        pygame.draw.rect(screen, (255, 0, 0), botaoPlay)
        screen.blit(textoStop, (botaoPlay.x+10, botaoPlay.y+10))
    else:
        pygame.draw.rect(screen, (0, 255, 0), botaoPlay)
        screen.blit(textoPlay, (botaoPlay.x+10, botaoPlay.y+10))
    pygame.draw.rect(screen, (0, 0, 255), botaoFerro)
    pygame.draw.rect(screen, (255, 0, 255), botaoAgua)
    pygame.draw.rect(screen, (255, 255, 0), botaoClear)
    pygame.draw.rect(screen, (255, 255, 255), botaoTemp)
    pygame.draw.rect(screen, (0, 255, 255), botaoAr)
    screen.blit(textoAnalise, (botaoAnalise.x+10, botaoAnalise.y+10))
    screen.blit(textoClear, (botaoClear.x+10, botaoClear.y+10))
    screen.blit(textoFerro, (botaoFerro.x+10, botaoFerro.y+10))
    screen.blit(textoAgua, (botaoAgua.x+10, botaoAgua.y+10))
    screen.blit(textoTemp, (botaoTemp.x+10, botaoTemp.y+10))
    screen.blit(textoAr, (botaoAr.x+10, botaoAr.y+10))
    screen.blit(textoAnalise, (botaoAnalise.x+10, botaoAnalise.y+10))
    pygame.display.update()
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        if pos[1] < rows*cell_size - 50 and brush_type != 'analise':
            for i in range(-4,4):
                for j in range(-4,4):
                    if brush_type == 'temp':
                        coords[pos[0]//cell_size + i][pos[1]//cell_size + j].temperatura += 20
                    else:
                        coords[pos[0]//cell_size + i][pos[1]//cell_size + j].tipo = TIPOS[brush_type]    
        elif brush_type == 'analise':
            print(coords[pos[0]//cell_size][pos[1]//cell_size].temperatura)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Jogando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                coords = atualizar(coords)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if botaoPlay.collidepoint(pos):
                play = not play
            elif botaoClear.collidepoint(pos):
                coords = generateGrid(size)
            elif botaoFerro.collidepoint(pos):
                brush_type = 'ferro'
            elif botaoAgua.collidepoint(pos):
                brush_type = 'agua'
            elif botaoTemp.collidepoint(pos):
                brush_type = 'temp'
            elif botaoAr.collidepoint(pos):
                brush_type = 'ar'
            elif botaoAnalise.collidepoint(pos):
                brush_type = 'analise'

    if play:
        pass
        coords = atualizar(coords)
    draw_maze(coords)
