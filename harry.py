from logic import *

rain = Symbol("It is raining today")
hagrid = Symbol("Harry visited hagrid today")
dumbledore = Symbol("Harry visited dumbledore today")

knowledge = And(
	Implication(Not(rain), hagrid),
	Or(hagrid, dumbledore),
	Not(And(hagrid, dumbledore)),
	dumbledore
)

print(model_check(knowledge, rain))
