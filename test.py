from typing import Sequence

def process_numbers(numbers: Sequence[int]):
    """Process a sequence of numbers."""
    for num in numbers:
        print(f"Number: {num}")

# Creating a sequence of integers
numbers = [1, 2, 3, 4, 5]

# Processing the numbers
process_numbers(numbers)
