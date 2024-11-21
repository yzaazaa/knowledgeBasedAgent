from abc import ABC

class Sentence(ABC):
	def evaluate(self, model):
		"""Evaluates the logical sentence."""
		raise Exception("nothing to evaluate")

	def formula(self):
		"""Returns string formula representing logical sentence."""
		return ""

	def symbols(self):
		"""Returns a set of all symbols in the logical sentence."""
		return set()

	@classmethod
	def validate(cls, sentence):
		if not isinstance(sentence, Sentence):
			raise TypeError("must be a logical sentence")
	
	@classmethod
	def parenthesize(cls, s):
		"""Parenthesizes an expression if not already parenthesized."""
		def balanced(s):
			"""Checks if a string has balanced parentheses."""
			count = 0
			for c in s:
				if c == "(":
					count += 1
				elif c == ")":
					if count <= 0:
						return False
					count -= 1
			return count == 0
		if not len(s) or s.isalpha() or (
			s[0] == "(" and s[-1] == ')' and balanced(s[1:-1])
		):
			return s
		else:
			return f"({s})"

class Symbol(Sentence):

	def __init__(self, name):
		self.name = name
	
	def __eq__(self, other):
		return isinstance(other, Symbol) and other.name == self.name
	
	def __hash__(self):
		return hash(("symbol", self.name))
	
	def __repr__(self):
		return self.name
	
	def evaluate(self, model):
		try:
			return bool(model[self.name])
		except KeyError:
			raise EvaluationException(f"variable {self.name} not in model")
	
	def formula(self):
		return self.name
	
	def symbols(self):
		return {self.name}
	

class Not(Sentence):

	def __init__(self, operand):
		Sentence.validate(operand)
		self.operand = operand
	
	def __eq__(self, other):
		return isinstance(other, Not) and self.operand == other.operand

	def __hash__(self):
		return hash(("not", self.operand))
	
	def __repr__(self):
		return f"Not({self.operand})"
	
	def evaluate(self, model):
		return not self.operand.evaluate(model)
	
	def formula(self):
		return "¬" + Sentence.parenthesize(self.operand.formula())
	
	def symbols(self):
		return self.operand.symbols()

class And(Sentence):
	
	def __init__(self, *conjuncts):
		for conjunct in conjuncts:
			Sentence.validate(conjunct)
		self.conjuncts = list(conjuncts)

	def __eq__(self, other):
		return isinstance(other, And) and self.conjuncts == other.conjuncts

	def __hash__(self):
		return hash(("and", tuple(hash(conjunct) for conjunct in self.conjucts)))
	
	def __repr__(self):
		return f"And({', '.join([str(conjunct) for conjunct in self.conjuncts])})"
	
	def add(self, conjunct):
		Sentence.validate(conjunct)
		self.conjuncts.append(conjunct)
	
	def evaluate(self, model):
		return not any(not conjunct.evaluate(model) for conjunct in self.conjuncts)
	
	def formula(self):
		if len(self.conjuncts) == 1:
			return self.conjuncts[0].formula()
		return " ∧ ".join([Sentence.parenthesize(conjunct.formula()) for conjunct in self.conjuncts])
	
	def symbols(self):
		return set.union(*[conjunct.symbols() for conjunct in self.conjuncts])

class Or(Sentence):
	
	def __init__(self, *disjuncts):
		for disjunct in disjuncts:
			Sentence.validate(disjunct)
		self.disjuncts = list(disjuncts)

	def __eq__(self, other):
		return isinstance(other, Or) and self.disjuncts == other.disjuncts

	def __hash__(self):
		return hash(("or", tuple(hash(disjunct) for disjunct in self.disjucts)))
	
	def __repr__(self):
		return f"Or({', '.join([str(disjunct) for disjunct in self.disjuncts])})"
	
	def evaluate(self, model):
		return any(disjunct.evaluate(model) for disjunct in self.disjuncts)
	
	def formula(self):
		if len(self.disjuncts) == 1:
			return self.disjuncts[0].formula()
		return " v ".join([Sentence.parenthesize(disjunct.formula()) for disjunct in self.disjuncts])
	
	def symbols(self):
		return set.union(*[disjunct.symbols() for disjunct in self.disjuncts])

class Implication(Sentence):
	
	def __init__(self, antecedant, consequent):
		Sentence.validate(antecedant)
		Sentence.validate(consequent)
		self.antecedant = antecedant
		self.consequent = consequent

	def __eq__(self, other):
		return isinstance(other, Implication) and self.antecedant == other.antecedant and self.consequent == other.consequent

	def __hash__(self):
		return hash(("implies", hash(self.antecedant), hash(self.consequent)))
	
	def __repr__(self):
		return f"Implication({self.antecedant}, {self.consequent})"
	
	def evaluate(self, model):
		return not self.antecedant.evaluate(model) or self.consequent.evaluate(model)

	def formula(self):
		return f"{Sentence.parenthesize(self.antecedant.formula())} => {Sentence.parenthesize(self.consequent.formula())}"
	
	def symbols(self):
		return set.union(self.antecedant.symbols(), self.consequent.symbols())

class Biconditional(Sentence):
	
	def __init__(self, left, right):
		Sentence.validate(left)
		Sentence.validate(right)
		self.left = left
		self.right = right

	def __eq__(self, other):
		return isinstance(other, Biconditional) and ((self.left == other.left and self.right == other.right) or (self.left == other.right and self.right == other.left))

	def __hash__(self):
		return hash(("biconditional", hash(self.left), hash(self.right)))
	
	def __repr__(self):
		return f"Biconditional({self.left}, {self.right})"
	
	def evaluate(self, model):
		left_eval = self.left.evaluate(model) 
		right_eval = self.right.evaluate(model)
		return (left_eval and right_eval) or (not left_eval and not right_eval)

	def formula(self):
		return f"{Sentence.parenthesize(self.left.formula())} <=> {Sentence.parenthesize(self.right.formula())}"
	
	def symbols(self):
		return set.union(self.left.symbols(), self.right.symbols())

def model_check(knowledge, query):
	"""Checks if knowledge base entails query."""
	def check_all(knowledge, query, symbols, model):
		"""Checks if knowledge base entails query, given a particular model."""
		if not symbols:
			if knowledge.evaluate(model):
				return query.evaluate(model)
			return True
		else:
			remaining = symbols.copy()
			p = remaining.pop()

			model_true = model.copy()
			model_true[p] = True

			model_false = model.copy()
			model_false[p] = False

			return (check_all(knowledge, query, remaining, model_true) and check_all(knowledge, query, remaining, model_false))
	
	symbols = set.union(knowledge.symbols(), query.symbols())
	return check_all(knowledge, query, symbols, dict())