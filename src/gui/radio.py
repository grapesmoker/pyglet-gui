# -*- coding: utf-8 -*-


import pyglet

from color import Color
from primitives import Rectangle, Clickable, Circle
from widget import Widget

class Radio(Widget, Clickable):
    
    def __init__(self, label, x, y, value, *args, **kwargs):
        
        self.label_font_name = kwargs.pop('title_font_name', 'Lucida Grande')
        self.label_font_size = kwargs.pop('title_font_size', 12)
        self.label_color = kwargs.pop('label_color', Color(255, 255, 255))
        self.label_x_pad = kwargs.pop('label_x_pad', 4)
        self.label_y_pad = kwargs.pop('label_y_pad', 4)
        self.bg_color = kwargs.pop('bg_color', Color(255, 0, 0))
        self.click_color = kwargs.pop('click_color', Color.from_hex('#4286f4'))
        
        super(Radio, self).__init__(*args, **kwargs)
        self.x = x
        self.y = y
        self.width = None
        self.height = None
        self.text = label
        self.value = value
        self.selected = False
        self.label = pyglet.text.Label(label)
        self.width, self.height = self.calc_item_size(self.label)
        self.frame = Rectangle(x, y, self.width, self.height, *args, **kwargs)
        self.vertices = self.frame.vertices
        
    def __str__(self):
        
        return 'Radio ({} x {}) at ({}, {})'.format(self.height, self.width,
                         self.x, self.y)
    
    def calc_item_size(self, label):
        
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
    
    def set_geometry(self, x, y, width, height):
        
        self.x, self.y, self.width, self.height = x, y, width, height
        self.frame.set_geometry(x, y, width, height)
    
    def on_mouse_press(self, x, y, button, modifiers):
        
        if self.frame.on_mouse_press(x, y, button, modifiers):
            self.dispatch_event('on_radio_click', self)
            print self, self.value
            self.selected = not self.selected
            
    def on_mouse_release(self, x, y, button, modifiers):
        
        if self.frame.on_mouse_release(x, y, button, modifiers):
            #print 'released', self
            pass
    
    def render(self, batch, group=None):
        
        self.frame.render(batch)
        l_x, l_y = self.calc_label_position(self.label)
        label = pyglet.text.Label(self.text, x=l_x, y=l_y, batch=batch)
        circ_y = l_y + round(self.label.content_height * 0.33)
        circ_x = round((self.frame.x + 10))
        circle = Circle(5, circ_x, circ_y, fill=self.selected)
        circle.render(batch)
        
        
Radio.register_event_type('on_radio_click')
Radio.register_event_type('on_radio_release')


class RadioGroup(Widget, Clickable):
    
    def __init__(self, x, y, *args, **kwargs):
        
        self.label_font_name = kwargs.pop('title_font_name', 'Lucida Grande')
        self.label_font_size = kwargs.pop('title_font_size', 12)
        self.label_color = kwargs.pop('label_color', Color(255, 255, 255))
        self.label_x_pad = kwargs.pop('label_x_pad', 4)
        self.label_y_pad = kwargs.pop('label_y_pad', 4)
        self.bg_color = kwargs.pop('bg_color', Color(255, 0, 0))
        self.click_color = kwargs.pop('click_color', Color.from_hex('#4286f4'))
        
        super(RadioGroup, self).__init__(*args, **kwargs)
        self.x = x
        self.y = y
        self.width = None
        self.height = None
        self.selection = None
        self.options = []
        self.width, self.height = 0, 0
        self.frame = Rectangle(x, y, self.width, self.height, *args, **kwargs)
        self.vertices = self.frame.vertices
        
    def __str__(self):
        
        return 'Radio ({} x {}) at ({}, {})'.format(self.height, self.width,
                         self.x, self.y)
        
    def add(self, item):
        
        self.options.append(item)
        item.parent = self
        self.calc_item_size()
        
    def calc_item_size(self):
        
        self.frame.width = max([option.width for option in self.options]) + 8
        self.frame.height = max([option.height for option in self.options])
        
    def calc_geometry(self):
        
        max_w = max([option.width for option in self.options]) + 8
        max_h = max([option.height for option in self.options])
        current_x, current_y = self.frame.x, self.frame.y
        for option in self.options:
            w, h = option.calc_item_size(option.label)
            option.set_geometry(current_x, current_y, w, h)
            current_y -= option.frame.height
            
    def on_mouse_press(self, x, y, button, modifiers):
        
        if self.frame.on_mouse_press(x, y, button, modifiers):
            for option in self.options:
                option.on_mouse_press(x, y, button, modifiers)
            
    def render(self, batch, group=None):
        
        self.calc_item_size()
        self.calc_geometry()
        self.frame.set_geometry(self.x, self.y, self.frame.width, self.frame.height)
        self.frame.render(batch, group=group)
        
        for item in self.options:
            item.render(batch, group=group)