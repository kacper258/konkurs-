import random
import constants
from world import World, Coordinates
from rover import Rover
from typing import List, Tuple

class EventManager:
    """Zarządza elementami świata i zdarzeniami losowymi."""

    @staticmethod
    def generate_world_elements(world: World, num_elements: int = constants.NUM_WORLD_ELEMENTS):
        """Generuje losowe elementy na mapie (paliwo, przeszkody, skróty)."""
        types = [constants.TYPE_FUEL, constants.TYPE_OBSTACLE, constants.TYPE_SHORTCUT]
        half_w = int(world.width / 2)
        half_h = int(world.height / 2)

        count = 0
        while count < num_elements:
            rx = random.randint(-half_w + 10, half_w - 10)
            ry = random.randint(-half_h + 10, half_h - 10)
            # Pomijamy środek mapy (okolice startu)
            if abs(rx) > 15 or abs(ry) > 15:
                world.add_element(rx, ry, random.choice(types))
                count += 1

    @staticmethod
    def trigger_random_event(rover: Rover) -> str:
        """Losuje i aplikuje zdarzenie środowiskowe."""
        events = [
            ("🌪️ Burza magnetyczna! Tracisz orientację (losowa zmiana kąta).", "BURZA"),
            ("☀️ Piękna pogoda! Zoptymalizowano zużycie zasobów (+10 paliwa).", "POGODA")
        ]
        ev_text, ev_type = random.choice(events)

        if ev_type == "BURZA":
            rover.angle = random.randint(0, 359)
        elif ev_type == "POGODA":
            rover.add_fuel(constants.WEATHER_BONUS_VALUE)

        return f"[LOSOWE] {ev_text}"

    @staticmethod
    def handle_interaction(rover: Rover, world: World) -> List[str]:
        """Sprawdza i obsługuje interakcje łazika z elementami świata."""
        journal_entries = []
        px, py = int(rover.position.x), int(rover.position.y)

        result = world.get_element_at(px, py)
        if result:
            pos, elem = result
            if elem == constants.TYPE_FUEL:
                rover.add_fuel(constants.FUEL_BONUS_VALUE)
                journal_entries.append(f"⛽ Znaleziono zbiornik z paliwem! Przywrócono +{constants.FUEL_BONUS_VALUE} pkt.")
            elif elem == constants.TYPE_OBSTACLE:
                rover.consume_fuel(constants.OBSTACLE_PENALTY_VALUE)
                journal_entries.append(f"💥 Pojazd wjechał w trudny teren. Strata -{constants.OBSTACLE_PENALTY_VALUE} pkt paliwa.")
            elif elem == constants.TYPE_SHORTCUT:
                rover.move(constants.SHORTCUT_MOVE_DISTANCE)
                journal_entries.append(f"🌀 Znaleziono bezpieczny skrót! Bezpieczne przyspieszenie o +{constants.SHORTCUT_MOVE_DISTANCE} jednostek.")

        return journal_entries
