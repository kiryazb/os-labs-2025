from typing import List, Sequence

from data_structures import LinkedList


def selection_sort_list(values: Sequence[int]) -> List[int]:
    arr = list(values)
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def selection_sort_linked_list(ll: LinkedList) -> LinkedList:
    current = ll.head
    while current:
        min_node = current
        runner = current.next
        while runner:
            if runner.value < min_node.value:
                min_node = runner
            runner = runner.next
        if min_node is not current:
            current.value, min_node.value = min_node.value, current.value
        current = current.next
    return ll
