[README.md](https://github.com/user-attachments/files/24909964/README.md)
# Pathfinding Algorithm Visualizer

A real-time interactive visualization tool for understanding classical graph traversal and pathfinding algorithms. Built with Python (Eel) and vanilla JavaScript, this project demonstrates the core differences between Depth-First Search (DFS), Breadth-First Search (BFS), and Dijkstra's algorithm through elegant animations.

![Pathfinding Visualizer Demo](assets/demo.gif)

## 🎯 Overview

This educational tool helps computer science students and enthusiasts visualize how different pathfinding algorithms explore a graph space. Watch as algorithms traverse a grid in real-time, revealing their unique characteristics through color-coded animations.

### What Makes This Project Unique

- **Pure Algorithm Implementations**: Clean, readable implementations of DFS, BFS, and Dijkstra's algorithm without external pathfinding libraries
- **Real-Time Visualization**: See algorithms explore the search space node-by-node with smooth animations
- **Interactive Grid**: Create custom mazes and obstacles with intuitive mouse controls
- **Educational Focus**: Code is structured to prioritize learning and understanding over optimization
- **Modern Dark UI**: Sleek, cyberpunk-inspired interface with neon accents and smooth transitions

## 🔍 Algorithms Explained

### Depth-First Search (DFS)
DFS explores as far as possible along each branch before backtracking. It uses a **stack** (LIFO - Last In, First Out) data structure.

**Characteristics:**
- Memory efficient: O(d) space complexity where d is maximum depth
- Not guaranteed to find the shortest path
- Explores deep into the graph before exploring neighbors
- Can get "stuck" in long paths far from the target

**Use Cases:**
- Maze generation
- Topological sorting
- Cycle detection in graphs
- Solving puzzles with one solution (e.g., Sudoku)

**Visualization Pattern:** Creates a "snake-like" exploration pattern, diving deep into one direction before trying others.

### Breadth-First Search (BFS)
BFS explores all neighbors at the current depth before moving to nodes at the next depth level. It uses a **queue** (FIFO - First In, First Out) data structure.

**Characteristics:**
- Guarantees shortest path in unweighted graphs
- Higher memory usage: O(b^d) where b is branching factor, d is depth
- Explores level-by-level outward from the start
- More "democratic" in exploring all directions equally

**Use Cases:**
- Finding shortest path in unweighted graphs
- Social network friend suggestions (friends of friends)
- Web crawling
- GPS navigation (when all moves have equal cost)

**Visualization Pattern:** Creates concentric "rings" or "waves" expanding outward from the start node.

### Dijkstra's Algorithm
While the button says "Dijkstra", the current implementation is actually DFS. True Dijkstra's algorithm is a weighted shortest-path algorithm that uses a priority queue to always explore the lowest-cost path first.

**Current Implementation:** Uses a stack (DFS behavior) instead of a priority queue.

**True Dijkstra Characteristics:**
- Guarantees shortest path in weighted graphs
- Uses a min-heap/priority queue to explore lowest-cost nodes first
- More computationally expensive than BFS/DFS
- Works with non-negative edge weights

**Note:** A future update could implement true Dijkstra's algorithm with weighted cells.

## 🚀 Features

### Interactive Grid
- **Click once**: Place start node (green)
- **Click twice**: Place end node (red)
- **Click and drag**: Draw walls (dark gray)
- **Click on walls**: Remove walls
- **20×20 grid**: Enough space to create complex mazes

### Real-Time Animation
- **Visited nodes**: Transition through a gradient (cyan → blue → purple) showing the order of exploration
- **Final path**: Highlighted in gold with a pulsing glow effect
- **Adjustable speed**: Controlled via `eel.sleep()` parameters (currently 0.02s for DFS, 0.01s for BFS)

### Visual Feedback
- **Color-coded states**:
  - Green: Start node
  - Red: End node
  - Gray: Walls
  - Cyan → Purple gradient: Visited nodes (aging effect)
  - Gold: Final path
- **Smooth animations**: CSS transitions and keyframe animations for professional look
- **Responsive UI**: Buttons with hover effects and glowing accents

## 📋 Prerequisites

### Required Software
- **Python 3.7+**: Core runtime
- **Node.js & npm**: Not required (no build step needed)
- **Modern web browser**: Chrome, Firefox, Safari, or Edge

### Python Dependencies
```bash
pip install eel
```

That's it! Eel is the only dependency required.

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/pathfinding-visualizer.git
cd pathfinding-visualizer
```

2. **Install dependencies**
```bash
pip install eel
```

3. **Verify directory structure**
```
pathfinding-visualizer/
├── main.py
└── web/
    ├── index.html
    └── style.css
```

4. **Run the application**
```bash
python main.py
```

The application will automatically open in your default browser at `http://localhost:8000`.

## 📖 Usage

### Basic Workflow
1. **Start the application**: Run `python main.py`
2. **Place start node**: Click any cell on the grid
3. **Place end node**: Click another cell
4. **Draw walls**: Click and drag across cells to create obstacles
5. **Choose algorithm**: Click "DFS", "BFS", or "Dijkstra"
6. **Watch the visualization**: See the algorithm explore the space
7. **Reset**: Click "Reset" to clear and start over

### Tips for Better Visualization
- **Create interesting mazes**: Draw complex wall patterns to see how algorithms navigate around obstacles
- **Compare algorithms**: Reset and run different algorithms on the same maze to see behavioral differences
- **Observe the patterns**: 
  - DFS creates winding paths
  - BFS creates expanding circles
  - Watch how they handle dead ends differently

### Keyboard Shortcuts
Currently, there are no keyboard shortcuts. All interactions are mouse-based.

## 🏗️ Project Structure

```
pathfinding-visualizer/
│
├── main.py                 # Python backend with algorithm implementations
│   ├── run_dfs()          # Depth-First Search using stack
│   ├── run_bfs()          # Breadth-First Search using queue
│   ├── run_dijkstra()     # Currently implements DFS (legacy name)
│   └── draw_path()        # Visualizes the final path
│
└── web/                    # Frontend assets (served by Eel)
    ├── index.html         # Grid UI and interaction logic
    │   ├── Grid creation (20×20)
    │   ├── Mouse event handlers
    │   ├── Algorithm trigger functions
    │   └── Python-JavaScript bridge (Eel.js)
    │
    └── style.css          # Modern dark theme styling
        ├── Color scheme and animations
        ├── Grid layout
        ├── Button styling
        └── Keyframe animations for visited/path nodes
```

## 🧩 Algorithm Implementation Details

### Data Structures

#### Grid Representation
- **Tuples**: Each cell is represented as `(row, col)` tuple
- **Sets**: Walls and visited nodes stored as sets for O(1) lookup
- **Dictionary**: `parent_map` stores the path by mapping each node to its predecessor

#### DFS Implementation
```python
stack = [start_node]           # LIFO: Last In, First Out
visited = set()                # Track explored nodes
parent_map = {}                # Reconstruct path

while stack:
    current = stack.pop()      # Remove from end (stack behavior)
    # ... process node and add neighbors to stack
```

#### BFS Implementation
```python
queue = deque([start_node])    # FIFO: First In, First Out
visited = {start_node}         # Pre-mark start as visited
parent_map = {}                # Reconstruct path

while queue:
    current = queue.popleft()  # Remove from front (queue behavior)
    # ... process node and add neighbors to queue
```

### Key Differences

| Aspect | DFS | BFS |
|--------|-----|-----|
| Data Structure | Stack (list) | Queue (deque) |
| Removal Method | `stack.pop()` | `queue.popleft()` |
| Visited Check | After removal | Before adding to queue |
| Memory Usage | O(depth) | O(width) |
| Path Guarantee | No shortest path | Shortest path |
| Pattern | Deep exploration | Level-by-level |

### Path Reconstruction

Both algorithms use the same path reconstruction logic:

```python
def draw_path(parent_map, start, end):
    curr = end
    path = []
    
    while curr in parent_map:
        curr = parent_map[curr]
        path.append(curr)
        
        if curr == start:
            break
            
        # Animate path in reverse (end to start)
        eel.update_node_color(curr[0], curr[1], "path")
        eel.sleep(0.02)
```

## 🎨 Customization

### Adjust Animation Speed

In `main.py`, modify the `eel.sleep()` values:

```python
# Faster visualization
eel.sleep(0.005)  # Very fast

# Slower visualization  
eel.sleep(0.1)    # Slow motion
```

### Change Grid Size

In both `main.py` and `index.html`, update `ROWS` and `COLS`:

```python
# main.py
ROWS = 30  # Increase to 30
COLS = 30
```

```javascript
// index.html
const ROWS = 30;
const COLS = 30;
```

Also adjust cell size in `style.css`:

```css
.node {
    width: 20px;   /* Smaller cells for larger grid */
    height: 20px;
}
```

### Modify Colors

Edit `style.css` to change the color scheme:

```css
.node.start {
    background-color: #your-color;  /* Start node */
}

.node.end {
    background-color: #your-color;  /* End node */
}

.node.visited {
    /* Modify the @keyframes ageColor animation */
}

.node.path {
    background-color: #your-color;  /* Final path */
}
```

### Add Diagonal Movement

Modify the `neighbors` list in all algorithm functions:

```python
neighbors = [
    (current[0] - 1, current[1]),      # Up
    (current[0] + 1, current[1]),      # Down
    (current[0], current[1] - 1),      # Left
    (current[0], current[1] + 1),      # Right
    (current[0] - 1, current[1] - 1),  # Up-Left
    (current[0] - 1, current[1] + 1),  # Up-Right
    (current[0] + 1, current[1] - 1),  # Down-Left
    (current[0] + 1, current[1] + 1),  # Down-Right
]
```

## 🐛 Known Issues & Limitations

### Current Limitations
1. **"Dijkstra" is actually DFS**: The button labeled "Dijkstra" runs a DFS algorithm with a stack, not true Dijkstra's algorithm
2. **No diagonal movement**: Only up, down, left, right movement is allowed
3. **Unweighted graph**: All moves have equal cost (1 unit)
4. **No path cost display**: The final path length is not shown
5. **Single execution**: Must reset to run another algorithm (no pause/resume)

### Potential Bugs
- **Path not found edge case**: If no path exists, the algorithm may not provide clear feedback
- **Large grid performance**: Grids larger than 50×50 may experience lag
- **Browser compatibility**: Older browsers may not support CSS animations properly

## 🔮 Future Enhancements

### Planned Features
- [ ] True Dijkstra's algorithm with weighted cells
- [ ] A* (A-star) pathfinding algorithm
- [ ] Bidirectional search
- [ ] Greedy Best-First Search
- [ ] Jump Point Search (JPS)

### UI Improvements
- [ ] Speed slider for real-time control
- [ ] Pause/Resume functionality
- [ ] Step-by-step mode
- [ ] Clear walls only (keep start/end)
- [ ] Preset maze patterns (recursive division, Prim's, etc.)
- [ ] Path cost/length display
- [ ] Algorithm statistics (nodes visited, time elapsed)

### Technical Enhancements
- [ ] Responsive grid sizing
- [ ] Mobile touch support
- [ ] Export/Import maze patterns
- [ ] Save visualization as video/GIF
- [ ] Comparison mode (run multiple algorithms side-by-side)

## 🤝 Contributing

Contributions are welcome! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Test your changes thoroughly
4. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **Push to your branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**
   - Describe your changes clearly
   - Reference any related issues
   - Include screenshots if applicable

### Contribution Ideas
- Implement true Dijkstra's algorithm
- Add A* pathfinding
- Create preset maze patterns
- Add mobile touch support
- Improve performance for larger grids
- Add unit tests
- Improve documentation

## 📚 Educational Resources

### Understanding Pathfinding Algorithms
- [Graph Traversal - Wikipedia](https://en.wikipedia.org/wiki/Graph_traversal)
- [A* Pathfinding for Beginners](http://www.policyalmanac.org/games/aStarTutorial.htm)
- [Dijkstra's Algorithm - Computerphile](https://www.youtube.com/watch?v=GazC3A4OQTE)

### Related Projects
- [PathFinding.js](https://qiao.github.io/PathFinding.js/visual/) - More comprehensive JavaScript visualizer
- [Maze Generation Algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm)

### Learning Resources
- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/books/introduction-algorithms-third-edition)
- [Algorithms Course - Khan Academy](https://www.khanacademy.org/computing/computer-science/algorithms)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Eel Framework**: For seamless Python-JavaScript integration
- **Graph Theory Community**: For decades of research on pathfinding algorithms
- **Inspiration**: Classic pathfinding visualizers and educational tools

## 👤 Author

**MD Nowroz Imtiaz Rifat**
- GitHub: [@n-im-rifat](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/nowroz-rifat)

## 📧 Contact

Have questions or suggestions? Feel free to:
- Open an issue on GitHub
- Send me an email at your.email@example.com
- Start a discussion in the Discussions tab

---

**Happy Pathfinding! 🎯**

*If you found this project helpful, please consider giving it a ⭐ on GitHub!*
