import os
import random
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

def start_simulation(view: SimulationView):
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
    target_x = random.uniform(-world.width / 2 + 20, world.width / 2 - 20)
    target_y = random.uniform(-world.height / 2 + 20, world.height / 2 - 20)
    target_coords = Coordinates(round(target_x, 2), round(target_y, 2))

    # Inicjalizacja silnika oraz widoku graficznego
    engine = SimulationEngine(vehicle=vehicle, world=world, target_coords=target_coords)
    view.reset_view()
    view.setup_initial_position(vehicle.position, vehicle.angle)
    view.draw_target(target_coords)
    view.draw_elements(world.elements)
    view.update_hud(vehicle.name, vehicle.fuel, vehicle.max_fuel, engine.step_counter, vehicle.total_distance)

    # Główna pętla symulacji (Event Loop)
    while not engine.game_over:
        clear_console()
        dist_to_target = engine.get_distance_to_target()
        avg_consumption = vehicle.total_fuel_consumed / vehicle.total_distance if vehicle.total_distance > 0 else 0
        
        print(f"🚀 Wyprawa: {vehicle.name} | Krok: {engine.step_counter}")
        print("------------------------------------------------")
        print(f"📍 Pozycja: X = {vehicle.position.x:.2f}, Y = {vehicle.position.y:.2f}")
        print(f"🧭 Kąt zwrotu: {vehicle.angle}°")
        print(f"🔋 Stan paliwa: {vehicle.fuel:.2f} / {vehicle.max_fuel:.1f} pkt")
        print(f"🛣️  Dystans: {vehicle.total_distance:.1f} j. | Śr. zużycie: {avg_consumption:.2f} pkt/j.")
        print(f"🎯 Cel: X = {target_coords.x}, Y = {target_coords.y} | 📏 Odległość: {dist_to_target:.2f} j.")
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
        view.update_hud(vehicle.name, vehicle.fuel, vehicle.max_fuel, engine.step_counter, vehicle.total_distance)

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
    print(f"• Całkowity dystans:     {vehicle.total_distance:.1f} j.")
    print(f"• Pozostałe zasoby:      {vehicle.fuel:.2f} pkt")
    avg_final = vehicle.total_fuel_consumed / vehicle.total_distance if vehicle.total_distance > 0 else 0
    print(f"• Średnie zużycie:       {avg_final:.2f} pkt/j.")
    print("================================================")

if __name__ == "__main__":
    # Inicjalizacja widoku raz, aby uniknąć powielania okien/żółwi
    view = SimulationView(world_width=300.0, world_height=300.0)
    
    while True:
        start_simulation(view)
        retry = input("\nCzy chcesz uruchomić nową symulację? [T/N]: ").strip().upper()
        if retry != 'T':
            print("Dziękujemy za skorzystanie z symulatora.")
            break
