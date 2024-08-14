from Window import *

# Graphics text with options
class GText:
    def __init__(self, size: int) -> None:
        self.text = ""
        self.size = size
        self.forground = Color(255,255,255)
        self.background = None
        self.font_name = None
        self.bold = False
        self.italic = False
    
    def write(self, text):
        self.text = text
        return self
    
    def generate_font(self):
        return pygame.font.SysFont(self.font_name, self.size, self.bold, self.italic)


class TextUtil:
    @staticmethod
    def get_font(name, size):

        return pygame.font.SysFont(name, size)

    @staticmethod
    def write(window: Window,
        g_text: GText,
        # Top left
        position,
        # The max width of a line of text (if 0 or negative, it will be added to width)
        width: int = 0,
        # The max lines count the write function will make to fit the text (-1 is no end)
        max_lines = -1,
        # This describes if the line offsets are the size parameter, or the max height of the text
        use_line_heigth = True,
        antialias=True):

        if width <= 0:
            width = window.size.w + width

        # Initialize the font
        font = g_text.generate_font()
        text = g_text.text
        size = g_text.size
        color = g_text.forground
        back_color = g_text.background

        words = []
        # Gotta replace the \n
        temp_words = text.split(' ')
        for word in temp_words:
            splits = word.split("\n")
            splits = ["\n" if w == "" else w for w in splits]
            words += splits

        space_width = font.size(' ')[0]
        x, y = position
        max_lines = max_lines if max_lines > 0 else float('inf')
        line_count = 0
        line_offset = size if not use_line_heigth else font.size(text)[1]
        
        while len(words) != 0 and line_count < max_lines:
            # Get the words that fit on a line
            line_text = [words.pop(0)]
            line_width = font.size(line_text[0])[0]

            while len(words) != 0:
                next_word = words[0]

                if next_word == "\n":
                    words.pop(0)
                    break

                word_width = font.size(next_word)[0]
                new_width = line_width + word_width + space_width

                if new_width < width:
                    line_width = new_width
                    words.pop(0)
                    line_text.append(next_word)
                else:
                    break
            
            text = ' '.join(line_text)

            window.draw_text(
                font, 
                text,
                (x,y),
                forgound = g_text.forground,
                background = g_text.background,
                antialias = antialias
            )

            y += line_offset
            line_count += 1
        
        # New y position and the line offset used. And remainder
        return y, line_offset, words