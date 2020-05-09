# Project Specification: Falca's Cave 
## Implemeting a least-cost search algorithm

Falca has ventured into a cave to collect the treasure that lies therein. This cave can be represented as a two-dimensional grid, completely enclosed by stone walls. Falca arrives at the entrance to the cave, and must locate all of the treasure it contains (a known quantity) before departing from the cave exit (a separate location to the entrance).

The cave is occupied by a dragon, who will not allow Falca to pass unless armed with a sword. Falca hasn't come prepared with a sword, but there is usually one to be found somewhere in the cave.

The overall problem to solve is to identify the shortest path through an arbitrary cave that will enable Falca to collect all of the treasure and escape from the exit. This is broken into several tasks:

1. Creating a representation of the cave
2. Checking whether a given path is a valid solution
3. Identifying the shortest path between two points
4. Identifying the optimal path that solves the whole problem

A valid cave satisfies the following requirements:

- There will only ever be (at most) a single feature (entrance, exit, wall, sword, dragon or treasure) in any given location in the cave.
- There will always be a single entrance and a single exit in the cave.
- There may be (at most) a single sword in the cave.
- There may be (at most) a single dragon in the cave.
- There may be (at most) three treasures in a cave.
- There may be multiple walls in a cave.
- A dragon, if one is present, will never be located in one of the locations (up to eight) adjacent to the entrance.
- A valid cave may contain no sword, dragon, treasures and/or walls.

A cave is specified via a dictionary with the following structure:

```python
data = {
'size': 4,  # the size of the cave
  'entrance': (0, 0),  # the location of the entrance (a row-column tuple)
  'exit': (2, 1),  # the location of the exit
  'dragon': (0, 2),  # the location of the dragon
  'sword': (3, 3),  # the location of the sword
  'treasure': [(1, 3)],  # a list of treasure locations
  'walls': [(1, 1), (1, 2), (2, 2), (2, 3)]  # a list of wall locations
}
```
  
The different types of location in the cave are identified with different symbols.

'empty 'is denoted by `'.'`;
'wall' is denoted by `‘#’`;
'entrance 'is denoted by `'@'`;
'exit 'is denoted by `‘X’`;
'treasure' is denoted by `'$'`;
'sword' is denoted by `’t’`; and
'dragon' is denoted by `'W'`.
The cave corresponding to the specification above is shown below.

![](https://groklearning-cdn.com/modules/9KPERmvwjpKmEwxcdD7cZf/Figure_1.png)

#### `check_path` parameters

- Falca begins at the entrance.

- Falca can only move one location at a time; eg, from (0, 0) to (1, 0).

- Falca can only move North (up), South (down), West (left) or East (right); ie, diagonal moves are not allowed.

- Falca can never move off the edge of the size-by-size grid constituting the cave.

- Falca can never move into a location containing a cave wall ('#').

- Falca cannot move into a location containing a dragon ('W') or any of the eight locations adjacent to a dragon (ie, including diagonally adjacent) unless carrying the sword ('t'), in which case it is considered equivalent to an empty location.

- Falca must end at the exit ('X'), after having collected all of the the treasures ('$') in the cave. Until all of the treasures have been collected, the exit location is equivalent to an empty location ('.'); ie, Falca may freely move into and out of it.

- Any item (treasure or sword) in the location currently occupied by Falca is considered to be collected, and no items are ever dropped.

An example input to this function would be `['S', 'S', 'S', 'E', 'E', 'E', 'W', 'W', 'W', 'N', 'N', 'N', 'E', 'E', 'E', 'S', 'N', 'W', 'W', 'W', 'S', 'S', 'E']`. 

#### `shortest_path` and `optimal_path`

The shortest path is the minimum number of valid moves required to move form the start location to the end location. This is a search problem which is solved using a breadth-first search algorithm.

`shortest_path` provides us with the means to quantify the cost of travelling between any pair of locations. `optimal_path` increases the scope of the problem to search for the optimal order in which to collect each of the treasures and then exit from a cave, optionally also collecting the sword, but only if that will reduce the overall path length.

`optimal_path` uses a uniform cost search, storing unexplored nodes as a priority queue according to the cost of reaching them.
