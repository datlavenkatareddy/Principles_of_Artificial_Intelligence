from collections import deque

# Generate all possible next states for 3 jugs
def get_next_states(state, caps):
    x, y, z = state
    cap_x, cap_y, cap_z = caps
    states = []

    # Fill jugs
    states.append((cap_x, y, z))
    states.append((x, cap_y, z))
    states.append((x, y, cap_z))

    # Empty jugs
    states.append((0, y, z))
    states.append((x, 0, z))
    states.append((x, y, 0))

    # Pour X -> Y
    pour = min(x, cap_y - y)
    states.append((x - pour, y + pour, z))

    # Pour X -> Z
    pour = min(x, cap_z - z)
    states.append((x - pour, y, z + pour))

    # Pour Y -> X
    pour = min(y, cap_x - x)
    states.append((x + pour, y - pour, z))

    # Pour Y -> Z
    pour = min(y, cap_z - z)
    states.append((x, y - pour, z + pour))

    # Pour Z -> X
    pour = min(z, cap_x - x)
    states.append((x + pour, y, z - pour))

    # Pour Z -> Y
    pour = min(z, cap_y - y)
    states.append((x, y + pour, z - pour))

    return states

# -------- BFS (A* with h = 0) --------
def bfs(caps, target):
    start = (0, 0, 0)
    queue = deque([(start, [])])
    visited = set([start])

    while queue:
        state, path = queue.popleft()

        if target in state:
            return path + [state]

        for next_state in get_next_states(state, caps):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [state]))

    return None

# -------- DFS --------
def dfs(caps, target, max_depth=30):
    start = (0, 0, 0)
    stack = [(start, [], 0)]
    visited = set()

    while stack:
        state, path, depth = stack.pop()

        if target in state:
            return path + [state]

        if depth >= max_depth:
            continue

        visited.add(state)

        for next_state in get_next_states(state, caps):
            if next_state not in visited:
                stack.append((next_state, path + [state], depth + 1))

    return None

# -------- MAIN --------
if __name__ == "__main__":
    capacities = (8, 5, 3)   # Jug capacities
    target = 4              # Desired amount

    print("BFS Solution (A* without heuristic):")
    bfs_solution = bfs(capacities, target)
    for s in bfs_solution:
        print(s)

    print("\nDFS Solution:")
    dfs_solution = dfs(capacities, target)
    for s in dfs_solution:
        print(s)
