# -*- coding: utf-8 -*-

import re, sys
from math import hypot, atan2, degrees, pi as PI
import numpy as np
reload(sys)
sys.setdefaultencoding('utf-8')

class DistMatrix(object):
    #vec: array of Point
    def __init__(self, vec):
        self.vec = vec
        self._dist_products()
        
    def _dist_products(self):
        r = (len(self.vec), len(self.vec))
        self.matrix = np.zeros(r)
        
        for c_i, c_p in enumerate(self.vec):
            for r_i, r_p in enumerate(self.vec):
                self.matrix[c_i,r_i] = c_p.distance(r_p)
                
                
    def select_in(self, index, max_dist):
        return np.where( self.matrix[index] <= max_dist )[0]
        
    def select_out(self, index, min_dist):
        return np.where( self.matrix[index] > min_dist )[0]
        
    def distance(self, from_index, to_index):
        return self.matrix[from_index, to_index]
        
    def __str__(self):
        return str(self.matrix)

class Point(object):
    POINT_PROG = re.compile('\[(-?[0-9]+),(-?[0-9]+)\]')
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # 0.0 <= angle < 2
    def angle(self, other):
        dy = self.y - other.y
        dx = self.x - other.x
        return (atan2(dy, dx) % (2.0*PI)) / PI
    
    @property
    def width(self):
        return self.x
        
    @property
    def height(self):
        return self.y

    def equals(self, point):
        return self.x == point.x and self.y == point.y
        
    def distance(self, point):
        return hypot(point.x-self.x, point.y-self.y)

    def __str__(self):
        return "[%d,%d]" % (self.x, self.y)
        
    @staticmethod
    def to_point(str_point):
        p1 = Point(0,0)
        try:
            m = re.match(Point.POINT_PROG, str_point)
            if(m is not None):
                p1 = Point(int(m.group(1)), int(m.group(2)))
        except:
            pass

        return p1

