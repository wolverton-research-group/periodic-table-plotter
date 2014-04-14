from __future__ import division
import os, os.path
import yaml

import numpy as np
import matplotlib.pylab as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

INSTALL_PATH = os.path.dirname(os.path.abspath(__file__))

__all__ = ['ElementDataPlotter', 'plt', 'Square']

elt_data = yaml.load(open(INSTALL_PATH+'/elements.yml').read())

def atomic_number(elt):
    """Atomic number (Z)"""
    return elt['z']

def eneg_diff(data):
    d = sorted([ elt_data[elt]['electronegativity'] for elt in data['pair']])
    return abs(d[0] - d[1])

def symbol(data):
    return data['symbol']

def get_coord_from_symbol(data):
    """Determines the cartesian coordinate of an element on the periodic
    table."""
    if isinstance(data, basestring):
        data = elt_data[data]
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
    return x, -y

class ElementDataPlotter(object):
    """
    Create an ElementDataPlotter which has all initial elemental data, plus
    custom elemental data, and custom pairwise elemental data.

    ..Notes::
        To change the square label: data[elt]['symbol'] = 'new string'

    ..Notes::
        The following variables are available (and correspond to an appropriate
        value) in any function you write:
        
        covalent_radii, scattering_factors, symbol, specific_heat,
        period, p_elec, volume, atomic_radii, f_elec, s_elec,
        electronegativity, d_elec, group, van_der_waals_radii, density,
        first_ionization_energy, melt, name, production, mass, z, and boil.

    Examples::
        
        >>> epd = ElementDataPlotter()
        >>> epd.ptable([func1, func2, func3], cmap_groups=[0,0,1])
        >>> plt.show()

    """
    def __init__(self, data={}, elements=None, pair_data={}, **kwargs):
        data = dict(elt_data)
        elts = {}
        for elt, value in data.items():
            assert isinstance(value, dict)
            if elements:
                if not elt in elements:
                    continue
            elts[elt] = data[elt]
            if elt in data:
                elts[elt].update(data[elt])
        
        self._pairs = pair_data
        self._elts = elts

        self._squares = []
        self._patches = []
        self.functions = []
        self.collections = []
        self.cmap_groups = []
        self.cmaps = []
        self._data = []

        if not 'axes' in kwargs:
            fig, axes = plt.subplots()
            fig.patch.set_visible(False)
        else:
            axes = kwargs.get('axes')
        self._ax = axes

    def add_square(self, square):
        self._squares.append(square)
        for ind, patch in zip(self.cmap_groups, square.patches):
            self.collections[ind].append(patch)

    def set_functions(self, functions):
        if not isinstance(functions, list):
            functions = [functions]
        self.functions = functions

    def set_cmap_groups(self, cmap_groups, cmaps=None):
        if not self.functions:
            raise InputError("Cannot assign cmap groups without first"
                    "assigning functions for the cmap")
        if cmap_groups is None:
            cmap_groups = [ i for i in range(len(self.functions))]
        self.cmap_groups = cmap_groups
        if cmaps is None:
            self.cmaps = ['jet' for i in range(len(cmap_groups)) ]

        self.collections = [ [] for i in range(len(cmap_groups)) ]


    def create_guide_square(self, x=7, y=-2.5,  **kwargs):
        data = [ 0 for v in self.functions ]
        dl = [ f.__doc__ for f in self.functions ]
        guide_square = Square(x, y, data=data, data_labels=dl, **kwargs)
        for p in guide_square.patches:
            p.set_facecolor(kwargs.get('color', 'white'))
        guide_square.set_labels()
        self._ax.add_collection(PatchCollection(guide_square.patches))

    def make_grid(self, xelts=[], yelts=[], functions=[eneg_diff],
            cmap_groups=None, **kwargs):
        """
        Plots a grid of squares colored by one or more properties for A-B 
        element combinations. 
        """
        self.set_functions(functions)
        self.set_cmap_groups(cmap_groups)

        if not xelts and not yelts:
            elts = set()
            for pair in self._pairs:
                elts |= set(pair)
            xelts = list(elts)
            yelts = list(elts)

        collections = []
        for i, elt1 in enumerate(xelts):
            self._ax.text(i+0.5, -0.25, elt1, va='center', ha='right')
            for j, elt2 in enumerate(yelts):
                pair = (elt1, elt2)
                data = self._pairs.get(frozenset(pair), {})
                if isinstance(data, dict):
                    data['pair'] = pair
                vals = [f(data) for f in functions]
                square = Square(i, j, data=vals)
                self.add_square(square)

        for j, elt2 in enumerate(yelts):
            self._ax.text(-0.25, j+0.5, elt2, va='bottom', ha='center')

        self._draw_collections()
        self._ax.autoscale_view()

    def ptable(self, functions=[atomic_number], cmap_groups=None,
            cmaps=None, **kwargs):
        """
        Create Squares in the form a periodic table.
        """
        self.set_functions(functions)
        self.set_cmap_groups(cmap_groups, cmaps=cmaps)

        self._ax.axis('off')
        self._ax.set_xticks([])
        self._ax.set_yticks([])

        for elt, data in self._elts.items():
            x, y = get_coord_from_symbol(elt)
            vals = [ f(data) for f in functions ]
            square = Square(x, y, label=data['symbol'], data=vals, **kwargs)
            self.add_square(square)
        self._draw_collections()

    def _draw_collections(self, **kwargs):
        self.cbars = []
        for i in range(len(self.collections)):
            c = self.collections[i]
            pc = PatchCollection(c, cmap=self.cmaps[i])
            pc.set_array(np.array([ p.value for p in c ]))
            self._ax.add_collection(pc)
            options = {
                    'orientation':'horizontal',
                    'pad':0.025, 'aspect':60
                    }
            options.update(kwargs)
            cbar = plt.colorbar(pc, **options)
            #cbar.set_label(label)
            self.cbars.append(cbar)

        fontdict = kwargs.get('font', {'color':'white'})
        fontdict.update(**kwargs)
        for s in self._squares:
            if not s.label:
                continue
            x = s.x + s.dx/2
            y = s.y + s.dy/2
            self._ax.text(x, y, s.label, ha='center', 
                                         va='center', 
                                         fontdict=fontdict)
        self._ax.autoscale_view()

    def pettifor(self, xaxis=atomic_number, yaxis=atomic_number,
            label=symbol):
        """
        Create a pettifor map with the specified x- and y-axes.

        Keyword Arguments:
            xaxis, yaxis:
                Function that takes a dict as an input, and returns a number.
                Will plot this data point with the elements symbol at the
                coordinate determined by the xaxis and yaxis functions.

        Examples::

            >>> # Define a function with the desired axis label as the
            >>> # docstring and which returns the x or y coord for the point.
            >>> def eneg2(d):
            >>>     '''Electronegativity squared'''
            >>>     return d['electronegativity']**2
            >>> epd = ElementDataPlotter()
            >>> # then assign that function to an axis
            >>> # (both axes are the atomic number by default)
            >>> epd.pettifor(xaxis=eneg2)
            >>> plt.show()

        """
        x, y = [],[]
        for elt, data in self._elts.items():
            xx = xaxis(data)
            yy = yaxis(data)
            x.append(xx)
            y.append(yy)
            self._ax.text(xx, yy, label(data))
        self._ax.scatter(x, y)
        self._ax.autoscale_view()
        self._ax.set_xlabel(xaxis.__doc__)
        self._ax.set_ylabel(yaxis.__doc__)

