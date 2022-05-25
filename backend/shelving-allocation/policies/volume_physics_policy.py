from .base import BasePolicy
from ..models.utils import Volume


class VolumePhysicsPolicy(BasePolicy):
    """体積の物理制約"""
    def is_satisfied_by(self,
                        capacity: Volume,
                        volumes: list[Volume]) -> bool:
        # 飛び出てる
        if capacity.height < max(volume.height for volume in volumes):
            return False
        # 奥に一個も入らない
        if capacity.depth < max(volume.depth for volume in volumes):
            return False
        # 横に入らない
        if capacity.width < sum(volume.width for volume in volumes):
            return False
        return True
