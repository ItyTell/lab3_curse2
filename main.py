import json
import pygame
import pygame.freetype
import random

import numpy as np
from scipy.spatial import Delaunay

import Djarvis
import Grehem
import Recursive
import Voronoi
from Edge import Edge, Segment
from colors import colors

pygame.font.init()

my_font = pygame.font.SysFont('Comic Sans MS', 25)
buttons = []
texts = ['Clear all', 'Clear edges', 'Clear segments', 'Add edges', 'Forchun', 'Delone', 'Djarvis', 'Grehem',
         'Recursive', '', '', '', '', '', '']
for text in texts:
    buttons.append(my_font.render(text, False, (0, 0, 0)))


class Game:

    def __init__(self):
        self.settings = {}
        self.edges = []
        self.segments_voronoi = []
        self.segments_delone = []
        self.segments_lin = []
        self.upload_settings()
        self.screen = pygame.display.set_mode((self.settings["screen"]["width"], self.settings["screen"]["heights"]))
        pygame.display.set_caption('Lab 3')
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.functions = [self.clear, self.edges.clear, self.clear_segments, self.add_points, self.voronoi, self.delone,
                          self.djarvis, self.grehem, self.recursive]

    def upload_settings(self):
        with open('settings.json') as file:
            file_content = file.read()
            self.settings = json.loads(file_content)
        file.close()

    def new_edge(self, cords):
        cords = np.array(cords)

        for edge1 in self.edges:
            if edge1.distance(cords) <= 18:
                return

        if cords[0] < 15 or cords[0] > 1110 or cords[1] < 15 or cords[1] > 700:
            return
        self.edges.append(Edge(cords))

    def clear(self):
        self.edges.clear()
        self.clear_segments()

    def clear_segments(self):
        self.segments_delone.clear()
        self.segments_voronoi.clear()
        self.segments_lin.clear()

    def add_points(self):
        for i in range(10):
            self.new_edge((int(1110 * random.random()), int(700 * random.random())))

    def voronoi(self):
        if len(self.edges) < 2:
            return
        diagram = Voronoi.Voronoi(self.edges)
        diagram.process()
        lines = diagram.get_output()
        for line in lines:
            self.segments_voronoi.append(Segment(line))

    def delone(self):
        if len(self.edges) < 2:
            return

        triangulation = Delaunay(self.edges)
        triangles = triangulation.simplices

        for triangle in triangles:
            self.segments_delone.append(
                Segment((self.edges[triangle[0]][0], self.edges[triangle[0]][1], self.edges[triangle[1]][0],
                         self.edges[triangle[1]][1])))
            self.segments_delone.append(
                Segment((self.edges[triangle[2]][0], self.edges[triangle[2]][1], self.edges[triangle[1]][0],
                         self.edges[triangle[1]][1])))
            self.segments_delone.append(
                Segment((self.edges[triangle[0]][0], self.edges[triangle[0]][1], self.edges[triangle[2]][0],
                         self.edges[triangle[2]][1])))

    def renew_segments(self, result):
        for i in range(len(result) - 1):
            self.segments_lin.append(Segment((result[i][0], result[i][1], result[i + 1][0], result[i + 1][1])))

    def djarvis(self):
        if len(self.edges) < 2:
            return
        result = Djarvis.djarvis(self.edges)
        self.renew_segments(result)

    def grehem(self):
        if len(self.edges) < 2:
            return
        result = Grehem.grehem(self.edges)
        self.renew_segments(result)

    def recursive(self):
        if len(self.edges) < 2:
            return
        result = Recursive.recursive(self.edges)
        self.renew_segments(result)

    def update_segments(self):
        for segment in self.segments_voronoi:
            pygame.draw.line(self.screen, colors[self.settings["segment"]["voronoi_color"]], segment.x, segment.y, width=4)

        for segment in self.segments_delone:
            pygame.draw.line(self.screen, colors[self.settings["segment"]["triangulation_color"]], segment.x, segment.y, width=4)

        for segment in self.segments_lin:
            pygame.draw.line(self.screen, colors[self.settings["segment"]["lin_color"]], segment.x, segment.y, width=4)

    def update_edges(self):

        for edge in self.edges:
            pygame.draw.circle(surface=self.screen, color=colors[self.settings["edge"]["color"]], center=edge.cords,
                               radius=8, width=0)

    def update_frames(self):

        pygame.draw.rect(self.screen, colors['white'], (self.settings["screen"]["width"] - 150, 3,
                                                        self.settings["screen"]["width"],
                                                        self.settings["screen"]["heights"]))

        pygame.draw.rect(self.screen, colors['black'], (self.settings["screen"]["width"] - 150, 3, 148,
                                                        self.settings["screen"]["heights"] - 3), width=6)

        pygame.draw.rect(self.screen, colors['black'], (3, 3, self.settings["screen"]["width"] - 6,
                                                        self.settings["screen"]["heights"] - 6), width=6)

    def update_buttons(self):
        for i, button in enumerate(buttons):
            self.screen.blit(button, (self.settings["screen"]["width"] - 140, 40 * i + 6))
            pygame.draw.rect(self.screen, colors['black'], (self.settings["screen"]["width"] - 150, 40 * i,
                                                            self.settings["screen"]["width"] - 6, 40), width=2)

    def update(self):
        self.screen.fill(colors[self.settings["screen"]["color"]])

        self.update_segments()
        self.update_edges()
        self.update_frames()
        self.update_buttons()

        pygame.display.update()

    def start(self):

        self.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if event.pos[0] < self.settings["screen"]["width"] - 150:
                            self.new_edge(event.pos)
                        else:
                            self.functions[event.pos[1] // 40]()
                        self.update()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    game = Game()
    game.start()
