from models import Coordinates, Vehicle, World
from engine import SimulationEngine

def test_basic_movement():
    world = World(width=100, height=100)
    start_coords = Coordinates(0, 0)
    vehicle = Vehicle(name="Test", position=start_coords, angle=0, fuel=100, max_fuel=150)
    target_coords = Coordinates(50, 50)

    engine = SimulationEngine(vehicle=vehicle, world=world, target_coords=target_coords)

    # Test movement forward
    engine.process_turn("M", 10)
    assert vehicle.position.x == 10.0
    assert vehicle.position.y == 0.0
    # Fuel: 100 - 2 (turn cost) - 5 (10 * 0.5) = 93.0
    assert vehicle.fuel == 93.0

    # Test rotation
    engine.process_turn("O", 90)
    assert vehicle.angle == 90.0
    # Fuel: 93 - 2 = 91
    assert vehicle.fuel == 91.0

    print("Basic tests passed!")

if __name__ == "__main__":
    test_basic_movement()
