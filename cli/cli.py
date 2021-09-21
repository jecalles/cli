from typing import Optional, Callable, Iterable

def pipeline_fxn(func):
    def wrapper(*args, **kwargs):
        if args[0] is None or len(args) == 0:
            return None
        else:
            return func(*args, **kwargs)
    return wrapper

def prompt_user(
        prompt_str: str,
        validator: Optional[Callable[[str],  bool]] = None,
) -> Optional[str]:
    quit_strings = {"quit", "exit", "q"}
    breakline = "-" * 80

    if validator is None:
        validator = lambda x: True

    while True:
        print(breakline)
        user_input = input(prompt_str)
        if user_input in quit_strings:
            return None
        elif validator(user_input):
            return user_input
        else:
           print(f"Error! Invalid input {user_input}")

@pipeline_fxn
def prompt_decorator(prompt_str: str):
    """
    A decorator used to make user-prompt-event-loops. Accepts a prompt for
    the user. Passes 'user_input' as the first positional argument to the
    wrapped function.

    E.g.,
    @userinterface
    >>> import cli
    >>> @cli.prompt_fxn("give me some input: ")
    ... def foo(user_input, bar):
    ...     if user_input == bar:
    ...         return "That's a nice bar"
    ...     else:
    ...         raise ValueError("That's not as nice a bar")
    ...
    >>> foo("chocolate")
    --------------------------------------------------------------------------------
    give me some input: banana
    input error; raised the following:
    --------------------------------------------------------------------------------
    That's not as nice a bar
    give me some input: chocolate
    "That's a nice bar"
    >>> foo("never gonna give you up")
    --------------------------------------------------------------------------------
    give me some input: quit
    >>> None
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            while True:
                user_input = prompt_user(prompt_str)
                if user_input is None:
                    return None
                else:
                    try:
                        func(user_input, *args, **kwargs)
                    except Exception as e:
                        print(f"Error! Invalid input. Raises the following: "
                              f"{e}")
        return wrapper
    return decorator


def choice_validator_factory(choices: list) -> Callable[[str], bool]:
    """ A factory function that returns a validator function for use with
    cli.prompt_user(). Returned validator checks that user input (1) can be
    cast to an int, and (2) is within the index bounds for the choices given
    """
    def validator(x: str) -> bool:
        try:
            return_bool = int(x) < len(choices)
        except:
            return_bool = False

        return return_bool

    return validator

