# Comparing different meta-heuristic algorithms in solving the graph bi-partitioning problem
* This project was created as part of the course Evolutionary Computing at Utrecht University for the master's in Artificial Intelligence
* It's purpose is to experimentally compare different meta-heuristic algorithms on their performance for solving a combinatorial optimization problem: **the graph bi-partitioning problem**
* For a comprehensive description of the project and the results, the reader can refer to the provided report
## The graph bi-partitioning problem
* Given a graph G of vertices and undirected edges connecting two vertices, the goal is to divide the set of vertices in two equally sized subset such that the number of edges that connect two vertices belonging to the two different subsets is minimized.
The planar graph used for comparing the algorithms consists of 500 vertices and is specified in the file Graph500.txt.
## The Fiduccia-Mattheyeses algorithm
* The FM algorithm is a particularly useful local search algorithm because of its ability to apply insertion and deletion in constant time when examining different partitions of the graph.
* All meta-heuristic algorithms that are compared in this project make use of the FM heuristic and aim to improve its performance
## Algorithms that are compared:
### 1. Multi-start Local Search (MLS)
* Simply restarts local search from a set of randomly generated initial solutions. The best local optimum is returned as final solution.
### 2. Iterated Local Search (ILS)
* Mutates the current solution found by local search and applies local search again from the mutated solution. When the new local optimum is better than the current one, ILS continues its search from this new local optimum, else it simply returns to the previous local optimum. The size of the mutation in this project was determined experimentally.
### 3. Genetic Local Search (GLS)
* Applies selection and recombination to a population of local optimal solutions obtained by a local search algorithm, in this case the FM heuristic. After applying recombination, the offspring is optimized with the FM heuristic to become a new local optimum. Thus, the solutions in the population of GLS are all local optimal solutions. Selection focuses the search towards good regions in the search space, while recombining local optima generates good starting points for the local search algorithm (the FM) in order to find new local optima.
### 4. Depth-First Multi-start Local Search (DF-MLS)
* Is similar to MLS in that it explores a larger variety of solutions. However, it aborts solutions if no reasonable improvement is found within a given time-frame.