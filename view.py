import turtle
from models import Coordinates

class SimulationView:
    def __init__(self, world_width: float, world_height: float):
        # Inicjalizacja okna graficznego Turtle
        self.screen = turtle.Screen()
        self.screen.title("Symulator Wyprawy")
        self.screen.setup(width=700, height=700)
        self.screen.tracer(0) # Wyłączamy animację dla szybszego rysowania tła

        self.world_width = world_width
        self.world_height = world_height

        # Skalowanie okna do rozmiarów zdefiniowanego świata z marginesem
        margin = 50
        self.screen.setworldcoordinates(
            -world_width / 2 - margin, -world_height / 2 - margin,
            world_width / 2 + margin, world_height / 2 + margin
        )

        # Żółw do rysowania elementów statycznych (granice, cel, przeszkody)
        self.static_drawer = turtle.Turtle()
        self.static_drawer.speed(0)
        self.static_drawer.hideturtle()

        # Żółw reprezentujący pojazd i rysujący ścieżkę
        self.vehicle_turtle = turtle.Turtle()
        self.vehicle_turtle.shape("arrow")
        self.vehicle_turtle.color("blue")
        self.vehicle_turtle.pensize(2)
        self.vehicle_turtle.speed(3)

        self._draw_bounds()
        self.screen.update()

    def _draw_bounds(self):
        w, h = self.world_width, self.world_height
        self.static_drawer.penup()
        self.static_drawer.goto(-w / 2, -h / 2)
        self.static_drawer.pendown()
        self.static_drawer.color("red")
        for _ in range(2):
            self.static_drawer.forward(w)
            self.static_drawer.left(90)
            self.static_drawer.forward(h)
            self.static_drawer.left(90)
        self.static_drawer.penup()

    def draw_target(self, coords: Coordinates):
        self.static_drawer.penup()
        self.static_drawer.goto(coords.x, coords.y - 5)
        self.static_drawer.pendown()
        self.static_drawer.color("green")
        self.static_drawer.begin_fill()
        self.static_drawer.circle(5)
        self.static_drawer.end_fill()
        self.static_drawer.penup()
        self.static_drawer.goto(coords.x, coords.y + 7)
        self.static_drawer.write("CEL", align="center", font=("Arial", 10, "bold"))
        self.screen.update()

    def draw_elements(self, elements: dict):
        self.screen.tracer(0)
        for (x, y), elem_type in elements.items():
            self.static_drawer.penup()
            self.static_drawer.goto(x, y)
            if elem_type == "PALIWO":
                self.static_drawer.color("orange")
                self.static_drawer.dot(8)
            elif elem_type == "PRZESZKODA":
                self.static_drawer.color("black")
                self.static_drawer.dot(10)
            elif elem_type == "SKRÓT":
                self.static_drawer.color("cyan")
                self.static_drawer.dot(8)
        self.screen.update()
        self.screen.tracer(1)

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
        self.vehicle_turtle.hideturtle()
        self.static_drawer.clear()
        # Przygotowanie do ewentualnego ponownego użycia lub zamknięcia
        self.screen.update()

    def reset_view(self):
        self.vehicle_turtle.clear()
        self.vehicle_turtle.showturtle()
        self.static_drawer.clear()
        self._draw_bounds()
        self.screen.update()
