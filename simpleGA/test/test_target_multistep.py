#!/usr/bin/env python3

from selfies import decoder, encoder
from simpleGA.selfies_solver import SelfiesGenAlgSolver
from simpleGA.fitness_functions_selfies import fitness_function_target_selfies
from simpleGA.wrappers import (
    sc2smiles,
    sc2selfies,
    sc2mol_structure,
    mol_structure2depictions,
)


def test_target_multistep():

    target_smiles = "CC(=O)NCCc1c[nH]c2c1cc(cc2)OC"
    target_selfies = encoder(target_smiles)
    print(
        "This test attempts to generate melatonin from random molecules in several steps. \n The target SELFIES is : {0}".format(
            target_selfies
        )
    )
    starting_selfies = []
    for i in range(50):
        solver = SelfiesGenAlgSolver(
            starting_random=True,
            n_genes=30,
            fitness_function=fitness_function_target_selfies(
                target_selfies, function_number=2
            ),  # See fitness_function_target_selfies
            max_gen=100,
            pop_size=50,
            n_crossover_points=2,
            to_file=False,
            verbose=False,
        )
        solver.solve()
        selfies = sc2selfies(solver.best_individual_)
        print(
            "The best fitness score is : {0} \nThe corresponding SELFIES is : {1}".format(
                solver.best_fitness_, sc2smiles(solver.best_individual_)
            )
        )
        starting_selfies.append(selfies)

    solver = SelfiesGenAlgSolver(
        starting_selfies=starting_selfies,
        n_genes=30,
        fitness_function=fitness_function_target_selfies(
            target_selfies, function_number=1
        ),  # See fitness_function_target_selfies
        max_gen=100,
        pop_size=50,
        n_crossover_points=2,
        logger_file="multistep.log",
        verbose=False,
        to_file=True,
        progress_bars=True,
    )
    solver.solve()
    selfies = sc2selfies(solver.best_individual_)
    print(
        "The best fitness score is : {0} \nThe corresponding SELFIES is : {1}".format(
            solver.best_fitness_, sc2smiles(solver.best_individual_)
        )
    )
    mol = sc2mol_structure(solver.best_individual_)
    mol_structure2depictions(mol, root_name="multistep")


if __name__ == "__main__":
    test_target_multistep()