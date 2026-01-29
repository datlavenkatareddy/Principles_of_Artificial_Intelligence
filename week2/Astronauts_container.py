import heapq

# Heuristic: how far container X is from the goal
def heuristic(state, goal):
    x, y = state
    return abs(x - goal)


def a_star_water_measure(cap_x, cap_y, goal):
    start_state = (0, 0)

    # Priority Queue elements:
    # (f = g + h, g = cost, state, path)
    pq = []
    heapq.heappush(pq, (heuristic(start_state, goal), 0, start_state, []))

    visited = set()

    while pq:
        f, g, (x, y), path = heapq.heappop(pq)

        # Goal condition: exactly 6L in container X
        if x == goal:
            return path + [("Goal Achieved", (x, y))]

        if (x, y) in visited:
            continue
        visited.add((x, y))

        # All possible astronaut actions
        actions = []

        # Fill container X
        actions.append(("Fill Container X", (cap_x, y)))

        # Fill container Y
        actions.append(("Fill Container Y", (x, cap_y)))

        # Empty container X
        actions.append(("Empty Container X", (0, y)))

        # Empty container Y
        actions.append(("Empty Container Y", (x, 0)))

        # Pour X → Y
        transfer = min(x, cap_y - y)
        actions.append(("Pour X into Y", (x - transfer, y + transfer)))

        # Pour Y → X
        transfer = min(y, cap_x - x)
        actions.append(("Pour Y into X", (x + transfer, y - transfer)))

        # Explore next states
        for action, next_state in actions:
            if next_state not in visited:
                new_g = g + 1
                new_f = new_g + heuristic(next_state, goal)
                heapq.heappush(
                    pq,
                    (new_f, new_g, next_state, path + [(action, next_state)])
                )

    return None


# -------- DRIVER CODE --------
cap_x = 7
cap_y = 4
goal = 6

solution = a_star_water_measure(cap_x, cap_y, goal)

if solution:
    print("🚀 Steps followed by Astronauts:\n")
    for i, (action, state) in enumerate(solution, 1):
        print(f"Step {i}: {action} → State {state}")
else:
    print("No solution found")
