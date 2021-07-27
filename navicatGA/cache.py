import numpy as np
import types
import logging
from functools import lru_cache
from navicatGA.chemistry_selfies import get_selfie_chars
from navicatGA.wrappers_selfies import sc2selfies
from navicatGA.wrappers_smiles import sc2smiles
from navicatGA.wrappers_xyz import gl2geom

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        from functools import lru_cache

        print("Monkeypatching the calculate_fitness method to add cacheing.")
    except ImportError as m:
        print(m)


def calculate_fitness_cache_selfies(self, population):
    """
    Calculates the fitness of the population using a SELFIES adapted cache.
    
    Parameters:
    :param population: population state at a given iteration
    :return: the fitness of the current population
    """
    if self.scalarizer is None:
        nvals = 1
    else:
        nvals = len(self.scalarizer.goals)
    fitness = np.zeros(shape=(population.shape[0], nvals), dtype=float)
    logger.debug("Evaluating fitness individually with cache.")

    for i in range(population.shape[0]):
        chromosome = population[i][0 : self.n_genes]
        selfies = sc2selfies(chromosome)
        fitness[i, :] = calculate_one_fitness_cache_selfies(
            selfies, self.fitness_function
        )

    logger.trace(calculate_one_fitness_cache_selfies.cache_info())
    if self.scalarizer is None:
        return np.squeeze(fitness), np.squeeze(fitness)
    else:
        return self.scalarizer.scalarize(fitness), (fitness)


def calculate_fitness_cache_smiles(self, population):
    """
    Calculates the fitness of the population using a SMILES adapted cache.
    
    Parameters:
    :param population: population state at a given iteration
    :return: the fitness of the current population
    """
    if self.scalarizer is None:
        nvals = 1
    else:
        nvals = len(self.scalarizer.goals)
    fitness = np.zeros(shape=(population.shape[0], nvals), dtype=float)
    logger.debug("Evaluating fitness individually with cache.")

    for i in range(population.shape[0]):
        chromosome = population[i][0 : self.n_genes]
        smiles = sc2smiles(chromosome)
        fitness[i, :] = calculate_one_fitness_cache_smiles(
            smiles, self.hashable_fitness_function
        )

    logger.trace(calculate_one_fitness_cache_selfies.cache_info())
    if self.scalarizer is None:
        return np.squeeze(fitness), np.squeeze(fitness)
    else:
        return self.scalarizer.scalarize(fitness), (fitness)


def calculate_fitness_cache_xyz(self, population):
    """
    Calculates the fitness of the population using a XYZ adapted cache.
    
    Parameters:
    :param population: population state at a given iteration
    :return: the fitness of the current population
    """
    if self.scalarizer is None:
        nvals = 1
    else:
        nvals = len(self.scalarizer.goals)
    fitness = np.zeros(shape=(population.shape[0], nvals), dtype=float)
    logger.debug("Evaluating fitness individually with cache.")
    for i in range(population.shape[0]):
        chromosome = population[i][0 : self.n_genes]
        geom = gl2geom(chromosome, self.h_positions)[1]
        fitness[i, :] = calculate_one_fitness_cache_xyz(
            geom, self.hashable_fitness_function
        )
    logger.trace(calculate_one_fitness_cache_xyz.cache_info())
    if self.scalarizer is None:
        return np.squeeze(fitness), np.squeeze(fitness)
    else:
        return self.scalarizer.scalarize(fitness), (fitness)


def calculate_fitness_cache(self, population):
    """
    Calculates the fitness of the population using a hashable fitness function.
    
    Parameters:
    :param population: population state at a given iteration
    :return: the fitness of the current population
    """
    if self.scalarizer is None:
        nvals = 1
    else:
        nvals = len(self.scalarizer.goals)
    fitness = np.zeros(shape=(population.shape[0], nvals), dtype=float)
    for i in range(population.shape[0]):
        chromosome = population[i][0 : self.n_genes]
        hashed_list = self.fitness_function(chromosome)
        fitness[i, :] = calculate_one_fitness_cache_xyz(
            hashed_list, self.hashable_fitness_function
        )
    logger.trace(self.hashable_fitness_function.cache_info())
    if self.scalarizer is None:
        return np.squeeze(fitness), np.squeeze(fitness)
    else:
        return self.scalarizer.scalarize(fitness), (fitness)


@lru_cache(maxsize=128)
def calculate_one_fitness_cache_selfies(selfies, hashable_fitness_function):
    return hashable_fitness_function(selfies)


@lru_cache(maxsize=128)
def calculate_one_fitness_cache_smiles(smiles, hashable_fitness_function):
    return hashable_fitness_function(smiles)


@lru_cache(maxsize=128)
def calculate_one_fitness_cache_xyz(geom, hashable_fitness_function):
    return hashable_fitness_function(geom)


def set_lru_cache(self):
    """
    Monkeypatches the calculate_fitness method of the base solver class in order to use a lru cache.
    If a specific wrapper exists for a given solver, it will try to use the unique expression of genes
    given by that wrapper to generate a hashable fitness function. If not, it will require
    a hashable fitness function given by the user AND expect the given fitness_function to generate
    a unique hash from a gene.
    """
    if self.problem_type == "selfies":
        self.calculate_fitness = types.MethodType(calculate_fitness_cache_selfies, self)
    elif self.problem_type == "smiles":
        self.calculate_fitness = types.MethodType(calculate_fitness_cache_smiles, self)
    elif self.problem_type == "xyz":
        self.calculate_fitness = types.MethodType(calculate_fitness_cache_xyz, self)
    else:
        self.calculate_fitness = types.MethodType(calculate_fitness_cache, self)
