from typing import List, Any
import datetime

from aqt.main import AnkiQt
from aqt.qt import *
from aqt.sound import av_player

from .form import Ui_Dialog
from .record import get_recordings
from .consts import *


class RecordingListModel(QAbstractListModel):
    def __init__(self, parent: QDialog):
        super().__init__(parent=parent)
        self.files = []

    def populate(self, files: List[str]):
        self.beginResetModel()
        self.files.extend(files)
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.files)

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        return self.files[index.row()]


class RecordingWidgetButton(QPushButton):
    def __init__(self, icon: QIcon, parent):
        super().__init__(parent)
        self.setIcon(icon)
        # FIXME
        self.setMaximumSize(32, 32)
        self.setFlat(True)
        # self.setStyleSheet("QPushButton {background-color: transparent; border: 0px;}")
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class RecordingWidget(QWidget):
    def __init__(self, file: os.DirEntry, item: QListWidgetItem, list_widget):
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
        play_button = RecordingWidgetButton(PLAY_BUTTON_ICON, self)
        qconnect(play_button.clicked, self.on_play)
        delete_button = RecordingWidgetButton(DELETE_BUTTON_ICON, self)
        qconnect(delete_button.clicked, self.on_delete)
        hbox.addWidget(play_button)
        hbox.addWidget(delete_button)
        self.setLayout(hbox)

    def on_play(self):
        print(f"on_play: {self.file.path}")
        av_player.play_file(self.file.path)

    def on_delete(self):
        os.remove(self.file.path)
        self.list_widget.takeItem(self.list_widget.indexFromItem(self.item).row())
        self.close()


class RecordingHistoryDialog(QDialog):
    def __init__(self, mw: AnkiQt, card_id: int):
        super().__init__(parent=mw)
        self.form = Ui_Dialog()
        self.form.setupUi(self)
        self.setWindowTitle(ADDON_NAME)
        self.card_id = card_id
        self.setup_recordings_list()

    def setup_recordings_list(self):
        files = get_recordings(self.card_id)
        self.form.label.setText(f"Recordings of card {self.card_id}")

        list_widget = self.form.listWidget
        for file in files:
            item = QListWidgetItem(list_widget)
            list_widget.addItem(item)
            widget = RecordingWidget(file, item, list_widget)
            item.setSizeHint(widget.minimumSizeHint())
            list_widget.setItemWidget(item, widget)
