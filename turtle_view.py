import turtle
import constants
from world import Coordinates

class TurtleView:
    """Obsługuje wizualizację graficzną za pomocą biblioteki Turtle."""

    def __init__(self):
        # Inicjalizacja ekranu
        self.screen = turtle.Screen()
        self.screen.title("Symulator Wyprawy Łazika")
        self.screen.setup(width=700, height=700)

        # Inicjalizacja żółwi
        self.bounds_drawer = turtle.Turtle()
        self.rover_turtle = turtle.Turtle()

        # Konfiguracja początkowa
        self.bounds_drawer.hideturtle()
        self.bounds_drawer.speed(0)

        self.rover_turtle.shape("arrow")
        self.rover_turtle.color(constants.COLOR_VEHICLE)
        self.rover_turtle.pensize(constants.PEN_SIZE)
        self.rover_turtle.speed(constants.TURTLE_SPEED)

    def setup_world(self, width: float, height: float):
        """Przygotowuje współrzędne świata i rysuje granice."""
        self.screen.clearscreen()  # Czyści wszystko, w tym tło i ustawienia

        # Ponowna konfiguracja po clearscreen()
        self.screen.setworldcoordinates(
            -width / 2 - constants.MARGIN, -height / 2 - constants.MARGIN,
            width / 2 + constants.MARGIN, height / 2 + constants.MARGIN
        )

        # Ponowna inicjalizacja żółwi (clearscreen je usuwa)
        self.bounds_drawer = turtle.Turtle()
        self.bounds_drawer.hideturtle()
        self.bounds_drawer.speed(0)
        self.bounds_drawer.color(constants.COLOR_BOUNDS)

        self.rover_turtle = turtle.Turtle()
        self.rover_turtle.shape("arrow")
        self.rover_turtle.color(constants.COLOR_VEHICLE)
        self.rover_turtle.pensize(constants.PEN_SIZE)
        self.rover_turtle.speed(constants.TURTLE_SPEED)

        # Rysowanie granic
        self._draw_bounds(width, height)

    def _draw_bounds(self, w: float, h: float):
        self.bounds_drawer.penup()
        self.bounds_drawer.goto(-w / 2, -h / 2)
        self.bounds_drawer.pendown()
        for _ in range(2):
            self.bounds_drawer.forward(w)
            self.bounds_drawer.left(90)
            self.bounds_drawer.forward(h)
            self.bounds_drawer.left(90)

    def set_initial_position(self, coords: Coordinates, angle: float):
        """Ustawia łazik na pozycji startowej bez rysowania linii."""
        self.rover_turtle.penup()
        self.rover_turtle.goto(coords.x, coords.y)
        self.rover_turtle.setheading(angle)
        self.rover_turtle.pendown()

    def update_rover(self, coords: Coordinates, angle: float):
        """Aktualizuje pozycję i zwrot łazika na ekranie."""
        self.rover_turtle.setheading(angle)
        self.rover_turtle.goto(coords.x, coords.y)

    def close(self):
        """Zamyka okno Turtle."""
        self.screen.bye()
