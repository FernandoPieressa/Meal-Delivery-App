import uuid

def is_valid_uuid(val):
    """Given a variable, it returns True if its a valid uuid

    Args:
        val (any): variable to check if valid uuid

    Returns:
        boolean: True if valid uuid, false otherwise
    """
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False
