"""Capa de persistencia archivos JSON."""

import json
import os
from typing import List


class JsonStorage:
    """Manejo de la persistencia."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    def load(self) -> List[dict]:
        """Carga de datos."""
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError) as error:
            print(f"Error al cargar la información {self.file_path}: {error}")
            return []

    def save(self, data: List[dict]) -> None:
        """Almacenamiento de datos."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except OSError as error:
            print(f"Error al guardar la información {self.file_path}: {error}")