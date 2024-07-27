from abc import ABC, abstractmethod
from typing import Any, List, Optional

class BaseColumn(ABC):
    """
    An abstract base class for implementing various data structure algorithms.

    This class provides a template for creating different data structures
    with common operations such as insertion, deletion, and retrieval.

    Attributes:
        data (List[Any]): A list to store the elements of the data structure.
        default (Any): The default value to be used when no value is provided.
    """

    def __init__(self, default: Any = None):
        """
        Initialize the BaseDataStructure.

        Args:
            default (Any, optional): The default value to be used when no value is provided.
                Defaults to None.
        """
        self.data = []
        self.default = default

    @abstractmethod
    def insert(self, value: Any) -> int:
        """
        Insert a value into the data structure.

        Args:
            value (Any): The value to be inserted.

        Returns:
            int: The index or position where the value was inserted.
        """
        pass

    @abstractmethod
    def delete(self, index: int) -> Any:
        """
        Delete an element from the data structure at the specified index.

        Args:
            index (int): The index of the element to be deleted.

        Returns:
            Any: The deleted element.

        Raises:
            IndexError: If the index is out of range.
        """
        pass

    @abstractmethod
    def update(self, index: int, value: Any) -> None:
        """
        Update the value at the specified index in the data structure.

        Args:
            index (int): The index of the element to be updated.
            value (Any): The new value to be set.

        Raises:
            IndexError: If the index is out of range.
        """
        pass

    @abstractmethod
    def get(self, index: int) -> Any:
        """
        Retrieve the value at the specified index in the data structure.

        Args:
            index (int): The index of the element to be retrieved.

        Returns:
            Any: The value at the specified index.

        Raises:
            IndexError: If the index is out of range.
        """
        pass

    def __len__(self) -> int:
        """
        Get the number of elements in the data structure.

        Returns:
            int: The number of elements in the data structure.
        """
        return len(self.data)

    def __iter__(self):
        """
        Return an iterator for the data structure.

        Returns:
            iterator: An iterator over the elements in the data structure.
        """
        return iter(self.data)

    def __repr__(self) -> str:
        """
        Return a string representation of the data structure.

        Returns:
            str: A string representation of the data structure.
        """
        return f"{self.__class__.__name__}({self.data})"

    def __eq__(self, other: Any) -> bool:
        """
        Check if this data structure is equal to another object.

        Args:
            other (Any): The object to compare with.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        if isinstance(other, BaseDataStructure):
            return self.data == other.data
        return False

    def __contains__(self, item: Any) -> bool:
        """
        Check if an item is present in the data structure.

        Args:
            item (Any): The item to search for.

        Returns:
            bool: True if the item is present, False otherwise.
        """
        return item in self.data