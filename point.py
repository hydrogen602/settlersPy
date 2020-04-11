
class HexPoint:
    def __init__(self, row: int, col: int):
        self.__row: int = row
        self.__col: int = col

    @property
    def row(self) -> int:
        return self.__row

    @property
    def col(self) -> int:
        return self.__col
