# Circular List class adapted from https://stackoverflow.com/questions/4151320/efficient-circular-buffer


from typing import List


class CircularList:
    """A circular list class.

    A circular list is a list whose index is never out of range. Say `mylist`
    has four elements, `mylist[4]` refers to the first element in the list,
    i.e., it is the same element referred to by `molest[0]`.

    A circular list has a fixed size. Elements can be added to the end
    (`append`) or to the beginning (`prepend`) of the list. If the list has
    reached its maximum length, adding an element pushes out the element on the
    opposite end of the list.

    Attributes
    ==========
    size:
        The maximum length of the circular list.

    """

    _start: int
    _data: List
    size: int

    def __init__(self, size, data=[]):
        """Initialize a circular list.

        Create a circular list with the given size and optional data. If the
        data contains more elements than `size` allows, it is truncated.

        Parameters
        ----------
        size
            The maximum length of the circular list.
        data
            The initial data.

        Examples
        --------
        c = CircularList(4)
        c.append(1); print(c)
        ==> [1] (1/4 items)

        d = CircularList(4, [1, 2, 3, 4, 5]); print(d)
        ==> [2, 3, 4, 5] (4/4 items) # list is truncated

        """
        assert size != 0, "Cannot create circular list of size 0."
        self._start = 0
        self.size = size
        self._data = list(data)[-size:]

    def __getitem__(self, index):
        """Return the element at position `index`.

        The first element of the list is at index position 0. `index` can be any
        integer, if it falls outside the range of the list, it is reduced using
        the modulo operation. Negative indices are allowed and count backwards
        from the end of the list.

        Parameters
        ----------
        index
            The index of the element to be retrieved.

        """
        return self._data[(index + self._start) % len(self._data)]

    def __str__(self):
        """Return string representation"""
        return (
            f"{self._data[self._start :] + self._data[: self._start]!r}"
            + f" ({len(self._data)!r}"
            + f"/{self.size!r} items)"
        )

    def __repr__(self):
        return f"CircularList({self.size!r}, {self._data[self._start :] + self._data[: self._start]!r})"

    def __len__(self):
        return len(self._data)

    def append(self, value):
        """Append an element"""
        if len(self._data) == self.size:
            self._data[self._start] = value
        else:
            self._data.append(value)
        self._start = (self._start + 1) % self.size

    def prepend(self, value):
        if len(self._data) == self.size:
            self._data[self._start - 1] = value
            self._start = (self._start - 1) % self.size
        else:
            self._data.append(value)
            self._start = len(self._data) - 1
