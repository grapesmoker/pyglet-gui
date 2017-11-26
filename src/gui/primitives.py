# -*- coding: utf-8 -*-
import pyglet
import math

from pyglet.graphics import vertex_list
from shapely.geometry.polygon import Polygon as ShPolygon
from shapely.geometry import Point as ShPoint
from collections import namedtuple
from abc import abstractmethod
from color import Color

Point = namedtuple('Point', ['x', 'y'])
VertexList = namedtuple('VertexList', ['num_points', 'mode', 'group',
                                       'vertices', 'colors'])

class Vector2d(object):
    
    def __init__(self, x, y):
        
        self.x = x
        self.y = y
        
    @property
    def norm(self):
        
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def __add__(self, other):
        
        if not isinstance(other, Vector2d):
            raise TypeError("Can't add a Vector2d to {}".format(type(other)))
        return Vector2d(self.x + other.x, self.y + other.y)
    
    def __mul__(self, other):
        
        if isinstance(other, Vector2d):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2d(self.x * other, self.y * other)
        else:
            raise TypeError("Can't multiply a Vector2d by {}".format(type(other)))
            
    def __div__(self, other):
        
        if isinstance(other, int) or isinstance(other, float):
            return self.__mul__(1 / float(other))
        else:
            raise TypeError("Can't divide a Vector2d by {}".format(type(other)))
            
    def __str__(self):
        
        return '<{}, {}>'.format(self.x, self.y)
    
    def __repr__(self):
        
        return self.__str__()
    
    @property
    def unit(self):
        
        return self.__div__(self.norm)


class Drawable(object):
    
    @abstractmethod
    def render(self, batch, group=None):
        
        pass

    def move(self, dx, dy):
    
        new_vertices = [(vertex[0] + dx, vertex[1] + dy) for vertex in self.vertices]
        self.vertices = new_vertices
        
    def __init__(self):
        
        self.visible = True
        self.enabled = True
        
class Clickable(object):
    
    def contains(self, point):
        
        poly = ShPolygon(self.vertices)
        pt = ShPoint(point[0], point[1])
        return poly.contains(pt)

    def on_mouse_press(self, x, y, button, modifiers):
        
        poly = ShPolygon(self.vertices)
        pt = ShPoint(x, y)
        if poly.contains(pt):
            return True
        
    def on_mouse_release(self, x, y, button, modifiers):
        
        poly = ShPolygon(self.vertices)
        pt = ShPoint(x, y)
        if poly.contains(pt):
            return True
        
    def __init__(self):
        
        self.enabled = True

class Line(Drawable):
    
    def __init__(self, x1, y1, x2, y2, *args, **kwargs):
        
        self.color = kwargs.pop('color', Color(255, 255, 255))
        self.thickness = kwargs.pop('thickness', 1)
        
        super(Line, self).__init__(*args, **kwargs)
        
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        
        self.vertices = [Point(x1, y1), Point(x2, y2)]
        
    def render(self, batch, group=None):

        pyglet.gl.glLineWidth(self.thickness)
        coords = (self.x1, self.y1, self.x2, self.y2)
 
        batch.add(2, pyglet.gl.GL_LINES, group,
                  ('v2f', coords), self.color_as_gl_spec(vertices=2))
        
        #return VertexList(2, pyglet.gl.GL_LINES, None,
        #                  ('v2f', coords),
        #                  self.color.as_gl_spec(vertices=2))
        
class Polygon(Drawable, Clickable):
    
    def __init__(self, vertices, closed=True, *args, **kwargs):
        
        self.border = kwargs.pop('border', 1)
        self.border_color = kwargs.pop('border_color', Color(255, 255, 255))
        self.bg_color = kwargs.pop('bg_color', Color(0, 255, 0))
        self.fill = kwargs.pop('fill', False)
        self.vertices = vertices
        self.closed = closed
        
        super(Polygon, self).__init__(*args, **kwargs)
        
    def set_vertices(self, vertices):
        
        self.vertices = vertices
        
    def compute_filled(self, n):
        
        solid_coords = []
        
        for vertex in self.vertices:
            solid_coords.append(vertex[0])
            solid_coords.append(vertex[1])
            
        return solid_coords
    
    def compute_frame(self):
        
        frame_coords = []
        prev_vertex = self.vertices[0]
        for vertex in self.vertices[1:]:
            frame_coords.append(prev_vertex[0])
            frame_coords.append(prev_vertex[1])
            frame_coords.append(vertex[0])
            frame_coords.append(vertex[1])
            prev_vertex = vertex
        if self.closed:
            frame_coords.append(prev_vertex[0])
            frame_coords.append(prev_vertex[1])
            frame_coords.append(self.vertices[0][0])
            frame_coords.append(self.vertices[0][1])
        return frame_coords
        
    def render(self, batch, group=None):
        
        pyglet.gl.glLineWidth(self.border)
    
        bg = pyglet.graphics.OrderedGroup(0, parent=group)
        fg = pyglet.graphics.OrderedGroup(1, parent=group)
        
        #print self, self.fill
        if self.fill:
            n = len(self.vertices)
            solid_coords = self.compute_filled(n)
            if isinstance(self, Triangle):
                mode = pyglet.gl.GL_TRIANGLES
            elif isinstance(self, Rectangle):
                mode = pyglet.gl.GL_QUADS
            else:
                mode = pyglet.gl.GL_POLYGON
            
            batch.add(n, mode, bg,
                      ('v2f', solid_coords), 
                      self.bg_color.as_gl_spec(vertices=n))
        frame_coords = self.compute_frame()    
        n = len(frame_coords) / 2
        batch.add(n, pyglet.gl.GL_LINES, fg,
                  ('v2f', frame_coords), 
                  self.border_color.as_gl_spec(vertices=n))
        
