
class NoEnvFoundError(Exception):
    """Exception to raise when environment not found
    """
    pass


class NoProcessFoundError(Exception):
    """Exception to raise when no current running process of ComfyUI found
    """
    pass


class AlreadyRunningError(Exception):
    """Exception to raise when ComfyUI is already running
    """
    pass
