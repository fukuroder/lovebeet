import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import json
import lovebeet


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.__create_widgets()

    def __update(self, high_quality=False):
        if not self.__update_enabled:
            return

        if high_quality:
            self.title("LOVEBEET (updating...)")
            scale = self.__q.get()*2+1
        else:
            scale = 1
        self.__array = lovebeet.draw(
            scale,
            self.__width.get(),
            self.__div.get(),
            self.__grad1.get(),
            (self.__r1.get(), self.__g1.get(), self.__b1.get()),
            (self.__r2.get(), self.__g2.get(), self.__b2.get()),
            (self.__r3.get(), self.__g3.get(), self.__b3.get()),
            self.__lines.get(),
            self.__angle.get(),
            self.__pad.get(),
            self.__grad2.get(),
            (self.__r4.get(), self.__g4.get(), self.__b4.get()),
            (self.__r5.get(), self.__g5.get(), self.__b5.get()))
        self.__photo_image = ImageTk.PhotoImage(
            image=Image.fromarray(self.__array))
        self.__label_image.config(image=self.__photo_image)

        if high_quality:
            self.title("LOVEBEET")

    def __save_image(self):
        self.__update(high_quality=True)
        filename = filedialog.asksaveasfilename(
            filetypes=[("image file", "*.png;*.webp;*.jpg;*.bmp")])
        if filename:
            Image.fromarray(self.__array).save(filename)

    def __load_setting(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON", "*.json")], defaultextension="json")
        if not filename:
            return

        with open(filename, "r") as f:
            d = json.load(f)

        self.__update_all(d)

    def __update_all(self, d):
        self.__update_enabled = False
        self.__r1.set(d["foreground"]["red1"])
        self.__g1.set(d["foreground"]["green1"])
        self.__b1.set(d["foreground"]["blue1"])
        self.__r2.set(d["foreground"]["red2"])
        self.__g2.set(d["foreground"]["green2"])
        self.__b2.set(d["foreground"]["blue2"])
        self.__r3.set(d["foreground"]["red3"])
        self.__g3.set(d["foreground"]["green3"])
        self.__b3.set(d["foreground"]["blue3"])
        self.__width.set(d["foreground"]["width"])
        self.__div.set(d["foreground"]["division"])
        self.__grad1.set(d["foreground"]["gradation1"])
        self.__lines.set(d["foreground"]["lines"])
        self.__angle.set(d["foreground"]["angle"])

        self.__r4.set(d["background"]["red4"])
        self.__g4.set(d["background"]["green4"])
        self.__b4.set(d["background"]["blue4"])
        self.__r5.set(d["background"]["red5"])
        self.__g5.set(d["background"]["green5"])
        self.__b5.set(d["background"]["blue5"])
        self.__grad2.set(d["background"]["gradation2"])
        self.__pad.set(d["background"]["padding"])
        self.__q.set(2)
        self.__update_enabled = True
        self.__update(high_quality=True)

    def __save_setting(self):
        filename = filedialog.asksaveasfilename(
            filetypes=[("JSON", "*.json")], defaultextension="json")
        if not filename:
            return

        d = {
            "foreground": {
                "red1": self.__r1.get(),
                "green1": self.__g1.get(),
                "blue1": self.__b1.get(),
                "red2": self.__r2.get(),
                "green2": self.__g2.get(),
                "blue2": self.__b2.get(),
                "red3": self.__r3.get(),
                "green3": self.__g3.get(),
                "blue3": self.__b3.get(),
                "width": self.__width.get(),
                "division": self.__div.get(),
                "gradation1": self.__grad1.get(),
                "lines": self.__lines.get(),
                "angle": self.__angle.get(),
            },
            "background": {
                "red4": self.__r4.get(),
                "green4": self.__g4.get(),
                "blue4": self.__b4.get(),
                "red5": self.__r5.get(),
                "green5": self.__g5.get(),
                "blue5": self.__b5.get(),
                "gradation2": self.__grad2.get(),
                "padding": self.__pad.get(),
            },
        }

        with open(filename, "w") as f:
            json.dump(d, f, indent=4)

    def __preset1(self):
        j = \
            """{
    "foreground": {
        "red1": 255,
        "green1": 255,
        "blue1": 0,
        "red2": 255,
        "green2": 255,
        "blue2": 255,
        "red3": 0,
        "green3": 0,
        "blue3": 0,
        "width": 512,
        "division": 32,
        "gradation1": 0,
        "lines": 6,
        "angle": 0
    },
    "background": {
        "red4": 255,
        "green4": 0,
        "blue4": 0,
        "red5": 255,
        "green5": 255,
        "blue5": 0,
        "gradation2": 100,
        "padding": 25
    }
}"""
        self.__update_all(json.loads(j))

    def __preset2(self):
        j = \
            """{
    "foreground": {
        "red1": 255,
        "green1": 0,
        "blue1": 0,
        "red2": 255,
        "green2": 255,
        "blue2": 255,
        "red3": 0,
        "green3": 0,
        "blue3": 0,
        "width": 400,
        "division": 40,
        "gradation1": 0,
        "lines": 1,
        "angle": 315
    },
    "background": {
        "red4": 255,
        "green4": 255,
        "blue4": 0,
        "red5": 255,
        "green5": 255,
        "blue5": 255,
        "gradation2": 0,
        "padding": 20
    }
}"""
        self.__update_all(json.loads(j))

    def __create_widgets(self):
        self.title("LOVEBEET")
        child = tk.Toplevel(self)
        child.protocol("WM_DELETE_WINDOW", self.destroy)
        self.__label_image = tk.Label(child)
        self.__label_image.pack()

        self.focus()

        menu = tk.Menu(self)
        menu1 = tk.Menu(menu, tearoff=0)
        menu1.add_command(label="Load Setting", command=self.__load_setting)
        menu1.add_command(label="Save Setting", command=self.__save_setting)
        menu1.add_separator()
        menu1.add_command(label="Save Image", command=self.__save_image)
        menu1.add_separator()
        menu1.add_command(label="Quit", command=self.quit)
        menu.add_cascade(label="File", menu=menu1)

        menu2 = tk.Menu(menu, tearoff=0)
        menu2.add_command(label="Type 1", command=self.__preset1)
        menu2.add_command(label="Type 2", command=self.__preset2)
        menu.add_cascade(label="Preset", menu=menu2)

        self.config(menu=menu)

        frame = tk.LabelFrame(self, text="foreground")
        frame.pack(padx=10, pady=10, anchor="w")

        self.__r1 = tk.IntVar()
        tk.Scale(frame, from_=0, to=255, length=100, variable=self.__r1, label="red1", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=0, column=0)

        self.__g1 = tk.IntVar()
        tk.Scale(frame, from_=0, to=255, length=100, variable=self.__g1, label="green1", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=0, column=1)

        self.__b1 = tk.IntVar()
        tk.Scale(frame, from_=0, to=255, length=100, variable=self.__b1, label="blue1", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=0, column=2)

        self.__r2 = tk.IntVar()
        tk.Scale(frame, from_=0, to=255, length=100, variable=self.__r2, label="red2", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=1, column=0)

        self.__g2 = tk.IntVar()
        tk.Scale(frame, from_=0, to=255, length=100, variable=self.__g2, label="green2", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=1, column=1)

        self.__b2 = tk.IntVar()
        tk.Scale(frame, from_=0, to=255, length=100, variable=self.__b2, label="blue2", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=1, column=2)

        self.__r3 = tk.IntVar()
        tk.Scale(frame, from_=0, to=255, length=100, variable=self.__r3, label="red3", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=2, column=0)

        self.__g3 = tk.IntVar()
        tk.Scale(frame, from_=0, to=255, length=100, variable=self.__g3, label="green3", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=2, column=1)

        self.__b3 = tk.IntVar()
        tk.Scale(frame, from_=0, to=255, length=100, variable=self.__b3, label="blue3", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=2, column=2)

        self.__width = tk.IntVar()
        tk.Scale(frame, from_=0, to=1000, length=100, variable=self.__width, label="width", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=3, column=0)

        self.__div = tk.IntVar()
        tk.Scale(frame, from_=1, to=100, length=100, variable=self.__div, label="division", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=3, column=1)

        self.__grad1 = tk.IntVar()
        tk.Scale(frame, from_=0, to=100, length=100, variable=self.__grad1, label="gradation1", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=3, column=2)

        self.__lines = tk.IntVar()
        tk.Scale(frame, from_=1, to=100, length=100, variable=self.__lines, label="lines", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=4, column=0)

        self.__angle = tk.IntVar()
        tk.Scale(frame, from_=0, to=359, length=100, variable=self.__angle, label="angle", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=4, column=1)

        frame = tk.LabelFrame(self, text="background")
        frame.pack(padx=10, pady=10, anchor="w")

        self.__r4 = tk.IntVar()
        tk.Scale(frame, from_=0, to=255, length=100, variable=self.__r4, label="red4", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=0, column=0)

        self.__g4 = tk.IntVar()
        tk.Scale(frame, from_=0, to=255, length=100, variable=self.__g4, label="green4", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=0, column=1)

        self.__b4 = tk.IntVar()
        tk.Scale(frame, from_=0, to=255, length=100, variable=self.__b4, label="blue4", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=0, column=2)

        self.__r5 = tk.IntVar()
        tk.Scale(frame, from_=0, to=255, length=100, variable=self.__r5, label="red5", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=1, column=0)

        self.__g5 = tk.IntVar()
        tk.Scale(frame, from_=0, to=255, length=100, variable=self.__g5, label="green5", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=1, column=1)

        self.__b5 = tk.IntVar()
        tk.Scale(frame, from_=0, to=255, length=100, variable=self.__b5, label="blue5", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=1, column=2)

        self.__grad2 = tk.IntVar()
        tk.Scale(frame, from_=0, to=100, length=100, variable=self.__grad2, label="gradation2", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=2, column=0)

        self.__pad = tk.IntVar()
        tk.Scale(frame, from_=0, to=100, length=100, variable=self.__pad, label="padding", orient=tk.HORIZONTAL, command=lambda _: self.__update()) \
            .grid(row=2, column=1)

        frame = tk.LabelFrame(self, text="quality")
        frame.pack(padx=10, pady=10, anchor="w")

        self.__q = tk.IntVar()
        tk.Scale(frame, from_=0, to=5, length=100, variable=self.__q, orient=tk.HORIZONTAL) \
            .grid(row=0, column=0)

        tk.Button(frame, text='update', command=lambda: self.__update(high_quality=True)) \
            .grid(row=0, column=1, padx=10, pady=5, sticky=tk.S)

        self.__preset1()


if __name__ == "__main__":
    Application().mainloop()
