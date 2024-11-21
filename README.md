# Logical Reasoning Library

## Overview

This is a Python library for logical reasoning and propositional logic, providing a comprehensive set of classes to represent, manipulate, and evaluate logical sentences.

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
# Create logical sentences
p = Symbol('P')
q = Symbol('Q')

# Construct complex sentences
sentence = Implication(And(p, q), p)

# Create a model (interpretation)
model = {
    'P': True,
    'Q': False
}

# Evaluate the sentence
result = sentence.evaluate(model)

# Check logical entailment
knowledge_base = And(p, q)
query = p
is_entailed = model_check(knowledge_base, query)
```

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
