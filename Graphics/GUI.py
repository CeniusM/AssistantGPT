from Graphics.Window import *
from Graphics.TextUtil import *
import threading
import json

class GUI:
    def __init__(self) -> None:
        self.window = None
        self.users = {}
        self.messages = []
        self.running = False
        self.scroll = 0.0
        self.clear_color = Color(40,40,40)

    # API
    def message(self, user, content):
        # Write to window
        self.messages.append({"user": user, "content": content})

    def add_user(self, user, alias, rgb):
        # If a message is by a user with a color, its text will be colored acordingly
        # The users name will be replaced with its alias
        self.users[user] = {"color": rgb, "alias": alias}

    def main_loop(self, width, height):
        self.window = Window(width, height)
        
        clock = pygame.time.Clock()
        self.running = True
        dt = 0
        while self.running: # main game loop
            for event in self.window.get_events():
                if event.type == QUIT:
                    self.running=False
                    break
                if event.type ==MOUSEWHEEL:
                    self.scroll += event.y * 20

            self.window.fill(self.clear_color)
            
            # Render the messages
            default_color = Color(255,255,255)
            text = GText(30)
            margine = 10
            y = margine + self.scroll
            for msg in self.messages:
                user_name = msg["user"]
                content = msg["content"]

                if user_name in self.users.keys():
                    user = self.users[user_name]

                    text.forground = user["color"]
                    if user["alias"]:
                        user_name = user["alias"] # last step!
                else:
                    text.forground = default_color

                y, _, _ = TextUtil.write(self.window, text.write(user_name), (margine, y), -margine*2)
                y += text.size / 4
                y, _, _ = TextUtil.write(self.window, text.write(content), (margine * 2, y), -margine*2)
                y += text.size





            self.window.render_present()
            dt = clock.tick(30)
        
        self.window.close()
        self.window = None
    
    def stop(self):
        self.running = False

    @staticmethod
    def start_async_window(width, height):
        gui = GUI()
        thread = threading.Thread(target = gui.main_loop, args = (width, height))

        thread.start()

        return gui, thread

# if __name__ == "__main__":
#     with open("Graphics\convo.json", "r") as file:
#         convo = json.loads(file.read())

#     gui, thread = GUI.start_async_window(800, 600)

#     gui.add_user("assistant", "ChatGPT", (50, 200, 150))
#     gui.add_user("system", "SYS", (200, 100, 0))
#     gui.add_user("user", "You", (250, 250, 250))
#     gui.add_user("summary", "Summary", (50, 100, 200))
#     gui.add_user("DEBUG", None, (200, 50, 150))

#     for m in convo:
#         gui.message(m["role"], m["content"])

#     gui.message("DEBUG", "Could not get name")

#     thread.join()

#     print("Exit")