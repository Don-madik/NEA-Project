from NLP_processing import NLPProcessor

nlp = NLPProcessor()

# Test Case 1
sentence1 = "Find the force when mass is 10kg and acceleration is 2m/s^2"
eq1, vals1 = nlp.parse(sentence1)
print("Test 1:")
print("Equation:", eq1)
print("Values:", vals1)
print()

# Test Case 2
sentence2 = "Energy is calculated when mass is 2kg and speed is 3e8m/s"
eq2, vals2 = nlp.parse(sentence2)
print("Test 2:")
print("Equation:", eq2)
print("Values:", vals2)
print()

# Test Case 3 (unmatched template)
sentence3 = "Find current and resistance"
eq3, vals3 = nlp.parse(sentence3)
print("Test 3:")
print("Equation:", eq3)
print("Values:", vals3)
