class RconCommandArgumentError(ValueError):
    def __init__(
        self,
        command_name: str,
        arguments: dict[str, object],
        errors: list[str],
    ) -> None:
        self.command_name: str = command_name
        self.arguments: dict[str, object] = arguments
        self.errors: list[str] = errors
        super().__init__(f"Invalid arguments for '{command_name}': {'; '.join(errors)}")


__all__ = [
    'RconCommandArgumentError',
]
