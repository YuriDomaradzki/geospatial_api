

def string_is_alphanumeric(text: str) -> bool:
    """
    Verifies if the string is alphanumeric or not.

    Parameters
    ----------
    text : str
        The string to be validated.

    Returns
    -------
    bool
        True if the string is valid, False otherwise.

    Example
    -------
    is_valid = string_is_alphanumeric("Yuri_Domaradzki") # Returns True
    """
    if not all(char.isalnum() for char in text):
        return False
    return True


def string_validation(text: str) -> bool:
    """
    Validate a string to ensure it only contains letters

    Parameters
    ----------
    text : str
        The string to be validated.

    Returns
    -------
    bool
        True if the string is valid, False otherwise.

    Example
    -------
    is_valid = string_validation("yuri nunes") # Returns False
    is_valid = string_validation("yuridomaradzki") # Returns True
    """
    if any(
        char.isdigit() or not char.isalnum() and char not in [" "]
        for char in text
    ):
        return False
    return True