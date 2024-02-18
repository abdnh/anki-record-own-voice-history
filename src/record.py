from __future__ import annotations

import os
import time
from concurrent.futures import Future
from pathlib import Path

from aqt import gui_hooks, mw
from aqt.main import AnkiQt
from aqt.qt import *
from aqt.reviewer import Reviewer
from aqt.sound import RecordDialog, _encode_mp3, av_player
from aqt.utils import showWarning, tooltip, tr
from markdown import markdown

from .consts import *


def get_card_recordings_dir(card_id: int) -> Path:
    card_dir = consts.dir / "user_files" / "recordings" / str(card_id)
    card_dir.mkdir(exist_ok=True)
    return card_dir


def get_most_recent_recording(card_id: int) -> str | None:
    files = get_recordings(card_id)
    if files:
        return files[0].path
    return None


def get_recordings(card_id: int) -> list[os.DirEntry]:
    card_dir = get_card_recordings_dir(card_id)
    # FIXME: st_ctime is not actually the creation date on Unix - not a big issue for now
    return sorted(os.scandir(card_dir), key=lambda e: e.stat().st_ctime, reverse=True)


# Adapted from https://github.com/ankitects/anki/blob/9c54f85be6f166735c3ab212bb497c6c6b15fd01/qt/aqt/sound.py


def encode_mp3(mw: AnkiQt, src_wav: str, on_done: Callable[[str], None]) -> None:
    filename = os.path.basename(src_wav.replace(".wav", "%d.mp3" % time.time()))
    dst_mp3 = str(get_card_recordings_dir(mw.reviewer.card.id) / filename)

    def _on_done(fut: Future) -> None:
        if exc := fut.exception():
            print(exc)
            showWarning(tr.editing_couldnt_record_audio_have_you_installed())
            return

        on_done(dst_mp3)

    mw.taskman.run_in_background(lambda: _encode_mp3(src_wav, dst_mp3), _on_done)


def record_audio(
    parent: QWidget, mw: AnkiQt, encode: bool, on_done: Callable[[str], None]
) -> None:
    def after_record(path: str) -> None:
        if not encode:
            on_done(path)
        else:
            encode_mp3(mw, path, on_done)

    try:
        _diag = RecordDialog(parent, mw, after_record)
    except Exception as exc:
        err_str = str(exc)
        showWarning(markdown(tr.qt_misc_unable_to_record(error=err_str)))


def onRecordVoice(self: Reviewer) -> None:
    def after_record(path: str) -> None:
        self._recordedAudio = path
        self.onReplayRecorded()

    record_audio(self.mw, self.mw, True, after_record)


def onReplayRecorded(self: Reviewer) -> None:
    if not self._recordedAudio:
        if path := get_most_recent_recording(self.card.id):
            self._recordedAudio = path
        else:
            tooltip(tr.studying_you_havent_recorded_your_voice_yet())
            return
    av_player.play_file(self._recordedAudio)


def on_reviewer_will_replay_recording(path: str) -> str:
    if not path:
        path = get_most_recent_recording(mw.reviewer.card.id)
    return path


def patch_recording() -> None:
    Reviewer.onRecordVoice = onRecordVoice  # type: ignore
    if hasattr(gui_hooks, "reviewer_will_replay_recording"):
        gui_hooks.reviewer_will_replay_recording.append(
            on_reviewer_will_replay_recording
        )
    else:
        Reviewer.onReplayRecorded = onReplayRecorded  # type: ignore
