import typing as tp
from dataclasses import dataclass

import flatbuffers  # noqa

from fbs_scheme import FBEdge, FBGraph, FBVertex  # noqa # type: ignore


@dataclass
class Edge:
    from_id: int
    to_id: int
    cost: float
    accessible: bool

    def __repr__(self) -> str:
        return f'({self.from_id}->{self.to_id}, c={self.cost}, a={self.accessible})'


class Graph:

    def __init__(self) -> None:
        self._vertex_names: tp.Dict[int, str] = {}
        self._edges: tp.Dict[int, tp.List[Edge]] = {}

    def size(self) -> int:
        return len(self._vertex_names)

    def outgoing_edges(self, vertex: int) -> tp.List[Edge]:
        return self._edges[vertex]

    def vertex_name(self, vertex: int) -> str:
        return self._vertex_names[vertex]

    def set_graph(
        self,
        vertex_names: tp.Dict[int, str],
        edges: tp.Dict[int, tp.List[Edge]]
        ) -> None:
        """Set graph directly from V/E"""

        self._vertex_names = dict(sorted(vertex_names.items()))
        self._edges = dict(sorted(edges.items()))

    def dumps(self) -> str:
        """String representation"""
        graph_description = {'V': self._vertex_names, 'E': self._edges}
        return str(graph_description).replace('\'', '"')

    def loadb(self, buf: bytes) -> None:
        """Set graph from binary representation"""
        raise NotImplementedError

    def dumpb(self) -> bytes:
        """Binary representation"""
        raise NotImplementedError
