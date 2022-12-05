import json
import math

import pygame
import pygame.freetype
import random

import numpy as np
import scipy.constants
from scipy.spatial import Delaunay

import Djarvis
import Grehem
import Recursive
import Voronoi
from Edge import Edge, Segment
from colors import colors

pygame.font.init()


def engels_norm(alfa):
    while alfa > math.pi / 2:
        alfa -= 2 * math.pi
    while alfa < -math.pi / 2:
        alfa += 2 * math.pi
    return alfa


class Game:

    def __init__(self):
        self.settings = {}
        self.edges = []
        self.segments_voronoi = []
        self.segments_delone = []
        self.segments_lin = []
        self.buttons = []

        self.upload_settings()
        self.upload_buttons()

        self.screen = pygame.display.set_mode((self.settings["screen"]["width"], self.settings["screen"]["heights"]))
        self.screen.fill(colors[self.settings["screen"]["color"]])

        pygame.display.set_caption('Lab 3')
        self.clock = pygame.time.Clock()
        self.fps = 100
        self.functions = [self.clear, self.edges.clear, self.clear_segments, self.add_some_points,
                          self.add_many_points, self.voronoi, self.delone, self.djarvis, self.grehem,
                          self.recursive, self.movement]
        self.is_moving = False
        self.angels = []

        self.distance = 5
        self.rad_edges = 10
        self.menu_width = 150

    def upload_settings(self):
        with open('settings.json') as file:
            file_content = file.read()
            self.settings = json.loads(file_content)
        file.close()

    def upload_buttons(self):
        my_font = pygame.font.SysFont('Comic Sans MS', 25)
        texts = ['Clear all', 'Clear edges', 'Clear segments', 'Add edges', 'Add more edges', 'Forchun', 'Delone',
                 'Djarvis', 'Grehem', 'Recursive', 'Move', 'Voronoi on', 'Delone on', 'Lin on', '', '', '', '']
        for text in texts:
            self.buttons.append(my_font.render(text, False, (0, 0, 0)))

    def check_edge(self, cords):
        cords = np.array(cords)

        for edge1 in self.edges:
            if edge1.distance(cords) < 2 * self.rad_edges:
                return True

        if cords[0] < self.rad_edges + self.distance or \
                cords[0] > self.settings["screen"]["width"] - self.menu_width - self.distance - self.rad_edges or \
                cords[1] < self.rad_edges + self.distance or \
                cords[1] > self.settings["screen"]["heights"] - self.rad_edges - + self.distance:
            return True

        return False

    def new_edge(self, cords):

        if self.check_edge(cords):
            return

        self.edges.append(Edge(cords))

        if self.is_moving:
            self.angels.append(random.random() * 2 * scipy.constants.pi)

    def clear(self):
        self.screen.fill(colors[self.settings["screen"]["color"]])
        self.edges.clear()
        self.clear_segments()
        self.angels.clear()

    def clear_segments(self):
        self.screen.fill(colors[self.settings["screen"]["color"]])
        self.segments_delone.clear()
        self.segments_voronoi.clear()
        self.segments_lin.clear()

    def add_points(self, k):
        for i in range(k):
            self.new_edge((
                int((self.settings["screen"]["width"] - self.menu_width -
                     self.distance - self.rad_edges) * random.random()),
                int((self.settings["screen"]["heights"] - self.rad_edges - + self.distance) * random.random())))

    def add_some_points(self):
        self.add_points(10)

    def add_many_points(self):
        self.add_points(100)

    def voronoi(self):

        self.segments_voronoi.clear()
        if len(self.edges) < 2:
            return
        diagram = Voronoi.Voronoi(self.edges)
        diagram.process()
        lines = diagram.get_output()
        for line in lines:
            self.segments_voronoi.append(Segment(line))

    def delone(self):

        self.segments_delone.clear()
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
        self.segments_lin.clear()
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
            pygame.draw.line(self.screen, colors[self.settings["segment"]["voronoi_color"]],
                             segment.x, segment.y, width=4)

        for segment in self.segments_delone:
            pygame.draw.line(self.screen, colors[self.settings["segment"]["triangulation_color"]],
                             segment.x, segment.y, width=4)

        for segment in self.segments_lin:
            pygame.draw.line(self.screen, colors[self.settings["segment"]["lin_color"]], segment.x, segment.y, width=4)

    def update_edges(self):
        for edge in self.edges:
            pygame.draw.circle(surface=self.screen, color=colors[self.settings["edge"]["color"]],
                               center=(int(edge.cords[0]), int(edge.cords[1])), radius=self.rad_edges, width=0)

    def update_frames(self):
        #pygame.draw.rect(self.screen, colors['white'], (self.settings["screen"]["width"] - self.menu_width, 3,
        #                                               self.settings["screen"]["width"],
        #                                                self.settings["screen"]["heights"]),  width=10)

        pygame.draw.rect(self.screen, colors['black'], (self.settings["screen"]["width"] - self.menu_width, 3,
                                                        self.menu_width - 3, self.settings["screen"]["heights"] - 6),
                         width=8)

        pygame.draw.rect(self.screen, colors['black'], (3, 3, self.settings["screen"]["width"] - self.menu_width,
                                                        self.settings["screen"]["heights"] - 8), width=8)

    def update_buttons(self):
        for i, button in enumerate(self.buttons):
            self.screen.blit(button, (self.settings["screen"]["width"] - self.menu_width + 10, 40 * i + 6))
            pygame.draw.rect(self.screen, colors['black'], (self.settings["screen"]["width"] - self.menu_width, 40 * i,
                                                            self.settings["screen"]["width"] - 6, 40), width=2)

    def update(self):
        self.screen.fill(colors[self.settings["screen"]["color"]])
        self.update_segments()
        self.update_edges()
        self.update_frames()
        self.update_buttons()
        pygame.display.update()

    def move(self):
        self.is_moving = True
        for i in range(len(self.edges)):
            self.angels.append(random.random() * 2 * scipy.constants.pi)

    def stop_moving(self):
        self.is_moving = False
        self.angels.clear()

    def movement(self):
        if self.is_moving:
            self.stop_moving()
        else:
            self.move()

    def cords_update(self, angel):
        v_x = math.cos(angel) * int(self.settings["edge"]["speed"])
        v_y = math.sin(angel) * int(self.settings["edge"]["speed"])
        return v_x, v_y

    def collisions_border(self, i, v_x, v_y):
        if self.edges[i][0] + v_x < self.rad_edges + self.distance:
            self.angels[i] = 3 * scipy.constants.pi - self.angels[i]
        elif self.edges[i][0] + v_x > self.settings["screen"]["width"] - \
                self.menu_width - self.distance - self.rad_edges:
            self.angels[i] = scipy.constants.pi - self.angels[i]

        if self.edges[i][1] + v_y < self.rad_edges + self.distance:
            self.angels[i] = 4 * scipy.constants.pi - self.angels[i]
        elif self.edges[i][1] + v_y > self.settings["screen"]["heights"] - self.rad_edges - self.distance:
            self.angels[i] = 2 * scipy.constants.pi - self.angels[i]

    def collisions_edges(self):
        for i in range(len(self.edges)):
            for j in range(i + 1, len(self.edges)):
                if i == j:
                    pass
                if self.edges[i].distance(self.edges[j]) <= 2 * self.rad_edges:
                    v_x, v_y = self.cords_update(self.angels[i])
                    edge_1 = Edge([self.edges[i].cords[0] + v_x, self.edges[i].cords[1] + v_y])

                    v_x, v_y = self.cords_update(self.angels[j])
                    edge_2 = Edge([self.edges[j].cords[0] + v_x, self.edges[j].cords[1] + v_y])

                    if edge_1.distance(edge_2) < self.edges[i].distance(self.edges[j]):
                        alfa = math.atan((self.edges[j][1] - self.edges[i][1])/(self.edges[j][0] - self.edges[i][0]))

                        if self.edges[j][0] - self.edges[i][0] < 0:
                            alfa += math.pi
                            alfa = engels_norm(alfa)

                        w1 = self.angels[i] - alfa
                        w2 = self.angels[j] - alfa

                        Vw2, Vwt1 = self.cords_update(w1)
                        Vw1, Vwt2 = self.cords_update(w2)
                        W1 = math.atan(Vwt1/Vw1)
                        if Vw1 < 0:
                            W1 += math.pi
                        W2 = math.atan(Vwt2/Vw2)
                        if Vw2 < 0:
                            W2 += math.pi

                        self.angels[i] = alfa + W1
                        self.angels[i] = engels_norm(self.angels[i])
                        self.angels[j] = alfa + W2
                        self.angels[j] = engels_norm(self.angels[j])

    def collisions(self):
        for i in range(len(self.edges)):
            v_x, v_y = self.cords_update(self.angels[i])
            self.collisions_border(i, v_x, v_y)
        self.collisions_edges()

    def moving(self):
        self.collisions()

        for i in range(len(self.edges)):
            v_x, v_y = self.cords_update(self.angels[i])

            self.edges[i].cords[0] += v_x
            self.edges[i].cords[1] += v_y

        #self.voronoi()

    def start(self):

        self.update()

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if event.pos[0] < self.settings["screen"]["width"] - self.menu_width:
                            self.new_edge(event.pos)
                        else:
                            self.functions[event.pos[1] // 40]()
                        self.update()
            if self.is_moving:
                self.moving()
                self.update()

            self.clock.tick(self.fps)


if __name__ == '__main__':
    game = Game()
    game.start()
