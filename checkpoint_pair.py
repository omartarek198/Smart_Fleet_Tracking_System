import math

def distance(
        a: tuple[float, float],
        b: tuple[float, float]
) -> float:
    x1, y1 = a
    x2, y2 = b
    dx, dy = x2 - x1, y2 - y1
    return math.sqrt(dx * dx + dy * dy)

def trigger_eta_between_checkpoints(
    bus_id: int,
    checkpoints: list[tuple[float, float]],
    actual_checkpoints_eta: list[float],
    notify,
):
    optimal_distances = []
    for i in range(0, len(checkpoints) - 1, 2):
        a = checkpoints[i]
        b = checkpoints[i + 1]
        optimal_distances.append(distance(a, b))

    for i, predicted, actual in zip(
        range(0, len(checkpoints)),
        optimal_distances,
        actual_checkpoints_eta
    ):
        if actual > predicted:
            notify({
                "bus_id": bus_id,
                "deviated_from": [checkpoints[i], checkpoints[i + 1]],
                "deviation": abs(actual - predicted),
            })

def handle_spec_eta_notification(
    specified_eta: int,
    bus_eta: int,
    notify, 
):
    if bus_eta < specified_eta:
        notify()

# trigger_eta_between_checkpoints(
#     bus_id=1,
#     checkpoints=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)],
#     actual_checkpoints_eta=[1.77, 1.55, 1.55],
#     notify=print
# )

