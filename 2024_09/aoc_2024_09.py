from enum import Enum
from typing import Optional


class BlockType(Enum):
    FREE = 1
    DATA = 2


class PartType(Enum):
    PART_1 = 1
    PART_2 = 2


class Block:
    def __init__(self, block_type: BlockType, id: int, length: int):
        self.block_type = block_type
        self.id = id
        self.length = length

    def __repr__(self) -> str:
        return (
            str(self.id) * self.length
            if self.block_type == BlockType.DATA
            else "." * self.length
        )


class Node:
    """Node class for doubly linked list."""

    def __init__(self, block: Block):
        self.block: Block = block
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None


class DoublyLinkedList:
    """Doubly linked list implementation."""

    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None

    def push_front(self, block: Block) -> None:
        """Insert a new block at the front of the list."""
        new_node = Node(block)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def push_back(self, block: Block) -> None:
        """Insert a new block at the back of the list."""
        new_node = Node(block)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def insert_after_node(self, target_node: Node, block: Block) -> None:
        """Insert a new block after the given node."""
        if target_node is None:
            raise ValueError("Target node cannot be None")
        new_node = Node(block)
        new_node.prev = target_node
        new_node.next = target_node.next
        if target_node.next is not None:
            target_node.next.prev = new_node
        else:
            self.tail = new_node
        target_node.next = new_node

    def remove_at_node(self, target_node: Node) -> None:
        """Remove the block at the given node."""
        if target_node is None:
            raise ValueError("Target node cannot be None")
        if target_node.prev is not None:
            target_node.prev.next = target_node.next
        else:
            self.head = target_node.next
        if target_node.next is not None:
            target_node.next.prev = target_node.prev
        else:
            self.tail = target_node.prev

    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next

    def __reversed__(self):
        current = self.tail
        while current:
            yield current
            current = current.prev

    def __str__(self) -> str:
        return " -> ".join(str(node.block) for node in self) + " -> None"

    def __repr__(self) -> str:
        return self.__str__()


def aggregate_block_values(blocks: DoublyLinkedList) -> int:
    pos = 0
    part_1 = 0
    for node in blocks:
        for _ in range(node.block.length):
            if node.block.block_type == BlockType.DATA:
                part_1 += node.block.id * pos
            pos += 1
    return part_1


def process_blocks(data: str, part: PartType) -> DoublyLinkedList:
    blocks = DoublyLinkedList()
    first_empty_node: Optional[Node] = None
    last_data_node: Optional[Node] = None
    for i, char in enumerate(data):
        num = int(char)
        if i % 2 == 0:
            blocks.push_back(Block(BlockType.DATA, i // 2, num))
            last_data_node = blocks.tail
        else:
            blocks.push_back(Block(BlockType.FREE, None, num))
            if first_empty_node is None:
                first_empty_node = blocks.tail
    if part == PartType.PART_1:
        part_1(blocks, first_empty_node, last_data_node)
    else:
        part_2(blocks)
    return blocks


def part_2(blocks: DoublyLinkedList) -> None:
    for last_node in reversed(blocks):
        if last_node.block.block_type == BlockType.DATA:
            for search_pointer in blocks:
                if search_pointer == last_node:
                    break
                if (
                    search_pointer.block.block_type == BlockType.FREE
                    and search_pointer.block.length >= last_node.block.length
                ):
                    search_pointer.block.length -= last_node.block.length
                    blocks.insert_after_node(
                        search_pointer.prev,
                        Block(
                            BlockType.DATA,
                            last_node.block.id,
                            last_node.block.length,
                        ),
                    )
                    last_node.block.id = None
                    last_node.block.block_type = BlockType.FREE
                    if search_pointer.block.length == 0:
                        blocks.remove_at_node(search_pointer)
                    break


def part_1(
    blocks: DoublyLinkedList,
    first_empty_node: Optional[Node],
    last_data_node: Optional[Node],
) -> None:
    while first_empty_node and last_data_node:
        if (
            first_empty_node.next is None
            or first_empty_node.next.block.block_type != BlockType.DATA
        ):
            break
        if first_empty_node.block.length > last_data_node.block.length:
            first_empty_node.block.length -= last_data_node.block.length
            blocks.insert_after_node(
                first_empty_node.prev,
                Block(
                    BlockType.DATA,
                    last_data_node.block.id,
                    last_data_node.block.length,
                ),
            )
            last_data_node.block.length = 0
            blocks.remove_at_node(last_data_node)
            last_data_node = last_data_node.prev.prev
        elif first_empty_node.block.length == last_data_node.block.length:
            blocks.insert_after_node(
                first_empty_node.prev,
                Block(
                    BlockType.DATA,
                    last_data_node.block.id,
                    last_data_node.block.length,
                ),
            )
            first_empty_node.block.length = 0
            last_data_node.block.length = 0
            blocks.remove_at_node(first_empty_node)
            blocks.remove_at_node(last_data_node)
            first_empty_node = first_empty_node.next.next
            last_data_node = last_data_node.prev.prev
        else:
            last_data_node.block.length -= first_empty_node.block.length
            blocks.insert_after_node(
                first_empty_node.prev,
                Block(
                    BlockType.DATA,
                    last_data_node.block.id,
                    first_empty_node.block.length,
                ),
            )
            first_empty_node.block.length = 0
            blocks.remove_at_node(first_empty_node)
            first_empty_node = first_empty_node.next.next


def main(input_file_path: str) -> dict:
    with open(input_file_path) as f:
        data = f.read().strip()
        blocks = process_blocks(data, part=PartType.PART_1)
        part_1_result = aggregate_block_values(blocks)
        blocks = process_blocks(data, part=PartType.PART_2)
        part_2_result = aggregate_block_values(blocks)
        return {"part_1": part_1_result, "part_2": part_2_result}


if __name__ == "__main__":
    result = main("./2024_09/2024_09_input.txt")
    print(result)