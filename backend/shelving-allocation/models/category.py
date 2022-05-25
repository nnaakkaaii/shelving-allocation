import dataclasses


@dataclasses.dataclass(frozen=False)
class Category:
    id: int
    name: str


@dataclasses.dataclass(frozen=False)
class ParentCategory(Category):
    children: list['ChildCategory']

    @classmethod
    def new(cls,
            id_: int,
            name: str) -> 'ParentCategory':
        self = cls(id_, name, [])
        return self


@dataclasses.dataclass(frozen=False)
class ChildCategory(Category):
    parent: ParentCategory

    @classmethod
    def new(cls,
            id_: int,
            name: str,
            parent: ParentCategory) -> 'ChildCategory':
        self = cls(id_, name, parent)
        parent.children.append(self)
        return self
