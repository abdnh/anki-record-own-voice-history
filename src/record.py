import os
from typing import List

from aqt.utils import tooltip, tr
from aqt.sound import av_player, record_audio
from aqt.reviewer import Reviewer

from .consts import *


def get_card_recordings_dir(card_id: int) -> str:
    card_dir = os.path.join(RECORDINGS_DIR, str(card_id))
    os.makedirs(card_dir, exist_ok=True)
    return card_dir


def get_most_recent_recording(card_id: int) -> str:
    card_dir = get_card_recordings_dir(card_id)
    # FIXME: st_ctime is not actually the creation date on Unix - not a big issue for now
    files = sorted(os.scandir(card_dir), key=lambda f: f.stat().st_ctime)
    if files[-1]:
        path = files[-1].path
        return path
    else:
        return ""


def get_recordings(card_id: int) -> List[os.DirEntry]:
    card_dir = get_card_recordings_dir(card_id)
    return os.scandir(card_dir)


def save_recording(card_id: int, path: str) -> str:
    card_dir = get_card_recordings_dir(card_id)
    files = os.listdir(card_dir)
    next_num = 1
    for file in files:
        num = int(file.split(".")[0].split("_")[1])
        if num >= next_num:
            next_num = num + 1

    # FIXME: change this once we do mp3 encoding
    dest_path = os.path.join(card_dir, f"rec_{next_num:03}.wav")
    with open(path, "rb") as f:
        with open(dest_path, "wb") as df:
            df.write(f.read())

    return dest_path


def onRecordVoice(self) -> None:
    def after_record(path: str) -> None:
        card_id = self.card.id
        self._recordedAudio = save_recording(card_id, path)
        self.onReplayRecorded()

    # TODO: encode file to mp3
    record_audio(self.mw, self.mw, False, after_record)


def onReplayRecorded(self) -> None:
    if not self._recordedAudio:
        if path := get_most_recent_recording(self.card.id):
            self._recordedAudio = path
        else:
            tooltip(tr.studying_you_havent_recorded_your_voice_yet())
            return
    av_player.play_file(self._recordedAudio)


def monkeypatch_recording():
    Reviewer.onRecordVoice = onRecordVoice
    Reviewer.onReplayRecorded = onReplayRecorded
