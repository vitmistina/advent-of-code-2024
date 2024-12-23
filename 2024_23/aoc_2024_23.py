from typing import Dict, FrozenSet, List, Set


class Node:
    def __init__(self, id: str):
        self.id: str = id
        self.connections: Set[str] = set()

    def __repr__(self):
        return f"N({self.id}, conns: {self.connections})"

    def add_connection(self, connection: str):
        self.connections.add(connection)

    def has_other_connections(self, other: Set[str]) -> bool:
        return self.connections.issuperset(other)


def main(input_file_path: str, has_part_2: bool) -> Dict[str, int | str | None]:
    data = read_input_file(input_file_path)
    computers = build_computer_network(data)
    unique_triplets = find_unique_triplets(computers)
    filtered_triplets = filter_triplets(unique_triplets)

    result = {
        "part_1": len(filtered_triplets),
        "part_2": None,
    }

    if has_part_2:
        result["part_2"] = find_maximal_intersect(computers, unique_triplets)

    return result


def read_input_file(input_file_path: str) -> List[str]:
    with open(input_file_path) as f:
        return [line.strip() for line in f.readlines()]


def filter_triplets(unique_triplets: Set[FrozenSet[str]]) -> Set[FrozenSet[str]]:
    return {
        triplet for triplet in unique_triplets if any(id[0] == "t" for id in triplet)
    }


def find_maximal_intersect(
    computers: Dict[str, Node], unique_triplets: Set[FrozenSet[str]]
) -> str:
    maximal_intersect_size = 0
    max_intersect_elems = None
    max_iterations = 2000
    unique_n_tets_list: List[FrozenSet[str]] = list(unique_triplets)

    while unique_n_tets_list and max_iterations > 0:
        max_iterations -= 1
        n_tet = unique_n_tets_list.pop()
        connections = [computers[id].connections for id in n_tet]
        intersection = set.intersection(*connections)

        for id in intersection:
            new_n_tet = frozenset(n_tet | {id})
            unique_n_tets_list = [
                tet for tet in unique_n_tets_list if not tet.issubset(new_n_tet)
            ]

            if len(new_n_tet) > maximal_intersect_size:
                maximal_intersect_size = len(new_n_tet)
                max_intersect_elems = new_n_tet

            unique_n_tets_list.append(new_n_tet)

    if max_intersect_elems is None:
        raise Exception("No maximal intersection found")

    return ",".join(sorted(max_intersect_elems))


def find_unique_triplets(computers: Dict[str, Node]) -> Set[FrozenSet[str]]:
    unique_triplets: Set[FrozenSet[str]] = set()
    for computer in computers.values():
        conn_list = list(computer.connections)
        for i in range(len(conn_list)):
            for j in range(i + 1, len(conn_list)):
                if computers[conn_list[i]].has_other_connections(
                    {computer.id, conn_list[j]}
                ) and computers[conn_list[j]].has_other_connections(
                    {computer.id, conn_list[i]}
                ):
                    triplet = frozenset({computer.id, conn_list[i], conn_list[j]})
                    unique_triplets.add(triplet)
    return unique_triplets


def build_computer_network(data: List[str]) -> Dict[str, Node]:
    computers: Dict[str, Node] = {}
    for line in data:
        c1, c2 = line.split("-")
        if c1 not in computers:
            computers[c1] = Node(c1)
        computers[c1].add_connection(c2)
        if c2 not in computers:
            computers[c2] = Node(c2)
        computers[c2].add_connection(c1)
    return computers


if __name__ == "__main__":
    result = main("./2024_23/2024_23_input.txt", True)
    print(result)
