#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class Node:
    value: int
    next: "Node | None" = None


class LinkedList:
    def __init__(self) -> None:
        self.head: Node | None = None

    @classmethod
    def from_iterable(cls, values: Iterable[int]) -> "LinkedList":
        ll = cls()
        iterator = iter(values)
        try:
            first_value = next(iterator)
        except StopIteration:
            return ll
        ll.head = Node(first_value)
        current = ll.head
        for value in iterator:
            current.next = Node(value)
            current = current.next
        return ll

    def to_list(self) -> List[int]:
        out: List[int] = []
        current = self.head
        while current:
            out.append(current.value)
            current = current.next
        return out
