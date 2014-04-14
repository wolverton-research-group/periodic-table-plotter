import matplotlib
matplotlib.use('Agg')
from plotter import ElementDataPlotter
import matplotlib.pylab as plt
import random
from StringIO import StringIO
from unittest import TestCase

def eneg(elt):
    """Electronegativity"""
    return elt['electronegativity']

def mass(elt):
    """Mass"""
    return elt['mass']

def rat(elt):
    """Mass/Electronegativity"""
    return elt['electronegativity']/elt['mass']

def atomic_number(elt):
    """Atomic number"""
    return elt['z']

class ElementDataPlotterTestCase(TestCase):
    def test_pettifor(self):
        elts = ['H', 'Li', 'Be', 'Fe', 'Ni', 'Pd', 'Pt', 'F', 'Xe', 'O', 'S']
        epd = ElementDataPlotter(elements=elts)
        epd.pettifor(mass, eneg)
        f = StringIO()
        plt.savefig(f, bbox_inches='tight')

    def test_periodic_table(self):
        f = StringIO()
        epd = ElementDataPlotter()#elements=['Fe','Ni','Li','Bi'])
        epd.ptable([eneg])
        plt.savefig(f, bbox_inches='tight')

        epd = ElementDataPlotter()
        epd.ptable([eneg, mass])
        epd.create_guide_square(x=8, y=-1.5)
        plt.savefig(f, bbox_inches='tight')

        epd = ElementDataPlotter()
        epd.ptable([[eneg, mass], rat])
        plt.savefig(f, bbox_inches='tight')

        epd = ElementDataPlotter()
        epd.ptable([eneg, mass, rat, atomic_number], colorbar=False)
        plt.savefig(f, bbox_inches='tight')

    def test_grid(self):
        epd = ElementDataPlotter()
        elts = [ 'Ti', 'V', 'Sc', 'Ni', 'Co', 'Fe' ]
        epd.make_grid(xelts=elts, yelts=elts)
        f = StringIO()
        plt.savefig(f, bbox_inches='tight')
