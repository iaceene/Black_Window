import tkinter as tk
from Xlib import X, display
from Xlib.ext import record
from Xlib.protocol import rq

# Grab all keyboard and mouse input
def grab_inputs(disp):
    root = disp.screen().root

    # Try to grab keyboard and mouse
    # Grab keyboard: asynchronously, owner_events False
    result = root.grab_keyboard(True, X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime)
    if result != X.GrabSuccess:
        print("Failed to grab keyboard")
        return False

    # Grab pointer (mouse)
    result = root.grab_pointer(True, X.ButtonPressMask | X.ButtonReleaseMask | X.PointerMotionMask,
                              X.GrabModeAsync, X.GrabModeAsync, X.NONE, X.NONE, X.CurrentTime)
    if result != X.GrabSuccess:
        print("Failed to grab pointer")
        root.ungrab_keyboard(X.CurrentTime)
        return False

    return True

def ungrab_inputs(disp):
    disp.screen().root.ungrab_keyboard(X.CurrentTime)
    disp.screen().root.ungrab_pointer(X.CurrentTime)

def main():
    # Connect to X server
    disp = display.Display()

    # Grab inputs
    if not grab_inputs(disp):
        print("Cannot grab input, exiting.")
        return

    # Setup fullscreen black tkinter window
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(background='black')

    # Hide the mouse cursor by configuring a transparent cursor
    root.config(cursor="none")

    # Bind keys and mouse inside tkinter window just in case
    root.bind_all("<Key>", lambda e: "break")
    root.bind_all("<Button>", lambda e: "break")
    root.bind_all("<Motion>", lambda e: "break")
    root.bind_all("<MouseWheel>", lambda e: "break")

    # On close, ungrab inputs
    def on_close():
        ungrab_inputs(disp)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    try:
        root.mainloop()
    finally:
        ungrab_inputs(disp)

if __name__ == "__main__":
    main()
