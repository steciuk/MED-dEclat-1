class Hello():
    def __init__(self, name: str) -> None:
        self.name: str = name

    def greet(self) -> None:
        print(f'Hello {self.name}')

    def sum(self, *args: int) -> int:
        """
        Sums ints

        Returns:
            int: ints to sum
        """
        return sum(args)

    def raises(self) -> None:
        raise ValueError('This is error')
