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


import turtle

from models import Coordinates


class SimulationView:

    def __init__(self, world_width: float, world_height: float):
        # Inicjalizacja okna graficznego Turtle

        self.screen = turtle.Screen()

        self.screen.title("Symulator Wyprawy")

        self.screen.setup(width=700, height=700)

        # Skalowanie okna do rozmiarów zdefiniowanego świata z marginesem

        margin = 50

        self.screen.setworldcoordinates(

            -world_width / 2 - margin, -world_height / 2 - margin,

            world_width / 2 + margin, world_height / 2 + margin

        )

        # Rysowanie granic świata

        self.bounds_drawer = turtle.Turtle()

        self.bounds_drawer.speed(0)

        self.bounds_drawer.hideturtle()

        self._draw_bounds(world_width, world_height)

        # Żółw reprezentujący pojazd i rysujący ścieżkę

        self.vehicle_turtle = turtle.Turtle()

        self.vehicle_turtle.shape("arrow")

        self.vehicle_turtle.color("blue")

        self.vehicle_turtle.pensize(2)

        self.vehicle_turtle.speed(3)

    def _draw_bounds(self, w: float, h: float):
        self.bounds_drawer.penup()

        self.bounds_drawer.goto(-w / 2, -h / 2)

        self.bounds_drawer.pendown()

        self.bounds_drawer.color("red")

        for _ in range(2):
            self.bounds_drawer.forward(w)

            self.bounds_drawer.left(90)

            self.bounds_drawer.forward(h)

            self.bounds_drawer.left(90)

    def setup_initial_position(self, coords: Coordinates, angle: float):
        self.vehicle_turtle.penup()

        self.vehicle_turtle.goto(coords.x, coords.y)

        self.vehicle_turtle.setheading(angle)

        self.vehicle_turtle.pendown()

    def update_position(self, coords: Coordinates, angle: float):
        self.vehicle_turtle.setheading(angle)

        self.vehicle_turtle.goto(coords.x, coords.y)

    def clear_window(self):
        self.vehicle_turtle.clear()

        self.bounds_drawer.clear()

        # Nie zamykamy okna, resetujemy stan do ponownego rysowania


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

        # Warunek 1: Dotarcie do celu (odległość euklidesowa < 5 jednostek)

        dist_to_target = math.sqrt(

            (self.vehicle.position.x - self.target.x) ** 2 +

            (self.vehicle.position.y - self.target.y) ** 2

        )

        if dist_to_target <= 6.0:
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


import os

from models import Coordinates, Vehicle, World

from engine import SimulationEngine

from view import SimulationView


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_validated_input(prompt, default_value, value_type=float):
    user_input = input(prompt)

    if not user_input.strip():
        print(f"-> Użyto wartości domyślnej: {default_value}")

        return default_value

    try:

        return value_type(user_input)

    except ValueError:

        print(f"❌ Niepoprawny typ danych. Zastosowano wartość bezpieczną: {default_value}")

        return default_value


