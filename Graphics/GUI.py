from Window import *
from TextUtil import *
import threading

class GUI:
    def __init__(self) -> None:
        self.window = None
        self.users = {}
        self.users_alias = {}
        self.messages = []
        self.run = False

    # API
    def message(self, user, content):
        # Write to window
        self.messages.append({"user": user, "content": content})

    def add_user_color(self, user, rgb):
        # If a message is by a user with a color, its text will be colored acordingly
        self.users[user] = rgb

    def add_user_alias(self, user, alias):
        # The users name will be replaced with its alias
        self.users_alias[user] = alias

    def main_loop(self, width, height):
        self.window = Window(width, height)
        
        clock = pygame.time.Clock()
        self.run = True
        dt = 0
        while self.run: # main game loop
            for event in self.window.get_events():
                if event.type == QUIT:
                    self.run=False
                    break

            self.window.fill(Color(50,50,50))
            
            # Render the messages
            default_color = Color(255,255,255)
            text = GText(50)
            margine = 10
            y = margine
            for msg in self.messages:
                user = msg["user"]
                content = msg["content"]

                if user in self.users.keys():
                    text.forground = self.users[user]
                else:
                    text.forground = default_color

                # last step!
                if user in self.users_alias.keys():
                    user = self.users_alias[user]

                y, _, _ = TextUtil.write(self.window, text.write(f"-{user}-"), (margine, y), -margine*2)
                y, _, _ = TextUtil.write(self.window, text.write(content), (margine * 2, y), -margine*2)





            self.window.render_present()
            dt = clock.tick(30)
        
        self.window.close()
        self.window = None
    
    def stop(self):
        self.run = False

    @staticmethod
    def start_async_window(width, height):
        gui = GUI()
        thread = threading.Thread(target = gui.main_loop, args = (width, height))

        thread.start()

        return gui, thread

if __name__ == "__main__":
    gui, thread = GUI.start_async_window(500, 500)

    gui.add_user_alias("assistant", "ChatGPT")
    gui.add_user_color("assistant", (110, 250, 200))

    gui.message("assistant", "yoyo, i just wanna say python is real")

    thread.join()

    print("Exit")



# wind.fill(Color(50, 50, 50))
# msg = "The conversation topics such as weather in different countries, dolphin facts, and the size off ant colonies."
# margine = 10

# wind.draw_box(margine, margine, wind.size.w - margine * 2, 3*50, Color(100,50,200))

# TextUtil.write(wind, msg, Color(100, 200, 100), (margine- 1000,margine- 1000), 30, -margine*2)

# wind.render_present()