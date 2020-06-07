# _*_ encoding: utf-8 _*_

import PySide2
from PySide2.QtWidgets import QPushButton, QWidget, QStyleOption, QStyle
from PySide2.QtGui import QPixmap, QPainter
from PySide2.QtCore import Property, Qt


class DImageButton(QPushButton):
    """图片按钮，只支持设置一个图片不支持文字等设置"""

    def __init__(self, parent=None):
        super(DImageButton, self).__init__(parent)
        self._icon_list = []

    def paintEvent(self, event: PySide2.QtGui.QPaintEvent):
        # super(DImageButton, self).paintEvent(event)
        # paint background
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        style_opt = QStyleOption()
        style_opt.init(self)
        if len(self._icon_list) < 4:
            return
        pix = self._icon_list[0]
        if self.isEnabled():
            if style_opt.state & QStyle.State_MouseOver:
                pix = self._icon_list[1]
            elif style_opt.state & QStyle.State_Selected:
                pix = self._icon_list[2]
        else:
            pix = self._icon_list[3]
        # x = abs(int((self.width() - pix.width()) / 2))
        # y = abs(int((self.height() - pix.height()) / 2))
        painter.drawPixmap(0, 0, pix)

    def icon_list(self):
        return self._icon_list

    def set_icon_list(self, lst: str):
        pix_lst = lst.split(",")
        for path in pix_lst:
            self._icon_list.append(QPixmap(path.strip()))

    icon_list_ = Property(str, fget=icon_list, fset=set_icon_list)

    def enterEvent(self, event:PySide2.QtCore.QEvent):
        self.setCursor(Qt.ArrowCursor)
        super(DImageButton, self).enterEvent(event)
   