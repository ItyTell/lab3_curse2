import random
import pygame
import pygame.freetype
import numpy as np
import json
from colors import colors
from Edge import Edge, Segment
import Voronoi
import Djarvis
import Grehem
import Recursive

pygame.font.init()

my_font = pygame.font.SysFont('Comic Sans MS', 25)
buttons = []
texts = ['Clear', 'Add edges', 'Forchun', 'Delone', 'Djarvis', 'Grehem', 'Recursive']
for text in texts:
    buttons.append(my_font.render(text, False, (0, 0, 0)))


def new_edge(cords):
    cords = np.array(cords)

    for edge1 in Edge.edges:
        if edge1.distance(cords) <= 18:
            return

    if cords[0] < 15 or cords[0] > 1110 or cords[1] < 15 or cords[1] > 700:
        return
    Edge(cords)


def clear():
    Edge.edges.clear()
    Segment.segments.clear()


def add_points():
    for i in range(10):
        new_edge((int(1110 * random.random()), int(700 * random.random())))


def voronoi():
    if len(Edge.edges) < 2:
        return
    diagram = Voronoi.Voronoi(Edge.edges)
    diagram.process()
    lines = diagram.get_output()
    Segment.segments.clear()
    for line in lines:
        Segment(line)


def delone():
    pass


def renew_segments(result):
    Segment.segments.clear()
    for i in range(len(result) - 1):
        Segment((result[i][0], result[i][1], result[i + 1][0], result[i + 1][1]))


def djarvis():
    if len(Edge.edges) < 2:
        return
    result = Djarvis.djarvis(Edge.edges)
    renew_segments(result)


def grehem():
    if len(Edge.edges) < 2:
        return
    result = Grehem.grehem(Edge.edges)
    renew_segments(result)


def recursive():
    if len(Edge.edges) < 2:
        return
    result = Recursive.recursive(Edge.edges)
    renew_segments(result)


def update_segments(screen, segment_color):
    for segment in Segment.segments:
        pygame.draw.line(screen, segment_color, segment.x, segment.y, width=4)


def update_edges(screen, edge_color):
    for edge in Edge.edges:
        pygame.draw.circle(surface=screen, color=edge_color, center=edge.cords, radius=8, width=0)


def update_frames(screen, width, heights):
    pygame.draw.rect(screen, colors['white'], (width - 150, 3, width, heights))
    pygame.draw.rect(screen, colors['black'], (width - 150, 3, 148, heights - 3), width=6)
    pygame.draw.rect(screen, colors['black'], (3, 3, width - 6, heights - 6), width=6)


def update_buttons(screen, width, heights):
    for i, button in enumerate(buttons):
        screen.blit(button, (width - 135, 40 * i + 6))
        pygame.draw.rect(screen, colors['black'], (width - 150, 40 * i, width - 6, 40), width=2)


def update(screen, settings):
    screen.fill(colors[settings["screen"]["color"]])

    update_segments(screen, segment_color=colors[settings["segment"]["color"]])
    update_edges(screen, edge_color=colors[settings["edge"]["color"]])
    update_frames(screen, width=settings["screen"]["width"], heights=settings["screen"]["heights"])
    update_buttons(screen, width=settings["screen"]["width"], heights=settings["screen"]["heights"])

    pygame.display.update()


def begin():

    with open('settings.json') as file:
        file_content = file.read()
        settings = json.loads(file_content)

    screen = pygame.display.set_mode((settings["screen"]["width"], settings["screen"]["heights"]))
    pygame.display.set_caption('Lab 3')
    clock = pygame.time.Clock()
    fps = 60

    update(screen, settings)

    functions = [clear, add_points, voronoi, delone, djarvis, grehem, recursive]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if event.pos[0] < settings["screen"]["width"] - 150:
                        new_edge(event.pos)
                    else:
                        functions[event.pos[1] // 40]()
                    update(screen, settings)
        clock.tick(fps)


if __name__ == '__main__':
    begin()
