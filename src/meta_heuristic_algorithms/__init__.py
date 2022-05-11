"""initializes the meta-heuristic algorithms module

The meta-heuristics examined, presented in increased complexity, are:
1. Multi-start Local Search (MLS)
2. Iterated Local Search (ILS)
3. Genetic Local Search (GLS)

The strategy applied by each meta-heuristic algorithm is problem independent,
also referred to as search bias, so they can be applied all combinatorial
optimization problems.

To be successful, the problem independent strategy needs to coincide with
the structure of the problem instance, otherwise it is like random search.

The goal of these meta-heuristic algorithms is to enhance the performance of
the Fiduccia-Mattheyeses local search heuristic for the graph bi-partitioning
problem: how to split a graph into two equal partitions, such that the number
of edges between the subsets is minimized"""
