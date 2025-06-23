## Black_Window

A Linux tool that grabs exclusive control over keyboard and mouse input by displaying a fullscreen black window with a hidden mouse cursor. It also streams random data into named pipes in `/dev/shm/*.pipe` as part of its operation.

---

## Legal Disclaimer ⛔

**Use this tool responsibly.**

* This software is provided for educational and lawful use cases such as kiosk setups, security research, or controlled environments requiring exclusive input control.
* The author **is not responsible** for any illegal, malicious, or unauthorized use of this software.
* Users assume all responsibility and risk arising from the use or misuse of this tool.
* Ensure you have proper authorization and permissions before running this software on any system.

---

## 📦 Installation


**Run the install script**:

   ```bash
   ./install.sh
   ```

   The script will:

   * Copy required files to your local app directory.
   * Prompt you for a SECRET key.
   * Create a `.desktop` launcher.
   * Install the required Python dependency (`python-xlib`).
   * Add Black Wind to your GNOME favorites.

---

## 🧹 Uninstallation

**Run the uninstaller**:

   ```bash
   ./uninstall.sh
   ```

   This will:

   * Remove the app files and launcher.
   * Update the desktop environment.
   * Remove Black Wind from your GNOME favorites.

---

## ⚙️ Requirements

* Linux system with GNOME desktop
* Python and `pip` installed
* `gnome-terminal` (used to run the app script)
* `python-xlib` (installed automatically)


---

## How It Works

* The Bash script detects dynamic named pipes in `/dev/shm` and launches background processes writing random data into these pipes.
* The Python script connects to the X server, grabs keyboard and mouse input exclusively, and creates a fullscreen black window with the mouse cursor hidden using Tkinter.
* Keyboard and mouse events are blocked from reaching other applications, effectively locking user input to this fullscreen window.
* When the window closes, input grabs are released, restoring normal system input behavior.

---

## License

This project is released under the MIT License.
