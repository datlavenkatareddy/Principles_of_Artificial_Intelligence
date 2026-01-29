import heapq

# Fuel properties
OCTANE_A = 87
OCTANE_B = 92
CAP_A = 7
CAP_B = 4
TARGET_OCTANE = 90


def compute_octane(a, b):
    """Calculate blended octane"""
    if a + b == 0:
        return 0
    return (a * OCTANE_A + b * OCTANE_B) / (a + b)


def heuristic(a, b):
    """Remaining octane mismatch"""
    return abs(TARGET_OCTANE - compute_octane(a, b))


def a_star_fuel_blending():
    start = (0, 0)

    # (f, g, state, path)
    pq = []
    heapq.heappush(pq, (heuristic(0, 0), 0, start, []))

    visited = set()

    while pq:
        f, g, (a, b), path = heapq.heappop(pq)

        current_octane = compute_octane(a, b)

        # Goal check (tolerance allowed)
        if abs(current_octane - TARGET_OCTANE) <= 0.01 and (a + b) > 0:
            return path + [("Goal Achieved", (a, b), current_octane)]

        if (a, b) in visited:
            continue
        visited.add((a, b))

        actions = []

        # Add fuel A (1 unit)
        if a < CAP_A:
            actions.append(("Add Fuel A", (a + 1, b)))

        # Add fuel B (1 unit)
        if b < CAP_B:
            actions.append(("Add Fuel B", (a, b + 1)))

        # Remove fuel A (1 unit)
        if a > 0:
            actions.append(("Remove Fuel A", (a - 1, b)))

        # Remove fuel B (1 unit)
        if b > 0:
            actions.append(("Remove Fuel B", (a, b - 1)))

        for action, (na, nb) in actions:
            if (na, nb) not in visited:
                new_g = g + 1
                new_f = new_g + heuristic(na, nb)
                heapq.heappush(
                    pq,
                    (new_f, new_g, (na, nb),
                     path + [(action, (na, nb), compute_octane(na, nb))])
                )

    return None


# -------- DRIVER CODE --------
solution = a_star_fuel_blending()

if solution:
    print("🚀 Fuel Blending Steps (A* Optimized):\n")
    for i, (action, state, octane) in enumerate(solution, 1):
        print(f"Step {i}: {action} → State {state}, Octane = {octane:.2f}")
else:
    print("No feasible blend found")