class Bounds(object):
    BOUNDS_PROG = re.compile(r'\[(-?[0-9]+),(-?[0-9]+)\]\[(-?[0-9]+),(-?[0-9]+)\]')
    SCROLL_SWIPE_MARGIN = 2
    
    RELATIVE_POS_OVERLAP    = 5
    RELATIVE_POS_LEFT       = 4
    RELATIVE_POS_TOP        = 2
    RELATIVE_POS_RIGHT      = 3
    RELATIVE_POS_BOTTOM     = 1
    RELATIVE_POS_UNKNOWN    = -1
    
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        
    @property
    def left(self):
        return self.p1.x
    
    @property
    def top(self):
        return self.p1.y
    
    @property
    def right(self):
        return self.p2.x
    
    @property
    def bottom(self):
        return self.p2.y
        
    @property
    def center(self):
        x = self.left + int(self.width*0.5)
        y = self.top + int(self.height*0.5)
        return Point(x, y)
    
    @property
    def width(self):
        w = self.right - self.left
        if w < 0:
            w = 0
        return w
        
    @property
    def height(self):
        h = self.bottom - self.top
        if h < 0:
            h = 0
        return h
    
    @property
    def area(self):
        a = self.width * self.height
        if a < 0:
            a = 0
        return a
    
    def _overlap_pos(self, bounds):
        p = self
        c = bounds
        if bounds.contains(self):
            p = bounds
            c = self
        
        h_width = p.width / 3
        h_height = p.height / 3
        
        # pos_01(8) | pos_02(9) | pos_03(7)
        # pos_04(6) | pos_05(5) | pos_06(4)
        # pos_07(3) | pos_08(2) | pos_09(1)
        pos_01 = Bounds(p.p1, Point(p.left+(h_width*1), p.top+(h_height*1)))
        pos_02 = Bounds(p.p1, Point(p.left+(h_width*2), p.top+(h_height*1)))
        pos_03 = Bounds(p.p1, Point(p.left+(h_width*3), p.top+(h_height*1)))
        
        pos_04 = Bounds(p.p1, Point(p.left+(h_width*1), p.top+(h_height*2)))
        pos_05 = Bounds(p.p1, Point(p.left+(h_width*2), p.top+(h_height*2)))
        pos_06 = Bounds(p.p1, Point(p.left+(h_width*3), p.top+(h_height*2)))
        
        pos_07 = Bounds(p.p1, Point(p.left+(h_width*1), p.top+(h_height*3)))
        pos_08 = Bounds(p.p1, Point(p.left+(h_width*2), p.top+(h_height*3)))
        pos_09 = Bounds(p.p1, Point(p.left+(h_width*3), p.top+(h_height*3)))
        
        b_center = c.center
        alpha = 0
        if pos_01.contains_point(b_center.x, b_center.y):
            alpha = 0.8
        elif pos_02.contains_point(b_center.x, b_center.y):
            alpha = 0.9
        elif pos_03.contains_point(b_center.x, b_center.y):
            alpha = 0.7
            
        elif pos_04.contains_point(b_center.x, b_center.y):
            alpha = 0.6
        elif pos_05.contains_point(b_center.x, b_center.y):
            alpha = 0.5
        elif pos_06.contains_point(b_center.x, b_center.y):
            alpha = 0.4
            
        elif pos_07.contains_point(b_center.x, b_center.y):
            alpha = 0.3
        elif pos_08.contains_point(b_center.x, b_center.y):
            alpha = 0.2
        elif pos_09.contains_point(b_center.x, b_center.y):
            alpha = 0.1
            
        return alpha
    
    #             top(2)
    # left(4)   overlap(5)  right(3)
    #           bottom(1)
    def relative_pos(self, bounds):
        # overlap
        if self.intersect(bounds).area > 0:
            alpha = 0
            # if self.contains(bounds) or bounds.contains(self):
            #     alpha = self._overlap_pos(bounds)
            
            return self.RELATIVE_POS_OVERLAP + alpha
        
        # # 0.0 <= angle < 2.8*PI
        # lt_angle = self.center.angle(self.p1)
        # lb_angle = self.center.angle(Point(self.left, self.bottom))
        # rt_angle = self.center.angle(Point(self.right, self.top))
        # rb_angle = self.center.angle(self.p2)
        #
        # c2c_angle = self.center.angle(bounds.center)
        #
        # #left(e.g., degree => c2c_angle > 315 && c2c_angle <= 45)
        # if c2c_angle > lb_angle and c2c_angle <= lt_angle:
        #     return self.RELATIVE_POS_LEFT
        #
        # #top(e.g., degree => c2c_angle > 45 && c2c_angle <= 135)
        # if c2c_angle > lt_angle and c2c_angle <= rt_angle:
        #     return self.RELATIVE_POS_TOP
        #
        # #right(e.g., degree => c2c_angle > 135 && c2c_angle <= 225)
        # if c2c_angle > rt_angle and c2c_angle <= rb_angle:
        #     return self.RELATIVE_POS_RIGHT
        #
        # #bottom(e.g., degree => c2c_angle > 225 && c2c_angle <= 315)
        # if c2c_angle > rb_angle and c2c_angle <= lb_angle:
        #     return self.RELATIVE_POS_BOTTOM
            
        # left
        if self.left > bounds.left and self.left >= bounds.right and self.top < bounds.bottom and self.bottom > bounds.top:
            return self.RELATIVE_POS_LEFT

        # top
        if self.top >= bounds.bottom:
            return self.RELATIVE_POS_TOP

        # right
        if self.right <= bounds.left and self.right < bounds.right and self.top < bounds.bottom and self.bottom > bounds.top:
            return self.RELATIVE_POS_RIGHT

        # bottom
        if self.top <= bounds.bottom:
            return self.RELATIVE_POS_BOTTOM
            
        return self.RELATIVE_POS_UNKNOWN
    
    def size_up(self, width, height):
        p1_x = self.left-width
        p1_y = self.top-height
        if p1_x <= 0: p1_x = 0
        if p1_y <= 0: p1_y = 0
        
        p2_x = self.right+width
        p2_y = self.bottom+height
        return Bounds(Point(p1_x, p1_y), Point(p2_x, p2_y))
    
    def contains_point(self, x, y):
        # check for empty first
        if self.area == 0:
            return False
            
        return (x >= self.left and y >= self.top and x <= self.right and y <= self.bottom)
        
    def contains(self, bounds):
        if bounds.area == 0:
            return False
            
        return self.contains_point(bounds.left, bounds.top) and self.contains_point(bounds.right, bounds.bottom)
    
    def intersect(self, bounds):
        p1 = Point(max(self.left, bounds.left), max(self.top, bounds.top))
        p2 = Point(min(self.right, bounds.right), min(self.bottom, bounds.bottom))
        
        return Bounds(p1, p2)

    def __str__(self):
        return "%s%s" % (self.p1, self.p2)

    def equals(self, bounds):
        return self.p1.equals(bounds.p1) and self.p2.equals(bounds.p2)

    @staticmethod
    def to_bounds(str_bounds):
        p1 = Point(0,0)
        p2 = Point(0,0)
        try:
            m = re.match(Bounds.BOUNDS_PROG, str_bounds)
            if(m is not None):
                p1 = Point(int(m.group(1)), int(m.group(2)))
                p2 = Point(int(m.group(3)), int(m.group(4)))
        except:
            pass

        return Bounds(p1, p2)
        
    ###################################### Optional
    def to_swipe_val(self):
        center = self.center
        x = self.p2.x-self.SCROLL_SWIPE_MARGIN
        if x < 0:
            x = self.SCROLL_SWIPE_MARGIN

        afrom = Point(x, center.y)
        ato = Point(self.p1.x+self.SCROLL_SWIPE_MARGIN, center.y)

        return Bounds(afrom, ato)

    def to_scroll_val(self):
        center = self.center
        y = self.p2.y-self.SCROLL_SWIPE_MARGIN
        if y < 0:
            y = self.SCROLL_SWIPE_MARGIN

        afrom = Point(center.x, y)
        ato = Point(center.x, self.p1.y+self.SCROLL_SWIPE_MARGIN)

        return Bounds(afrom, ato)

    def to_touch_val(self):
        return self.center
