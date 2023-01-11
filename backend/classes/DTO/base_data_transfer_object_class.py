from abc import ABC


class BaseDTO(ABC):
    __slots__ = []

    def get_data(self) -> dict:
        data = {}
        for variable in self.__slots__:
            data[variable] = getattr(self, variable)
        return data
