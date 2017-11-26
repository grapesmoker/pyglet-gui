# -*- coding: utf-8 -*-

import pyglet

from widget import Widget
from primitives import Rectangle, Triangle
from color import Color

class ListBox(Widget):
    
    def __init__(self, x, y, options=None, *args, **kwargs):
        
        self.label_x_pad = kwargs.pop('label_x_pad', 4)
        self.label_y_pad = kwargs.pop('label_y_pad', 4)
        super(ListBox, self).__init__(*args, **kwargs)
        
        if not options:
            self.options = []
        else:
            self.options = options
        self.selection = None
        self.x = x
        self.y = y
        self.frame = Rectangle(x, y, 0, 0, *args, **kwargs)
        self.expanded = False
        
    def add(self, option):
        
        self.options.append(option)
        self.calc_geometry()
        
    def calc_item_size(self):
        
#        if self.selection:
#            label = self.selection.label
#            w = round(1.5 * label.content_width + 2 * self.selection.label_x_pad)
#            h = round(label.content_height + 2 * self.selection.label_y_pad)
#            self.frame.width = w
#            self.frame.height = h
#        else:
        self.frame.width = max([option.width for option in self.options]) + 8
        self.frame.height = max([option.height for option in self.options])
        
    def calc_label_position(self, label):
        
        h = label.content_height
        mid_y = round(self.y + self.frame.height / 2.0)
        x = self.x + self.label_x_pad
        y = mid_y - round(h / 2.0) + 2.0
        return x, y
        
    def calc_geometry(self):
        
        max_w = max([option.width for option in self.options]) + 8
        max_h = max([option.height for option in self.options])
        current_x, current_y = self.frame.x, self.frame.y
        for option in self.options:
            current_y -= option.frame.height
            w, h = option.calc_item_size()
            option.set_geometry(current_x, current_y, w, h)
            
    def render(self, batch, group=None):
        
        self.calc_item_size()
        self.calc_geometry()
        self.frame.set_geometry(self.x, self.y, self.frame.width, self.frame.height)
        print self, self.frame
        self.frame.render(batch, group=group)
        chevron = Triangle([(self.x + self.frame.width - 12, self.y + round(self.frame.height * 0.75)),
                            (self.x + self.frame.width - 8, self.y + round(self.frame.height * 0.25)),
                            (self.x + self.frame.width - 4, self.y + round(self.frame.height * 0.75))])
        chevron.render(batch, group=group)
        if self.selection:
            l_x, l_y = self.calc_label_position(self.selection.label)
            label = pyglet.text.Label(self.selection.text, x=l_x, y=l_y, 
                                      batch=batch, group=group)
            self.dispatch_event('on_listbox_select', self.selection)

        if self.expanded:
            for item in self.options:
                item.render(batch, group=group)
                
    def on_mouse_press(self, x, y, button, modifiers):
        
        if self.frame.on_mouse_press(x, y, button, modifiers):
            if self.expanded:
                self.expanded = False
            else:
                self.expanded = True
        else:
            if self.expanded:
                for option in self.options:
                    if option.frame.on_mouse_press(x, y, button, modifiers):
                        self.selection = option
                        self.expanded = False
                        break
                    
    def on_mouse_release(self, x, y, button, modifiers):
        
        pass
        
ListBox.register_event_type('on_listbox_click')
ListBox.register_event_type('on_listbox_select')

    
class Option(Widget):
    
    def __init__(self, text, value, *args, **kwargs):
        
        self.label_font_name = kwargs.pop('title_font_name', 'Lucida Grande')
        self.label_font_size = kwargs.pop('title_font_size', 12)
        self.bg_color = kwargs.pop('bg_color', Color.from_hex('#0099cc'))
        self.label_color = kwargs.pop('label_color', Color(255, 255, 255))
        self.label_x_pad = kwargs.pop('label_x_pad', 4)
        self.label_y_pad = kwargs.pop('label_y_pad', 4)
        self.value = value
        self.depth = 0
        self.expanded = False
        
        super(Option, self).__init__(*args, **kwargs)
        self.label = pyglet.text.Label(text)
        self.text = text
        self.width, self.height = self.calc_item_size()
        self.frame = Rectangle(0, 0, self.width, self.height, *args, **kwargs)
        
    def calc_item_size(self):
        
        w = round(1.5 * self.label.content_width + 2 * self.label_x_pad)
        h = round(self.label.content_height + 2 * self.label_y_pad)
        return w, h
        
    def set_geometry(self, x, y, width, height):
        
        self.x, self.y, self.width, self.height = x, y, width, height
        self.frame.set_geometry(x, y, width, height)
        
    def calc_label_position(self, label):
        
        h = label.content_height
        mid_y = round(self.y + self.height / 2.0)
        x = self.x + self.label_x_pad
        y = mid_y - round(h / 2.0) + 2.0
        return x, y
    
    def render(self, batch, group=None):
        
        self.frame.render(batch, group=group)
        l_x, l_y = self.calc_label_position(self.label)
        label = pyglet.text.Label(self.text, x=l_x, y=l_y, 
                                  batch=batch, group=group)
        