import customtkinter
import time
import random
import tkinter as tk
import json
import os
#--------------------
customtkinter.set_appearance_mode("dark")
#--------------------
SCRAMBLE_FONT = ("Comic Sans MS", 35)
TIMER_FONT = ("Comic Sans MS", 45)
BUTTON_FONT = ("Comic Sans MS", 25)
INF_FONT = ("Comic Sans MS", 20)
JSON_FILE_EX = {
    "total_time_solved": 0,
    "time": 0,
    "avg":0,
    "solved_time":0,
    "best": {},
    "allScrambleTime": []
}
elapsed_time = 0

if not os.path.exists("users.json"):
    print("Created users.json")
    with open("users.json","w") as f_r:
        json.dump(JSON_FILE_EX, f_r, indent=4)
        f_r.close()
    f_r= open("users.json","r")
    INFORMATION = json.loads(f_r.read())
else:
    f_r= open("users.json","r")
    INFORMATION = json.loads(f_r.read())



#--------------------
class WCATimer:
    def __init__(self, windows):
        self.windows = windows
        self.running = False

        #information
        self.text_scrtimer = customtkinter.CTkFrame(self.windows)
        self.text_scrtimer.grid(row=0, column=0)
        
        self.information = customtkinter.CTkFrame(self.windows)
        self.information.grid(row=0,column=1)



        self.button = customtkinter.CTkFrame(self.windows)
        self.button.grid(row=1,column=0)


        self.avg_timer = customtkinter.CTkLabel(self.information, text=f'Average: {INFORMATION["avg"]}', font=INF_FONT)
        self.avg_timer.grid(row=0, column=0, padx =5, pady=5)


        self.last_timer = customtkinter.CTkLabel(self.information, text=f'Last: ', font=INF_FONT)
        self.last_timer.grid(row=1, column=0, padx =5, pady=5)






        self.scramble = customtkinter.CTkLabel(self.text_scrtimer, text=self.generate_3x3x3_scramble(), font =SCRAMBLE_FONT)
        self.scramble.pack(padx=10, pady=10)
        
        self.timer_label = customtkinter.CTkLabel(self.text_scrtimer, text="0.000", font=TIMER_FONT)
        self.timer_label.pack(padx=10, pady=10)

        self.start_timer = customtkinter.CTkButton(self.button, text="Start", font=BUTTON_FONT, command=self.run)
        self.start_timer.grid(padx=10, pady=10,row= 0, column=0)

        self.stop_timer = customtkinter.CTkButton(self.button, text="Stop", font=BUTTON_FONT, command=self.stop)
        self.stop_timer.grid(padx=10, pady=10,row= 0, column=1)

        self.reset_timer = customtkinter.CTkButton(self.button, text="Reset", font=BUTTON_FONT, command=self.reset)
        self.reset_timer.grid(padx=10, pady=10,row= 0, column=2)

        self.reset_timer = customtkinter.CTkButton(self.button, text="New Scramble", font=BUTTON_FONT, command=self.newscramble)
        self.reset_timer.grid(padx=10, pady=10,row= 0, column=3)

    def update(self):
        global elapsed_time
        if self.running:
            elapsed_time = time.time() - self.start_time
            hours = int(elapsed_time / 3600)
            minutes = int((elapsed_time % 3600) / 60)
            seconds = int(elapsed_time % 60)
            milliseconds = int((elapsed_time % 1) * 1000)
            time_str = f"{seconds}.{milliseconds:03d}"
            if minutes >0:
                time_str = f"{minutes}:{seconds:02d}.{milliseconds:03d}"
            if hours >0:
                time_str = f"{hours}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
            self.timer_label.configure(text=time_str)
        self.windows.after(10, self.update)

    def newscramble(self):
        if not self.running:
            self.scramble.configure(text=self.generate_3x3x3_scramble())        
    
    def stop(self):
        global elapsed_time
        if self.running:
            seconds = int(elapsed_time % 60)
            milliseconds = int((elapsed_time % 1) * 1000)
            self.running = False
            self.get_avg_time()
            hours = int(elapsed_time / 3600)
            minutes = int((elapsed_time % 3600) / 60)
            seconds = int(elapsed_time % 60)
            milliseconds = int((elapsed_time % 1) * 1000)
            time_str = f"{seconds}.{milliseconds:03d}"
            if minutes >0:
                time_str = f"{minutes}:{seconds:02d}.{milliseconds:03d}"
            if hours >0:
                time_str = f"{hours}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
            self.scramble.configure(text=self.generate_3x3x3_scramble())
            self.last_timer.configure(text="Last: "+time_str)
            
    def run(self):
        if not self.running:
            self.start_time = time.time()
            self.running = True
            self.update()

    
    def reset(self):
        self.running = False
        self.timer_label.configure(text="0.000")
        self.newscramble()

    def generate_3x3x3_scramble(self,length=20):
        MOVES = ["U", "D", "R", "L", "F", "B"]
        scramble = []
        last_move = ""
        
        for _ in range(length):
            move = random.choice(MOVES)
            while move[0] == last_move:
                move = random.choice(MOVES)
            last_move = move[0]
            
            if random.random() < 0.5:
                move += random.choice(["", "'", "2"])
            
            scramble.append(move)
        
        return " ".join(scramble)

    def get_avg_time(self):
        global elapsed_time
        global INFORMATION
        total_time_solved =  INFORMATION["total_time_solved"]
        INFORMATION["solved_time"]+=1
        solved_time = INFORMATION["solved_time"]
        total_time_solved += elapsed_time
        avg_time = round(total_time_solved/solved_time, 3)
        hours = int(avg_time / 3600)
        minutes = int((avg_time % 3600) / 60)
        seconds = int(avg_time % 60)
        milliseconds = int((avg_time % 1) * 1000)
        INFORMATION["total_time_solved"] = total_time_solved
        INFORMATION["avg"] = avg_time
        time_str = f"{seconds}.{milliseconds:03d}"
        if minutes > 0:
            time_str = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        if hours >0:
            time_str = f"{hours}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        self.avg_timer.configure(text="Avegare: "+time_str)
        with open("users.json","w") as f:
            json.dump(INFORMATION, f, indent=4)
            f.close()

        



if __name__ == "__main__":
    windows = customtkinter.CTk()
    app = WCATimer(windows)
    windows.title("Timer 1.0")
    windows.resizable(width=False, height=False)
    windows.mainloop()
    f_r.close()