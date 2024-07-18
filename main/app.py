import tkinter as tk

def configurar_app():
    app = tk.Tk()
    app.geometry("1280x720")
    app.configure(bg="white")
    app.resizable(width=True, height=True)
    return app
