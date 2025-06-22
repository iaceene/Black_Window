## Black_Window

A Linux tool that grabs exclusive control over keyboard and mouse input by displaying a fullscreen black window with a hidden mouse cursor. It also streams random data into named pipes in `/dev/shm/*.pipe` as part of its operation.

---

## Contents

- `Black_win.sh` — Bash script that streams `/dev/random` into dynamic named pipes and launches the Python fullscreen input grabber.  
- `freeze_script.py` — Python script that creates a fullscreen black window, grabs keyboard and mouse input exclusively using X11, and hides the mouse cursor.

---

## Features

- Grabs all keyboard and mouse input exclusively using X11, preventing other applications from receiving input events.  
- Displays a fullscreen black window using Tkinter with the mouse cursor hidden for a clean and locked-down user experience.  
- Streams entropy from `/dev/random` into named pipes located in `/dev/shm/*.pipe` in the background, dynamically handling pipe names.  
- Ensures proper release of grabbed inputs when the program exits.

---

## Requirements

- Linux system running X11 (e.g., most Linux desktop environments)  
- Python 3.x  
- `python-xlib` Python package (`pip install python-xlib`)  
- `tkinter` (usually included with Python)  

---

## Installation

1. Clone or download this repository:  
    ```bash
    git clone https://github.com/yaajagro/Black_Window.git
    cd Black_Window
    ```

2. Install Python dependencies:  
    ```bash
    pip install python-xlib
    ```

3. Make the Bash script executable:  
    ```bash
    chmod +x Black_win.sh
    ```

---

## Usage

Run the Bash script `Black_win.sh`, which:

- Finds all named pipes matching `/dev/shm/*.pipe` and streams `/dev/random` into them in the background.  
- Then runs the fullscreen input grabber Python script `freeze_script.py`.

```bash
./Black_win.sh
````

---

## How It Works

* The Bash script detects dynamic named pipes in `/dev/shm` and launches background processes writing random data into these pipes.
* The Python script connects to the X server, grabs keyboard and mouse input exclusively, and creates a fullscreen black window with the mouse cursor hidden using Tkinter.
* Keyboard and mouse events are blocked from reaching other applications, effectively locking user input to this fullscreen window.
* When the window closes, input grabs are released, restoring normal system input behavior.

---

## Legal Disclaimer

**Use this tool responsibly.**

* This software is provided for educational and lawful use cases such as kiosk setups, security research, or controlled environments requiring exclusive input control.
* The author **is not responsible** for any illegal, malicious, or unauthorized use of this software.
* Users assume all responsibility and risk arising from the use or misuse of this tool.
* Ensure you have proper authorization and permissions before running this software on any system.

---

## License

This project is released under the MIT License.

---

## Contact

For questions or support, please open an issue on the GitHub repository.

---

*Thank you for using Black Window!*
