from typing import Tuple, List

import aqt
from aqt.qt import *
from aqt.gui_hooks import (
    reviewer_will_show_context_menu,
    state_shortcuts_will_change,
    reviewer_did_answer_card,
)
from aqt.reviewer import Reviewer
from aqt.browser.previewer import Previewer
from anki.cards import Card
from anki.hooks import wrap

from .dialog import RecordingHistoryDialog
from .consts import *
from .record import monkeypatch_recording


def open_dialog(parent: QWidget, card_id: int):
    if card_id:
        dialog = RecordingHistoryDialog(parent, card_id)
        dialog.show()


def add_menu_item(reviewer, menu: QMenu):
    action = menu.addAction(ADDON_NAME)
    action.setShortcut(config["shortcut"])
    qconnect(action.triggered, lambda: open_dialog(mw, reviewer.card.id))


def add_state_shortcut(state: str, shortcuts: List[Tuple[str, Callable]]) -> None:
    if state == "review":
        shortcuts.append(
            (config["shortcut"], lambda: open_dialog(mw, mw.reviewer.card.id))
        )


def clear_last_recording_reference(reviewer: Reviewer, card: Card, ease) -> None:
    # Clear reference of the last recording of the answered card so that a recording only plays on its card
    reviewer._recordedAudio = None


def add_previewer_shortcut(previewer: Previewer):
    action = QAction(ADDON_NAME, previewer)
    action.setShortcut(config["shortcut"])
    qconnect(action.triggered, lambda: open_dialog(previewer, previewer.card().id))
    previewer.addAction(action)


if aqt.mw:
    mw = aqt.mw
    config = mw.addonManager.getConfig(__name__)
    monkeypatch_recording()
    reviewer_will_show_context_menu.append(add_menu_item)
    state_shortcuts_will_change.append(add_state_shortcut)
    reviewer_did_answer_card.append(clear_last_recording_reference)
    Previewer.open = wrap(Previewer.open, add_previewer_shortcut, "after")
