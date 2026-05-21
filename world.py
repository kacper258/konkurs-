import math
from dataclasses import dataclass, field
from typing import Dict, Tuple, Optional

@dataclass(frozen=True)
class Coordinates:
    """Reprezentuje współrzędne X, Y na mapie."""
    x: float
    y: float

    def move_by_angle(self, angle_degrees: float, distance: float) -> 'Coordinates':
        """Oblicza nowe współrzędne na podstawie kąta i odległości."""
        radians = math.radians(angle_degrees)
        new_x = self.x + distance * math.cos(radians)
        new_y = self.y + distance * math.sin(radians)
        return Coordinates(round(new_x, 2), round(new_y, 2))

@dataclass
class World:
    """Reprezentuje świat symulacji, granice i elementy na mapie."""
    width: float
    height: float
    # Rzadka macierz (słownik) przechowująca elementy świata
    elements: Dict[Tuple[int, int], str] = field(default_factory=dict)

    def is_out_of_bounds(self, coords: Coordinates) -> bool:
        """Sprawdza, czy podane współrzędne znajdują się poza granicami świata."""
        half_w = self.width / 2
        half_h = self.height / 2
        return not (-half_w <= coords.x <= half_w and -half_h <= coords.y <= half_h)

    def add_element(self, x: int, y: int, element_type: str):
        """Dodaje element świata na określonych współrzędnych."""
        self.elements[(x, y)] = element_type

    def distance_to(self, other: 'Coordinates') -> float:
        """Oblicza odległość euklidesową do innego punktu."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def get_element_at(self, x: int, y: int, radius: int = 2) -> Optional[Tuple[Tuple[int, int], str]]:
        """Szuka elementu w bliskim sąsiedztwie podanych współrzędnych."""
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                check_pos = (x + dx, y + dy)
                if check_pos in self.elements:
                    return check_pos, self.elements.pop(check_pos)
        return None
