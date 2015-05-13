# Copyright (c) 2015-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
#
from __future__ import print_function

import output 

class ColorPrinter(object):

    """A thin wrapper over screens in ncurses that caches colors and
    attribute state"""

    DEFAULT_COLOR_INDEX = 1

    def __init__(self, screen, cursesAPI):
        self.colors = {}
        self.colors[(0, 0)] = 0  # 0,0 = white on black is hardcoded
        # in general, we want to use -1,-1 for most "normal" text printing
        self.colors[(-1, -1)] = self.DEFAULT_COLOR_INDEX
        self.cursesAPI = cursesAPI
        self.cursesAPI.initPair(self.DEFAULT_COLOR_INDEX, -1, -1)
        self.screen = screen
        self.currentAttributes = False  # initialized in setAttributes

    def setAttributes(self, foreColor, backColor, other):
        colorIndex = -1
        colorPair = (foreColor, backColor)
        if not colorPair in self.colors:
            newIndex = len(self.colors)
            if newIndex < self.cursesAPI.getColorPairs():
                self.cursesAPI.initPair(newIndex, foreColor, backColor)
                self.colors[colorPair] = newIndex
                colorIndex = newIndex
        else:
            colorIndex = self.colors[colorPair]

        attr = self.cursesAPI.colorPair(colorIndex)

        attr = attr | other

        self.currentAttributes = attr

        self.screen.attrset(self.currentAttributes)

    def restoreAttributes(self):
        self.screen.attrset(self.currentAttributes)

    def addstr(self, y, x, text, attr=None):
        if attr is None:
            attr = self.cursesAPI.colorPair(self.DEFAULT_COLOR_INDEX)

        self.screen.addstr(y, x, text, attr)