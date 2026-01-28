# Contributing to Pathfinding Algorithm Visualizer

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## 🎯 Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in all interactions.

### Expected Behavior
- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Git for version control
- A code editor (VS Code, PyCharm, Sublime, etc.)
- Basic understanding of Python and JavaScript

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork locally**
   ```bash
   git clone https://github.com/YOUR-USERNAME/pathfinding-visualizer.git
   cd pathfinding-visualizer
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/ORIGINAL-OWNER/pathfinding-visualizer.git
   ```

4. **Install dependencies**
   ```bash
   pip install eel
   ```

5. **Create a branch for your feature**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- **Clear title**: Briefly describe the problem
- **Description**: Detailed explanation of the issue
- **Steps to reproduce**: List the exact steps to trigger the bug
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Screenshots**: If applicable
- **Environment**: OS, Python version, browser

**Example:**
```
Title: Path not found when walls surround end node

Description:
When the end node is completely surrounded by walls, the algorithm 
doesn't clearly indicate that no path exists.

Steps to reproduce:
1. Place start node at (5, 5)
2. Place end node at (10, 10)
3. Draw walls around end node in all 4 directions
4. Click any algorithm button
5. Algorithm runs indefinitely without feedback

Expected behavior:
Should display message "No path found" and stop execution

Actual behavior:
Algorithm explores entire grid and stops without feedback

Environment:
- OS: Windows 11
- Python: 3.11
- Browser: Chrome 120
```

### Suggesting Enhancements

For feature requests, create an issue with:
- **Clear title**: What feature do you want?
- **Motivation**: Why is this feature needed?
- **Proposed solution**: How would it work?
- **Alternatives considered**: Other approaches you thought about
- **Additional context**: Mockups, examples, references

### Pull Requests

1. **Ensure your code follows the project style**
   - See Code Style Guide below

2. **Update documentation**
   - Modify README.md if adding features
   - Add docstrings to new functions
   - Update comments for clarity

3. **Test your changes**
   - Test all algorithms
   - Try edge cases (no path, single cell, etc.)
   - Test on different browsers if modifying frontend

4. **Write clear commit messages**
   ```
   Good: "Add A* pathfinding algorithm with heuristic function"
   Bad: "fixed stuff"
   ```

5. **Keep pull requests focused**
   - One feature/fix per PR
   - Small PRs are easier to review

6. **Fill out the PR template**
   - Describe what changed
   - Link related issues
   - Add screenshots if UI changed

## 💻 Code Style Guide

### Python Style (PEP 8 Compliant)

**Naming Conventions:**
```python
# Variables and functions: snake_case
start_node = (0, 0)
def calculate_path(start, end):
    pass

# Classes: PascalCase
class PathFinder:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_GRID_SIZE = 50
DEFAULT_SPEED = 0.02
```

**Function Documentation:**
```python
def run_algorithm(start_list, end_list, wall_list):
    """
    Execute the pathfinding algorithm and visualize the process.
    
    Args:
        start_list (list): [row, col] coordinates of start node
        end_list (list): [row, col] coordinates of end node  
        wall_list (list): List of [row, col] coordinates for wall cells
        
    Returns:
        None: Directly updates the frontend via Eel
        
    Note:
        This function blocks until path is found or search completes.
    """
    pass
```

**Code Organization:**
```python
# 1. Imports at top
import eel
from collections import deque

# 2. Constants
ROWS = 20
COLS = 20

# 3. Helper functions
def draw_path(parent_map, start, end):
    pass

# 4. Exposed functions (algorithms)
@eel.expose
def run_bfs(start_list, end_list, wall_list):
    pass

# 5. Application startup
eel.start('index.html', size=(800, 700))
```

**Commenting Best Practices:**
```python
# Good: Explain WHY, not WHAT
# Use deque for O(1) popleft operation instead of list
queue = deque([start_node])

# Bad: States the obvious
# Create a queue with the start node
queue = deque([start_node])

# Good: Document algorithm-specific choices
# DFS explores depth-first, so we pop from the end (stack behavior)
current = stack.pop()

# Good: Warn about important behavior
# IMPORTANT: Mark as visited BEFORE adding to queue to prevent duplicates
visited.add(neighbor)
queue.append(neighbor)
```

### JavaScript Style

**Naming Conventions:**
```javascript
// Variables and functions: camelCase
const startNode = [0, 0];
function updateNodeColor(row, col, type) { }

// Constants: UPPER_SNAKE_CASE
const ROWS = 20;
const COLS = 20;
```

**Code Organization:**
```javascript
// 1. Expose functions to Python FIRST
eel.expose(update_node_color);
function update_node_color(row, col, type) { }

// 2. Constants
const ROWS = 20;
const COLS = 20;

// 3. State variables
let startNode = null;
let endNode = null;

// 4. Grid creation
const container = document.getElementById('grid-container');

// 5. Event handlers
function handleMouseDown(node, r, c) { }

// 6. Algorithm triggers
function startAlgo(algoType) { }
```

### CSS Style

