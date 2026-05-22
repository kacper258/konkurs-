import random
from models import Coordinates, Vehicle, World
from engine import SimulationEngine

def test_basic_movement():
    # Ustawiamy ziarno, aby uniknąć losowości w testach
    random.seed(42)

    world = World(width=100, height=100)
    start_coords = Coordinates(0, 0)
    vehicle = Vehicle(name="Test", position=start_coords, angle=0, fuel=100, max_fuel=150)
    target_coords = Coordinates(50, 50)

    engine = SimulationEngine(vehicle=vehicle, world=world, target_coords=target_coords)

    # Pierwszy ruch
    engine.process_turn("M", 10)
    # Sprawdzamy czy nie wystąpiło losowe zdarzenie zmieniające kąt
    # Przy seed(42) sprawdzimy co się dzieje.

    assert vehicle.position.x == 10.0
    assert vehicle.position.y == 0.0

    # Drugi ruch - obrót
    engine.process_turn("O", 45)
    assert vehicle.angle == 45.0

    print("Basic tests passed with seed!")

if __name__ == "__main__":
    test_basic_movement()
