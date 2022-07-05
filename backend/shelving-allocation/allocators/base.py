import abc
import pulp

from ..models.item import ItemType
from ..models.shelve import Shelve, ShelveStep, ShelveSection

class BaseAllocator(metaclass=abc.ABCMeta): # 棚に対して、アイテムを入れていく。最適化手法ごとに
    def __call__(self,
                 item_types: list[ItemType],
                 shelves: list[Shelve]) -> None:
        pass
    



