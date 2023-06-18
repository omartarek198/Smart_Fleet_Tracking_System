import math
import route_distance


def distance(a: tuple[float, float], b: tuple[float, float]):
    x1, y1 = a
    x2, y2 = b
    dx, dy = x2 - x1, y2 - y1
    return math.sqrt(dx * dx + dy * dy)


def trigger_eta_between_checkpoints(
    bus_id: int,
    checkpoints: list[tuple[float, float]],
    groundtruth_checkpoints_eta: list[float],
    notify,
):
    optimal_distances = []
    for i in range(1, len(checkpoints) - 1):
        lon1, lat1 = checkpoints[i - 1]
        lon2, lat2 = checkpoints[i]

        origin = f"{lon1},{lat1}"
        dest = f"{lon2},{lat2}"
        result = route_distance.calculate_route_distance(origin, dest)

        if result is not None:
            dist, estimated_eta = result
            optimal_distances.append(dist)


    for i, predicted, actual in zip(
        range(0, len(checkpoints)),
        optimal_distances,
        groundtruth_checkpoints_eta
    ):
        # TODO: check if driver is speeding or taking too long to 
        # reach checkpoint using the eta

        # check for deviation through the distance
        if actual > predicted:
            notify(
                {
                    "bus_id": bus_id,
                    "deviated_from": [checkpoints[i], checkpoints[i + 1]],
                    "predicted_eta": predicted,
                    "actual_eta": actual,
                    "deviation": abs(predicted - actual),
                }
            )
