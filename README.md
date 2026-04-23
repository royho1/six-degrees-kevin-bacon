# Six Degrees of Kevin Bacon

Graph-based shortest path analysis that computes the minimum number of connections (degrees of separation) between any actor and Kevin Bacon using BFS traversal.

**Course:** ECS 032B - Introduction to Data Structures, UC Davis  
**Author:** Roy Ho  
**Date:** December 2023

---

## Overview

The "Six Degrees of Kevin Bacon" is a classic graph theory problem: given a network where actors are nodes and shared movie appearances are edges, find the shortest path from any actor to Kevin Bacon.

This project models the actor-movie network as a graph, parses a CSV dataset of movies and their casts, and implements a breadth-first search (BFS) traversal to find the minimum-length "Bacon path" between any given actor and Kevin Bacon.

## How It Works

The program reads a CSV file where each row contains a movie title followed by all actors who appeared in that movie. It builds an undirected graph where actors are connected by edges labeled with their shared movies. Two actors can share multiple edges if they appeared in multiple movies together.

Given a query actor, BFS finds the shortest path to Kevin Bacon and returns it in the format:

```
[Actor, Movie, Actor, Movie, ..., Kevin Bacon]
```

For example:

```python
>>> baconator.find_min_baconpath("Zoe Saldana")
['Zoe Saldana', 'Guardians of the Galaxy', 'Brendan Fehr', 'X-Men: First Class', 'Kevin Bacon']
```

## Project Structure

```
six-degrees-kevin-bacon/
├── README.md
├── baconator.py       # Main application: CSV parsing, BFS pathfinding, path validation
└── graph.py           # Graph data structure: nodes, edges, BFS/DFS/Dijkstra traversals
```

## Key Features

- **Multi-edge support:** Two actors can share multiple movie connections. The graph stores sets of movies per edge rather than a single weight.
- **BFS shortest path:** Guarantees the minimum degree of separation between any actor and Kevin Bacon.
- **Path validation:** `is_baconpath()` verifies that a path is valid (correct actor-movie-actor chain), and `is_min_baconpath()` checks that it is also the shortest possible path.
- **Bidirectional edges:** The graph maintains both forward and backward edge references for traversal flexibility.

## Usage

Place `moviedata.csv` (a CSV where column 0 is the movie title and columns 1+ are actors) in the same directory, then run:

```bash
python3 baconator.py moviedata.csv
```

Or without arguments to default to `moviedata.csv`:

```bash
python3 baconator.py
```

## Example Output

```
['Meg Ryan', 'In the Cut', 'Kevin Bacon']
['Tom Hanks', 'Apollo 13', 'Kevin Bacon']
['Snoop Dogg', 'Turbo', 'Samuel L. Jackson', 'Lakeview Terrace', 'Kevin Bacon']
['Steve Carell', 'Crazy, Stupid, Love.', 'Kevin Bacon']
['Kevin Bacon']
```

## Data Structures and Algorithms

- **Graph** (adjacency list with dictionary-based edges)
- **Breadth-First Search** (BFS) for shortest path
- **Depth-First Search** (DFS), iterative and recursive implementations
- **Dijkstra's algorithm** for weighted shortest paths

## Built With

Python 3, csv, collections.deque, json
