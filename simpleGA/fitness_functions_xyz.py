import logging

from simpleGA.score_modifiers import score_modifier
from simpleGA.quantum_wrappers_xyz import gl2gap, gl2ehomo, gl2elumo

logger = logging.getLogger(__name__)


def fitness_function_xyz(
    function_number=1,
):

    if function_number == 1:  # gl2gap

        return lambda chromosome: gl2gap(chromosome)


def fitness_function_target_property(
    target,
    function_number=1,
    score_modifier_number=1,
    parameter=1,
):

    if function_number == 1:

        return lambda chromosome: score_modifier(
            gl2gap(chromosome),
            target,
            score_modifier_number,
            parameter,
        )
