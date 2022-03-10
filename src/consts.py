import os

from aqt.qt import QIcon

ADDON_NAME = "Record Own Voice History"
ADDON_DIR = os.path.dirname(__file__)
USER_FILES = os.path.join(ADDON_DIR, "user_files")
RECORDINGS_DIR = os.path.join(USER_FILES, "recordings")
os.makedirs(RECORDINGS_DIR, exist_ok=True)
ICONS_DIR = os.path.join(ADDON_DIR, "icons")
PLAY_BUTTON_ICON = QIcon(os.path.join(ICONS_DIR, "play-fill.svg"))
DELETE_BUTTON_ICON = QIcon(os.path.join(ICONS_DIR, "x-square-fill.svg"))
FOLDER_BUTTON_ICON = QIcon(os.path.join(ICONS_DIR, "folder-fill.svg"))
