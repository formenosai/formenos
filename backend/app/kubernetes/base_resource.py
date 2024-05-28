from abc import ABC, abstractmethod
from typing import Any, Dict

import yaml


class BaseResource(ABC):
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Abstract method that should be implemented by subclasses to convert the resource to a dictionary.

        Returns:
            dict: A dictionary representation of the resource.
        """
        pass

    def to_yaml(self) -> str:
        """
        Converts the resource to a YAML string.

        Returns:
            str: A YAML string representation of the resource.
        """
        return yaml.dump(self.to_dict(), sort_keys=False)
