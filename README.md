# 🚀 Symulator Wyprawy 2D

Profesjonalny symulator wyprawy pojazdu po dwuwymiarowym świecie, napędzany silnikiem logicznym w Pythonie z wizualizacją graficzną w module `turtle`.

## 📋 Spis treści
- [O projekcie](#-o-projekcie)
- [Funkcje](#-funkcje)
- [Struktura plików](#-struktura-plików)
- [Wymagania](#-wymagania)
- [Instrukcja uruchomienia](#-instrukcja-uruchomienia)
- [Instrukcja obsługi](#-instrukcja-obsługi)
- [Legenda elementów mapy](#-legenda-elementów-mapy)

---

## 🧐 O projekcie
Symulator pozwala na przeprowadzenie misji badawczej pojazdu typu łazik. Zadaniem użytkownika jest dotarcie do wyznaczonego celu, zarządzając ograniczonymi zasobami paliwa i omijając przeszkody. Świat jest generowany dynamicznie, a każde działanie ma swój koszt energetyczny.

## ✨ Funkcje
- **Wizualizacja w czasie rzeczywistym:** Śledź ruch pojazdu na graficznej mapie.
- **Interfejs HUD:** Dynamiczny pasek energii oraz statystyki misji widoczne bezpośrednio w oknie graficznym.
- **Zaawansowany komputer pokładowy:** Szczegółowe statystyki w konsoli (odległość do celu, średnie zużycie paliwa, całkowity dystans).
- **Dynamiczne środowisko:** Losowe przeszkody, zbiorniki z paliwem oraz "bezpieczne skróty".
- **Zdarzenia losowe:** Burze magnetyczne wpływające na orientację oraz okna pogodowe poprawiające wydajność.

## 📂 Struktura plików
Projekt został podzielony na moduły zgodnie z zasadą separacji odpowiedzialności:

- `main.py` – Punkt wejścia aplikacji, zarządza pętlą zdarzeń i interakcją z użytkownikiem.
- `engine.py` – Silnik symulacji, odpowiada za logikę ruchu, kolizje i warunki zwycięstwa/porażki.
- `models.py` – Klasy danych (klasy `Vehicle`, `World`, `Coordinates`).
- `view.py` – Moduł graficzny oparty na bibliotece `turtle`, obsługuje HUD i rysowanie mapy.

## 💻 Wymagania
- Python 3.7 lub nowszy.
- System operacyjny z obsługą środowiska graficznego (wymagane dla `turtle`).
- Biblioteka `turtle` (zazwyczaj dołączona do standardowej instalacji Pythona).

## 🚀 Instrukcja uruchomienia

1. **Sklonuj repozytorium lub pobierz pliki:**
   Upewnij się, że wszystkie pliki (`main.py`, `engine.py`, `models.py`, `view.py`) znajdują się w jednym folderze.

2. **Uruchom program:**
   Otwórz terminal w folderze projektu i wpisz:
   ```bash
   python main.py
   ```

## 🎮 Instrukcja obsługi

1. **Konfiguracja:** Na starcie podaj nazwę wyprawy oraz parametry początkowe (lub naciśnij Enter, aby użyć domyślnych).
2. **Sterowanie:**
   - `M` – Ruch naprzód (podać odległość).
   - `O` – Obrót pojazdu (kąt dodatni w lewo, ujemny w prawo).
   - `Q` – Przerwanie misji.
3. **Cel:** Dotrzyj do zielonego punktu oznaczonego jako "CEL" (odległość < 10 j.).
4. **Przegrana:** Misja kończy się porażką, jeśli skończy się paliwo lub przekroczysz limit 50 kroków.

## 🗺️ Legenda elementów mapy
- 🟢 **Zielony Okrąg:** Cel wyprawy.
- 🔵 **Niebieska Strzałka:** Twój pojazd (zostawia ślad trasy).
- 🟠 **Pomarańczowa Kropka:** Paliwo (+30 pkt energii).
- ⚫ **Czarna Kropka:** Przeszkoda (-20 pkt energii).
- 🔵 **Jasnoniebieska (Cyan) Kropka:** Skrót (darmowe przesunięcie o +15 j.).

---
*Powodzenia w Twojej wyprawie!* 🚀
