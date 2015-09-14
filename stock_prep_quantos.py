# goal: compute grams of solute per gram of solvent, for a target concentration

from simtk.unit import *

# solvent properties (h2o at room temperature)
solvent_density = 1 * kilogram / liter
solvent_molar_mass = 18.01528 * grams/mole

# desired stock volume
solvent_volume = 10 * milliliter

# solute properties
molar_mass = dict()
molar_mass['glucose'] = 180.1559 * grams/mole
#molar_mass['amino_acids'] = # soup
molar_mass['folinic_acid'] = 601.5 * grams / mole # 473.44 * grams/mole
molar_mass['AMP'] = 365.24 * grams/mole
molar_mass['UMP'] = 368.15 * grams/mole
molar_mass['CMP'] = 367.16 * grams/mole
molar_mass['GMP'] = 407.18 * grams/mole

# target concentrations
target_concentration = dict()
target_concentration['glucose'] = 600 * millimolar
#target_concentration['amino_acids'] = # soup
target_concentration['folinic_acid'] = ((340 * micrograms / milliliter) / molar_mass['folinic_acid']).in_units_of(millimolar)
target_concentration['AMP']  = 12 * millimolar
target_concentration['UMP']  = 8.5 * millimolar
target_concentration['CMP']  = 8.5 * millimolar
target_concentration['GMP']  = 8.5 * millimolar

def compute_mass_fraction(solute_molar_mass,
                     solvent_volume,
                     solvent_density,
                     solvent_molar_mass,
                     target_concentration):

    # amount of solvent
    solvent_mass = solvent_volume*solvent_density
    mols_solvent = solvent_mass / solvent_molar_mass

    # required amount of solute
    mols_solute = (target_concentration * solvent_volume).in_units_of(moles)
    solute_mass = mols_solute * solute_molar_mass

    # compute molality
    molality = (mols_solute / solvent_mass).in_units_of(moles / kilogram)

    # compute_mass_fraction
    mass_fraction = solute_mass / solvent_mass

    return mass_fraction

if __name__=='__main__':
    for reagent in molar_mass:
        mass_fraction = compute_mass_fraction(molar_mass[reagent],
                        solvent_volume,
                        solvent_density,
                        solvent_molar_mass,
                        target_concentration[reagent])
        print('{0}: {1:.5f}'.format(reagent,mass_fraction))
