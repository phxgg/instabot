import math

# Configuration
total_comments = 4428 # Total comments on the post
your_comments = 310 # Your comments
winners = 3 # Number of winners

def calculate_probability(total_comments, your_comments, winners):
    other_comments = total_comments - your_comments

    # Total combinations of selecting the given number of winners from total comments
    total_combinations = math.comb(total_comments, winners)

    # Unfavorable combinations (none of your comments are selected)
    unfavorable_combinations = math.comb(other_comments, winners)

    # Favorable combinations (at least one of your comments is selected)
    favorable_combinations = total_combinations - unfavorable_combinations

    # Probability of winning
    probability_winning = favorable_combinations / total_combinations

    return probability_winning

# Calculate the probability
probability_winning = calculate_probability(total_comments, your_comments, winners)

# Print the results
print(f"Total comments: {total_comments}")
print(f"Your comments: {your_comments}")
print(f"Number of winners: {winners}")
print(f"Probability of you winning: {probability_winning * 100:.2f}%")
