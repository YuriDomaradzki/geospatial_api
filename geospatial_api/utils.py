
def string_is_alphanumeric(text: str) -> bool:
    """
        Verifies if the string is alphanumeric or not.

    Args
    ----
        text : str
            The string to be validated.

    Returns
    -------
        bool
            True if the string is alphanumeric, False otherwise.

    Example
    -------
        is_valid = string_is_alphanumeric("YuriDomaradzki") # Returns True
        is_valid = string_is_alphanumeric("Yuri_Domaradzki") # Returns False
    """
    if not all(char.isalnum() for char in text):
        return False
    return True


def string_validation(text: str) -> bool:
    """
        Validate a string to ensure it only contains letters and spaces.

    Args
    ----
        text : str
            The string to be validated.

    Returns
    -------
        bool
            True if the string is valid (contains only letters and spaces), False otherwise.

    Example
    -------
        is_valid = string_validation("yuri nunes") # Returns True
        is_valid = string_validation("yuri123")    # Returns False
    """
    if any(
        char.isdigit() or not char.isalnum() and char not in [" "]
        for char in text
    ):
        return False
    return True

