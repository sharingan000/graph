import random
import sys
import collections
import time

import numpy
import numpy as np

import pygame as p

p.init()


class Node:
    def __init__(self, name, pose, window, color=p.Color('black'), radius=10):
        self.name = name
        self.pose = pose
        self.color = color
        self.radius = radius
        self.window = window

    def render(self, clr=None):
        if clr is None:
            p.draw.circle(self.window, self.color, self.pose, self.radius)
        else:
            p.draw.circle(self.window, clr, self.pose, self.radius)

    def __str__(self):
        return str(self.name)


class Graph:
    def __init__(self, pair_of_nodes, n, window, nodes):
        self.INF = 10 ** 9
        self.clock = p.time.Clock()
        self.window = window
        self.n = n
        self.nodes = nodes
        self.pair_of_nodes = pair_of_nodes
        self.graph = self.new_matrix()

    def new_matrix(self):
        graph = [[self.INF] * self.n for i in range(self.n)]
        for i in self.pair_of_nodes:
            u = int(str(i[0])) - 1
            v = int(str(i[1])) - 1
            w = i[2]

            graph[u][v] = w
            graph[v][u] = w

        return graph

    def render(self, colored_nodes):
        for i in self.nodes:
            name = int(str(i)) - 1
            pose = i.pose
            clr = None
            if colored_nodes[name]:
                clr = p.Color('Red')
            i.render(clr)
            f = self.graph[name]
            for j in range(self.n):
                el = f[j]
                if el < self.INF:
                    p.draw.line(self.window, p.Color('Black'), pose, self.nodes[j].pose)

    def add_node(self, node):
        self.nodes.append(node)
        self.n += 1
        self.nodes.append(node)
        self.graph = self.new_matrix()

    def add_r(self, node1, node2):
        self.pair_of_nodes.append([node1, node2, 10])
        n1 = int(node1.name)
        n2 = int(node2.name)
        self.graph[n1][n2] = 10
        self.graph[n2][n1] = 10

    def bfs(self, point, t):
        visited = [False] * self.n
        visited[point] = True

        queue = collections.deque([point])
        self.render(visited)
        self.clock.tick(t)

        while queue:
            vertex = queue.pop()
            v = self.graph[vertex]
            for i in range(self.n):
                if not visited[i] and v[i] < self.INF:
                    queue.append(i)
                    visited[i] = True

                    self.render(visited)
                    p.display.flip()
                    self.clock.tick(t)

        return visited

    def bfs_for_col(self, point, t):
        visited = [0] * self.n
        visited[point] = 1
        queue = collections.deque([point])

        while queue:
            vertex = queue.pop()
            vv = visited[vertex]
            v = self.graph[vertex]
            for i in range(self.n):
                if visited[i] == 0 and v[i] < self.INF:
                    queue.append(i)
                    visited[i] = vv
                else:
                    visited[i] += 1

        return visited


class Main:
    def __init__(self):
        self.width, self.height = 700, 700
        self.window = p.display.set_mode((self.width, self.height))
        self.clock = p.time.Clock()
        self.FPS = 100

        self.nodes = []
        self.n = 0
        lin = np.linspace(50, 650, num=self.n // 2)
        la = lambda x: (330 ** 2 - (x - 350) ** 2) ** 0.5 + 350
        lin2 = la(lin)
        for i in range(self.n // 2):
            self.nodes.append(Node(i + 1, [int(lin[i]), int(lin2[i])], self.window))
            self.nodes.append(Node(2 * (i + 1), [int(lin[i]), int(700 - lin2[i])], self.window))

        self.nodes = []

        self.pair_of_nodes = []
        for i in range(0):
            l = list(range(self.n))
            f = random.choice(l)
            l.remove(f)
            s = random.choice(l)
            self.pair_of_nodes.append([self.nodes[f], self.nodes[s], 10])

        self.graph = Graph(self.pair_of_nodes, self.n, self.window, self.nodes)

    def get_node(self, pose):
        node = None
        pose = p.mouse.get_pos()
        for i in self.nodes:
            position = i.pose
            if (pose[0] - position[0]) ** 2 + (pose[1] - position[1]) ** 2 <= i.radius ** 2:
                node = i
                break

        return node

    def main_loop(self):
        s = [p.K_1, p.K_2, p.K_3, p.K_4, p.K_5, p.K_6, p.K_7, p.K_8, p.K_9]
        d = []
        visited = [False] * self.n
        redaction = False
        r = []
        t = 3
        while True:
            self.window.fill(p.Color('white') if not redaction else p.Color('grey'))
            for event in p.event.get():
                if event.type == p.QUIT:
                    p.quit()
                    sys.exit()

                if event.type == p.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if not redaction:
                            node = self.get_node(p.mouse.get_pos())
                            visited = self.graph.bfs(int(str(node)) - 1, t)
                        else:
                            pose = p.mouse.get_pos()
                            flag = True
                            for i in self.nodes:
                                position = i.pose
                                if (pose[0] - position[0]) ** 2 + (pose[1] - position[1]) ** 2 <= i.radius ** 2 * 4:
                                    flag = False
                                    break
                            if flag:
                                self.n += 1
                                self.nodes.append(Node(self.n, pose, self.window))
                                d.append(0)
                                self.graph = Graph(self.pair_of_nodes, self.n, self.window, self.nodes)
                                visited.append(False)

                    if event.button == 3:
                        if redaction:
                            node = self.get_node(p.mouse.get_pos())
                            if node is not None:
                                if len(r) == 0:
                                    r.append(node)
                                elif len(r) == 1 and r[0] != node:
                                    self.pair_of_nodes.append([node, r[0], 10])
                                    d.append(1)
                                    self.graph = Graph(self.pair_of_nodes, self.n, self.window, self.nodes)
                                    r = []
                        else:
                            node = None
                            pose = p.mouse.get_pos()
                            for i in self.nodes:
                                position = i.pose
                                if (pose[0] - position[0]) ** 2 + (pose[1] - position[1]) ** 2 <= i.radius ** 2:
                                    node = i
                                    break
                            if node is not None:
                                vis = self.graph.bfs_for_col(int(str(node)) - 1, t)
                                vis = [i - 1 for i in vis]

                    if event.button == 4:
                        t += 1
                    if event.button == 5:
                        t -= 1
                        t = max(t, 1)

                if event.type == p.KEYDOWN:
                    if event.key == p.K_ESCAPE:
                        p.quit()
                        sys.exit()
                    if event.key in s:
                        visited = self.graph.bfs(s.index(event.key), t)
                    if event.key == p.K_0:
                        visited = [False] * self.n
                    if event.key == p.K_z:
                        t = 0
                    if event.key == p.K_x:
                        t = 3
                    if event.key == p.K_r:
                        redaction = not redaction

                    if event.key == p.K_z:
                        mods = p.key.get_mods()
                        if mods & p.KMOD_CTRL:
                            if d[-1] == 0:
                                self.n -= 1
                                del visited[-1]
                                del self.nodes[-1]
                            elif d[-1] == 1:
                                del self.pair_of_nodes[-1]

                            del d[-1]

                            self.graph = Graph(self.pair_of_nodes, self.n, self.window, self.nodes)

                    if event.key == p.K_g:
                        self.pair_of_nodes = []

            self.graph.render(visited)

            p.display.update()

            self.clock.tick(self.FPS)


main = Main()
main.main_loop()