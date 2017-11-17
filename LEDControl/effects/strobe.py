import time


class Strobe:
    def __init__(self, main, freq=1):
        self.main = main
        self.freq = freq
        self.run = True

    def start(self):
        # self.main.curColor()
        self.main.save_color()
        while self.run:
            wait_time = 1/self.freq
            self.main.send_saved()
            time.sleep(.005)
            self.main.all_off()
            self.main.update()
            time.sleep(wait_time-.005)
        self.main.send_saved()
