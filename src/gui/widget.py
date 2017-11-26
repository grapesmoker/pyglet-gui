# -*- coding: utf-8 -*-
import pyglet

# some notes on event dispatch:
# I had this notion in my head from working with GUI toolkits like Gtk
# and Qt that the "correct" way of doing event dispatch was to connect a
# function to some change in state in a widget. So in Gtk you would connect
# a signal emitted by a button click to some arbitrary function and handle
# the signal in that function. Pyglet takes a different approach, where an
# EventDispatcher pushes a handler object onto its stack, and when you
# dispatch that event, the function named after the event is looked up
# in the object you pushed onto the stack and is handled accordingly.
# As I understand this structure, the connection here becomes one that is
# between two objects, the dispatcher and the listener. So if you have a
# Button widget and you want the window that it's in to listen for something
# you have to do button.connect(window) and then have the appropriate
# function on your window subclass or whatever.

class Widget(pyglet.event.EventDispatcher):
    
    def __init__(self, parent=None, batch=None, **kwargs):
        
        self.parent = parent
        self.batch = batch
        self.vertex_lists = []
        self.visible = True
        self.enabled = True
