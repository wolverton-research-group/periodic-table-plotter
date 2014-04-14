periodic-table-plotter 
======================
[![Build Status](https://travis-ci.org/wolverton-research-group/periodic-table-plotter.svg?branch=master)](https://travis-ci.org/wolverton-research-group/periodic-table-plotter)

Make a periodic table that plots 1-4 values per tile, easily configure grids 
of pair-wise elemental data (with 1-4 values per tile) and create 
pettifor-style trend plots.

Periodic table with one value per tile

```python
def eneg(elt):
    """Electronegativity"""
    return elt['electronegativity']

epd = ElementDataPlotter()
epd.ptable([eneg])
plt.show()
```
![Single value colormap](ptplotter/examples/uni.png)

Periodic table with two values per tile
```python
def mass(elt):
    """Mass"""
    return elt['mass']

epd = ElementDataPlotter()
epd.ptable([eneg, mass])
plt.show()
```
![Double value colormap](ptplotter/examples/bi.png)

Periodic table with three values per tile
```python
def rat(elt):
    """Mass/Electronegativity"""
    return elt['electronegativity']/elt['mass']

epd = ElementDataPlotter()
epd.ptable([eneg, mass, rat])
plt.show()
```
![Triple value colormap](ptplotter/examples/tri.png)

Periodic table with four values per tile
```python
def atomic_number(elt):
    """Atomic number"""
    return elt['z']

epd = ElementDataPlotter()
epd.ptable([eneg, mass, rat, atomic_number])
plt.show()
```
![Quadrupel value colormap](ptplotter/examples/quad.png)

Pettifor style map:
```python
elts = ['H', 'Li', 'Be', 'Fe', 'Ni', 'Pd', 'Pt', 'F', 'Xe', 'O', 'S']
epd = ElementDataPlotter(elements=elts)
epd.pettifor(mass, eneg)
plt.savefig('pettifor.png', bbox_inches='tight')
plt.show()
```
![Pettifor map](ptplotter/examples/pettifor.png)

Grid of pair-wise elemental data:
```python
elts = [ 'Ti', 'V', 'Sc', 'Ni', 'Co', 'Fe' ]
epd = ElementDataPlotter()
epd.make_grid(xelts=elts, yelts=elts)
plt.show()
```
![Pair data](ptplotter/examples/grid.png)
