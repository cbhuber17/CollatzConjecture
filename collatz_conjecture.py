
# ----------------------------------------------------------------------------------------------

def get_number() -> str:
    """
    Asks the user to input an integer number and returns it as a string.

    This function prompts the user to enter an integer number through the console, 
    and then returns the user input as a string. If the input is not a valid integer, 
    it will be returned as a string regardless.

    Returns:
    - A string that represents the integer number entered by the user.
    """

    n = input('Enter an integer number: ')
    return n

# ----------------------------------------------------------------------------------------------

def check_number(n) -> int:
    """Converts the input parameter to an integer and returns it if it is a valid integer.

    Args:
        n (Any): A value that can be cast to an integer.

    Returns:
        int: The integer value of the input parameter.

    Raises:
        SystemExit: If the input parameter cannot be cast to an integer.

    Examples:
        >>> check_number(5.5)
        ERROR: 5.5 is not an integer.
        SystemExit: -1

        >>> check_number("10")
        10

        >>> check_number(True)
        1
    """

    try:
        n = int(n)
    except ValueError:
        print(f"ERROR: {n} is not an integer.")
        exit(-1)

    return n

# ----------------------------------------------------------------------------------------------

def single_collatz_conjecture(n):
    """Implements the Collatz Conjecture for one iteration of the given number.

    The Collatz Conjecture states that, for any positive integer n, if you repeatedly apply the following steps to it, you will eventually reach the number 1:
        1. If n is even, divide it by 2.
        2. If n is odd, multiply it by 3 and add 1.

    Args:
        n (int): The starting number for the Collatz Conjecture.

    Returns:
        None
    """

    if n % 2 == 0:
        n //= 2
    else:
        n = 3*n + 1

    return n


# ----------------------------------------------------------------------------------------------

if __name__ == '__main__':

    n = get_number()
    n = check_number(n)

    print(f'Starting number: {n}\n')

    num_steps = 1

    while n != 1:
        n = single_collatz_conjecture(n)
        print(n)
        num_steps += 1

    print(f'Steps: {num_steps}')