#!/bin/bash


loading_bar() {
  local duration=$1
  local message=$2
  echo -n "$message"
  for ((i=0; i<duration; i++)); do
    echo -n "."
    sleep 0.2
  done
  echo " Done."
}

clear

loading_bar 5 "Defining paths"
DESK_DIR="$HOME/.local/share/applications/Black_Wind"
DESK_FILE="$DESK_DIR/Black_Wind.desktop"

loading_bar 4 "Creating directory"
mkdir -p "$DESK_DIR"

loading_bar 3 "Copying icon"
cp "app_icon.png" "$DESK_DIR/image.png"

loading_bar 6 "Creating .desktop file"
cat > "$DESK_FILE" <<EOF
[Desktop Entry]
Name=Black Wind by IACEENE
Comment=Launch Black Wind by IACEENE
Exec=gnome-terminal --geometry=10x10 -- bash -c '$HOME/.local/share/apps/Black_win/Black_win.sh'
Icon=$DESK_DIR/image.png
Terminal=false
Type=Application
Categories=Development;Utility;
EOF

loading_bar 3 "Updating desktop database"
update-desktop-database "$HOME/.local/share/applications/"

loading_bar 4 "Adding to GNOME favorites (if needed)"
APP="Black_Wind.desktop"
FAVS=$(gsettings get org.gnome.shell favorite-apps)
if [[ $FAVS != *"$APP"* ]]; then
  NEW_FAVS=$(echo "$FAVS" | sed "s/]$/, '$APP']/")
  gsettings set org.gnome.shell favorite-apps "$NEW_FAVS"
fi

loading_bar 5 "Installing Python dependency (python-xlib)"
pip install python-xlib

echo -e "\n✅ Setup completed successfully!"
echo  "Thanks to IACEENE"
