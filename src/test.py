def calculate_weights(importance1, importance2, importance3, importance4):
    total_importance = importance1 + importance2 + importance3 + importance4

    weight1 = importance1 / total_importance
    weight2 = importance2 / total_importance
    weight3 = importance3 / total_importance
    weight4 = importance4 / total_importance

    weight_sum = weight1 + weight2 + weight3 + weight4
    # if weight_sum != 1:
    #     weight1 /= weight_sum
    #     weight2 /= weight_sum
    #     weight3 /= weight_sum
    #     weight4 /= weight_sum

    return weight1, weight2, weight3, weight4

# Mock data
importance1 = 745
importance2 = 286
importance3 = 125
importance4 = 340

# Calculate weights
weight1, weight2, weight3, weight4 = calculate_weights(importance1, importance2, importance3, importance4)

# Print the results
print("Importance Values:")
print("Input 1:", importance1)
print("Input 2:", importance2)
print("Input 3:", importance3)
print("Input 4:", importance4)

print("\nWeight Values:")
print("Input 1 Weight:", weight1)
print("Input 2 Weight:", weight2)
print("Input 3 Weight:", weight3)
print("Input 4 Weight:", weight4)