**Organization:**
```css
/* 1. Global styles and resets */
body { }

/* 2. Layout components */
.navbar { }
#grid-container { }

/* 3. Basic elements */
.node { }
button { }

/* 4. State classes */
.node.start { }
.node.visited { }

/* 5. Animations at the end */
@keyframes ageColor { }
```

**Naming:**
```css
/* Use BEM-like naming for clarity */
.navbar { }
.navbar__button { }
.navbar__button--reset { }

/* Or simple semantic names */
.btn-reset { }
.node.path { }
```

## 🧪 Testing Guidelines

### Manual Testing Checklist

Before submitting a PR, test these scenarios:

**Basic Functionality:**
- [ ] Place start node
- [ ] Place end node
- [ ] Draw walls by clicking
- [ ] Draw walls by dragging
- [ ] Remove walls by clicking
- [ ] Run each algorithm (DFS, BFS, Dijkstra)
- [ ] Reset button clears everything

**Edge Cases:**
- [ ] No path exists (start completely surrounded by walls)
- [ ] Direct path (start and end are neighbors)
- [ ] Start and end are the same cell
- [ ] Empty grid (no walls)
- [ ] Grid completely filled with walls except start/end
- [ ] Algorithm runs before placing start/end (should show alert)

**Visual Checks:**
- [ ] Colors display correctly
- [ ] Animations are smooth
- [ ] Path highlights correctly
- [ ] No visual glitches during execution
- [ ] Buttons have hover effects

**Browser Compatibility:**
- [ ] Chrome
- [ ] Firefox  
- [ ] Safari
- [ ] Edge

### Automated Testing (Future)

We plan to add:
- Unit tests for algorithms
- Integration tests for Eel communication
- Visual regression tests for UI

## 🌟 Feature Development Guidelines

### Adding a New Algorithm

1. **Implement the algorithm in `main.py`:**
   ```python
   @eel.expose
   def run_new_algorithm(start_list, end_list, wall_list):
       """
       Your algorithm description here.
       
       Algorithm: [Name]
       Time Complexity: O(?)
       Space Complexity: O(?)
       """
       # Convert input
       start_node = tuple(start_list)
       end_node = tuple(end_list)
       walls = {tuple(w) for w in wall_list}
       
       # Your algorithm logic
       # ...
       
       # Draw the path
       draw_path(parent_map, start_node, end_node)
   ```

2. **Add UI button in `index.html`:**
   ```html
   <button onclick="startAlgo('new_algo')">New Algorithm</button>
   ```

3. **Wire up the JavaScript in `index.html`:**
   ```javascript
   function startAlgo(algoType) {
       // ... existing code ...
       
       else if (algoType === 'new_algo') {
           eel.run_new_algorithm(startNode, endNode, walls);
       }
   }
   ```

4. **Update README.md** with:
   - Algorithm description
   - Time/space complexity
   - Use cases
   - Visualization pattern

### Adding UI Features

1. **Plan the feature:**
   - What problem does it solve?
   - How will users interact with it?
   - What should it look like?

2. **Implement in stages:**
   - HTML structure first
   - CSS styling second  
   - JavaScript logic last
   - Python integration if needed

3. **Keep consistent with existing design:**
   - Use the dark theme color palette
   - Follow existing animation patterns
   - Match button styles

## 📦 Project Structure Understanding

```
pathfinding-visualizer/
│
├── main.py                      # Backend (Python + Eel)
│   ├── Algorithm implementations
│   ├── Grid processing
│   └── Eel exposed functions
│
└── web/                         # Frontend (HTML/CSS/JS)
    ├── index.html              # UI structure + interaction logic
    │   ├── Grid creation
    │   ├── Event handlers
    │   └── Eel.js integration
    │
    └── style.css               # Styling + animations
        ├── Dark theme colors
        ├── Grid layout
        └── Keyframe animations
```

## 🔍 Common Issues and Solutions

### Issue: Changes to Python don't appear
**Solution:** Restart `main.py` - Eel needs to be restarted to pick up Python changes

### Issue: Changes to HTML/CSS don't appear  
**Solution:** Hard refresh the browser (Ctrl+Shift+R or Cmd+Shift+R)

### Issue: "eel.js not found" error
**Solution:** Ensure `eel.init('web')` points to the correct directory

### Issue: Grid not displaying
**Solution:** Check browser console for JavaScript errors, verify `web/` directory exists

### Issue: Algorithm runs but nothing happens
**Solution:** Ensure `eel.expose(update_node_color)` is before the function definition

## 🎓 Learning Resources

If you're new to the technologies used:

**Python:**
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/)

**JavaScript:**
- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [JavaScript.info](https://javascript.info/)

**Eel:**
- [Eel Documentation](https://github.com/ChrisKnott/Eel)

**Pathfinding Algorithms:**
- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/books/introduction-algorithms)
- [Pathfinding Algorithms Visualization](https://qiao.github.io/PathFinding.js/visual/)

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion  
- **Email**: your.email@example.com for direct contact

## 🏆 Recognition

Contributors will be recognized in:
- README.md acknowledgments section
- GitHub contributors graph
- Release notes for their contributions

Thank you for contributing to making pathfinding algorithms more accessible and understandable!

---

**Questions?** Don't hesitate to ask! We're here to help. 😊
