import abc


class BasePolicy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def is_satisfied_by(self, *args, **kwargs) -> bool:
        pass
