import pyglet
from widget import Widget
from color import Color
from primitives import Rectangle, Line, Clickable


class Panel(Widget, Clickable):
    
    def __init__(self, x, y, width, height, title=None, *args, **kwargs):
        
        self.title_font_name = kwargs.pop('title_font_name', 'Lucida Grande')
        self.title_font_size = kwargs.pop('title_font_size', 12)
        self.title_color = kwargs.pop('title_color', Color(255, 255, 255))
        self.title_x_pad = kwargs.pop('title_x_pad', 4)
        self.title_y_pad = kwargs.pop('title_y_pad', 4)
        
        super(Panel, self).__init__(*args, **kwargs)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.frame = Rectangle(x, y, width, height, *args, **kwargs)
        self.vertices = self.frame.vertices
        
    def __str__(self):
        
        return 'Panel ({} x {}) at ({}, {})'.format(self.height, self.width,
                      self.x, self.y)
        
    def calc_title_position(self, label):
        
        w = label.content_width
        h = label.content_height
        x = self.x + self.title_x_pad
        y = self.y + self.height - (h + self.title_y_pad)
        return (x, y)
            
    def render(self, batch):
        
        if self.title:
            self.vertex_lists = []
            label = pyglet.text.Label(self.title)
            t_x, t_y = self.calc_title_position(label)
            label = pyglet.text.Label(self.title, x=t_x, y=t_y, batch=batch)
            sep_y = self.y + self.height - 2 * self.title_y_pad - label.content_height
            print self.x, sep_y, self.x + self.width
            separator = Line(self.x, sep_y, self.x + self.width, sep_y)
            batch.add(*separator.render())
            batch.add(*self.frame.render())
            
            self.vertex_lists.append(separator.render())
            self.vertex_lists.append(self.frame.render())
            
#    def click(self, x, y, button):
#        
#        pass
#            
#    