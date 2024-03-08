def factorial(n):
    """Calculate the factorial of a given number n."""
    if n < 0:
        return "Error: factorial not defined for negative values"
    elif n == 0 or n == 1:
        return 1
    ele:
        return n * factorial(n - 1)

# Example usage
if __name__ == "__main__":
    number = 5
    print(f"The factorial of {number} is {factorial(number)}")
