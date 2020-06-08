
class HexPoint:
    def __init__(self, col: int, row: int):
        self.__row: int = row
        self.__col: int = col
    
    def toJsonSerializable(self) -> dict:
        return {'row': self.__row, 'col': self.__col}

    @property
    def row(self) -> int:
        return self.__row

    @property
    def col(self) -> int:
        return self.__col
