# _*_ coding:utf-8 _*_

# from PySide2.QtWidgets import QPushButton
from PySide2.QtCore import Qt, QPoint
from qtcomponent import StyleWindow
from PySide2.QtWidgets import QDesktopWidget, QVBoxLayout, QBoxLayout, QStackedLayout
from qtcomponent import Title
from .home_page import HomePage

class MainWindow(StyleWindow):
    def __init__(self, parent=None):
        StyleWindow.__init__(self, parent)
        self.init_window_attr()
        self.setObjectName("MainWindow")
        self._title = Title()
        self.mouse_drag_enabled = True
        self._stacked_layout = QStackedLayout()
        self._init_view()

    def init_window_attr(self):
        """
        初始化window falg & window attributes
        """
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)

    def init_title(self, layout: QBoxLayout):
        self._title.setObjectName("MainTitle")
        self._title.setFixedHeight(40)
        self._title.title_text = self.tr("DVideoEditTools")
        self._title.close.connect(self.close)
        self._title.show_minimized.connect(self.showMinimized)
        self._title.show_maximized.connect(self.show_max_normal)
        layout.addWidget(self._title)

    def _init_view(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.set_layout(main_layout)
        self.init_title(main_layout)
        main_layout.addLayout(self._stacked_layout)
        
        self._stacked_layout.addWidget(HomePage())
        
        # main_layout.addStretch(0)

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