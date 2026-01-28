import eel
import time
from collections import deque

# 1. Initialize the 'web' folder
eel.init('web')

# 2. Global Helper to Draw the Path
def draw_path(parent_map, start, end):
    curr = end
    path_found = False
    
    # Check if end is actually reachable
    if curr in parent_map:
        path_found = True
    path =[]    
    while curr in parent_map:
        curr = parent_map[curr]
        path.append(curr)
        if curr == start:
            print(path)
            break
        
        # Don't color the start node yellow
        if curr != start:
            eel.update_node_color(curr[0], curr[1], "path")
            eel.sleep(0.02) # Draw path quickly
    
# 3. EXISTING ALGORITHM (Your DFS/Stack Logic)
@eel.expose
def run_dijkstra(start_list, end_list, wall_list):
    # Data Conversion
    start_node = tuple(start_list)
    end_node = tuple(end_list)
    walls = {tuple(w) for w in wall_list}
    ROWS = 20 
    COLS = 20
    
    # Setup (Stack = DFS behavior)
    stack = [start_node]
    visited = set()
    parent_map = {} 

    print(f"Dijkstra(Stack) started. Start: {start_node}, End: {end_node}")

    while stack:
        current = stack.pop()
        
        # Target found?
        if current == end_node:
            print("Target found! Drawing path...")
            draw_path(parent_map, start_node, end_node)
            return

        if current in visited:
            continue
        
        visited.add(current)

        # Update Frontend
        if current != start_node and current != end_node:
            eel.update_node_color(current[0], current[1], "visited")
            eel.sleep(0.02)

        # Check Neighbors
        neighbors = [
            (current[0] - 1, current[1]), (current[0] + 1, current[1]), 
            (current[0], current[1] - 1), (current[0], current[1] + 1)
        ]

        for neighbor in neighbors:
            nr, nc = neighbor
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if neighbor in walls:
                    continue
                if neighbor not in visited:
                    stack.append(neighbor)
                    if neighbor not in parent_map:
                        parent_map[neighbor] = current

    print("Algorithm finished (Target not found)")


# 4. NEW ALGORITHM (BFS Logic)
@eel.expose
def run_bfs(start_list, end_list, wall_list):
    # Data Conversion
    start_node = tuple(start_list)
    end_node = tuple(end_list)
    walls = {tuple(w) for w in wall_list}
    ROWS = 20
    COLS = 20
    
    # Setup (Deque/Queue = BFS behavior)
    queue = deque([start_node])
    visited = {start_node}
    parent_map = {} 

    print(f"BFS started. Start: {start_node}, End: {end_node}")

    while queue:
        # .popleft() is the key difference! It makes it BFS (Breadth First)
        current = queue.popleft() 

        # Target found?
        if current == end_node:
            print("Target found! Drawing path...")
            draw_path(parent_map, start_node, end_node)
            return

        # Update Frontend
        if current != start_node and current != end_node:
            eel.update_node_color(current[0], current[1], "visited")
            eel.sleep(0.01) # Slightly faster for BFS

        # Check Neighbors
        neighbors = [
            (current[0] - 1, current[1]), (current[0] + 1, current[1]), 
            (current[0], current[1] - 1), (current[0], current[1] + 1)
        ]

        for neighbor in neighbors:
            nr, nc = neighbor
            # Bounds check
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                # Wall & Visited check
                if neighbor not in walls and neighbor not in visited:
                    visited.add(neighbor)
                    parent_map[neighbor] = current
                    queue.append(neighbor)
                    print(f"Enqueued: {neighbor}")

    print("BFS finished (Target not found)")

# ... (Keep your existing run_dijkstra and run_bfs functions) ...

@eel.expose
def run_dfs(start_list, end_list, wall_list):
    # Data Conversion
    start_node = tuple(start_list)
    end_node = tuple(end_list)
    walls = {tuple(w) for w in wall_list}
    ROWS = 20
    COLS = 20
    
    # --- SETUP FOR DFS ---
    # We use a simple LIST as a Stack (Last-In, First-Out)
    stack = [start_node]
    visited = set()
    parent_map = {} 

    print(f"DFS started. Start: {start_node}, End: {end_node}")

    while stack:
        # Pop from the END of the list (Stack behavior)
        current = stack.pop()

        if current == end_node:
            print("Target found via DFS! Drawing path...")
            draw_path(parent_map, start_node, end_node)
            return

        if current in visited:
            continue
        
        visited.add(current)

        # Update Frontend
        if current != start_node and current != end_node:
            eel.update_node_color(current[0], current[1], "visited")
            eel.sleep(0.02) # DFS can be fast, this slows it down to see

        # Check Neighbors
        # NOTE: Changing the order of these neighbors changes the "shape" of the DFS snake
        neighbors = [
            (current[0] - 1, current[1]), # Up
            (current[0] + 1, current[1]), # Down
            (current[0], current[1] - 1), # Left
            (current[0], current[1] + 1)  # Right
        ]

        for neighbor in neighbors:
            nr, nc = neighbor
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if neighbor not in walls and neighbor not in visited:
                    stack.append(neighbor)
                    if neighbor not in parent_map:
                        parent_map[neighbor] = current

    print("DFS finished (Target not found)")
# 5. Start the App
eel.start('index.html', size=(800, 700))