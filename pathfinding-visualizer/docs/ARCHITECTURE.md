# Architecture Documentation

This document provides an in-depth technical overview of the Pathfinding Algorithm Visualizer, explaining design decisions, data flow, and implementation details.

## 🏛️ System Architecture

### Overview

The application follows a **client-server architecture** with a Python backend and JavaScript frontend, connected via the Eel framework. This design separates concerns while enabling real-time bidirectional communication.

```
┌─────────────────────────────────────────────────────────┐
│                     User Interface                       │
│                    (Web Browser)                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │   Grid UI   │  │   Controls   │  │   Animations  │  │
│  │  (Canvas)   │  │  (Buttons)   │  │ (CSS/Keyframes)  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
│                           │                              │
│                    index.html (DOM)                      │
│                           │                              │
│                    JavaScript Logic                      │
│              (Event Handling, State Mgmt)                │
└───────────────────────────│──────────────────────────────┘
                            │
                    Eel.js (WebSocket)
                            │
┌───────────────────────────│──────────────────────────────┐
│                   Python Backend                         │
│                      (main.py)                           │
│                           │                              │
│  ┌────────────────────────┴────────────────────────┐    │
│  │          Algorithm Implementations              │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │    │
│  │  │   DFS    │  │   BFS    │  │  Dijkstra*   │  │    │
│  │  └──────────┘  └──────────┘  └──────────────┘  │    │
│  │                                                  │    │
│  │  ┌─────────────────────────────────────────┐   │    │
│  │  │        Path Reconstruction              │   │    │
│  │  │         (draw_path)                     │   │    │
│  │  └─────────────────────────────────────────┘   │    │
│  └──────────────────────────────────────────────────┘    │
│                                                           │
│           Eel Framework (Exposed Functions)              │
└───────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Python 3.7+ | Algorithm logic and execution |
| **Frontend** | Vanilla JavaScript | UI interaction and state management |
| **Bridge** | Eel Framework | Python ↔ JavaScript communication |
| **UI** | HTML5 + CSS3 | Structure and styling |
| **Visualization** | CSS Animations | Real-time visual feedback |

## 🔄 Data Flow

### Initialization Sequence

```
1. User runs: python main.py
   │
2. eel.init('web')
   │   - Locates web/ directory
   │   - Prepares to serve static files
   │
3. eel.start('index.html')
   │   - Starts local web server
   │   - Opens browser window
   │   - Injects eel.js script
   │
4. Browser loads index.html
   │   - Parses HTML structure
   │   - Loads style.css
   │   - Executes JavaScript
   │
5. JavaScript creates 20×20 grid
   │   - 400 div elements generated
   │   - Event listeners attached
   │
