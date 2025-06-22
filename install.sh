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
TARG_PATH="$HOME/.local/share/"
APP_PATH="$TARG_PATH/apps/Black_wind"
DESK_DIR="$TARG_PATH/applications"
DESK_FILE="$DESK_DIR/Black_Wind.desktop"

loading_bar 4 "Creating directory"
mkdir -p "$APP_PATH"

loading_bar 3 "Copying Files"
cp "./src/app_icon.png" "$APP_PATH/image.png"
cp "./src/Black_win.sh" "$APP_PATH/Black_win.sh"
cp "./src/freeze_script.py" "$APP_PATH/freeze_script.py"

loading_bar 6 "Creating .desktop file"
cat > "$DESK_FILE" <<EOF
[Desktop Entry]
Name=Black Wind by IACEENE
Comment=Launch Black Wind by IACEENE
Exec=gnome-terminal --geometry=10x10 -- bash -c '$HOME/.local/share/apps/Black_win/Black_win.sh'
Icon=$APP_PATH/image.png
Terminal=false
Type=Application
Categories=Development;Utility;
EOF

loading_bar 3 "Updating desktop database"
update-desktop-database "$HOME/.local/share/applications/"

loading_bar 4 "Adding to GNOME favorites"
APP="Black_Wind.desktop"
FAVS=$(gsettings get org.gnome.shell favorite-apps)
if [[ $FAVS != *"$APP"* ]]; then
  NEW_FAVS=$(echo "$FAVS" | sed "s/]$/, '$APP']/")
  gsettings set org.gnome.shell favorite-apps "$NEW_FAVS"
fi

loading_bar 5 "Installing Python dependency (python-xlib)"
cd $APP_PATH
pip install python-xlib

echo -e "\n✅ Setup completed successfully!"
echo  "Thanks to IACEENE"