class Square(object):
    def __init__(self, x, y, label=None, data=[], data_labels=[],
            dx=1., dy=1., **kwargs):
        self.x, self.y = x,y
        self.dx, self.dy = dx, dy
        self.label = label
        self.data = data
        self.data_labels = data_labels
        self.dims = len(data)
        self.set_patches(**kwargs)
        for p, d in zip(self.patches, self.data):
            p.value = d

    def __getitem__(self, index):
        return self.patches[index]

    def __len__(self):
        return len(self.patches)

    def set_labels(self, **kwargs):
        if self.dims == 1:
            self.single_label(**kwargs)
        elif self.dims == 2:
            self.double_label(**kwargs)
        elif self.dims == 3:
            self.triple_label(**kwargs)
        elif self.dims == 4:
            self.quadra_label(**kwargs)

    def set_patches(self, **kwargs):
        if self.dims == 1:
            self.single_color(**kwargs)
        elif self.dims == 2:
            self.double_color(**kwargs)
        elif self.dims == 3:
            self.triple_color(**kwargs)
        elif self.dims == 4:
            self.quadra_color(**kwargs)
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

    def single_label(self, position="top", **kwargs):
        """
        Labels a single Patch. Label position can be set with the "position"
        keyword argument as shown below:
                
                   top
             +------------+
             |            |
             |            |
        left |     1st    | right
             |            |
             |            |
             +------------+
                bottom
        """
        if position == 'top':
            x = self.x + self.dx/2
            y = self.y + self.dy*1.25
            ha, va = 'center', 'bottom'
        elif position == 'bottom':
            x = self.x + self.dx/2
            y = self.y - self.dy*0.25
            ha, va = 'center', 'top'
        elif position == 'left':
            x = self.x - self.dx*0.25
            y = self.y + self.y/2
            ha, va = 'right', 'center'
        elif position == 'right':
            x = self.x + self.dx*1.25
            y = self.y + self.y/2
            ha, va = 'left', 'center'
        else:
            raise ValueError("`position` must be one of:"
                    "'top', 'bottom', 'left', 'right'")
        fontdict = kwargs.get('fontdict', {})
        plt.text(x, y, self.data_labels[0], ha=ha, va=va, fontdict=fontdict) 

    def double_color(self, **kwargs):
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

    def double_label(self, position="horizontal", **kwargs):
        """
        Plots 2 colors in a square:
            
                      vertical
                   +-------------+
                   |            /|
                   |   1st    /  |
                   |        /    |
        horizontal |      /      | horizontal
                   |    /        |
                   |  /   2nd    |
                   |/            |
                   +-------------+
                       vertical
        """
        if position == 'horizontal':
            x1 = self.x - self.dx*0.25
            x2 = self.x + self.dx*1.25
            y1 = y2 = self.y + self.dy/2
            ha1, ha2 = 'right', 'left'
            va1 = va2 = 'center'
        elif position == 'vertical':
            x1 = x2 = self.x + self.dx/2
            y1 = self.y + self.dy*1.25
            y2 = self.y - self.dy*0.25
            ha1 = ha2 = 'center'
            va1, va2 = 'bottom', 'top'
        else:
            raise ValueError("`position` must be one of:"
                    "'horizontal', 'vertical'")
        fontdict = kwargs.get('fontdict', {})
        plt.text(x1, y1, self.data_labels[0], ha=ha1, va=va1, fontdict=fontdict) 
        plt.text(x2, y2, self.data_labels[1], ha=ha2, va=va2, fontdict=fontdict) 

    def triple_color(self, **kwargs):
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

    def triple_label(self, **kwargs):
        """
        Plots 3 values in a square:

                +-----+-----+
        label1  |     |     | label2
                | 1st | 2nd |
                |    / \    |
                |   /   \   |
                |  /     \  |
                | /  3rd  \ |
                |/         \|
                +-----------+
                    label3

        """
        x1 = self.x + self.dx*0.25
        x2 = self.x + self.dx*1.25
        x3 = self.x + self.dx/2
        y1 = y2 = self.y + self.dy*0.75
        y3 = self.y - self.dy*0.25
        fontdict = kwargs.get('fontdict', {})
        plt.text(x1, y1, self.data_labels[0], ha='right', fontdict=fontdict)
        plt.text(x2, y2, self.data_labels[1], ha='left', fontdict=fontdict)
        plt.text(x3, y3, self.data_labels[2], ha='center', va='top',
                fontdict=fontdict)

    def quadra_color(self, **kwargs):
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

    def quadra_label(self, **kwargs):
        """
        Plots 4 values in a square:

                +------+-----+
                |      |     |
        label1  | 1st  | 2nd | label2
                |      |     |
                +------+-----+
                |      |     |
        label4  | 4th  | 3rd | label3
                |      |     |
                +------+-----+

        """
        x1 = x4 = self.x + self.dx*0.75
        x2 = x3 = self.x + self.dx*0.25
        y1 = y2 = self.y - self.dy*0.25
        y3 = y4 = self.y + self.dy*1.25
        ha1 = ha4 = 'right'
        ha2 = ha3 = 'left'
        va = 'center'
        fontdict = kwargs.get('fontdict', {})
        plt.text(x1, y1, self.data_labels[0], ha=ha1, va=va, fontdict=fontdict)
        plt.text(x2, y2, self.data_labels[1], ha=ha2, va=va, fontdict=fontdict)
        plt.text(x3, y3, self.data_labels[2], ha=ha3, va=va, fontdict=fontdict)
        plt.text(x4, y4, self.data_labels[3], ha=ha4, va=va, fontdict=fontdict)
