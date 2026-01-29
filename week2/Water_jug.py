import heapq   # Used for priority queue (min-heap)


# Heuristic function:
# Estimates how close the current state is to the goal
def heuristic(x, y, goal):
    # Minimum difference between jug water and goal
    return min(abs(x - goal), abs(y - goal))


def water_jug_a_star(cap1, cap2, goal):
    # Initial state: both jugs are empty
    start = (0, 0)

    # Priority queue stores tuples:
    # (f = g + h, g = cost so far, current_state, path_taken)
    pq = []
    heapq.heappush(pq, (0, 0, start, []))

    # Set to keep track of visited states
    visited = set()

    # A* Search Loop
    while pq:
        # Pop the state with the lowest f value
        f, g, (x, y), path = heapq.heappop(pq)

        # Goal test: if any jug has the required amount
        if x == goal or y == goal:
            return path

        # Skip already visited states
        if (x, y) in visited:
            continue
        visited.add((x, y))

        # List to store possible next states and actions
        successors = []

        # 1. Fill Jug 1 completely
        successors.append(((cap1, y), "Fill Jug 1 completely"))

        # 2. Fill Jug 2 completely
        successors.append(((x, cap2), "Fill Jug 2 completely"))

        # 3. Empty Jug 1
        successors.append(((0, y), "Empty Jug 1"))

        # 4. Empty Jug 2
        successors.append(((x, 0), "Empty Jug 2"))

        # 5. Pour water from Jug 1 into Jug 2
        t = min(x, cap2 - y)   # Amount transferred
        successors.append(((x - t, y + t), "Pour Jug 1 into Jug 2"))

        # 6. Pour water from Jug 2 into Jug 1
        t = min(y, cap1 - x)   # Amount transferred
        successors.append(((x + t, y - t), "Pour Jug 2 into Jug 1"))

        # Add all valid successor states to the priority queue
        for (nx, ny), action in successors:
            if (nx, ny) not in visited:
                h = heuristic(nx, ny, goal)   # Heuristic value
                heapq.heappush(
                    pq,
                    (g + 1 + h,           # f = g + h
                     g + 1,               # Increment cost
                     (nx, ny),            # New state
                     path + [(action, (nx, ny))])  # Path update
                )

    # If no solution is found
    return None


# ---------------- DRIVER CODE ----------------

# Capacities of jugs
cap1 = 4
cap2 = 3

# Goal amount of water
goal = 2

# Call A* algorithm
solution = water_jug_a_star(cap1, cap2, goal)

# Print the solution steps
if solution:
    print("Solution Steps:\n")
    for i, (action, state) in enumerate(solution, 1):
        print(f"Step {i}: {action} → State {state}")
else:
    print("No solution found")
