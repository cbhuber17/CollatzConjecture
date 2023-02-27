"""Contains functionality for computing the Collatz Conjecture."""

from timeit import default_timer as timer

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
    """

    try:
        n = int(n)
    except ValueError:
        print(f"ERROR: {n} is not an integer.")
        exit(-1)

    return n

# ----------------------------------------------------------------------------------------------

def single_collatz_conjecture(n) -> int:
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

def do_cc(n) -> tuple:
    """
    Computes the Collatz conjecture sequence for a given integer.

    Parameters:
    -----------
    n : int
        The starting integer for the Collatz sequence.

    Returns:
    --------
    tuple : (step_num, conjecture, processing_time)
        A tuple containing the following:
        - step_num : list
            A list of integers representing the number of steps taken to reach each element in the sequence.
        - conjecture : list
            A list of integers representing the elements in the Collatz sequence.
        - processing_time : float
            The amount of time taken (in seconds) to compute the sequence.

    """

    num_steps = 0
    step_num = []
    conjecture = []

    start = timer()

    while n != 1:
        n = single_collatz_conjecture(n)
        num_steps += 1

        step_num.append(num_steps)
        conjecture.append(n)

    end = timer()
    processing_time = end - start
    return step_num, conjecture, processing_time

# ----------------------------------------------------------------------------------------------

if __name__ == '__main__':

    n = get_number()
    n = check_number(n)
    
    print(f'Starting number: {n}\n')

    step_num, conjecture, processing_time = do_cc(n)

    print(f'Steps: {len(step_num)} in {processing_time*1e6:.3f} us.')