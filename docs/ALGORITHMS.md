# Algorithm Deep Dive

This document provides a comprehensive theoretical and practical explanation of the pathfinding algorithms implemented in this project. It's designed for students and developers who want to truly understand how these algorithms work.

## 📚 Table of Contents
- [Graph Theory Fundamentals](#graph-theory-fundamentals)
- [Depth-First Search (DFS)](#depth-first-search-dfs)
- [Breadth-First Search (BFS)](#breadth-first-search-bfs)
- [Dijkstra's Algorithm](#dijkstras-algorithm)
- [Comparison and When to Use Each](#comparison-and-when-to-use-each)
- [Implementation Details](#implementation-details)
- [Optimization Techniques](#optimization-techniques)

## Graph Theory Fundamentals

### What is a Graph?

A **graph** G = (V, E) consists of:
- **V**: Set of vertices (nodes)
- **E**: Set of edges (connections between nodes)

#### Our Grid as a Graph

In this visualizer, the 20×20 grid is a graph where:
- **Vertices**: Each cell is a vertex (400 total)
- **Edges**: Adjacent cells (up, down, left, right) are connected
- **Weights**: All edges have equal weight (1 unit)

```
Cell (5,5) connects to:
- (4,5) - Up
- (6,5) - Down
- (5,4) - Left
- (5,6) - Right
```

### Graph Representation

**Implicit Representation** (what we use):
```python
def get_neighbors(row, col):
    """Generate neighbors on-the-fly"""
    return [
        (row-1, col),  # Up
        (row+1, col),  # Down
        (row, col-1),  # Left
        (row, col+1)   # Right
    ]
```

**Advantages:**
- Memory efficient: O(1) instead of O(V²)
- No preprocessing needed
- Works for huge grids

**Alternative: Adjacency List** (not used):
```python
graph = {
    (0,0): [(0,1), (1,0)],
    (0,1): [(0,0), (0,2), (1,1)],
    # ... for all 400 cells
}
```

**Why we don't use it:**
- Uses O(V) memory
- Requires preprocessing
- Redundant for regular grids

## Depth-First Search (DFS)

### Algorithm Overview

DFS explores as **deep** as possible before backtracking. It's like exploring a maze by always taking the first unexplored path you see.

### Metaphor

Imagine you're in a corn maze:
- **DFS approach**: Walk forward until you hit a dead end, then backtrack to the last intersection and try a different path
- You might walk very far from the entrance before finding the exit
- You'll thoroughly explore each branch before moving to the next

### Pseudocode

```
DFS(start, end, walls):
    stack = [start]
    visited = {}
    parent_map = {}
    
    while stack is not empty:
        current = stack.pop()  // Remove from end (LIFO)
        
        if current == end:
            reconstruct_path(parent_map, start, end)
            return SUCCESS
            
        if current in visited:
            continue
            
        visited.add(current)
        
        for each neighbor of current:
            if neighbor not in walls and neighbor not in visited:
                stack.append(neighbor)
                parent_map[neighbor] = current
                
    return NO_PATH_FOUND
```

### Implementation Details

#### Data Structures

**Stack (LIFO - Last In, First Out):**
```python
stack = [start_node]

# Add to end
stack.append((5, 5))

# Remove from end
current = stack.pop()
```

**Why a stack creates depth-first behavior:**
```
Initial: stack = [(0,0)]

Step 1: Pop (0,0), add neighbors [(0,1), (1,0)]
        stack = [(0,1), (1,0)]

Step 2: Pop (1,0) <- Most recent addition
        Continue deeper in this direction first

Step 3: Pop from that branch, going deeper...
        (2,0), (3,0), (4,0)... until dead end
```

**Visited Set:**
```python
visited = set()

# O(1) check if already visited
if current in visited:
    continue

# O(1) add to visited
visited.add(current)
```

**Why use a set instead of list:**
- List: `if current in visited_list` is O(n)
- Set: `if current in visited_set` is O(1)
- For 400 cells, this is 400x faster!

**Parent Map (for path reconstruction):**
```python
parent_map = {
    (1,0): (0,0),  # (1,0) was reached from (0,0)
    (2,0): (1,0),  # (2,0) was reached from (1,0)
    (0,1): (0,0),  # (0,1) was reached from (0,0)
}

# Reconstruct path by following backwards
current = end
while current in parent_map:
    current = parent_map[current]  # Move to parent
```

### Time and Space Complexity

**Time Complexity: O(V + E)**
- V = number of vertices (cells)
- E = number of edges (connections)
- In a grid: E ≈ 4V (each cell has ~4 neighbors)
- Therefore: O(V + 4V) = O(V)

**Worst case:** Visit all 400 cells
**Best case:** Target is adjacent to start = O(1)

**Space Complexity: O(V)**
- Stack: O(d) where d is maximum depth
- Visited: O(V) in worst case
- Parent map: O(V) in worst case

For 20×20 grid (400 cells):
- Worst case: ~1200 entries (stack + visited + parent)
- Memory: ~10 KB (very efficient!)

### Characteristics

✅ **Advantages:**
- Memory efficient for sparse graphs
- Good for finding *any* path (doesn't need shortest)
- Natural implementation with recursion
- Useful for topological sorting, cycle detection

❌ **Disadvantages:**
- **Does NOT guarantee shortest path**
- Can get stuck in long branches far from target
- May explore unnecessary deep paths
- Order of exploration depends on neighbor ordering

### Visual Pattern

DFS creates a "snake" pattern:
```
S . . . .    S→→. . .    S→→→→→    S→→→→→
. . . . .    ↓ . . . .    ↓ . . .    ↓ . . ↓
. . . . .    ↓ . . . .    ↓ . . .    ↓ . . ↓
. . . . .    ↓→→→. .    ↓→→→→    ↓→→→→
. . . . E    . . . . E    . . . . E    . . . . E
```

## Breadth-First Search (BFS)

### Algorithm Overview

BFS explores all nodes at distance *k* before exploring nodes at distance *k+1*. It's like ripples expanding in a pond.

### Metaphor

Imagine you're searching for a person in a crowd:
- **BFS approach**: Ask everyone within 5 feet, then everyone within 10 feet, then 15 feet, etc.
- You explore in layers
- **Guaranteed** to find the closest person

### Pseudocode

```
BFS(start, end, walls):
    queue = [start]
    visited = {start}
    parent_map = {}
    
    while queue is not empty:
        current = queue.dequeue()  // Remove from front (FIFO)
        
        if current == end:
            reconstruct_path(parent_map, start, end)
            return SUCCESS
            
        for each neighbor of current:
            if neighbor not in walls and neighbor not in visited:
                visited.add(neighbor)
                parent_map[neighbor] = current
                queue.enqueue(neighbor)
                
    return NO_PATH_FOUND
```

### Implementation Details

#### Data Structures

**Queue (FIFO - First In, First Out):**
```python
from collections import deque

queue = deque([start_node])

# Add to back
queue.append((5, 5))

# Remove from front
current = queue.popleft()  # O(1) operation
```

**Why deque instead of list:**
```python
# ❌ Using list as queue (BAD)
queue = [start]
current = queue.pop(0)  # O(n) - shifts all elements!

# ✅ Using deque (GOOD)
queue = deque([start])
current = queue.popleft()  # O(1) - efficient!
```

**Why a queue creates breadth-first behavior:**
```
Initial: queue = [(0,0)]

Step 1: Dequeue (0,0), enqueue neighbors [(0,1), (1,0)]
        queue = [(0,1), (1,0)]

Step 2: Dequeue (0,1) <- First addition
        Enqueue its neighbors [(0,2), (1,1)]
        queue = [(1,0), (0,2), (1,1)]

Step 3: Dequeue (1,0) <- Second from step 1
        Process next neighbor from same level
```

**Critical Difference from DFS:**

**Visited Timing:**
```python
# ❌ DFS - mark visited when PROCESSING
current = stack.pop()
if current not in visited:
    visited.add(current)

# ✅ BFS - mark visited when ADDING to queue
for neighbor in neighbors:
    if neighbor not in visited:
        visited.add(neighbor)  # ← Mark NOW!
        queue.append(neighbor)
```

**Why this matters:**
```
Without pre-marking:
    A adds B to queue
    C also adds B to queue (B not yet visited!)
    B gets processed twice → inefficient

With pre-marking:
    A adds B to queue, marks as visited
    C sees B is visited, skips it
    B processed exactly once → efficient
```

### Time and Space Complexity

**Time Complexity: O(V + E)**
- Same as DFS
- Every vertex processed once
- Every edge examined once

**Space Complexity: O(V)**
- Queue can contain up to one full level
- In worst case: O(V) for a single level
- Visited set: O(V)
- Parent map: O(V)

**Worst case queue size** (for grid graph):
```
Grid dimensions: 20×20
Maximum level width: ~diagonal ≈ 28 cells
Queue size: O(28) << O(400)
```

**Memory comparison:**
- DFS: O(depth) = potentially O(V) if path is long
- BFS: O(width) = O(√V) for grid graphs

### Characteristics

✅ **Advantages:**
- **Guarantees shortest path** in unweighted graphs
- Fair exploration (all directions equally)
- Good for finding closest target
- Level-order traversal natural

❌ **Disadvantages:**
- Higher memory usage than DFS
- Slower for finding *any* path (not necessarily shortest)
- Not suitable for very large graphs

### Visual Pattern

BFS creates "concentric circles" or "wave" pattern:
```
S . . . .    S→. . .    S→→. . .    S→→→. .
. . . . .    →→. . .    →→→. . .    →→→→. .
. . . . .    . . . . .    →→. . . .    →→→→. .
. . . . .    . . . . .    . . . . .    →→→. .
. . . . E    . . . . E    . . . . E    . . . . E

(Level 0)    (Level 1)   (Level 2)    (Level 3)
```

### Path Optimality Proof

**Theorem:** BFS finds the shortest path in an unweighted graph.

**Proof:**
1. BFS explores nodes in order of increasing distance from start
2. When BFS first visits a node N, it has found the shortest path to N
3. Why? Any shorter path would have been discovered in an earlier level

**Example:**
```
Start at S, target at E

Path 1: S → A → B → E (distance 3)
Path 2: S → C → E (distance 2)

BFS exploration:
Level 0: [S]
Level 1: [A, C]  ← C is discovered
Level 2: [B, E]  ← E is discovered via C
```

BFS discovers E via the shorter path automatically!

## Dijkstra's Algorithm

### Important Note

**Current Implementation:** The button labeled "Dijkstra" actually runs DFS (due to using a stack). This section describes what **true Dijkstra's algorithm** would do.

### Algorithm Overview

Dijkstra's algorithm finds the shortest path in a **weighted** graph by always exploring the lowest-cost path first.

### Difference from BFS

| BFS | Dijkstra |
|-----|----------|
| All edges cost 1 | Edges have different costs |
| Uses queue | Uses priority queue |
| Explores by level | Explores by cost |

### When Dijkstra is Necessary

**BFS is sufficient when:**
- All moves have the same cost
- Like our current grid

**Dijkstra is needed when:**
- Different terrains have different costs
- Example: Road = 1, Forest = 3, Mountain = 5

### Pseudocode (True Dijkstra)

```
Dijkstra(start, end, weights):
    pq = PriorityQueue()
    pq.add(start, cost=0)
    distances = {start: 0}
    visited = {}
    parent_map = {}
    
    while pq is not empty:
        current, current_cost = pq.pop_min()
        
        if current == end:
            reconstruct_path(parent_map, start, end)
            return SUCCESS
            
        if current in visited:
            continue
            
        visited.add(current)
        
        for neighbor in get_neighbors(current):
            edge_cost = weights[current][neighbor]
            new_cost = current_cost + edge_cost
            
            if neighbor not in distances or new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                parent_map[neighbor] = current
                pq.add(neighbor, cost=new_cost)
                
    return NO_PATH_FOUND
```

### Key Data Structure: Priority Queue

**Priority Queue (Min-Heap):**
```python
import heapq

# Python's heapq implements a min-heap
pq = []

# Add (priority, item)
heapq.heappush(pq, (5, 'Node A'))  # cost 5
heapq.heappush(pq, (2, 'Node B'))  # cost 2
heapq.heappush(pq, (8, 'Node C'))  # cost 8

# Pop lowest priority
priority, node = heapq.heappop(pq)  # Returns (2, 'Node B')
```

**Why priority queue is critical:**
```
Without priority queue (using regular queue):
    Process nodes in order they're added
    Might process expensive path before cheap path
    
With priority queue:
    Always process cheapest unexplored path first
    Guaranteed to find optimal solution
```

### Example with Weighted Grid

```
Grid with terrain costs:
R=Road(1), F=Forest(3), M=Mountain(5)

S(R) - F - F - E(R)
  |    |   |    |
  R  - M - F  - R
  |    |   |    |
  R  - R - R  - R

BFS path: S→F→F→E (cost: 0+3+3+0 = 6)
Dijkstra path: S→R→R→R→R→E (cost: 0+1+1+1+1+0 = 4)

Dijkstra finds cheaper path!
```

### Time Complexity

**With Binary Heap: O((V + E) log V)**
- Each vertex added/removed: O(V log V)
- Each edge examined: O(E log V)

**With Fibonacci Heap: O(E + V log V)**
- Better for dense graphs
- More complex to implement

### Space Complexity: O(V)
- Priority queue: O(V)
- Distances: O(V)
- Visited: O(V)
- Parent map: O(V)

### Implementing True Dijkstra

To implement true Dijkstra's algorithm in this project:

```python
import heapq

@eel.expose
def run_dijkstra_true(start_list, end_list, wall_list, weights):
    """
    True Dijkstra implementation with weighted cells
    
    weights: dict mapping (row, col) to cost
             e.g., {(5,5): 3, (5,6): 1, ...}
    """
    start_node = tuple(start_list)
    end_node = tuple(end_list)
    walls = {tuple(w) for w in wall_list}
    
    # Priority queue: (cost, node)
    pq = [(0, start_node)]
    distances = {start_node: 0}
    visited = set()
    parent_map = {}
    
    while pq:
        current_cost, current = heapq.heappop(pq)
        
        if current == end_node:
            draw_path(parent_map, start_node, end_node)
            return
            
        if current in visited:
            continue
            
        visited.add(current)
        eel.update_node_color(current[0], current[1], "visited")
        eel.sleep(0.02)
        
        for neighbor in get_neighbors(current):
            if neighbor in walls or neighbor in visited:
                continue
                
            # Get edge cost (default to 1 if not specified)
            edge_cost = weights.get(neighbor, 1)
            new_cost = current_cost + edge_cost
            
            if neighbor not in distances or new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                parent_map[neighbor] = current
                heapq.heappush(pq, (new_cost, neighbor))
```

## Comparison and When to Use Each

### Feature Comparison

| Feature | DFS | BFS | Dijkstra |
|---------|-----|-----|----------|
| **Shortest Path** | ❌ No | ✅ Yes (unweighted) | ✅ Yes (weighted) |
| **Memory** | O(depth) | O(width) | O(V) |
| **Speed** | Fast | Medium | Slower |
| **Implementation** | Easy | Easy | Medium |
| **Weighted Graphs** | ❌ No | ❌ No | ✅ Yes |
| **Completeness** | ✅ Yes* | ✅ Yes | ✅ Yes |

*If graph is finite

### Decision Tree: Which Algorithm to Use?

```
Start
  │
  ├─ Is the graph weighted?
  │   ├─ Yes → Use Dijkstra or A*
  │   └─ No → Continue
  │
  ├─ Do you need the shortest path?
  │   ├─ Yes → Use BFS
  │   └─ No → Continue
  │
  ├─ Is memory very limited?
  │   ├─ Yes → Use DFS
  │   └─ No → Use BFS (safer choice)
  │
  └─ Special requirements?
      ├─ Topological sort → DFS
      ├─ Cycle detection → DFS
      ├─ Find any path quickly → DFS
      └─ Level-order traversal → BFS
```

### Real-World Applications

**DFS:**
- Maze solving (any solution acceptable)
- Topological sorting (task scheduling)
- Finding connected components
- Detecting cycles in graphs
- Solving puzzles (Sudoku, N-Queens)
- File system traversal

**BFS:**
- GPS navigation (unweighted roads)
- Social networking (find friends within N hops)
- Web crawling (find pages within N links)
- Finding shortest path in chess
- Minimum spanning tree (Prim's algorithm variant)
- Network broadcasting

**Dijkstra:**
- GPS navigation with traffic
- Network routing protocols
- Flight planning (cheapest route)
- Robot navigation with terrain costs
- Resource allocation in operating systems

## Implementation Details

### Neighbor Generation

```python
def get_neighbors(row, col, rows=20, cols=20):
    """
    Generate valid neighbors for a cell
    
    Returns: List of (row, col) tuples
    """
    neighbors = []
    
    # Up
    if row > 0:
        neighbors.append((row - 1, col))
    
    # Down
    if row < rows - 1:
        neighbors.append((row + 1, col))
    
    # Left
    if col > 0:
        neighbors.append((row, col - 1))
    
    # Right
    if col < cols - 1:
        neighbors.append((row, col + 1))
    
    return neighbors
```

**Why check bounds?**
```python
# Without bounds check:
neighbors = [
    (row - 1, col),  # Could be (-1, 5) → INVALID!
    (row + 1, col),  # Could be (20, 5) → INVALID!
]

# With bounds check:
neighbors = [
    (0, 5),  # Top row: no up neighbor
    (1, 5),  # Valid down neighbor
]
```

### Path Reconstruction

```python
def reconstruct_path(parent_map, start, end):
    """
    Build path from end to start using parent pointers
    
    Returns: List of (row, col) tuples from start to end
    """
    path = []
    current = end
    
    while current != start:
        path.append(current)
        current = parent_map[current]
    
    path.append(start)
    path.reverse()  # Reverse to get start → end
    
    return path
```

**Example:**
```python
parent_map = {
    (1,0): (0,0),
    (1,1): (1,0),
    (1,2): (1,1),
}

path = reconstruct_path(parent_map, (0,0), (1,2))
# Returns: [(0,0), (1,0), (1,1), (1,2)]
```

### Avoiding Duplicate Processing

**DFS Pattern:**
```python
while stack:
    current = stack.pop()
    
    if current in visited:
        continue  # Skip if already processed
        
    visited.add(current)
    # Process current...
```

**BFS Pattern:**
```python
while queue:
    current = queue.popleft()
    # No need to check visited here!
    
    for neighbor in neighbors:
        if neighbor not in visited:
            visited.add(neighbor)  # Mark BEFORE adding
            queue.append(neighbor)
```

**Why different patterns?**
- DFS: Nodes may be added multiple times to stack
- BFS: Pre-marking prevents duplicate additions

## Optimization Techniques

### 1. Early Exit

```python
# ✅ Stop as soon as target found
if current == end_node:
    draw_path(parent_map, start_node, end_node)
    return  # Exit immediately

# ❌ Don't continue searching
if current == end_node:
    found = True
    # ... continue loop? Wasteful!
```

### 2. Bidirectional Search

**Concept:** Search from both start and end simultaneously

```python
def bidirectional_bfs(start, end, walls):
    queue_start = deque([start])
    queue_end = deque([end])
    visited_start = {start}
    visited_end = {end}
    
    while queue_start and queue_end:
        # Expand from start
        current_start = queue_start.popleft()
        if current_start in visited_end:
            return "Path found!"  # Paths met!
        
        # Expand from end
        current_end = queue_end.popleft()
        if current_end in visited_start:
            return "Path found!"
```

**Benefits:**
- Explores O(b^(d/2)) instead of O(b^d)
- Much faster for long paths
- Same result as regular BFS

### 3. Heuristic Search (A* Preview)

**Idea:** Guide search toward target

```python
def manhattan_distance(a, b):
    """Heuristic: estimate distance to goal"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# In priority queue, use: cost + heuristic
priority = distances[node] + manhattan_distance(node, end)
```

### 4. Jump Point Search

**For uniform grids:** Skip intermediate nodes

```
Instead of: S → A → B → C → E
Jump to: S ————————————→ E
```

## Further Reading

**Books:**
- "Introduction to Algorithms" (CLRS) - Chapter 22-24
- "Algorithm Design Manual" (Skiena) - Chapter 5-6
- "Algorithms" (Sedgewick & Wayne) - Chapter 4

**Online Resources:**
- [VisuAlgo](https://visualgo.net/) - Interactive algorithm visualizations
- [GeeksforGeeks](https://www.geeksforgeeks.org/graph-data-structure-and-algorithms/)
- [Khan Academy - Algorithms](https://www.khanacademy.org/computing/computer-science/algorithms)

**Research Papers:**
- Dijkstra, E. W. (1959). "A note on two problems in connexion with graphs"
- Hart, P. E., et al. (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths" (A* algorithm)

---

**Questions or confused?** Open an issue on GitHub! Understanding algorithms takes time and practice. 🧠
