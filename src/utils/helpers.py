class Helpers:
    """
    Utilities and methods which provide assistance to other classes.
    """

    def convert_string_to_nativekey(self, value: str) -> list:
        """
        Convert a string of digits (and backslash) to Android NativeKey module.

        This allows for interaction with the keypad/digit keyboard type.
        """
        value_to_nativekeycode = {
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

        codes = []

        try:
            for char in value:
                if char in value_to_nativekeycode:
                    codes.append(value_to_nativekeycode[char])
                else:
                    raise ValueError(
                        f"Failed to map string ({value}) to NativeKey, there may be invalid characters such as: ({char})."
                    )
        except ValueError as e:
            raise e

        return codes
