import datetime

from aqt.qt import *
from aqt.sound import av_player
from aqt.utils import openFolder

from .consts import consts
from .gui.dialog import Dialog
from .record import get_card_recordings_dir, get_recordings


class RecordingWidgetButton(QPushButton):
    def __init__(self, icon: QIcon, parent: QWidget):
        super().__init__(parent)
        self.setIcon(icon)
        self.setMaximumSize(32, 32)
        self.setFlat(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class RecordingWidget(QWidget):
    def __init__(
        self, file: os.DirEntry, item: QListWidgetItem, list_widget: QListWidget
    ):
        super().__init__(list_widget)

        self.file = file
        self.item = item
        self.list_widget = list_widget

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(file.name))
        date = datetime.datetime.fromtimestamp(file.stat().st_ctime).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        hbox.addWidget(QLabel(date))
        play_button = RecordingWidgetButton(
            QIcon(str(consts.dir / "icons" / "play-fill.svg")), self
        )
        qconnect(play_button.clicked, self.on_play)
        delete_button = RecordingWidgetButton(
            QIcon(str(consts.dir / "icons" / "x-square-fill.svg")), self
        )
        qconnect(delete_button.clicked, self.on_delete)
        hbox.addWidget(play_button)
        hbox.addWidget(delete_button)
        self.setLayout(hbox)

    def on_play(self) -> None:
        av_player.play_file(self.file.path)

    def on_delete(self) -> None:
        os.remove(self.file.path)
        self.list_widget.takeItem(self.list_widget.indexFromItem(self.item).row())
        self.close()


class RecordingHistoryDialog(Dialog):
    key = "recording_history"

    def __init__(self, parent: QWidget, card_id: int):
        self.card_id = card_id
        super().__init__(parent)

    def setup_ui(self) -> None:
        super().setup_ui()
        self.setWindowTitle(consts.name)
        vbox = QVBoxLayout()
        self.label = QLabel(f"Recordings of card {self.card_id}", self)
        self.open_folder_button = RecordingWidgetButton(
            QIcon(str(consts.dir / "icons" / "folder-fill.svg")), self
        )
        qconnect(
            self.open_folder_button.clicked,
            lambda: openFolder(str(self.recordings_folder)),
        )
        widget = QWidget()
        hbox = QHBoxLayout()
        hbox.addWidget(self.label)
        hbox.addWidget(self.open_folder_button)
        widget.setLayout(hbox)
        vbox.addWidget(widget)
        list_widget = self.list_widget = QListWidget(self)
        vbox.addWidget(list_widget)
        self.setLayout(vbox)
        self.recordings_folder = get_card_recordings_dir(self.card_id)
        files = get_recordings(self.card_id)

        for file in files:
            item = QListWidgetItem(list_widget)
            list_widget.addItem(item)
            widget = RecordingWidget(file, item, list_widget)
            item.setSizeHint(widget.minimumSizeHint())
            list_widget.setItemWidget(item, widget)
