# -*- coding: utf-8 -*-

import pyglet

from panel import Panel
from color import Color
from primitives import Rectangle


class Label(Panel):
    
    def __init__(self, text, x, y, **kwargs):
        
        self.text = text
        self.text_color = kwargs.pop('text_color', Color.from_string('blue'))
        self.font_size = kwargs.pop('font_size', 10)
        self.font_name = kwargs.pop('font_name', 'Times New Roman')
        self.bg_color = kwargs.pop('bg_color', Color(255, 255, 255))
        self.v_spacing = kwargs.pop('v_spacing', 2)
        self.h_spacing = kwargs.pop('h_spacing', 2)
        self.x = x
        self.y = y
        self.batch = pyglet.graphics.Batch()
        
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.font = self.document.get_font()
        height = self.font.ascent - self.font.descent
        
        self.label = pyglet.text.Label(self.text, font_name=self.font_name, 
                                       font_size=self.font_size,
                                       x=self.x + self.h_spacing, 
                                       y=self.y + self.v_spacing)
        width = self.label.content_width + 1
        self.border = Rectangle(self.x, self.y, 
                                width + self.h_spacing, 
                                height + self.v_spacing)
        
        self.size = (width, height)

        
    def render(self):

        self.border.render()
        self.label.draw()
