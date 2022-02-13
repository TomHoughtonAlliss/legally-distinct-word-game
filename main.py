import pyglet
import wordle_engine


WORD_LENGTH = 5
NUMBER_OF_GUESSES = 6
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600
TEXT_WINDOW_WIDTH = 400
TEXT_WINDOW_HEIGHT = 500
TEXT_OFFSET = 10
BOX_WIDTH = TEXT_WINDOW_WIDTH // 5
BOX_HEIGHT = TEXT_WINDOW_WIDTH // 5
TEXT_WINDOW_LEFT = (SCREEN_WIDTH - TEXT_WINDOW_WIDTH) // 2
TEXT_WINDOW_BOTTOM = (SCREEN_HEIGHT - TEXT_WINDOW_HEIGHT) // 2


class Game:
    def __init__(self):
        self.wordle = wordle_engine.Wordle()
        self.window = pyglet.window.Window(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, caption='(not) Wordle')

        self.current_typed_letters = []
        self.alphabet = {pyglet.window.key.A:'A', pyglet.window.key.B:'B', pyglet.window.key.C:'C', pyglet.window.key.D:'D', pyglet.window.key.E:'E', pyglet.window.key.F:'F', pyglet.window.key.G:'G', pyglet.window.key.H:'H', pyglet.window.key.I:'I', pyglet.window.key.J:'J', pyglet.window.key.K:'K', pyglet.window.key.L:'L', pyglet.window.key.M:'M', pyglet.window.key.N:'N', pyglet.window.key.O:'O', pyglet.window.key.P:'P', pyglet.window.key.Q:'Q', pyglet.window.key.R:'R', pyglet.window.key.S:'S', pyglet.window.key.T:'T', pyglet.window.key.U:'U', pyglet.window.key.V:'V', pyglet.window.key.W:'W', pyglet.window.key.X:'X', pyglet.window.key.Y:'Y', pyglet.window.key.Z:'Z'}

        # decides what colour to shade each square.
        # 0: black - this square is either un-entered or the letter is not present
        # 1: yellow - this square contains a letter which is in the word but not this position
        # 2: green - this square contains the correct later in the correct position
        self.guess_statuses = [[0 for _ in range(WORD_LENGTH)] for _ in range(NUMBER_OF_GUESSES)]
        self.confirmed_rows = [[] for _ in range(NUMBER_OF_GUESSES)]
        self.colour_dictionary = {0:(0, 0, 0), 1:(153, 135, 43), 2:(60, 130, 59)}

        self.game_won = False
        self.game_lost = False

    def on_draw(self):
        self.window.clear()

        batch = pyglet.shapes.Batch()
        shapes = []

        if (not self.game_won) and (not self.game_lost):
            # draw_grid
            for y in range(NUMBER_OF_GUESSES):
                this_guess = self.guess_statuses[y]
                for x in range(WORD_LENGTH):
                    colour = self.colour_dictionary[this_guess[x]]
                    # create x and y positions such that they're centred within the text window and have a space between
                    # themselves of 5 pixels
                    x_pos = (x*5) + TEXT_WINDOW_LEFT + (x*BOX_WIDTH) - (5 * WORD_LENGTH) / 2
                    y_pos = TEXT_WINDOW_HEIGHT - ((y*5) + TEXT_WINDOW_BOTTOM + (y*BOX_HEIGHT) - (5 * NUMBER_OF_GUESSES) / 2)-7

                    # Background square
                    shapes.append(pyglet.shapes.Rectangle(x_pos, y_pos, BOX_WIDTH, BOX_HEIGHT, color=(255, 255, 255), batch=batch))
                    # Foreground square, with a 1 pixel border from background square
                    shapes.append(pyglet.shapes.Rectangle(x_pos+1, y_pos+1, BOX_WIDTH-2, BOX_HEIGHT-2, color=colour, batch=batch))

            # draw letters
            for y in range(len(self.confirmed_rows)):
                y_pos = TEXT_WINDOW_HEIGHT - ((y*5) + TEXT_WINDOW_BOTTOM + (y*BOX_HEIGHT) - (5 * NUMBER_OF_GUESSES) / 2)
                for x, guess in enumerate(self.confirmed_rows[y]):
                    x_pos = (x*5) + TEXT_WINDOW_LEFT + (x*BOX_WIDTH) - (5 * WORD_LENGTH) / 2
                    pyglet.text.Label(text=''.join(guess), font_name="Lucida Sans Typewriter", font_size=65, x=x_pos+12, y=y_pos, batch=batch, bold=True)

            y_pos = TEXT_WINDOW_HEIGHT - ((self.wordle.number_of_guesses * 5) + TEXT_WINDOW_BOTTOM + (self.wordle.number_of_guesses * BOX_HEIGHT) - (5 * NUMBER_OF_GUESSES) / 2)
            for x, char in enumerate(self.current_typed_letters):
                x_pos = (x * 5) + TEXT_WINDOW_LEFT + (x * BOX_WIDTH) - (5 * WORD_LENGTH) / 2
                pyglet.text.Label(text=char, font_name="Lucida Sans Typewriter", font_size=65, x=x_pos + 12, y=y_pos, batch=batch, bold=True)

        x = SCREEN_WIDTH // 2
        y = SCREEN_HEIGHT // 2
        if self.game_won:
            t = "you done it !1!!".upper()
            shapes.append(pyglet.text.Label(text=t, font_name="Lucida Sans Typewriter", font_size=40, x=x + 12, y=y, anchor_x='center', anchor_y='center', batch = batch, bold = True, color=(0, 255, 0, 255)))
        elif self.game_lost:
            t = "you lose oof".upper()
            shapes.append(pyglet.text.Label(text=t, font_name="Lucida Sans Typewriter", font_size=55, x=x + 12, y=y, anchor_x='center', anchor_y='center', batch=batch, bold=True, color=(255, 0, 0, 255)))
            t = ("word was " + self.wordle.word).upper()
            shapes.append(pyglet.text.Label(text=t, font_name="Lucida Sans Typewriter", font_size=25, x=x + 12, y=y-50, anchor_x='center', anchor_y='center', batch=batch, bold=True, color=(255, 0, 0, 255)))


        batch.draw()

    def on_key_press(self, button, modifiers):
        if button in self.alphabet.keys():
            if len(self.current_typed_letters) < 5:
                character = self.alphabet[button]
                self.current_typed_letters.append(character)
        elif button == pyglet.window.key.BACKSPACE:
            if len(self.current_typed_letters) > 0:
                del self.current_typed_letters[-1]
        elif button == pyglet.window.key.ENTER:
            if len(self.current_typed_letters) == 5:
                if self.wordle.check_if_valid_guess(''.join(self.current_typed_letters).lower()):
                    guess_number = self.wordle.number_of_guesses

                    self.guess_statuses[guess_number], self.game_won = self.wordle.get_guess_results(''.join(self.current_typed_letters).lower())
                    self.confirmed_rows[guess_number] = self.current_typed_letters
                    self.current_typed_letters = []

                    if self.wordle.number_of_guesses == 6:
                        self.game_lost = True

    def main(self):
        self.window.event(self.on_draw)
        self.window.event(self.on_key_press)

        pyglet.app.run()


if __name__ == "__main__":
    game = Game()
    game.main()
