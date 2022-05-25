from .base import BasePolicy
from ..models.category import ChildCategory, ParentCategory


class ShelveCategoryPolicy(BasePolicy):
    """同じ棚には同じカテゴリ"""
    def is_satisfied_by(self,
                        shelve_section_category: ChildCategory,
                        shelve_category: ParentCategory) -> bool:
        return shelve_section_category.parent.id == shelve_category.id
