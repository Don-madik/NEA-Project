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

test_cases = [
    "Find the force when mass is 10kg and acceleration is 2m/s^2",      # F = m * a
    "Calculate energy when mass is 2kg and speed is 3e8m/s",            # E = m * v^2
    "What is the voltage when current is 2A and resistance is 5 ohm",   # V = I * R
    "Power when energy is 100J and time is 5s",                         # P = E / t
    "Find the mass",                                                   # Should fail
]

for i, sentence in enumerate(test_cases, 1):
    print(f"\nTest {i}: {sentence}")
    print(ai.solve_from_natural_language(sentence))