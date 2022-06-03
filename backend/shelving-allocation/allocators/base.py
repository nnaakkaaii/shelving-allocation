import abc
import pulp

from ..models.item import ItemType
from ..models.shelve import Shelve, ShelveStep, ShelveSection

class BaseAllocator(metaclass=abc.ABCMeta):
    def __call__(self,
                 item_types: list[ItemType],
                 shelves: list[Shelve]) -> None:
        pass

@dataclasses.dataclass(frozen=False)
class Allocator():
    shelves: list[Shelve] # 棚のリスト
    shelve_steps: list[ShelveStep] # 段のリスト
    shelve_sections: list[ShelveSection] # 区画のリスト
    item_types: list[ItemType] # 商品のリスト

    """前提
    1. self.shelves.storedには同じカテゴリーかつ体積の条件を満たした商品しか入れられていない
    2. 段、区画はそれぞれ、棚、段の体積条件を満たすとする
    """

    def init_prob(self):
        # 【初期化】
        self.prob = pulp.Problem("ShelfAllocateProblem", pulp.LpMaxmize)

        # 【リスト】
        self.ShelveItem = [ # 棚と商品のペアのリスト
            (s.id, i.id)
            for s in self.shelves
            for i in self.item_types
        ]
        
        self.SectionItem = [ # 区画と商品のペアのリスト
            (s.id, i.id)
            for s in self.shelve_section
            for i in self.item_types
        ]
        
        # 【変数】商品i区画sに置く(1)・置かない(0)
        self.x = pulp.LpVariable.dicts("x", self.SectionItem, cat="Binary")
        

    # 【制約条件】
    # 1. 1つの区画における商品は1種類
    def only_one_item(self):
        for s in self.shelve_sections:
            self.prob += pulp.lpSum([self.x[s.id,i.id] for i in self.item_types]) == 1

    # 2. すべての商品を1つ以上の区画に配置する
    def allocate_all_items(self):
        for i in self.item_types:
            self.prob += pulp.lpSum([self.x[s.id,i.id] for s in self.shelve_sections]) >= 1

    # 3. すべての棚において各区画kに置かれている商品の高さの最大の和は棚の高さを超えない
    # 4. すべての棚において各区画kに置かれている商品の幅の和は棚の幅を超えない
    # 5. すべての棚には。同一の大属性ParentCategoryを持つ商品のみが置かれる
    # 6. すべての小属性ChildCategoryは一箇所にまとめられる
    # -> ShelveSelectionインスタンスの.soredに含まれる時点で満たされる？
    def allow_allocate(self):
        for i in self.item_types:
            for s in self.shelve_sections:
                if self.x[s.id, i.id] == 1:
                    self.pulp += i in s.stored
    



