from plotter import *

def eneg(elt):
    """Electronegativity"""
    return elt['electronegativity']

def mass(elt):
    """Mass"""
    return elt['mass']

def rat(elt):
    """Mass/Electronegativity"""
    return elt['electronegativity']/elt['mass']

epd = ElementDataPlotter(elements=['Fe','Ni','Li','Bi'])
#epd.make_periodic_table(values=[eneg, mass, rat])
#plt.show()

epd.make_pettifor_map(mass, eneg)
plt.show()

#epd.make_periodic_table()
#plt.show()
