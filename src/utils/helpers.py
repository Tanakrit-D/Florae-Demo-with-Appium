from __future__ import annotations

VALUE_TO_NATIVEKEYCODE: dict[str, int] = {
    "0": 7,
    "1": 8,
    "2": 9,
    "3": 10,
    "4": 11,
    "5": 12,
    "6": 13,
    "7": 14,
    "8": 15,
    "9": 16,
    "/": 76,
}

class Helpers:
    """Utilities and methods which provide assistance to other classes."""

    @staticmethod
    def convert_string_to_nativekey(value: str) -> list[int]:
        """
        Convert a string of digits (and backslash) to Android NativeKey module.

        This allows for interaction with the keypad/digit keyboard type.

        Args:
            value (str): The string to convert.

        Returns:
            List[int]: A list of NativeKey codes.

        Raises:
            ValueError: If an invalid character is encountered in the input string.

        """
        try:
            return [VALUE_TO_NATIVEKEYCODE[char] for char in value]
        except KeyError as e:
            invalid_char = str(e.args[0])
            msg = f"Failed to map string ({value}) to NativeKey. Invalid character: {invalid_char}"
            raise ValueError(msg) from e
