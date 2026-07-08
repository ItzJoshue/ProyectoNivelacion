from tkinter import Tk



from Vistas.app import App





def _habilitar_dpi() -> None:

    try:

        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)

    except Exception:

        pass





if __name__ == "__main__":

    _habilitar_dpi()

    root = Tk()

    App(root)

    root.mainloop()