# Basic Python Script Example

def greet_user(name: str) -> str:
    """Returns a greeting message for the given name."""
    return f"Hello, {name}! Welcome to Python programming."

def calculate_stats(numbers: list[float]) -> dict:
    """Calculates basic statistics for a list of numbers."""
    if not numbers:
        return {"total": 0, "average": 0, "count": 0}
    
    total = sum(numbers)
    count = len(numbers)
    average = total / count
    return {
        "total": total,
        "average": average,
        "count": count
    }

def main():
    print("=" * 40)
    print("      Welcome to Python Basics!")
    print("=" * 40)
    
    # 1. Greeting
    user_name = input("Enter your name (or press Enter for default): ").strip()
    if not user_name:
        user_name = "Developer"
    
    print(greet_user(user_name))
    print()
    
    # 2. Number processing
    print("Let's calculate some basic statistics.")
    sample_numbers = [10, 25, 42, 7, 19, 88, 34]
    print(f"Sample List: {sample_numbers}")
    
    stats = calculate_stats(sample_numbers)
    print(f"Count  : {stats['count']}")
    print(f"Total  : {stats['total']}")
    print(f"Average: {stats['average']:.2f}")
    
    print("\nFiltered numbers (> 20):")
    high_numbers = [num for num in sample_numbers if num > 20]
    print(high_numbers)
    
    print("=" * 40)

if __name__ == "__main__":
    main()
