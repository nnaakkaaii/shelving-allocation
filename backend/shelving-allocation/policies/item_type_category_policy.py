from .base import BasePolicy
from ..models.category import ChildCategory


class ItemTypeCategoryPolicy(BasePolicy):
    """同じ棚の区画には同じカテゴリの商品"""
    def is_satisfied_by(self,
                        item_type_category: ChildCategory,
                        shelve_section_category: ChildCategory) -> bool:
        return item_type_category.id == shelve_section_category.id