6. System ready for interaction
```

### User Interaction Flow

#### Placing Nodes and Walls

```
User clicks grid cell
     │
     ├─ JavaScript: handleMouseDown()
     │      │
     │      ├─ No start node? → Add 'start' class, store [row, col]
     │      ├─ No end node? → Add 'end' class, store [row, col]
     │      └─ Has both? → Toggle 'wall' class
     │
     └─ CSS applies styling
            - Start: green (#00e676)
            - End: red (#ff1744)
            - Wall: gray (#4a5568)
```

#### Running an Algorithm

```
User clicks "BFS" button
     │
     ├─ JavaScript: startAlgo('bfs')
     │      │
     │      ├─ Validation: Are start & end set?
     │      │      └─ No → Alert user, abort
     │      │
     │      ├─ Collect walls:
     │      │      - Query all .wall elements
     │      │      - Extract [row, col] from data attributes
     │      │      - Build walls array
     │      │
     │      └─ Call Python: eel.run_bfs(start, end, walls)
     │
     └─ Python: run_bfs() executes
            │
            ├─ Algorithm explores graph:
            │      │
            │      ├─ For each visited node:
            │      │      │
            │      │      └─ eel.update_node_color(row, col, "visited")
            │      │             │
            │      │             └─ JavaScript: update_node_color()
            │      │                    │
            │      │                    └─ Add 'visited' class to cell
            │      │                           │
            │      │                           └─ CSS animation triggers
            │      │
            │      └─ Path found! → draw_path()
            │             │
            │             └─ For each path node:
            │                    │
            │                    └─ eel.update_node_color(row, col, "path")
            │                           │
            │                           └─ JavaScript adds 'path' class
            │                                  │
            │                                  └─ Gold pulsing animation
            │
            └─ Algorithm completes, control returns to browser
```

## 🧱 Component Architecture

### Backend Components (main.py)

#### 1. Initialization
```python
eel.init('web')  # Sets root directory for serving files
```
- **Purpose**: Configure Eel to serve static files from `web/` directory
- **Critical**: Must be called before any `@eel.expose` decorators

#### 2. Helper Functions

##### `draw_path(parent_map, start, end)`
```python
def draw_path(parent_map, start, end):
    """
    Reconstructs and visualizes the path from end to start.
    
    Algorithm:
        1. Start at end node
        2. Follow parent_map backwards
        3. Stop when reaching start node
        4. Animate each step with yellow color
    
    Time Complexity: O(path_length)
    Space Complexity: O(path_length) for path list
    """
```

**Design Decision**: Path is drawn in reverse (end → start) because:
- `parent_map` naturally points backwards
- More efficient than reversing the entire path
- Visual effect is identical to user

#### 3. Algorithm Implementations

Each algorithm follows this structure:
```python
@eel.expose  # Allows JavaScript to call this function
def run_algorithm(start_list, end_list, wall_list):
    # 1. Data conversion (lists → tuples, sets)
    # 2. Initialize data structures
    # 3. Main algorithm loop
    # 4. Visualize visited nodes
    # 5. Draw final path
```

##### Data Structure Choices

| Algorithm | Primary DS | Reason |
|-----------|-----------|--------|
| DFS | `list` (as stack) | LIFO behavior via `pop()` |
| BFS | `deque` | O(1) `popleft()` for FIFO |
| All | `set` for visited | O(1) membership testing |
| All | `dict` for parent_map | O(1) path reconstruction |

**Why sets for walls and visited?**
```python
# ❌ Bad: O(n) lookup
if neighbor in walls_list:  # Linear search through list

# ✅ Good: O(1) lookup
if neighbor in walls_set:   # Hash table lookup
```

### Frontend Components (web/)

#### index.html Structure

```html
<!DOCTYPE html>
<html>
  <head>
    <!-- Eel.js injected automatically -->
    <script src="/eel.js"></script>
  </head>
  <body>
    <!-- Control Panel -->
    <div class="navbar">
      <button onclick="startAlgo('bfs')">BFS</button>
      <!-- ... other buttons ... -->
    </div>
    
    <!-- Grid Container -->
    <div id="grid-container">
      <!-- 400 cells generated by JavaScript -->
    </div>
    
    <script>
      // 1. Expose functions to Python
      // 2. Create grid
      // 3. Attach event listeners
      // 4. Define interaction logic
    </script>
  </body>
</html>
```

#### JavaScript Architecture

##### State Management
```javascript
// Global state (simple approach for small app)
let startNode = null;    // [row, col] or null
let endNode = null;      // [row, col] or null
let isMouseDown = false; // For drag-to-draw walls
```

**Design Choice**: Global variables are acceptable here because:
- Single page application
- No state persistence needed
- No concurrent modifications
- Simple to reason about

**Alternative Considered**: Object-based state management
```javascript
const state = {
  startNode: null,
  endNode: null,
  isMouseDown: false
};
```
**Rejected because**: Adds complexity without benefit for this scale.

##### Event-Driven Architecture

```
User Interaction
       ↓
Event Listener (mousedown, mouseenter, mouseup)
       ↓
Event Handler (handleMouseDown, handleMouseEnter)
       ↓
State Update + DOM Manipulation
       ↓
CSS Styling Applied
```

**Critical Pattern**: Expose before Define
```javascript
// ✅ CORRECT ORDER
eel.expose(update_node_color);  // Expose first
function update_node_color(row, col, type) {
    // Function body
}

// ❌ WRONG ORDER (won't work)
function update_node_color(row, col, type) {
    // Function body  
}
eel.expose(update_node_color);  // Too late!
```

#### style.css Architecture

##### Organization Strategy
```css
/* 1. Global/Reset Styles */
body, * { }

/* 2. Layout Components */
.navbar { }
#grid-container { }

/* 3. Basic Elements */
.node { }
button { }

/* 4. State Modifiers */
.node.start { }
.node.end { }
.node.wall { }
.node.visited { }
.node.path { }

/* 5. Animations (last) */
@keyframes ageColor { }
@keyframes pathPulse { }
```

##### Animation Design

**The "Aging" Effect** (`@keyframes ageColor`):
```
Purpose: Show the chronological order of exploration
Duration: 1.5s
Stages:
  0%   → Cyan (#a7f3d0)  - Just visited
  50%  → Blue (#00b4d8)  - Middle age
  100% → Purple (#3759c9) - Fully aged

Why it matters:
  - Visually communicates temporal information
  - Helps understand algorithm behavior
  - Creates a "heat map" of exploration order
```

**The "Pulse" Effect** (`@keyframes pathPulse`):
```
Purpose: Draw attention to the final path
Duration: 1.5s (infinite loop)
Effect: Scale and glow intensity oscillation

Why alternate (not loop):
  - Creates breathing effect
  - Less jarring than restart
  - Maintains visual interest
```

## 🔐 Security Considerations

### Current Security Model

**Eel's Security:**
- Localhost only (not exposed to network)
- WebSocket communication over local loopback
- No authentication required (single-user desktop app)

**Potential Vulnerabilities:**
- XSS: Not applicable (no user HTML input)
- CSRF: Not applicable (no external requests)
- Code Injection: Minimal risk (input is numeric grid data)

**Input Validation:**
```python
# Current: Implicit validation
start_node = tuple(start_list)  # Assumes [row, col] format

# Future: Explicit validation
def validate_node(node_list):
    if not isinstance(node_list, list) or len(node_list) != 2:
        raise ValueError("Invalid node format")
    if not all(isinstance(x, int) for x in node_list):
        raise ValueError("Coordinates must be integers")
    return tuple(node_list)
```

## ⚡ Performance Analysis

### Time Complexity

| Algorithm | Best Case | Average Case | Worst Case |
|-----------|-----------|--------------|------------|
| DFS | O(1) | O(V + E) | O(V + E) |
| BFS | O(1) | O(V + E) | O(V + E) |

Where:
- V = number of vertices (cells) = 400 in 20×20 grid
- E = number of edges ≈ 4V in grid graph (each cell has ~4 neighbors)

### Space Complexity

| Algorithm | Data Structure | Space |
|-----------|---------------|-------|
| DFS | Stack + Visited + Parent | O(V) |
| BFS | Queue + Visited + Parent | O(V) |

**Worst-case scenario**: All 400 cells visited
- Visited set: 400 entries
- Parent map: 399 entries (all except start)
- Stack/Queue: Up to 400 entries
- Total: ~1200 entries ≈ 10KB memory

### Bottlenecks

1. **Visualization Delay**:
   ```python
   eel.sleep(0.02)  # 20ms per node
   ```
   - For 400 cells: 8 seconds maximum
   - Trade-off: Speed vs. comprehensibility
   
2. **DOM Manipulation**:
   ```javascript
   cell.classList.add('visited');  // Triggers CSS recalculation
   ```
   - 400 potential DOM updates
   - Browser handles efficiently with batching

3. **Network Overhead**:
   - Each `eel.update_node_color()` is a WebSocket message
   - Minimal overhead for localhost
   - Future: Batch updates for larger grids

### Optimization Opportunities

**Current**: Sequential updates
```python
for node in visited_nodes:
    eel.update_node_color(node[0], node[1], "visited")
    eel.sleep(0.02)
```

**Future**: Batch updates
```python
# Send all updates at once, animate client-side
eel.update_multiple_nodes(visited_nodes, "visited")
```

## 🎨 UI/UX Design Decisions

### Color Palette

```css
Background:  #121212 (near-black)
Cards:       #1e1e1e (dark gray)
Text:        #e0e0e0 (off-white)
Accent:      #00f2ff (cyan)
Start:       #00e676 (green)
End:         #ff1744 (red)
Walls:       #4a5568 (gray)
Path:        #ffd700 (gold)
```

**Rationale**:
- Dark mode reduces eye strain
- High contrast for accessibility
- Neon accents for modern aesthetic
- Color-blind friendly (red-green distinction not critical)

### Animation Timing

```css
Button hover: 0.3s    /* Fast enough to feel responsive */
Cell hover: 0.1s      /* Instant feedback */
Visited fade: 1.5s    /* Slow enough to see progression */
Path pulse: 1.5s      /* Matches visited animation */
```

### Grid Sizing

**20×20 Grid Choice**:
- Small enough: Fits on screen without scrolling
- Large enough: Demonstrates algorithm behavior clearly
- Optimal: Each cell visible at 25px × 25px
- Total dimensions: 500px × 500px (comfortable viewport size)

## 🔧 Configuration & Extensibility

### Easy Configuration Points

**Grid size** (3 places to change):
```python
# main.py
ROWS = 20
COLS = 20
```
```javascript
// index.html
const ROWS = 20;
const COLS = 20;
```
```css
/* style.css - adjust cell size */
.node {
    width: 25px;
    height: 25px;
}
```

**Animation speed**:
```python
eel.sleep(0.02)  # Decrease for faster, increase for slower
```

**Color scheme**:
All colors defined in CSS custom properties (future enhancement):
```css
:root {
  --color-start: #00e676;
  --color-end: #ff1744;
  /* ... */
}
```

### Extension Points

**Adding new algorithms**:
1. Create function in `main.py`
2. Add button in `index.html`
3. Wire up in `startAlgo()` function

**Adding visualization features**:
- Heatmap mode: Adjust `ageColor` keyframes
- Step-through mode: Add pause/resume buttons
- Statistics overlay: Track and display metrics

## 📊 Testing Strategy

### Current Testing Approach
- **Manual testing**: Developer runs through scenarios
- **Visual verification**: Confirm animations work correctly

### Recommended Testing Levels

#### Unit Tests (Future)
```python
# test_algorithms.py
def test_bfs_finds_shortest_path():
    walls = set()
    path = run_bfs_test([0, 0], [5, 5], walls)
    assert len(path) == 10  # Manhattan distance
```

#### Integration Tests (Future)
```python
# test_eel_integration.py
def test_algorithm_communicates_with_frontend():
    mock_eel.update_node_color = Mock()
    run_bfs([0, 0], [1, 1], [])
    assert mock_eel.update_node_color.called
```

#### Visual Tests (Future)
- Screenshot comparison
- Animation timing validation
- Cross-browser rendering

## 🚀 Deployment Considerations

### Current Deployment
- Local execution only
- No build process required
- Dependencies: Python 3.7+, Eel library

### Future Deployment Options

**Desktop Application**:
```bash
# Using PyInstaller
pyinstaller --onefile --add-data "web:web" main.py
```

**Web Application**:
- Rewrite backend as Flask/FastAPI
- Use WebSockets for real-time updates
- Deploy to cloud (Heroku, AWS, etc.)

**Progressive Web App**:
- Move algorithms to WebAssembly
- Add service worker for offline use
- Responsive design for mobile

## 📝 Design Patterns Used

### Observer Pattern
```
Python (Subject) ──notifies──> JavaScript (Observer)
                via eel.update_node_color()
```

### State Pattern
```javascript
// Cell state determines behavior
if (!startNode) { /* place start */ }
else if (!endNode) { /* place end */ }
else { /* toggle wall */ }
```

### Strategy Pattern
```javascript
// Algorithm selection
function startAlgo(algoType) {
    if (algoType === 'dfs') { eel.run_dfs(...) }
    if (algoType === 'bfs') { eel.run_bfs(...) }
}
```

## 🔮 Future Architecture Considerations

### Scalability
- **Problem**: Current design blocks during execution
- **Solution**: Web Workers for background processing
- **Benefit**: UI remains responsive

### Modularity
- **Problem**: All code in single files
- **Solution**: Split into modules (grid.js, algorithms.py, etc.)
- **Benefit**: Easier testing and maintenance

### State Management
- **Problem**: Global variables in JavaScript
- **Solution**: Redux-like state container
- **Benefit**: Predictable state transitions, time-travel debugging

---

This architecture is designed for **educational clarity** over enterprise-grade complexity. As requirements grow, it can be incrementally refactored while maintaining the core learning objectives.
