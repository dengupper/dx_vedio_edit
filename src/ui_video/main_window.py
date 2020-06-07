# _*_ coding:utf-8 _*_

# from PySide2.QtWidgets import QPushButton
from PySide2.QtCore import Qt, QPoint
from qtcomponent import StyleWindow
from PySide2.QtWidgets import QDesktopWidget, QVBoxLayout, QBoxLayout
from qtcomponent import Title


class MainWindow(StyleWindow):
    def __init__(self, parent=None):
        StyleWindow.__init__(self, parent)
        self.init_window_attr()
        self.setObjectName("MainWindow")
        self._title = None
        self.mouse_drag_enabled = True
        self._content_layout = None
        self._init_view()

    def init_window_attr(self):
        """
        初始化window falg & window attributes
        """
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)

    def init_title(self, layout: QBoxLayout):
        self._title = Title()
        self._title.setObjectName("MainTitle")
        self._title.setFixedHeight(40)
        self._title.title_text = self.tr("DVideoEditTools")
        self._title.close.connect(self.close)
        self._title.show_minimized.connect(self.showMinimized)
        self._title.show_maximized.connect(self.show_max_normal)
        layout.addWidget(self._title)

    def _init_view(self):
        self._content_layout = QVBoxLayout()
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self.set_layout(self._content_layout)
        self.init_title(self._content_layout)
        self._content_layout.addStretch(0)

    def move_center(self):
        screen_rect = QDesktopWidget().availableGeometry()
        x = (screen_rect.right() - self.width()) / 2
        y = (screen_rect.bottom() - self.height()) / 2
        center_pos = QPoint(int(x), int(y))
        self.move(center_pos)

    def show_max_normal(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()