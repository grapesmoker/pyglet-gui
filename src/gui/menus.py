# -*- coding: utf-8 -*-

import pyglet

from primitives import *
from panel import Panel
from widget import Widget
from color import Color

class MenuBar(Widget, Clickable):
    
    def __init__(self, parent, *args, **kwargs):
        
        self.title_font_name = kwargs.pop('title_font_name', 'Lucida Grande')
        self.title_font_size = kwargs.pop('title_font_size', 12)
        self.bg_color = kwargs.pop('bg_color', Color.from_hex('#0099cc'))
        self.title_color = kwargs.pop('title_color', Color(255, 255, 255))
        self.title_x_pad = kwargs.pop('title_x_pad', 4)
        self.title_y_pad = kwargs.pop('title_y_pad', 4)
        
        super(MenuBar, self).__init__(parent, *args, **kwargs)
        self.menu_items = []
        self.frame = Rectangle(0, 0, 0, 0, *args, **kwargs)
        assert(isinstance(self.parent, pyglet.window.Window) or 
               isinstance(self.parent, Panel))
        
    def add(self, menu_item):
        
        self.menu_items.append(menu_item)
        self.calc_bar_geometry()
        self.calc_child_geometry()
        menu_item.parent = self
        menu_item.depth = 0
        
    def clear_items(self):
        
        self.menu_items = []
        
    def calc_bar_geometry(self):
        
        if len(self.menu_items) > 0:
            max_h = max([item.height for item in self.menu_items])
            if isinstance(self.parent, pyglet.window.Window):
                self.x = 0
                self.y = self.parent.height - max_h
                self.width = self.parent.width
                self.height = max_h
            elif isinstance(self.parent, Panel):
                self.x = self.parent.x
                self.y = self.parent.y + self.parent.height - max_h
                self.width = self.parent.width
                self.height = max_h
            self.frame.set_geometry(self.x, self.y, self.width, self.height)
            
    def calc_child_geometry(self):
        
        current_x = self.x
        current_y = self.y
        for item in self.menu_items:
            w, h = item.calc_item_size()
            item.set_geometry(current_x, current_y, w, h)
            #print item, item.frame.x, item.frame.y
            current_x += w
            item.calc_child_positions()
        
    def render(self, batch, group=None):
        
        bg = pyglet.graphics.OrderedGroup(0)
        fg = pyglet.graphics.OrderedGroup(1)
        
        self.calc_child_geometry()
        self.frame.render(batch, group=bg)
        for item in self.menu_items:
            item.render(batch, group=fg)
            
    def on_mouse_press(self, x, y, button, modifiers):
        
        for item in self.menu_items:
            item.on_mouse_press(x, y, button, modifiers)
            
    def on_mouse_release(self, x, y, button, modifiers):
        
        for item in self.menu_items:
            item.on_mouse_release(x, y, button, modifiers)
        
    
class MenuItem(Widget, Drawable, Clickable):
    
    def __init__(self, text, value=None, *args, **kwargs):
        
        self.label_font_name = kwargs.pop('title_font_name', 'Lucida Grande')
        self.label_font_size = kwargs.pop('title_font_size', 12)
        self.bg_color = kwargs.pop('bg_color', Color.from_hex('#0099cc'))
        self.label_color = kwargs.pop('label_color', Color(255, 255, 255))
        self.label_x_pad = kwargs.pop('label_x_pad', 4)
        self.label_y_pad = kwargs.pop('label_y_pad', 4)
        self.value = value
        self.depth = 0
        self.expanded = False
        
        super(MenuItem, self).__init__(*args, **kwargs)
        self.text = text
        self.label = pyglet.text.Label(text)
        self.width, self.height = self.calc_item_size()
        self.frame = Rectangle(0, 0, self.width, self.height, *args, **kwargs)
        
        self.menu_items = []
        
    def add(self, menu_item):
        
        self.menu_items.append(menu_item)
        self.calc_child_positions()
        menu_item.parent = self
        menu_item.depth = self.depth + 1
        
    def calc_item_size(self):
        
        w = round(1.5 * self.label.content_width + 2 * self.label_x_pad)
        h = round(self.label.content_height + 2 * self.label_y_pad)
        return w, h
    
    def set_frame_size(self):
        
        w, h = self.calc_item_size()
        #self.frame.set_g
        
    def set_geometry(self, x, y, width, height):
        
        self.x, self.y, self.width, self.height = x, y, width, height
        self.frame.set_geometry(x, y, width, height)
        
    def calc_label_position(self, label):
        
        w = label.content_width
        h = label.content_height
        mid_x = round(self.x + self.width / 2.0)
        mid_y = round(self.y + self.height / 2.0)
        x = mid_x - round(w / 2.0)
        y = mid_y - round(h / 2.0) + 2.0
        return x, y
    
    def calc_child_positions(self):
        if len(self.menu_items) > 0:
            if self.depth == 0:
                current_x, current_y = self.frame.x, self.frame.y
                for child in self.menu_items:
                    current_y -= child.frame.height
                    w, h = self.calc_item_size()
                    child.set_geometry(current_x, current_y, w, h)
    
    def on_mouse_press(self, x, y, button, modifiers):

        print self.text, len(self.menu_items), self.frame.on_mouse_press(x, y, button, modifiers) 
        if self.frame.on_mouse_press(x, y, button, modifiers) and len(self.menu_items) > 0:
            self.dispatch_event('menu_item_select', self)
            self.expanded = True
            for item in self.menu_items:
                item.on_mouse_press(x, y, button, modifiers)
        elif self.frame.on_mouse_press(x, y, button, modifiers) and len(self.menu_items) == 0:
            print('selecting menu item with no children')
            self.dispatch_event('menu_item_select', self)
            self.parent.expanded = False
        #print self.text, self.expanded, self.parent
            
    def on_mouse_release(self, x, y, button, modifiers):
        
        if self.frame.on_mouse_release(x, y, button, modifiers):
            print 'unexpanding asdfasdfa'
            #self.expanded = False
        
        
    def render(self, batch, group=None):
        
        self.frame.render(batch, group=group)
        l_x, l_y = self.calc_label_position(self.label)
        label = pyglet.text.Label(self.text, x=l_x, y=l_y, 
                                  batch=batch, group=group)
        
        for item in self.menu_items:
            if self.expanded:
                item.visible = True
                item.render(batch, group=group)
            else:
                item.visible = False
        
MenuItem.register_event_type('menu_item_select')