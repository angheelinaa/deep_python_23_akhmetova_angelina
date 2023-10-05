class CustomList(list):
    @staticmethod
    def extend_list_with_zeros(lst_1, lst_2):
        lst_res = CustomList(lst_1)
        if len(lst_1) < len(lst_2):
            lst_res.extend([0 for _ in range(len(lst_2) - len(lst_1))])
        return lst_res

    def __add__(self, other):
        result = self.extend_list_with_zeros(self, other)
        for i, elem in enumerate(other):
            result[i] += elem
        return result

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        result = self.extend_list_with_zeros(self, other)
        for i, elem in enumerate(other):
            result[i] -= elem
        return result

    def __rsub__(self, other):
        result = self.extend_list_with_zeros(other, self)
        for i, elem in enumerate(self):
            result[i] -= elem
        return result

    def __eq__(self, other):
        return sum(self) == sum(other)

    def __ne__(self, other):
        return sum(self) != sum(other)

    def __lt__(self, other):
        return sum(self) < sum(other)

    def __le__(self, other):
        return sum(self) <= sum(other)

    def __gt__(self, other):
        return sum(self) > sum(other)

    def __ge__(self, other):
        return sum(self) >= sum(other)

    def __str__(self):
        return f"elements = {super().__str__()}, sum = {sum(self)}"
