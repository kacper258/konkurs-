import math
import random
from models import Vehicle, World, Coordinates

class SimulationEngine:
    def __init__(self, vehicle: Vehicle, world: World, target_coords: Coordinates):
        self.vehicle = vehicle
        self.world = world
        self.target = target_coords
        self.step_counter = 0
        self.journal = []
        self.game_over = False
        self.success = False
        self.reason = ""
        # Generowanie losowych elementów na mapie
        self._generate_world_elements()

    def _generate_world_elements(self):
        # Generowanie punktów z bonusem (paliwo) i przeszkodami
        types = ["PALIWO", "PRZESZKODA", "SKRÓT"]
        half_w = int(self.world.width / 2)
        half_h = int(self.world.height / 2)
        for _ in range(15):
            rx = random.randint(-half_w + 10, half_w - 10)
            ry = random.randint(-half_h + 10, half_h - 10)
            # Pomijamy pozycję startową pojazdu i cel
            if abs(rx) > 5 and abs(ry) > 5:
                self.world.add_element(rx, ry, random.choice(types))

    def process_turn(self, action: str, modifier_value: float):
        if self.game_over:
            return

        self.step_counter += 1
        self.journal.clear()
        # Koszt bazowy przetrwania tury
        self.vehicle.fuel -= 2

        if action == "M":  # Ruch naprzód
            distance = modifier_value
            new_pos = self.vehicle.position.move_by_angle(self.vehicle.angle, distance)
            if self.world.is_out_of_bounds(new_pos):
                self.journal.append("⚠️ Próba wyjścia poza granice świata! Pojazd zatrzymał się.")
                self.vehicle.fuel -= 5  # Kara za uderzenie w barierę
            else:
                self.vehicle.position = new_pos
                # Koszt paliwa zależny od przebytej drogi
                self.vehicle.fuel -= round(distance * 0.5, 2)
                self.journal.append(f"Pojazd przemieścił się o {distance} jednostek.")

        elif action == "O":  # Obrót (Zmiana kąta)
            self.vehicle.angle = (self.vehicle.angle + modifier_value) % 360
            self.journal.append(f"Zmieniono kierunek o {modifier_value}° (Aktualny kąt: {self.vehicle.angle}°).")

        # Sprawdzenie interakcji z elementami świata w bliskim sąsiedztwie
        self._check_world_interactions()

        # Generowanie losowych zdarzeń środowiskowych (15% szans)
        if random.random() < 0.15:
            self._trigger_random_event()

        # Sprawdzenie warunków zakończenia symulacji
        self._check_end_conditions()

    def _check_world_interactions(self):
        px, py = int(self.vehicle.position.x), int(self.vehicle.position.y)
        # Sprawdzamy promień wokół pojazdu z racji ciągłych współrzędnych
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                check_pos = (px + dx, py + dy)
                if check_pos in self.world.elements:
                    elem = self.world.elements.pop(check_pos)  # Konsumujemy element
                    if elem == "PALIWO":
                        self.vehicle.fuel = min(self.vehicle.max_fuel, self.vehicle.fuel + 30)
                        self.journal.append("⛽ Znaleziono zbiornik z paliwem! Przywrócono +30 pkt.")
                    elif elem == "PRZESZKODA":
                        self.vehicle.fuel -= 20
                        self.journal.append("💥 Pojazd wjechał w trudny teren. Strata -20 pkt paliwa.")
                    elif elem == "SKRÓT":
                        # Przesunięcie losowe do przodu
                        self.vehicle.position = self.vehicle.position.move_by_angle(self.vehicle.angle, 15)
                        self.journal.append("🌀 Znaleziono bezpieczny skrót! Bezpieczne przyspieszenie o +15 jednostek.")
                    return

    def _trigger_random_event(self):
        events = [
            ("🌪️ Burza magnetyczna! Tracisz orientację (losowa zmiana kąta).", "BURZA"),
            ("☀️ Piękna pogoda! Zoptymalizowano zużycie zasobów (+10 paliwa).", "POGODA")
        ]
        ev_text, ev_type = random.choice(events)
        self.journal.append(f"[LOSOWE] {ev_text}")
        if ev_type == "BURZA":
            self.vehicle.angle = random.randint(0, 359)
        elif ev_type == "POGODA":
            self.vehicle.fuel = min(self.vehicle.max_fuel, self.vehicle.fuel + 10)

    def _check_end_conditions(self):
        # Warunek 1: Dotarcie do celu (odległość euklidesowa <= 10 jednostek)
        dist_to_target = math.sqrt(
            (self.vehicle.position.x - self.target.x) ** 2 +
            (self.vehicle.position.y - self.target.y) ** 2
        )
        if dist_to_target <= 10.0:
            self.game_over = True
            self.success = True
            self.reason = "Sukces! Cel wyprawy został osiągnięty!"
            return

        # Warunek 2: Brak paliwa
        if self.vehicle.fuel <= 0:
            self.vehicle.fuel = 0
            self.game_over = True
            self.success = False
            self.reason = "Porażka! Skończyły się zasoby energii/paliwa."
            return

        # Warunek 3: Limit kroków symulacji (zabezpieczenie przed nieskończoną grą)
        if self.step_counter >= 50:
            self.game_over = True
            self.success = False
            self.reason = "Porażka! Czas wyprawy minął (osiągnięto limit 50 kroków)."
            return
