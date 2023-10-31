from dataclasses import dataclass, astuple
from collections import deque
from typing import Iterator, Self


@dataclass(slots=True)
class WeightedEdge[T]:
    u: T
    v: T
    weight: int

    def __iter__(self) -> Iterator[tuple[T, T, int]]:
        return iter(astuple(self))


@dataclass(slots=True)
class NodeVisitor[T]:
    ancestor: T | None
    current: T

    def __iter__(self) -> Iterator[tuple[T | None, T]]:
        return iter(astuple(self))


type AdjacencyListGraph[T] = list[list[WeightedEdge[T]]]


class VertexIndexer[T]:
    def __init__(self) -> None:
        self.__key_solver: dict[T, int] = {}
        self.__sequence = 0

    def add(self, key: T) -> None:
        self.__key_solver[key] = self.__sequence
        self.__sequence += 1

    @property
    def vertices(self) -> list[T]:
        return list(self.__key_solver)

    def __contains__(self, key: T) -> bool:
        return key in self.__key_solver

    def __getitem__(self, key: T) -> int:
        return self.__key_solver[key]

    def __repr__(self) -> str:
        return f"key_solver: {self.__key_solver}, sequence: {self.__sequence}"


class WeightedDigraph[T]:
    def __init__(self) -> None:
        self.__graph: AdjacencyListGraph[T] = []
        self.__vertex_indexer = VertexIndexer[T]()
        self.__vertex_count = 0
        self.__edge_count = 0

    def add_vertex(self, key: T) -> None:
        if key not in self.__vertex_indexer:
            self.__vertex_indexer.add(key)
            self.__graph.append([])

            self.__vertex_count += 1

    def add_edge(self, u: T, v: T, w: int) -> None:
        safety_checks: list[Exception] = []

        if u not in self.__vertex_indexer:
            safety_checks.append(Exception(f"Vertex {u} doesn't exist"))
        if v not in self.__vertex_indexer:
            safety_checks.append(Exception(f"Vertex {v} doesn't exist"))

        if len(safety_checks) > 0:
            raise ExceptionGroup("A given vertex doesn't exist", safety_checks)

        if not self.has_edge(u, v):
            i = self.__vertex_indexer[u]
            self.__graph[i].append(WeightedEdge(u, v, w))

            self.__edge_count += 1

    def has_edge(self, u: T, v: T) -> bool:
        i = self.__vertex_indexer[u]

        for edge in self.__graph[i]:
            if v == edge.v:
                return True

        return False

    def neighbors(self, v: T) -> Iterator[T]:
        i = self.__vertex_indexer[v]
        for edge in self.__graph[i]:
            yield edge.v

    def get_vertex_id(self, v: T) -> int:
        return self.__vertex_indexer[v]

    @property
    def vertices(self) -> list[T]:
        return self.__vertex_indexer.vertices

    @property
    def edges(self) -> list[WeightedEdge]:
        E = []
        for node in self.__graph:
            for edge in node:
                E.append(edge)

        return E

    @property
    def vertex_count(self) -> int:
        return self.__vertex_count

    @property
    def edge_count(self) -> int:
        return self.__edge_count


class dfsIterator[T]:
    def __init__(self, graph: WeightedDigraph[T], v: T) -> None:
        self.__marked = [False] * graph.vertex_count
        self.__stack = deque([NodeVisitor[T](None, v)])
        self.__graph = graph

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> NodeVisitor[T]:
        if len(self.__stack) > 0:
            visitor = self.__stack.pop()

            current = visitor.current
            current_id = self.__graph.get_vertex_id(current)

            if not self.__marked[current_id]:
                self.__marked[current_id] = True

                for to_visit_node in self.__graph.neighbors(current):
                    node_id = self.__graph.get_vertex_id(to_visit_node)
                    if not self.__marked[node_id]:
                        self.__stack.append(NodeVisitor(current, to_visit_node))

                return visitor

        raise StopIteration


def main() -> None:
    graph = WeightedDigraph[str]()

    graph.add_vertex("a")
    graph.add_vertex("b")
    graph.add_vertex("c")
    graph.add_vertex("d")

    graph.add_edge("a", "b", 1)
    graph.add_edge("a", "c", 5)
    graph.add_edge("b", "d", 5)
    graph.add_edge("d", "a", 5)

    print(f"Graph vertices: {graph.vertices}")
    print(f"Graph edges {graph.edges}")

    for node_visitor in dfsIterator(graph, "a"):
        ancestor, current = node_visitor

        if ancestor is None:
            print(f"Starting from {current}")
        else:
            print(f"{ancestor} visited {current}")


if __name__ == "__main__":
    main()
