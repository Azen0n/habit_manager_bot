import os


def get_environment_variable(name: str) -> str:
    """Return environment variable by name, raise error if not found."""
    try:
        return os.environ[name]
    except KeyError:
        raise KeyError(f'Environment variable "{name}" not set.')
