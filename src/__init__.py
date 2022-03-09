from typing import Tuple, List

from aqt import mw
from aqt.qt import *
from aqt.gui_hooks import reviewer_will_show_context_menu, state_shortcuts_will_change

from .dialog import RecordingHistoryDialog
from .consts import *
from .record import monkeypatch_recording

config = mw.addonManager.getConfig(__name__)


def open_dialog():
    dialog = RecordingHistoryDialog(mw, mw.reviewer.card.id)
    dialog.show()


def add_menu_item(reviewer, menu: QMenu):
    action = menu.addAction(ADDON_NAME)
    action.setShortcut(config["shortcut"])
    qconnect(action.triggered, open_dialog)


def add_state_shortcut(state: str, shortcuts: List[Tuple[str, Callable]]) -> None:
    if state == "review":
        shortcuts.append((config["shortcut"], open_dialog))


monkeypatch_recording()
reviewer_will_show_context_menu.append(add_menu_item)
state_shortcuts_will_change.append(add_state_shortcut)