def start_simulation():
    clear_console()

    print("================================================")

    print("   SYMULATOR WYPRAWY PO DWUWYMIAROWYM ŚWIECIE   ")

    print("================================================\n")

    # Pobieranie parametrów początkowych z walidacją i wartościami domyślnymi

    expedition_name = input("Podaj nazwę wyprawy (domyślnie: 'Rover-1'): ").strip()

    if not expedition_name:
        expedition_name = "Rover-1"

    start_x = get_validated_input("Pozycja startowa X (od -100 do 100, domyślnie 0): ", 0.0)

    start_y = get_validated_input("Pozycja startowa Y (od -100 do 100, domyślnie 0): ", 0.0)

    start_angle = get_validated_input("Kąt startowy w stopniach (0-359, domyślnie 90): ", 90.0) % 360

    initial_fuel = get_validated_input("Początkowy stan paliwa/energii (domyślnie 100): ", 100.0)

    # Inicjalizacja obiektów dziedziny (World, Vehicle)

    world = World(width=300.0, height=300.0)

    start_coords = Coordinates(start_x, start_y)

    vehicle = Vehicle(name=expedition_name, position=start_coords, angle=start_angle, fuel=initial_fuel,
                      max_fuel=initial_fuel * 1.5)

    # Cel wyprawy umieszczony losowo na mapie

    target_coords = Coordinates(100.0, 100.0)

    # Inicjalizacja silnika oraz widoku graficznego

    engine = SimulationEngine(vehicle=vehicle, world=world, target_coords=target_coords)

    view = SimulationView(world_width=world.width, world_height=world.height)

    view.setup_initial_position(vehicle.position, vehicle.angle)

    # Główna pętla symulacji (Event Loop)

    while not engine.game_over:

        clear_console()

        print(f"🚀 Wyprawa: {vehicle.name} | Krok: {engine.step_counter}")

        print("------------------------------------------------")

        print(f"📍 Pozycja: X = {vehicle.position.x:.2f}, Y = {vehicle.position.y:.2f}")

        print(f"🧭 Kąt zwrotu: {vehicle.angle}°")

        print(f"🔋 Stan paliwa: {vehicle.fuel:.2f} pkt")

        print(f"🎯 Cel wyprawy znajduje się w okolicach: X = {target_coords.x}, Y = {target_coords.y}")

        print("------------------------------------------------")

        if engine.journal:

            print("📝 Ostatnie wydarzenia:")

            for entry in engine.journal:
                print(f" - {entry}")

            print("------------------------------------------------")

        print("[M] - Ruch naprzód o zadaną odległość")

        print("[O] - Obrót pojazdu (w lewo dodatnie, w prawo ujemne)")

        print("[Q] - Przerwanie symulacji")

        choice = input("\nWybierz akcję [M/O/Q]: ").strip().upper()

        if choice == 'Q':

            engine.game_over = True

            engine.reason = "Symulacja przerwana na żądanie użytkownika."

            break

        elif choice == 'M':

            dist = get_validated_input("Podaj odległość (krok ruchu, domyślnie 15): ", 15.0)

            engine.process_turn(action="M", modifier_value=dist)

        elif choice == 'O':

            deg = get_validated_input("Podaj kąt zmiany kierunku w stopniach (np. -45 lub 90): ", 45.0)

            engine.process_turn(action="O", modifier_value=deg)

        else:

            # W przypadku błędnego wyboru tura mija bez akcji użytkownika

            engine.process_turn(action="WAIT", modifier_value=0)

        # Aktualizacja pozycji na ekranie Turtle

        view.update_position(vehicle.position, vehicle.angle)

    # Ekran podsumowania i raport końcowy

    clear_console()

    print("================================================")

    print("               RAPORT KOŃCOWY                   ")

    print("================================================")

    print(f"Status końcowy: {engine.reason}")

    print(f"Wynik wyprawy:  {'SUKCES 🎉' if engine.success else 'PORAŻKA ❌'}")

    print("------------------------------------------------")

    print(f"• Nazwa obiektu:         {vehicle.name}")

    print(f"• Początkowe współrzędne: X = {start_x}, Y = {start_y}")

    print(f"• Końcowe współrzędne:   X = {vehicle.position.x:.2f}, Y = {vehicle.position.y:.2f}")

    print(f"• Wykonane kroki/tury:   {engine.step_counter}")

    print(f"• Pozostałe zasoby:      {vehicle.fuel:.2f} pkt")

    print("================================================")

    # Obsługa ponownego uruchomienia programu

    retry = input("\nCzy chcesz uruchomić nową symulację? [T/N]: ").strip().upper()

    if retry == 'T':

        view.clear_window()

        start_simulation()

    else:

        print("Dziękujemy za skorzystanie z symulatora.")


if __name__ == "__main__":
    start_simulation()





