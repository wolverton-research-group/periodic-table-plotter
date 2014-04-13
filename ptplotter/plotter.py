import os, os.path
import yaml

import numpy as np
import matplotlib.pylab as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

INSTALL_PATH = os.path.dirname(os.path.abspath(__file__))

__all__ = ['ElementDataPlotter', 'plt', 'Square']

def atomic_number(elt):
    """Atomic number (Z)"""
    return elt['z']

def get_colors(values, **kwargs):
    """
    For an arbitrary list of values, return a list of colors.
    """
    raise NotImplementedError

def symbol(data):
    return data['symbol']

class ElementDataPlotter(object):
    """

    Notes:
        
        To change the square label: data[elt]['symbol'] = 'new string'

    """
    def __init__(self, data={}, elements=None, pair_data={}):
        """
        """
        _data = yaml.load(open(INSTALL_PATH+'/elements.yml').read())
        _pair_data = {}
        _d = {}
        for elt, value in _data.items():
            assert isinstance(value, dict)
            if elements:
                if not elt in elements:
                    continue
            _d[elt] = _data[elt]
            if elt in data:
                _d[elt].update(data[elt])
        
        for pair, value in pair_data.items():
            _pair_data[frozenset(pair)] = value

        self._pd = _pair_data
        self._d = _d

    def make_periodic_table(self, values=[atomic_number], colors='jet',
            plot=True, **kwargs):
        self.values = values
        self.colors = colors
        fig, ax = plt.subplots()
        fig.patch.set_visible(False)
        ax.axis('off')
        squares = []
        _values = []
        indices = []
        for elt, data in self._d.items():
            x = data['group']
            y = data['period']

            if x == 0:
                if data['z'] > 56 and data['z'] < 74:
                    # is a lanthanide 
                    y = 9.0
                    x =  data['z'] - 54
                elif data['z'] > 88 and data['z'] < 106:
                    # is an actinide
                    y = 10.0
                    x = data['z'] - 86

            vals = [ v(data) for v in values ]
            _values += vals
            indices += [ i for i in range(len(values)) ]
            squares.append(Square(x, -y, data['symbol'], vals, dy=-1.0,
                **kwargs))

        self.values = _values
        self.indices = indices
        self.squares = squares
        self.patches = []
        for s in squares:
            self.patches += s.patches

        if isinstance(colors, basestring):
            colors = [colors]*len(values)

        if not plot:
            return

        collections = []
        for i, val in enumerate(values):
            cmap = plt.get_cmap(colors[i]) 
            values = []
            patches = []
            for s in self.squares:
                patches.append(s.patches[i])
                values.append(s.data[i])
            pc = PatchCollection(patches, cmap=cmap, edgecolor="grey")
            pc.set_array(np.array(values))
            ax.add_collection(pc)
            if kwargs.get('colorbar', True):
                options = {
                        'orientation':'horizontal',
                        'pad':0.025, 'aspect':60
                        }
                options.update(kwargs)
                cbar = plt.colorbar(pc, **options)
                if val.__doc__:
                    cbar.set_label(val.__doc__)

        ax.autoscale_view()
        ax.set_xticks([])
        ax.set_yticks([])
        return ax, collections

    def add_legend(self, values):
        patches = Square(0, 0, range(len(values)))

    def make_arbitrary_grid(self, xelts=[], yelts=[], values=None):
        """
        Plots a grid of squares colored by one or more properties for A-B 
        element combinations. 
        """
        fig, ax = plt.subplots()
        x, y = [], []
        if not xelts:
            xelts = self.pair_data.keys()

        if not yelts:
            for x in xelts:
                yelts += self.pair_data[x].keys()

    def make_pettifor_map(self, xaxis=atomic_number, yaxis=atomic_number,
            label=symbol):
        """
        Create a pettifor map with the specified x- and y-axes.

        Keyword Arguments:
            xaxis:
                Function that takes a dict as an input, and returns a number.
                For each element in the 

        """
        fig, ax = plt.subplots()
        x, y = [],[]
        for elt, data in self._d.items():
            xx = xaxis(data)
            yy = yaxis(data)
            x.append(xx)
            y.append(yy)
            plt.text(xx, yy, label(data))
        plt.scatter(x, y)

        ax.autoscale_view()
        plt.xlabel(xaxis.__doc__)
        plt.ylabel(yaxis.__doc__)

