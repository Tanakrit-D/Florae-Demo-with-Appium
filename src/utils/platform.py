# pylint: disable=C0114

import datetime
import shutil
from pathlib import Path


class Platform:
    """
    A class representing a platform with output management capabilities.

    This class handles the creation and removal of output folders,
    with optional debug functionality.
    """

    def __init__(self, debug: bool) -> None:  # noqa: FBT001
        """
        Initialize the Platform instance.

        Args:
            debug (bool): If True, enables debug mode. Defaults to False.

        """
        self.debug = debug
        self.output_dir = self._create_output_folder()

    def _create_output_folder(self) -> str:
        """
        Create a timestamped output folder.

        Returns:
            str: The path of the created output folder.

        """
        base_dir = "./output"
        timestamp = datetime.datetime.now(tz=datetime.UTC).strftime("%Y-%m-%d_%H-%M-%S")
        folder_path = Path(base_dir) / timestamp
        Path(folder_path).mkdir(parents=True)

        return folder_path

    def remove_output_folder(self) -> None:
        """
        Remove the output folder if not in debug mode.

        This method only removes the folder if self.debug from config.cfg is False.
        """
        if not self.debug:
            shutil.rmtree(self.output_dir)
