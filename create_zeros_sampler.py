import cirq

sampler = cirq.ZerosSampler()

print("repr:")
print(repr(sampler))

print("\njson:")
print(cirq.to_json(sampler))
