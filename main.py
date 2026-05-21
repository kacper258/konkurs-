import os
import random
import constants
from world import World, Coordinates
from rover import Rover
from events import EventManager
from turtle_view import TurtleView

def clear_console():
    """Czyści konsolę w zależności od systemu operacyjnego."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_validated_input(prompt, default_value, value_type=float):
    """Pobiera i waliduje dane wejściowe od użytkownika."""
    user_input = input(prompt).strip()
    if not user_input:
        print(f"-> Użyto wartości domyślnej: {default_value}")
        return default_value
    try:
        value = value_type(user_input)
        return value
    except ValueError:
        print(f"❌ Niepoprawny typ danych. Zastosowano wartość bezpieczną: {default_value}")
        return default_value

def display_status(rover, target_coords, step_counter, journal):
    """Wyświetla aktualny stan symulacji w konsoli."""
    clear_console()
    print("================================================")
    print(f"🚀 Łazik: {rover.name} | Krok: {step_counter}/{constants.MAX_STEPS}")
    print("------------------------------------------------")
    print(f"📍 Pozycja: X = {rover.position.x:.2f}, Y = {rover.position.y:.2f}")
    print(f"🧭 Kąt zwrotu: {rover.angle:.1f}°")
    print(f"🔋 Stan paliwa: {rover.fuel:.2f} pkt")
    print(f"🎯 Cel wyprawy: X = {target_coords.x}, Y = {target_coords.y}")
    print("------------------------------------------------")

    if journal:
        print("📝 Ostatnie wydarzenia:")
        for entry in journal:
            print(f" - {entry}")
        print("------------------------------------------------")

    print("[M] - Ruch naprzód")
    print("[O] - Obrót pojazdu")
    print("[Q] - Przerwanie symulacji")

def start_simulation(view):
    """Główna logika pojedynczej symulacji."""
    clear_console()
    print("================================================")
    print("   SYMULATOR WYPRAWY PO DWUWYMIAROWYM ŚWIECIE   ")
    print("================================================\n")

    # Pobieranie parametrów
    name = input(f"Podaj nazwę łazika (domyślnie: '{constants.DEFAULT_EXPEDITION_NAME}'): ").strip()
    if not name:
        name = constants.DEFAULT_EXPEDITION_NAME

    start_x = get_validated_input(f"Pozycja startowa X (domyślnie {constants.DEFAULT_START_X}): ", constants.DEFAULT_START_X)
    start_y = get_validated_input(f"Pozycja startowa Y (domyślnie {constants.DEFAULT_START_Y}): ", constants.DEFAULT_START_Y)
    start_angle = get_validated_input(f"Kąt startowy (domyślnie {constants.DEFAULT_START_ANGLE}): ", constants.DEFAULT_START_ANGLE) % 360
    initial_fuel = get_validated_input(f"Początkowe paliwo (domyślnie {constants.DEFAULT_INITIAL_FUEL}): ", constants.DEFAULT_INITIAL_FUEL)

    # Inicjalizacja obiektów
    world = World(width=constants.WORLD_WIDTH, height=constants.WORLD_HEIGHT)
    rover = Rover(name=name, position=Coordinates(start_x, start_y), angle=start_angle, fuel=initial_fuel, max_fuel=initial_fuel * 1.5)

    # Cel wyprawy
    target_x = round(random.uniform(-world.width / 2 + 20, world.width / 2 - 20), 2)
    target_y = round(random.uniform(-world.height / 2 + 20, world.height / 2 - 20), 2)
    target_coords = Coordinates(target_x, target_y)

    # Przygotowanie świata i wizualizacji
    EventManager.generate_world_elements(world)
    view.setup_world(world.width, world.height)
    view.set_initial_position(rover.position, rover.angle)

    step_counter = 0
    journal = ["Rozpoczęto misję."]
    game_over = False
    reason = ""
    success = False

    # Pętla główna symulacji
    while not game_over:
        display_status(rover, target_coords, step_counter, journal)

        choice = input("\nWybierz akcję [M/O/Q]: ").strip().upper()
        journal = []

        if choice == 'Q':
            game_over = True
            reason = "Symulacja przerwana przez użytkownika."
            break
        elif choice == 'M':
            dist = get_validated_input("Podaj odległość (domyślnie 15): ", 15.0)

            new_pos = rover.position.move_by_angle(rover.angle, dist)
            if world.is_out_of_bounds(new_pos):
                journal.append("⚠️ Próba wyjścia poza granice świata! Zatrzymano łazik.")
                rover.consume_fuel(constants.OUT_OF_BOUNDS_PENALTY)
            else:
                rover.move(dist)
                journal.append(f"Przesunięto łazik o {dist} jednostek.")
        elif choice == 'O':
            deg = get_validated_input("Podaj kąt obrotu (np. -45 lub 90): ", 45.0)
            rover.rotate(deg)
            journal.append(f"Obrócono łazik o {deg}°.")
        else:
            journal.append("Oczekiwanie... (brak akcji)")

        # Koszt tury i zdarzenia
        step_counter += 1
        rover.consume_fuel(constants.TURN_BASE_COST)

        # Interakcje i zdarzenia losowe
        journal.extend(EventManager.handle_interaction(rover, world))
        if random.random() < constants.RANDOM_EVENT_CHANCE:
            journal.append(EventManager.trigger_random_event(rover))

        # Aktualizacja wizualizacji
        view.update_rover(rover.position, rover.angle)

        # Warunki zakończenia
        dist_to_target = rover.position.distance_to(target_coords)
        if dist_to_target <= constants.TARGET_RADIUS:
            game_over = True
            success = True
            reason = "Sukces! Cel wyprawy został osiągnięty!"
        elif rover.is_out_of_fuel():
            game_over = True
            reason = "Porażka! Skończyło się paliwo."
        elif step_counter >= constants.MAX_STEPS:
            game_over = True
            reason = "Porażka! Przekroczono limit kroków."

    # Raport końcowy
    clear_console()
    print("================================================")
    print("               RAPORT KOŃCOWY                   ")
    print("================================================")
    print(f"Status: {reason}")
    print(f"Wynik:  {'SUKCES 🎉' if success else 'PORAŻKA ❌'}")
    print("------------------------------------------------")
    print(f"• Łazik:                {rover.name}")
    print(f"• Pozycja końcowa:      X = {rover.position.x:.2f}, Y = {rover.position.y:.2f}")
    print(f"• Wykonane kroki:       {step_counter}")
    print(f"• Pozostałe paliwo:     {max(0, rover.fuel):.2f} pkt")
    print("================================================")

if __name__ == "__main__":
    # Jeden widok dla całego cyklu życia programu (możliwość restartu symulacji)
    main_view = TurtleView()
    try:
        while True:
            start_simulation(main_view)
            retry = input("\nCzy chcesz uruchomić nową misję? [T/N]: ").strip().upper()
            if retry != 'T':
                print("Dziękujemy za skorzystanie z symulatora.")
                break
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")
    finally:
        pass
