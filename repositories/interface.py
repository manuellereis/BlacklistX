
from abc import ABC, abstractmethod
import typing as t

class Repository(ABC):
    @abstractmethod
    def get(self, *args, **kargs) -> t.Any:
        raise NotImplementedError