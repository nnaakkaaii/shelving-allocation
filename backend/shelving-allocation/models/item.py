import dataclasses

from .utils import Volume
from .category import ChildCategory


@dataclasses.dataclass(frozen=True)
class ItemType:
    """商品種類"""
    id: int # 変更
    cost_price: int  # 原価
    selling_price: int  # 売値
    records: int  # 一定期間内の過去販売個数
    volume: Volume
    category: ChildCategory

    @property
    def profit(self) -> int:
        return self.selling_price - self.cost_price
