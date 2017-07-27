import operator

import numpy as np
import pytest

from cgp.cgp import *


@pytest.fixture()
def pset():
    terminals = [Terminal("x_0"), Terminal("x_1")]
    operators = [Primitive("neg", operator.neg, 1)]
    pset = create_pset(terminals + operators)
    return pset

@pytest.fixture(params=[pset])
def individual(request):
    pset = request.param()
    MyCartesian = type("MyCartesian", (Base, ), {"pset": pset})
    code = [[[2, 0]]]
    outputs = [2]
    return MyCartesian(code, outputs)


def test_PrimitiveSet(pset):
    assert pset.mapping == {0: pset.terminals[0], 1: pset.terminals[1], 2: pset.operators[0]}
    assert pset.max_arity == 1
    assert pset.context[pset.operators[0].name] == operator.neg


def test_Cartesian(individual):
    x = np.ones((1, 2))
    y = individual.fit_transform(x)
    assert y == np.array([-1])

def test_Cartesian_get(individual):
    assert individual[0] == 0
    assert individual[1] == 1

def test_Cartesian_set(individual):
    n = len(individual)
    individual[n-1] = 1
    assert individual.outputs[0] == 1

def test_to_polish(individual):
    polish, used_arguments = to_polish(individual)
    assert polish == ["neg(x_0)"]
    assert len(used_arguments) == 1


def test_boilerplate(individual):
    assert boilerplate(individual) == "lambda x_0, x_1:"
    assert boilerplate(individual, used_arguments=[individual.pset.terminals[0]]) == "lambda x_0:"


def test_compile(individual):
    f = compile(individual)
    assert f(1, 1) == -1