# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- True Dijkstra's algorithm with weighted cells
- A* (A-star) pathfinding algorithm
- Pause/Resume functionality
- Speed control slider
- Step-by-step execution mode
- Preset maze patterns
- Path statistics display (length, nodes visited)
- Export/Import maze configurations
- Mobile touch support

## [1.0.0] - 2026-01-28

### Added
- Initial release of Pathfinding Algorithm Visualizer
- Depth-First Search (DFS) implementation
- Breadth-First Search (BFS) implementation
- Pseudo-Dijkstra implementation (currently runs DFS)
- 20×20 interactive grid
- Real-time visualization with color-coded animations
- Mouse-based interaction:
  - Click to place start node
  - Click again to place end node
  - Click and drag to draw walls
  - Click walls to remove them
- Reset functionality
- Modern dark-themed UI with neon accents
- Smooth CSS animations:
  - Visited nodes "aging" effect (cyan → blue → purple)
  - Path highlighting with pulsing gold effect
  - Button hover effects with glow
- Documentation:
  - Comprehensive README
  - Architecture documentation
  - Algorithm deep dive
  - Contributing guidelines
  - Setup instructions
- Python backend using Eel framework
- Vanilla JavaScript frontend (no dependencies)
- MIT License

### Technical Details
- Grid representation: 20 rows × 20 columns (400 cells)
- Movement: 4-directional (up, down, left, right)
- Graph type: Unweighted, undirected
- Visualization speed: 20ms per node (DFS), 10ms per node (BFS)

### Known Limitations
- "Dijkstra" button actually runs DFS (not true Dijkstra's algorithm)
- No diagonal movement
- No weighted cells
- Single algorithm execution (must reset between runs)
- Desktop only (no mobile optimization)
- No path length display
- No execution statistics

## Version History Notes

### Version Numbering
- **Major version (X.0.0)**: Breaking changes, major new features
- **Minor version (0.X.0)**: New features, backward compatible
- **Patch version (0.0.X)**: Bug fixes, small improvements

### Release Types
- **[Unreleased]**: Features in development
- **[Version]**: Released versions with date

---

For a detailed list of changes in each version, see the [GitHub Releases](https://github.com/yourusername/pathfinding-visualizer/releases) page.
