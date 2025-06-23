import os
import tkinter as tk
import argparse
import threading
from Xlib import X, display
from Xlib.ext import record
from Xlib.protocol import rq, event

# Grab all keyboard and mouse input
def grab_inputs(disp):
    root = disp.screen().root

    result = root.grab_keyboard(True, X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime)
    if result != X.GrabSuccess:
        print("Failed to grab keyboard")
        return False

    result = root.grab_pointer(True,
                               X.ButtonPressMask | X.ButtonReleaseMask | X.PointerMotionMask,
                               X.GrabModeAsync, X.GrabModeAsync, X.NONE, X.NONE, X.CurrentTime)
    if result != X.GrabSuccess:
        print("Failed to grab pointer")
        root.ungrab_keyboard(X.CurrentTime)
        return False

    return True

def ungrab_inputs(disp):
    disp.screen().root.ungrab_keyboard(X.CurrentTime)
    disp.screen().root.ungrab_pointer(X.CurrentTime)

# Convert keysym to string
def keycode_to_char(keysym):
    from Xlib.XK import keysym_to_string
    return keysym_to_string(keysym)

def main():
    # --- Argument parsing ---
    parser = argparse.ArgumentParser(description="Screen lock script with optional debug.")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode (auto-unlock after 10s)")
    args = parser.parse_args()
    debug_mode = args.debug

    if debug_mode:
        print("Debug mode enabled. Screen will unlock after 10 seconds.")

    # --- Load password ---
    if not os.path.exists('.secret'):
        print("No .secret file found.")
        return

    with open('.secret', 'r') as f:
        password = f.read().strip().lower()

    typed = ""  # Buffer for typed characters

    # Connect to X server
    disp = display.Display()

    # Grab inputs
    if not grab_inputs(disp):
        print("Cannot grab input, exiting.")
        return

    # Setup tkinter window
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(background='black')
    root.config(cursor="none")

    # Block all input events in tkinter
    for seq in ["<Key>", "<Button>", "<Motion>", "<MouseWheel>"]:
        root.bind_all(seq, lambda e: "break")

    # Close function
    def on_close():
        print("Unlocking...")
        ungrab_inputs(disp)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    # --- DEBUG: Auto-close after 10 seconds ---
    if debug_mode:
        root.after(10000, on_close)  # 10 seconds = 10000 ms

    # Setup X record extension
    def callback(reply):
        nonlocal typed
        if reply.category != record.FromServer:
            return
        if reply.client_swapped or not reply.data or reply.data[0] < 2:
            return

        try:
            evt = rq.EventField(None).parse_binary_value(reply.data, disp.display, None, None)
        except Exception as e:
            if debug_mode:
                print(f"Event parse error: {e}")
            return

        if isinstance(evt, event.KeyPress):
            keycode = evt.detail
            keysym = disp.keycode_to_keysym(keycode, 0)
            char = keycode_to_char(keysym)
            if char:
                char = char.lower()
                typed += char
                if debug_mode:
                    print(f"Typed so far: {typed}")
                if password in typed:
                    print("Password matched. Exiting.")
                    on_close()
                if len(typed) > 100:
                    typed = typed[-100:]

    ctx = disp.record_create_context(
        0,
        [record.AllClients],
        [{
            'core_requests': (0, 0),
            'core_replies': (0, 0),
            'ext_requests': (0, 0, 0, 0),
            'ext_replies': (0, 0, 0, 0),
            'delivered_events': (0, 0),
            'device_events': (X.KeyPress, X.KeyRelease),
            'errors': (0, 0),
            'client_started': False,
            'client_died': False,
        }]
    )

    # Run record context in a separate thread
    record_thread = threading.Thread(
        target=disp.record_enable_context,
        args=(ctx, callback),
        daemon=True
    )
    record_thread.start()

    try:
        root.mainloop()
    finally:
        ungrab_inputs(disp)
        disp.record_disable_context(ctx)
        disp.flush()

if __name__ == "__main__":
    main()
