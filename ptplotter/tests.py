from plotter import ElementDataPlotter
import matplotlib.pylab as plt
import random

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

pair_data_elts = [ 'Ti', 'V', 'Sc', 'Ni', 'Co', 'Fe' ]

pair_data = {}
for elt in pair_data_elts:
    for elt2 in pair_data_elts:
        pair_data[frozenset([elt, elt2])] = {'property':random.random()}

def test_pettifor():
    epd = ElementDataPlotter()#elements=['Fe','Ni','Li','Bi'])
    epd.pettifor(mass, eneg)
    plt.savefig('pettifor.png', bbox_inches='tight')

def test_periodic_table():
    epd = ElementDataPlotter()#elements=['Fe','Ni','Li','Bi'])
    epd.ptable([eneg])
    plt.savefig('uni.png', bbox_inches='tight')

    epd = ElementDataPlotter()
    epd.ptable([eneg, mass])
    plt.savefig('bi.png', bbox_inches='tight')

    epd = ElementDataPlotter()
    epd.ptable([[eneg, mass], rat])
    plt.savefig('tri.png', bbox_inches='tight')

    epd = ElementDataPlotter()
    epd.ptable([eneg, mass, rat, atomic_number])
    plt.savefig('quad.png', bbox_inches='tight')

def test_grid():
    epd = ElementDataPlotter(pair_data=pair_data)
    epd.make_grid()
    plt.savefig('grid.png', bbox_inches='tight')

test_pettifor()
test_periodic_table()
test_grid()
