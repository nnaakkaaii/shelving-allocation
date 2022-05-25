import dataclasses

from .item import ItemType
from .utils import Volume
from .category import ParentCategory, ChildCategory
from ..policies.shelve_category_policy import ShelveCategoryPolicy
from ..policies.item_type_category_policy import ItemTypeCategoryPolicy
from ..policies.volume_physics_policy import VolumePhysicsPolicy


@dataclasses.dataclass(frozen=False)
class ShelveSection:
    """棚の一段の中のある区画"""
    volume: Volume
    step: 'ShelveStep'
    category: ChildCategory
    records: int  # 販売実績
    stored: list[ItemType] = dataclasses.field(default_factory=list, init=False)
    can_allocate_flag: bool = dataclasses.field(default=False, init=False)

    @classmethod
    def new(cls,
            volume: Volume,
            shelve_step: 'ShelveStep',
            category: ChildCategory,
            records: int) -> 'ShelveSection':
        assert ShelveCategoryPolicy().is_satisfied_by(
            category,
            shelve_step.shelve.category), f'{category.name}は棚の子カテゴリではありません'
        self = cls(volume, shelve_step, category, records)
        shelve_step.sections.append(self)
        return self

    def can_allocate(self, item_type: ItemType) -> bool:
        self.can_allocate_flag = VolumePhysicsPolicy().is_satisfied_by(
            self.volume,
            [stored.volume for stored in self.stored] + [item_type.volume]
        ) and ItemTypeCategoryPolicy().is_satisfied_by(
            item_type.category,
            self.category,
        )
        return self.can_allocate_flag

    def allocate(self, item_type: ItemType) -> None:
        assert self.can_allocate_flag
        self.stored.append(item_type)
        self.can_allocate_flag = False


@dataclasses.dataclass(frozen=False)
class ShelveStep:
    """棚の一段"""
    sections: list[ShelveSection]
    shelve: 'Shelve'

    @classmethod
    def new(cls,
            shelve: 'Shelve') -> 'ShelveStep':
        self = cls([], shelve)
        shelve.steps.append(self)
        return self


@dataclasses.dataclass(frozen=False)
class Shelve:
    steps: list[ShelveStep]
    category: ParentCategory
