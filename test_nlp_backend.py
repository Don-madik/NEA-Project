from backend import PhysicsAI

ai = PhysicsAI()

# Test Case 1
sentence1 = "Find the force when mass is 10kg and acceleration is 2m/s^2"
print("Input:", sentence1)
print("Output:", ai.solve_from_natural_language(sentence1))

# Test Case 2
sentence2 = "Energy is calculated when mass is 2kg and speed is 3e8m/s"
print("\nInput:", sentence2)
print("Output:", ai.solve_from_natural_language(sentence2))

# Test Case 3
sentence3 = "Calculate voltage if current is 2A and resistance is 5ohm"
print("\nInput:", sentence3)
print("Output:", ai.solve_from_natural_language(sentence3))

# Test Case 4 (Unrecognized)
sentence4 = "Find the mass when object is flying"
print("\nInput:", sentence4)
print("Output:", ai.solve_from_natural_language(sentence4))
