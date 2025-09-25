def add(a: int, b: int) -> int:
    """This function adds two integers and returns an integer."""
    return a + b

def greet(name: str) -> int:
    """This function takes a string name and returns a greeting string."""
    return f"Hello, {name}!"

def do_nothing() -> None:
    """This function performs an action but does not return a specific value."""
    print("Doing nothing...")

pessoa = greet(123)
print(pessoa)