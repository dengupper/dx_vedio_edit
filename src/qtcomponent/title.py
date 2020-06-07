# _*_ coding:utf-8 _*_

from .style_window import StyleWindow
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PySide2.QtCore import Property, Qt, QPoint, Signal
from .image_button import DImageButton
from enum import IntEnum


class Title(StyleWindow):

    class TitleControl(IntEnum):
        TitleLog = 1 << 1,
        TitleText = 1 << 2,
        TitleMinimized = 1 << 3,
        TitleMaximized = 1 << 4,
        TitleClose = 1 << 5

    def __init__(self, parent=None):
        super(Title, self).__init__(parent)
        self._layout = None
        self._enabled_movie = False  # 是否支持拖动
        self._left_button_pressed = False
        self._pressed_pos = QPoint()
        self._log = None
        self._title = None
        self._maximize_btn = None
        self._minimize_btn = None
        self._close_btn = None
        self.mouse_drag_enabled = False
        self._init_def_layout()
        self.set_show_title_ctrls(self.TitleControl.TitleText
                     | self.TitleControl.TitleMinimized | self.TitleControl.TitleMaximized | self.TitleControl.TitleClose)
        
    close = Signal()
    show_minimized = Signal()
    show_maximized = Signal()

    def _init_def_layout(self):
        self._layout = QHBoxLayout()
        self.set_layout(self._layout)
        self._layout.setContentsMargins(5, 0, 10, 5)
        self._layout.setSpacing(10)
        #
        self._log = QLabel()
        self._log.setObjectName("Title_LogLabel")
        self._layout.addWidget(self._log)
        self._log.hide()
        self._title = QLabel()
        self._title.setObjectName("Title_TitleLabel")
        self._layout.addWidget(self._title)
        # self._title.hide()
        self._layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed))
        # close button
        self._close_btn = DImageButton()
        self._close_btn.setObjectName("Title_CloseButton")
        self._maximize_btn = DImageButton()
        self._maximize_btn.setObjectName("Title_MaximizeButton")
        self._minimize_btn = DImageButton()
        self._minimize_btn.setObjectName("Title_MinimizeButton")
        self._layout.addWidget(self._minimize_btn, 0, Qt.AlignRight)
        self._layout.addWidget(self._maximize_btn, 0, Qt.AlignRight)
        self._layout.addWidget(self._close_btn, 0, Qt.AlignRight)

        #self._close_btn.hide()
        self._maximize_btn.hide()
        # self._minimize_btn.hide()

        self._close_btn.clicked.connect(self.close)
        self._minimize_btn.clicked.connect(self.show_minimized)
        self._maximize_btn.clicked.connect(self.show_maximized)

    def log(self):
        return self._log

    def set_log(self, pix: QPixmap):
        self._log_label.setPixmap(pix)

    log_ = Property(QPixmap, fget=log, fset=set_log)

    @property
    def enabled_movie(self):
        return self._enabled_movie

    @enabled_movie.setter
    def enabled_movie(self, enabled):
        self._enabled_movie = enabled

    def mousePressEvent(self, event):
        self.set_calc_mouse_type(self._calc_cursor_pos(event.pos(), self._calc_cursor_col(event.pos())))
        if self._mouse_drag_is_center_type():
            if Qt.LeftButton == event.button() and self.parent() is not None:
                self._left_button_pressed = True
                self._pressed_pos = event.globalPos() - self.parent().pos()
        super(Title, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._left_button_pressed = False
        super(Title, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self._mouse_drag_is_center_type():
            if self._left_button_pressed and self.parent() is not None:
                self.parent().move(event.globalPos() - self._pressed_pos)
        super(Title, self).mouseMoveEvent(event)

    @property
    def title_text(self):
        return self._title.text()
    
    @title_text.setter
    def title_text(self, text):
        self._title.setText(text)
    
    def set_show_title_ctrls(self, ctrls):
        """设置标题需要显示的控件"""
        self._log.setVisible(ctrls & self.TitleControl.TitleLog)
        self._title.setVisible(ctrls & self.TitleControl.TitleText)
        self._minimize_btn.setVisible(ctrls & self.TitleControl.TitleMinimized)
        self._maximize_btn.setVisible(ctrls & self.TitleControl.TitleMaximized)
        self._close_btn.setVisible(ctrls & self.TitleControl.TitleClose)