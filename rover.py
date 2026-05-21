from dataclasses import dataclass
from world import Coordinates
import constants

@dataclass
class Rover:
    """Klasa reprezentująca łazik (dawniej Vehicle)."""
    name: str
    position: Coordinates
    angle: float
    fuel: float
    max_fuel: float

    def move(self, distance: float):
        """Przemieszcza łazik o zadaną odległość."""
        self.position = self.position.move_by_angle(self.angle, distance)
        # Zużycie paliwa zależne od dystansu
        self.fuel -= round(distance * constants.MOVE_COST_PER_UNIT, 2)

    def rotate(self, degrees: float):
        """Obraca łazik o zadany kąt."""
        self.angle = (self.angle + degrees) % 360

    def consume_fuel(self, amount: float):
        """Zmniejsza stan paliwa o określoną wartość."""
        self.fuel -= amount

    def add_fuel(self, amount: float):
        """Dodaje paliwo, nie przekraczając limitu maksymalnego."""
        self.fuel = min(self.max_fuel, self.fuel + amount)

    def is_out_of_fuel(self) -> bool:
        """Sprawdza, czy zabrakło paliwa."""
        return self.fuel <= 0
