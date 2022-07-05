import pulp
from .base import BaseAllocator

from ..models.item import ItemType
from ..models.shelve import Shelve, ShelveStep, ShelveSection

from ..selling_probability.basic_selling_probability import BasicSellingProbability

class LpAllocator(BaseAllocator): # __init__コンストラクタで購買成約確率を選択
    def __init__(self, shelves, item_types, selling_prob: BasicSellingProbability):
        self.shelves = shelves # Shelveのリスト
        self.shelve_steps = self.shelves.steps # ShelveStepのリスト
        self.shelve_sections = self.shelve_steps.sections # ShelveSectionのリスト
        self.item_types =  # ItemTypeのリスト
        self.selling_prob = selling_prob # 購買制約確率の式

    """前提
    1. self.shelves.storedには同じカテゴリーかつ体積の条件を満たした商品しか入れられていない
    2. 段、区画はそれぞれ、棚、段の体積条件を満たすとする（登録の際に満たしているはずである）
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
            for s in self.shelve_sections
            for i in self.item_types
        ]
        
        # 【変数】商品i区画sに置く(1)・置かない(0)
        self.x = pulp.LpVariable.dicts("x", self.SectionItem, cat="Binary")
        self.y = pulp.LpVariable.dicts("y", self.ShelveItem, cat="Binary") 

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
    # -> 各区画の高さ＝段の高さ かつ 段の高さの和＝棚の高さは満たされている前提であれば、ある区画における
    #    商品の高さの最大値がその区画の高さを超えなければいい。
    def height_constraint(self):
        # 各区画に対して入らない商品のリスト作成
        self.S_NgHeightItem = [{
            s.id: [i.id for i in self.item_types if i.Volume.height > s.Volume.height]
        } for s in self.shelve_sections]

        for s in self.shelve_sctions:
            self.prob += pulp.lpSum([self.x[s.id, i.id] for i in self.S_NgHeightItem[s]]) == 0

    # 4. すべての棚において各区画kに置かれている商品の幅の和は棚の幅を超えない
    def width_constraint(self):
        self.S_NgWidthItem = [{
            s.id: [i.id for i in self.item_types if i.Volume.width > s.Volume.width]
        } for s in self.shelve_sections]

        for s in self.shelve_sctions:
            self.prob += pulp.lpSum([self.x[s.id, i.id] for i in self.S_NgWidthItem[s]]) == 0


    # 5. すべての棚には。同一の大属性ParentCategoryを持つ商品のみが置かれる
    def shelve_category(self):
        for shelve in self.shelves:
            for i in self.item_types:
                if not i.category in shelve.category.children:
                    self.prob += self.y[shelve.id, i.id] == 0

    # 6. すべての小属性ChildCategoryは１箇所（１区画）にまとめられる
    def unify_child_category(self):
        for s in self.shelve_sections:
            for i in self.item_types:
                if s.category != i.category:
                    self.prob += self.x[s.id, i.id] == 0

    # 【目的関数】
    def objective_func(self):
        self.prob += pulp.lpSum(
            [
                # 商品の利益＊購買制約確率＊区画に入る商品数
                i.profit*BasicSellingProbability(i, s, self.x[s.id, i.id]*s.Volume.depth/i.Volume.depth, 0)*self.x[s.id, i.id]*s.Volume.depth/i.Volume.depth
                for i in self.item_types
                for s in self.shelve_sections
            ]
        )
    
    def __call__(self,
                 item_types: list[ItemType],
                 shelves: list[Shelve]) -> None:
        self.init_prob()
        # 制約式
        self.only_one_item()
        self.allocate_all_items()
        self.height_constraint()
        self.width_constraint()
        self.shelve_category()
        self.unify_child_category()
        # 目的関数
        self.objective_func()
        # 求解
        status = self.prob.solve()
        print("Status:", pulp.LpStatus[status])


