from argparse import ArgumentParser
from decimal import Decimal, localcontext
from math import floor
from tkinter import Canvas, Tk, mainloop

# Tupper's formula constant
K = 960939379918958884971672962127852754715004339660129306651505519271702802395266424689642842174350718121267153782770623355993237280874144307891325963941337723487857735749823926629715517173716995165232890538221612403238855866184013235585136048828693337902491454229288667081096184496091705183454067827731551705405381627380967602565625016981482083418783163849115590225610003652351370343874461848378737238198224849863465033159410054974700593138339226497249461751545728366702369745461014655997933798537483143786841806593422227898388722980000748404719

X_MAX = 106
Y_MAX = 17

# TKinter's window
MARGIN = 20
PIXEL_SIZE = 12
WINDOW_WIDTH = PIXEL_SIZE * X_MAX + 2 * MARGIN
WINDOW_HEIGHT = PIXEL_SIZE * Y_MAX + 2 * MARGIN

# Console's "Pixel"
PIXEL_CHAR = chr(11035)  # Unicode character of square
SPACE_CHAR = " "


# Tupper fomrula
def tupper(x: int, y: int) -> bool:
    class Dec(Decimal):
        pass

    x_decimal: Decimal = Dec(x)
    y_decimal: Decimal = Dec(y)
    return 1 / 2 < floor(
        (
            floor(y_decimal / Dec(17))
            * 2 ** (-17 * floor(x_decimal) - floor(y_decimal) % Dec(17))
        )
        % 2
    )


def painter() -> list[list[bool]]:
    with localcontext() as context:
        context.prec = len(str(K))
        matrix = [[tupper(x, y + K) for x in range(X_MAX)] for y in range(Y_MAX)]
        for row in matrix:
            row.reverse()
        return matrix


def draw_console(values: list[list[bool]]) -> None:
    print(
        "\n".join(
            "".join(PIXEL_CHAR if value else SPACE_CHAR for value in row)
            for row in values
        )
    )


def show_window(values: list[list[bool]]) -> None:
    window = Tk()
    window.title("Tupper's formula")
    window.resizable(False, False)

    canvas = Canvas(window, bg="white", height=WINDOW_HEIGHT, width=WINDOW_WIDTH)

    for y, row in enumerate(values):
        for x, cell in enumerate(row):
            if cell:
                x1 = MARGIN + x * PIXEL_SIZE
                y1 = MARGIN + y * PIXEL_SIZE
                x2 = x1 + PIXEL_SIZE
                y2 = y1 + PIXEL_SIZE
                canvas.create_rectangle(x1, y1, x2, y2, fill="black")

    canvas.pack()
    mainloop()


def main(*, console: bool = True, window: bool = True) -> None:
    if not console and not window:
        console = True

    matrix = painter()

    if console:
        draw_console(matrix)
    if window:
        show_window(matrix)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--console", "-c", default=False, help="Draw in Console", action="store_true"
    )
    parser.add_argument(
        "--window", "-w", default=False, help="Show Window", action="store_true"
    )
    args = parser.parse_args()
    main(console=args.console, window=args.window)
