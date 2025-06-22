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

APP_NAME="Black_Wind"
APP_DIR="$HOME/.local/share/apps/Black_wind"
DESKTOP_FILE="$HOME/.local/share/applications/${APP_NAME}.desktop"

loading_bar 4 "Removing application files"
if [ -d "$APP_DIR" ]; then
  rm -rf "$APP_DIR"
  echo "🗑️ Removed $APP_DIR"
else
  echo "ℹ️ Application directory not found: $APP_DIR"
fi

loading_bar 3 "Removing desktop entry"
if [ -f "$DESKTOP_FILE" ]; then
  rm "$DESKTOP_FILE"
  echo "🗑️ Removed $DESKTOP_FILE"
else
  echo "ℹ️ Desktop file not found: $DESKTOP_FILE"
fi

loading_bar 2 "Updating desktop database"
update-desktop-database "$HOME/.local/share/applications/"

loading_bar 3 "Removing from GNOME favorites"
CURRENT_FAVS=$(gsettings get org.gnome.shell favorite-apps)
if [[ $CURRENT_FAVS == *"$APP_NAME.desktop"* ]]; then
  NEW_FAVS=$(echo "$CURRENT_FAVS" | sed "s/'$APP_NAME.desktop',\? *//g")
  gsettings set org.gnome.shell favorite-apps "$NEW_FAVS"
  echo "✅ Removed $APP_NAME from GNOME favorites"
else
  echo "ℹ️ $APP_NAME not found in GNOME favorites"
fi

echo -e "\n✅ Uninstallation complete."
