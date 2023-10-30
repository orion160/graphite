from dataclasses import dataclass
from collections import deque
from typing import Callable


@dataclass
class WeightedEdge[T]:
    u: T
    v: T
    weight: int


type AdjacencyListGraph[T] = list[list[WeightedEdge[T]]]


class VertexIndexer[T]:
    def __init__(self) -> None:
        self.__key_solver: dict[T, int] = {}
        self.__sequence: int = 0

    def add(self, key: T) -> None:
        self.__key_solver[key] = self.__sequence
        self.__sequence += 1

    def __contains__(self, key: T) -> bool:
        return key in self.__key_solver

    def __getitem__(self, key: T) -> int:
        return self.__key_solver[key]


class WeightedDigraph[T]:
    def __init__(self) -> None:
        self.__graph: AdjacencyListGraph[T] = []
        self.__vertex_indexer: VertexIndexer = VertexIndexer()
        self.__vertex_count: int = 0
        self.__edge_count: int = 0

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

    def has_edge(self, u: T, v: T):
        i = self.__vertex_indexer[u]

        for edge in self.__graph[i]:
            if v == edge.v:
                return True

        return False

    def neighbors(self, v: T):
        i = self.__vertex_indexer[v]
        for edge in self.__graph[i]:
            yield edge.v

    def get_vertex_id(self, v: T) -> int:
        return self.__vertex_indexer[v]

    @property
    def vertex_count(self) -> int:
        return self.__vertex_count

    @property
    def edge_count(self) -> int:
        return self.__edge_count


def dfs[T](graph: WeightedDigraph, v: T, f: Callable[[T], None]) -> None:
    marked = [False] * graph.vertex_count

    stack = deque([v])

    while len(stack) > 0:
        v = stack.pop()
        current = graph.get_vertex_id(v)

        if not marked[current]:
            f(v)
            marked[current] = True
            for node in graph.neighbors(v):
                defered = graph.get_vertex_id(node)
                if not marked[defered]:
                    stack.append(node)


def main() -> None:
    graph = WeightedDigraph[str]()
    graph.add_vertex("a")
    graph.add_vertex("b")
    graph.add_edge("a", "b", 1)

    dfs(graph, "a", lambda v: print(v))


if __name__ == "__main__":
    main()
