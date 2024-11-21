# Logical Reasoning Library

## Overview

This is a Python library for logical reasoning and propositional logic, providing a comprehensive set of classes to represent, manipulate, and evaluate logical sentences.

## Inspiration

This library was developed as part of the exploration of concepts introduced in Harvard's CS50 AI course (AI50), focusing on knowledge representation and reasoning techniques in artificial intelligence.

## Features

- Supports multiple logical operators:
  - Symbols (atomic propositions)
  - Negation (Not)
  - Conjunction (And)
  - Disjunction (Or)
  - Implication 
  - Biconditional

- Model checking for logical entailment
- Flexible sentence construction
- Symbol evaluation
- Formula generation

## Logical Sentence Classes

### `Sentence` (Base Class)
- Abstract base class for all logical sentences
- Provides common methods like `evaluate()`, `formula()`, and `symbols()`

### `Symbol`
- Represents atomic propositions
- Can be evaluated in a given model
- Stores a symbolic name

### `Not`
- Represents logical negation
- Negates the truth value of its operand

### `And`
- Represents logical conjunction
- Evaluates to True only if all conjuncts are True

### `Or`
- Represents logical disjunction
- Evaluates to True if at least one disjunct is True

### `Implication`
- Represents logical implication (=>)
- Follows standard truth table for material implication

### `Biconditional`
- Represents logical equivalence (<=>)
- True when both sides have the same truth value

## Model Checking

The `model_check()` function determines logical entailment:
- Checks if a knowledge base logically implies a query
- Uses recursive exhaustive checking of all possible symbol assignments

## Usage Example

```python
from logic import *

# Creating logical sentences
rain = Symbol("It is raining today")
hagrid = Symbol("Harry visited hagrid today")
dumbledore = Symbol("Harry visited dumbledore today")

# Creating knowledge base
knowledge = And(
	Implication(Not(rain), hagrid),
	Or(hagrid, dumbledore),
	Not(And(hagrid, dumbledore)),
	dumbledore
)

# Checking if the query is true or false depending on the knowledge based
result = model_check(knowledge, rain)
print(result)
```

Consider the following logical statements:
1. If it didn't rain, Harry visited Hagrid today.
2. Harry visited Hagrid or Dumbledore today, but not both.
3. Harry visited Dumbledore today.

Using logical reasoning, we can solve the question "Did it rain today?":

- We know Harry visited Dumbledore today.
- The second statement implies Harry cannot have visited both Hagrid and Dumbledore.
- Since Harry visited Dumbledore, he did not visit Hagrid.
- The first statement says that if it didn't rain, Harry would have visited Hagrid.
- But we know Harry did not visit Hagrid.
- Therefore, it must have rained today.

This example demonstrates how logical reasoning can be used to draw conclusions from a set of given statements.

## Key Methods

Each logical sentence class implements:
- `evaluate(model)`: Determines truth value
- `formula()`: Generates a string representation
- `symbols()`: Collects all unique symbols
- `__eq__()` and `__hash__()`: For comparison and use in sets/dicts

## Requirements
- Python 3.7+
- No external dependencies

## Notes
- Supports complex nested logical expressions
- Provides comprehensive logical reasoning capabilities
- Primarily for educational and research purposes in propositional logic
