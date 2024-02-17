import os
import sys
from typing import List, Literal, Tuple

from anki.cards import Card
from anki.hooks import wrap
from aqt import mw
from aqt.browser.previewer import Previewer
from aqt.gui_hooks import (
    reviewer_did_answer_card,
    reviewer_will_show_context_menu,
    state_shortcuts_will_change,
)
from aqt.qt import *
from aqt.reviewer import Reviewer

sys.path.append(os.path.join(os.path.dirname(__file__), "vendor"))


from .config import config
from .consts import consts
from .dialog import RecordingHistoryDialog
from .record import monkeypatch_recording


def open_dialog(parent: QWidget, card_id: int) -> None:
    if card_id:
        dialog = RecordingHistoryDialog(parent, card_id)
        dialog.show()


def add_menu_item(reviewer: Reviewer, menu: QMenu) -> None:
    action = menu.addAction(consts.name)
    action.setShortcut(config["shortcut"])
    qconnect(action.triggered, lambda: open_dialog(mw, reviewer.card.id))


def add_state_shortcut(state: str, shortcuts: List[Tuple[str, Callable]]) -> None:
    if state == "review":
        shortcuts.append(
            (config["shortcut"], lambda: open_dialog(mw, mw.reviewer.card.id))
        )


def clear_last_recording_reference(
    reviewer: Reviewer, card: Card, ease: Literal[1, 2, 3, 4]
) -> None:
    # Clear reference of the last recording of the answered card so that a recording only plays on its card
    reviewer._recordedAudio = None


def add_previewer_shortcut(previewer: Previewer) -> None:
    action = QAction(consts.name, previewer)
    action.setShortcut(config["shortcut"])
    qconnect(action.triggered, lambda: open_dialog(previewer, previewer.card().id))
    previewer.addAction(action)


monkeypatch_recording()
reviewer_will_show_context_menu.append(add_menu_item)
state_shortcuts_will_change.append(add_state_shortcut)
reviewer_did_answer_card.append(clear_last_recording_reference)
Previewer.open = wrap(Previewer.open, add_previewer_shortcut, "after")  # type: ignore
