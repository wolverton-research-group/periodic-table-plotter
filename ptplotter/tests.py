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

def atomic_number(elt):
    """Atomic number"""
    return elt['z']


epd = ElementDataPlotter()#elements=['Fe','Ni','Li','Bi'])
epd.make_pettifor_map(mass, eneg)
plt.savefig('pettifor.png', bbox_inches='tight')

epd = ElementDataPlotter()#elements=['Fe','Ni','Li','Bi'])
epd.make_periodic_table(values=[eneg])
plt.savefig('uni.png', bbox_inches='tight')

epd = ElementDataPlotter()
epd.make_periodic_table(values=[eneg, mass], colorbar=False)
plt.savefig('bi.png', bbox_inches='tight')

epd = ElementDataPlotter()
epd.make_periodic_table(values=[eneg, mass, rat], colorbar=False)
plt.savefig('tri.png', bbox_inches='tight')

epd = ElementDataPlotter()
epd.make_periodic_table(values=[eneg, mass, rat, atomic_number], colorbar=False)
plt.savefig('quad.png', bbox_inches='tight')
