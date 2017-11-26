# -*- coding: utf-8 -*-

class Color(object):
    
    color_map = {'blue': (0, 0, 255, 0),
                 'red': (255, 0, 0, 0),
                 'green': (0, 255, 0, 0)}
    
    def __init__(self, r, g, b, a=0):
        
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        
    def __str__(self):
        
        return '(R: {}, G: {}, B: {}, A: {})'.format(self.r, self.g, self.b, self.a)
    
    def as_gl_spec(self, with_alpha=False, vertices=1):
        if not with_alpha:
            return ('c3B', (self.r, self.g, self.b) * vertices)
        else:
            return ('c3B', (self.r, self.g, self.b, self.a) * vertices)
    
    @property
    def color(self):
        return (self.r, self.g, self.b, self.a)
    
    @classmethod
    def from_string(cls, color):
        
        c = cls.color_map[color]
        return cls(*c)
    
    @classmethod
    def from_hex(cls, color):
        
        if color[0] == '#':
            r = int('0x' + color[1:3], 16)
            g = int('0x' + color[3:5], 16)
            b = int('0x' + color[5:7], 16)
            return cls(r, g, b)
                            