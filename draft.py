import pynini
bruh = pynini.Fst()
bruh |= pynini.cross('một', '1')
bruh |= pynini.cross('hai', '2')
bruh.rmepsilon()
lattice = pynini.compose('một hai', bruh)
print(lattice.string())