class Square(object):
    def __init__(self, x, y, s=None, data=[],
            dx=1., dy=1., **kwargs):
        self.x, self.y = x,y
        self.dx, self.dy = dx, dy
        self.label = s
        self.data = data
        self.dims = len(data)
        self.set_patches(**kwargs)
        if self.label:
            plt.text(self.x + self.dx/2, self.y+self.dy/2, self.label, ha='center',
                    va='center', fontdict={'color':'white'})# {'weight' : 'bold'})#, 'color':"white"})

    def __getitem__(self, index):
        return self.patches[index]

    def __len__(self):
        return len(self.patches)

    def set_patches(self, **kwargs):
        if self.dims == 1:
            self.single_color(**kwargs)
        elif self.dims == 2:
            self.bicolor(**kwargs)
        elif self.dims == 3:
            self.tricolor(**kwargs)
        elif self.dims == 4:
            self.tetracolor(**kwargs)
        else:
            self.patches = []

    def single_color(self, **kwargs):
        """
        Creates a single Patch.

        +------------+
        |            |
        |            |
        |     1st    |
        |            |
        |            |
        +------------+

        """
        x1, x2 = self.x, self.x+self.dx
        y1, y2 = self.y, self.y+self.dy
        patch = Polygon([
            [x1, y1], # origin
            [x2, y1], # to bottom right
            [x2, y2], # to top right
            [x1, y2], # to top left
            [x1, y1]])# to origin
        self.patches = [patch]

    def bicolor(self, **kwargs):
        """
        Plots 2 colors in a square:

        +-------------+
        |            /|
        |   1st    /  |
        |        /    |
        |      /      |
        |    /        |
        |  /   2nd    |
        |/            |
        +-------------+

        """
        x1, x2 = self.x, self.x+self.dx
        y1, y2 = self.y, self.y+self.dy

        top = Polygon([
            [x1, y1], # origin
            [x1, y2], # to top left
            [x2, y1], # to bottom right
            [x1, y1]]) # back to origin

        bot = Polygon([
            [x2, y2], # top right
            [x1, y2], # to top left
            [x2, y1], # to bottom right
            [x2, y2]]) # back to top right

        self.patches = [top, bot]

    def tricolor(self, **kwargs):
        """
        Plots 3 values in a square:

        +-----+-----+
        |     |     |
        | 1st | 2nd |
        |    / \    |
        |   /   \   |
        |  /     \  |
        | /  3rd  \ |
        |/         \|
        +-----------+

        """
        x1, x2 = self.x, self.x+self.dx
        x3 = self.x + self.dx*0.5
        y1, y2 = self.y, self.y+self.dy
        y3 = self.y + self.dy*0.666

        left = Polygon([
            [x3, y3], # center
            [x1, y1], # to bottom left
            [x1, y2], # to top left
            [x3, y2], # to top middle
            [x3, y3]])# back to center

        right = Polygon([
            [x3, y3], # center
            [x2, y1], # to bottom right
            [x2, y2], # to top right
            [x3, y2], # to top middle
            [x3, y3]])# back to center

        bot = Polygon([
            [x3, y3], # center
            [x1, y1], # to bottom left
            [x2, y1], # to bottom right
            [x3, y3]])# back to center
        self.patches = [left, right, bot]

    def tetracolor(self, **kwargs):
        """
        Plots 4 values in a square:

        +------+-----+
        |      |     |
        | 1st  | 2nd |
        |      |     |
        +------+-----+
        |      |     |
        | 4th  | 3rd |
        |      |     |
        +------+-----+

        """
        x1, x2 = self.x, self.x+self.dx
        y1, y2 = self.y, self.y+self.dy
        x3 = (x1+x2)/2
        y3 = (y1+y2)/2

        bl = Polygon([
            [x3, y3], # center
            [x3, y1], # to middle bottom
            [x1, y1], # to bottom left
            [x1, y3], # to middle left
            [x3, y3]])# back to center
        tl = Polygon([
            [x3, y3], # center
            [x3, y2], # to middle top
            [x1, y2], # to top left
            [x1, y3], # to middle left
            [x3, y3]])# back to center
        tr = Polygon([
            [x3, y3], # center
            [x3, y2], # to middle top
            [x2, y2], # to top right
            [x2, y3], # to middle right
            [x3, y3]])# back to center
        br = Polygon([
            [x3, y3], # center
            [x3, y1], # to middle bottom
            [x2, y1], # to bottom right
            [x2, y3], # to middle right
            [x3, y3]])# back to center

        self.patches = [tl, tr, br, bl]

