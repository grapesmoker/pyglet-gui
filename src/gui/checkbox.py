# -*- coding: utf-8 -*-


import pyglet

from color import Color
from primitives import Rectangle, Clickable
from widget import Widget

class Checkbox(Widget, Clickable):
    
    def __init__(self, label, x, y, value, *args, **kwargs):
        
        self.label_font_name = kwargs.pop('title_font_name', 'Lucida Grande')
        self.label_font_size = kwargs.pop('title_font_size', 12)
        self.label_color = kwargs.pop('label_color', Color(255, 255, 255))
        self.label_x_pad = kwargs.pop('label_x_pad', 4)
        self.label_y_pad = kwargs.pop('label_y_pad', 4)
        self.bg_color = kwargs.pop('bg_color', Color(255, 0, 0))
        self.click_color = kwargs.pop('click_color', Color.from_hex('#4286f4'))
        
        super(Checkbox, self).__init__(*args, **kwargs)
        self.x = x
        self.y = y
        self.width = None
        self.height = None
        self.text = label
        self.value = value
        self.selected = False
        self.label = pyglet.text.Label(label)
        self.width, self.height = self.calc_button_size(self.label)
        self.frame = Rectangle(x, y, self.width, self.height, *args, **kwargs)
        self.vertices = self.frame.vertices
        
    def __str__(self):
        
        return 'Checkbox ({} x {}) at ({}, {})'.format(self.height, self.width,
                         self.x, self.y)
    
    def calc_button_size(self, label):
        
        w = round(label.content_width + 2 * self.label_x_pad) + 20
        h = round(label.content_height + 2 * self.label_y_pad)
        return w, h
        
    def calc_label_position(self, label):
        
        w = label.content_width 
        h = label.content_height
        mid_x = 10 + round(self.x + self.width / 2.0)
        mid_y = round(self.y + self.height / 2.0)
        x = mid_x - round(w / 2.0)
        y = mid_y - round(h / 2.0) + 2.0
        return x, y
    
    def on_mouse_press(self, x, y, button, modifiers):
        
        if self.frame.on_mouse_press(x, y, button, modifiers):
            self.dispatch_event('on_checkbox_click', self)
            self.selected = not self.selected
            
    def on_mouse_release(self, x, y, button, modifiers):
        
        if self.frame.on_mouse_release(x, y, button, modifiers):
            #print 'released', self
            pass
    
    def render(self, batch):
        
        self.frame.render(batch)
        l_x, l_y = self.calc_label_position(self.label)
        label = pyglet.text.Label(self.text, x=l_x, y=l_y, batch=batch)
        box_y = round((self.frame.height - 12) / 2)
        box = Rectangle(self.x + self.label_x_pad, self.y + box_y,
                        12, 12, fill=self.selected)
        box.render(batch)
        
        
Checkbox.register_event_type('on_checkbox_click')
Checkbox.register_event_type('on_checkbox_release')