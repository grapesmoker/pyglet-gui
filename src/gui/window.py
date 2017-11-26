# -*- coding: utf-8 -*-

import pyglet

from gui.widget import Widget
from gui.primitives import Drawable
from gui.menus import MenuBar

class Window(pyglet.window.Window):
    
    def __init__(self, batch=None, **kwargs):
        
        self.windows = []
        super(Window, self).__init__(**kwargs)
           
        if batch is not None:
            self.batch = batch
        else:
            self.batch = pyglet.graphics.Batch()
            
        self.objects = []
        self.sorted = False
        self.focus = None
        #self.push_handlers(pyglet.window.event.WindowEventLogger())
        #self.push_handlers(on_button_click=self.on_button_click)
        
    def add_window(self, window):
        
        self.windows.append()
        
    def add_object(self, obj, z=1):
        
        self.objects.append((obj, z))
        self.sorted = False
        obj.parent = self
        
    def clear_objects(self):
        
        self.objects = []
        
    def sort_objects(self):
        
        if not self.sorted:
            self.objects = sorted(self.objects, key=lambda x: x[1])
            self.sorted = True
        
    def render(self, batch):
        
        self.sort_objects()
        
        for obj, z in self.objects:
            obj.render(batch)
            
    def on_draw(self):
        batch = pyglet.graphics.Batch()
        self.clear()
        self.render(batch)
        batch.draw()
        
    def connect(self, widget):
        
        self.push_handlers(widget)
        
    def on_mouse_press(self, x, y, button, modifiers):
        
        self.sort_objects()
        
        for item, z in self.objects[::-1]:
            if isinstance(item, MenuBar):
                child_menus = []
                def gather_child_menus(menu):
                    child_menus.extend(menu.menu_items)
                    if len(menu.menu_items) > 0:
                        for menu_item in menu.menu_items:
                            gather_child_menus(menu_item)
                gather_child_menus(item)
                for menu_item in child_menus:
                    if menu_item.visible and menu_item.enabled:
                        menu_item.on_mouse_press(x, y, button, modifiers)
            if item.visible and item.enabled and item.on_mouse_press(x, y, button, modifiers):
                #print 'clicked', x, y
                self.focus = item
                break
    
    def on_mouse_release(self, x, y, button, modifiers):
        
        self.sort_objects()
        
#        for item, z in self.objects[::-1]:
#            if isinstance(item, MenuBar):
#                #print 'unexpanding'
#                for child in item.menu_items:
#                    child.expanded = False
        
        for item, z in self.objects[::-1]:
            if item.on_mouse_release(x, y, button, modifiers):
                #print 'released', x, y
                break
                
#GuiManager.register_event_type('on_button_click')