import re


class String:

    @staticmethod
    def toKebabCase(value: str) -> str:
        value = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1-\2', value)
        value = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', value)
        value = re.sub(r'[\s_]+', '-', value)
        return value.lower()
