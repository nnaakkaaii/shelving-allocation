import dataclasses


@dataclasses.dataclass(frozen=True)
class Volume:
    width: float
    height: float
    depth: float
