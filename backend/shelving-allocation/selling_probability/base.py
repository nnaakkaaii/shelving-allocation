import abc

from ..models.item import ItemType
from ..models.shelve import ShelveSection


class SellingProbability(metaclass=abc.ABCMeta):
    """売買成立確率の導出式
    """
    @abc.abstractmethod
    def __call__(self,
                 item_type: ItemType,
                 shelve_section: ShelveSection) -> float:
        pass
