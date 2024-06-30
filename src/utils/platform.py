import os
from datetime import datetime

class Platform:
    def __init__(self):
        self.output_dir = self._create_output_folder()

    def _create_output_folder(self) -> None:
        base_dir = "./output"
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder_path = os.path.join(base_dir, timestamp)

        os.makedirs(folder_path, exist_ok=True)
        return folder_path
