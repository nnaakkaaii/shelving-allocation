from .base import SellingProbability

from ..models.item import ItemType
from ..models.shelve import ShelveSection

class BasicSellingProbability(SellingProbability):
    # Ni=Tjk*Ri/(Xijkl*Tdj/Sdi+α)
    # 商品iの購買成立確率Ni：棚の区画の基礎価値Tjk を販売実績数Ri / 商品数Xijkl*Tdj/Sdi+α と掛け合わせたもの
    def __call__(self,
                 item_type: ItemType,
                 shelve_section: ShelveSection,
                 num_items: int,
                 a: float) -> float:
        return shelve_section.records*item_type.records/(num_items+a)
