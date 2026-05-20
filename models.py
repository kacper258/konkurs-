import math
from dataclasses import dataclass, field
from typing import Dict, Tuple

@dataclass(frozen=True)
class Coordinates:
    x: float
    y: float

    def move_by_angle(self, angle_degrees: float, distance: float) -> 'Coordinates':
        # Konwersja kąta na radiany i wyznaczenie przesunięcia wektorowego
        radians = math.radians(angle_degrees)
        new_x = self.x + distance * math.cos(radians)
        new_y = self.y + distance * math.sin(radians)
        return Coordinates(round(new_x, 2), round(new_y, 2))

@dataclass
class Vehicle:
    name: str
    position: Coordinates
    angle: float
    fuel: float
    max_fuel: float

@dataclass
class World:
    width: float
    height: float
    # Rzadka macierz (słownik) przechowująca elementy świata, gdzie klucz to (int(x), int(y))
    elements: Dict[Tuple[int, int], str] = field(default_factory=dict)

    def is_out_of_bounds(self, coords: Coordinates) -> bool:
        half_w = self.width / 2
        half_h = self.height / 2
        return not (-half_w <= coords.x <= half_w and -half_h <= coords.y <= half_h)

    def add_element(self, x: int, y: int, element_type: str):
        self.elements[(x, y)] = element_type
