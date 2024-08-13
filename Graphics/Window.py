import tkinter as tk
import threading


class Window:
    def __init__(self) -> None:
        self.root = None
        
    def init(self):
        self.root = tk.Tk()

        self.root.geometry("500x500")
        self.root.title("Hello World!")

    def run(self):
        self.init()
        self.root.mainloop()

    def run_async(self):
        thread = threading.Thread(target=Window.run, args=(self,))
        thread.start()
        return thread
    
    def close(self):
        self.root.quit()



if __name__ == "__main__":
    wind = Window()
    thread = wind.run_async()

    print("closing")

    wind.close()

    print("Exit")

