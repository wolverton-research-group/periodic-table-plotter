import matplotlib
matplotlib.use('Agg')
import plotter
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
        epd = plotter.ElementDataPlotter(elements=elts)
        epd.pettifor(mass, eneg)

    def test_periodic_table(self):
        f = StringIO()
        epd = plotter.ElementDataPlotter()#elements=['Fe','Ni','Li','Bi'])
        epd.ptable([eneg])

        epd = plotter.ElementDataPlotter()
        epd.ptable([eneg, mass])
        epd.create_guide_square(x=8, y=-1.5)

        epd = plotter.ElementDataPlotter()
        epd.ptable([[eneg, mass], rat])

        epd = plotter.ElementDataPlotter()
        epd.ptable([eneg, mass, rat, atomic_number], colorbar=False)

    def test_grid(self):
        epd = plotter.ElementDataPlotter()
        elts = [ 'Ti', 'V', 'Sc', 'Ni', 'Co', 'Fe' ]
        epd.make_grid(xelts=elts, yelts=elts)