class PolyLine(Polygon):
    
    def __init__(self, vertices, *args, **kwargs):
        super(PolyLine, self).__init__(vertices, closed=False, *args, **kwargs)
        
        
class Triangle(Polygon):
    
    def __init__(self, vertices, closed=True, *args, **kwargs):
        
        assert(len(vertices) == 3)
        super(Triangle, self).__init__(vertices, closed=closed, *args, **kwargs)
        
class Rectangle(Polygon):
    
    def __init__(self, x, y, width, height, *args, **kwargs):

        self.radius = kwargs.pop('radius', 0)
        self.rounded = kwargs.pop('rounded', False)
        if self.radius > 0:
            self.rounded = True
        else:
            if self.rounded and self.radius == 0:
                min_dim = min(width / 2.0, height / 2.0)
                self.radius = min_dim / 5.0
                
                
        self.vertices = [Point(x, y), Point(x, y + height), 
                         Point(x + width, y + height), Point(x + width, y)]
        super(Rectangle, self).__init__(self.vertices, closed=True, *args, **kwargs)
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def __str__(self):
        
        return 'Rectangle ({} x {}) at ({}, {})'.format(self.width, self.height,
                          self.x, self.y)
        
    def set_geometry(self, x, y, width, height):
        
        self.vertices = [(x, y), (x, y + height), 
                         (x + width, y + height), (x + width, y)]
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def render(self, batch, group=None):
        
        if self.radius == 0:
            return super(Rectangle, self).render(batch)
        elif self.radius > 0 and self.radius <= min(self.width / 2.0, self.height / 2.0):
            
            v1 = Vector2d(0, self.height).unit * self.radius
            v2 = Vector2d(self.width, 0).unit * self.radius
            v3 = Vector2d(0, -self.height).unit * self.radius
            v4 = Vector2d(-self.width, 0).unit * self.radius
            
            coords = [(self.x, self.y + v1.y), (self.x, self.y + self.height + v3.y)]
            coords.extend(Arc(self.radius, self.x + v2.x, self.y + self.height + v3.y, 180, 90).get_vertices())
            coords.append((self.x + self.width + v4.x, self.y + self.height))
            coords.extend(Arc(self.radius, self.x + self.width + v4.x, self.y + self.height + v3.y, 90, 0).get_vertices())
            coords.append((self.x + self.width, self.y + v1.y))
            coords.extend(Arc(self.radius, self.x + self.width + v4.x, self.y + v1.y, 0, -90).get_vertices())
            coords.append((self.x + v2.x, self.y))
            coords.extend(Arc(self.radius, self.x + v2.x, self.y + v1.y, 270, 180).get_vertices())
            
            self.vertices = coords
            super(Rectangle, self).render(batch)
        else:
            raise ValueError('Invalid value of curvature radius: {}, for rectangle of size {} x {}'.format(self.radius, self.width, self.height))
            
        
class Arc(Polygon):
    
    def __init__(self, radius, center_x, center_y, start_angle, end_angle, num_sections=24, *args, **kwargs):
    
        super(Arc, self).__init__([], *args, **kwargs)
        self.radius = radius
        self.center_x = center_x
        self.center_y = center_y
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.num_sections = num_sections
        
        if self.fill and not self.closed:
            self.closed = True
        
    def calc_vertices(self):
        
        self.vertices = []
        theta = (self.end_angle - self.start_angle) / float(self.num_sections)
        prev_x = self.center_x + self.radius * math.cos(math.radians(self.start_angle))
        prev_y = self.center_y + self.radius * math.sin(math.radians(self.start_angle))
        for i in range(1, int(self.num_sections) + 1):
            angle = self.start_angle + theta * i
            dx = self.radius * math.cos(math.radians(angle))
            dy = self.radius * math.sin(math.radians(angle))
            x = self.center_x + dx
            y = self.center_y + dy
            self.vertices.append((prev_x, prev_y))
            self.vertices.append((x, y))
            prev_x = x
            prev_y = y
    
    def get_vertices(self):
        
        self.calc_vertices()
        return self.vertices
        
    def render(self, batch, group=None):
        
        self.calc_vertices()
        super(Arc, self).render(batch)
        
class Circle(Arc):
    
    def __init__(self, radius, center_x, center_y, num_sections=24, *args, **kwargs):
        
        super(Circle, self).__init__(radius, center_x, center_y, 0, 360, num_sections=num_sections, *args, **kwargs)
        
class CheckMark(Polygon):
    
    def __init__(self, x, y, *args, **kwargs):
        
        self.x = x
        self.y = y
        super(CheckMark, self).__init__([], *args, **kwargs)
        
    def render(self, batch, group=None):
        
        font = pyglet.font.load('Times New Roman', 18)
        start_x = font.size * 0.307 + 0.5
        rem_third = (font.size - start_x) / 3.0
        bx = self.x + 0.5 + start_x + rem_third
        by = self.y - 1.0 + (font.ascent * (font.size / font.size) + 0.5) + 1.0
        self.vertices = [(bx - rem_third, by - rem_third), (bx, by),
                         (bx + rem_third * 2, by - rem_third * 2)]
        self.closed = False
        super(CheckMark, self).render(batch)
