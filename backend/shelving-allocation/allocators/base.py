import abc

from ..models.item import ItemType
from ..models.shelve import Shelve


class BaseAllocator(metaclass=abc.ABCMeta):
    def __call__(self,
                 item_types: list[ItemType],
                 shelves: list[Shelve]) -> None:
        pass
