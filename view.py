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
