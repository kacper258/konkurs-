import constants
from world import Coordinates, World
from rover import Rover

def test_basic_movement():
    world = World(width=100, height=100)
    start_coords = Coordinates(0, 0)
    rover = Rover(name="Test", position=start_coords, angle=0, fuel=100, max_fuel=150)

    # Test movement forward
    dist = 10
    rover.move(dist)
    assert rover.position.x == 10.0
    assert rover.position.y == 0.0
    # Fuel: 100 - (10 * 0.5) = 95.0
    assert rover.fuel == 95.0

    # Test rotation
    rover.rotate(90)
    assert rover.angle == 90.0

    print("Podstawowe testy jednostkowe zaliczone!")

def test_out_of_bounds():
    world = World(width=100, height=100)
    pos_inside = Coordinates(10, 10)
    pos_outside = Coordinates(60, 0)

    assert world.is_out_of_bounds(pos_inside) == False
    assert world.is_out_of_bounds(pos_outside) == True
    print("Test granic świata zaliczony!")

if __name__ == "__main__":
    test_basic_movement()
    test_out_of_bounds()
