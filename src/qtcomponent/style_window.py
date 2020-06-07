# _*_ coding:utf-8 _*_

from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QStyleOption, QStyle, QApplication, QGraphicsDropShadowEffect
from PySide2.QtGui import QPainter, Qt, QCursor, QColor, QPen, QBrush, QPainterPath
from PySide2.QtCore import Property, QPoint
from PySide2.QtWidgets import QVBoxLayout
from .auxiliary import parse_pix_width
from enum import IntEnum


class MousePosition(IntEnum):
    TopLeftPos = 11
    TopPos = 12
    TopRightPos = 13
    LeftPos = 21
    CenterPos = 22
    RightPos = 23
    BottomLeftPos = 31
    BottomPos = 32
    BottomRightPos = 33


class StyleWindow(QWidget):

    def __init__(self, parent=None):
        """
        基于QWidget的窗口，作为一些窗口的基类，提供一些基础的属性
        background_color_: 背景色， 目前只支持单色
        border_width_: 边框宽度， 为0表示没有边框
        border_color_:
        opacity_: 窗口透明度
        shadow_on_: 是否开启阴影
        shadow_color_:
        shadow_blur_: 阴影半径
        border_radius_: 四个角的弧度
        分别设置4个角的radius
        left_top_border_radius:
        left_bottom_border_radius_:
        right_top_border_radius_:
        right_bottom_border_radius_
        """
        QWidget.__init__(self, parent)

        self._border_width = 0
        self._border_indicator_width = 5
        self._mouse_left_button_pressed = False
        self._rt_pre_geometry = self.geometry()
        self._mouse_move_pre_pos = QPoint()
        self._background_color = Qt.white
        self._border_color = Qt.transparent
        self._border_width = 0
        self._border_radius = 0
        self._opacity = 1.0
        self._shadow = None
        self._main_v_layout_ = None
        self._cursor_calc_type = MousePosition.CenterPos
        # border
        self._left_top_border_radius = 0
        self._left_bottom_border_radius = 0
        self._right_top_border_radius = 0
        self._right_bottom_border_radius = 0
        self._enabled_drag = False
        self.setMouseTracking(True)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self._init_default_layout()


    def paint_style_widget(self, painter):
        style_opt = QStyleOption()
        style_opt.init(self)
        self.style().drawPrimitive(QStyle.PE_Widget, style_opt, painter)

    def paintEvent(self, event):
        """ paintEvent(self, event:PySide2.QtGui.QPaintEvent) """
        painter = QPainter(self)
        self.paint_border_background(painter)

    def border_width(self):
        return self._border_width

    def set_border_width(self, width):
        self._border_width = parse_pix_width(width)
        if self._main_v_layout_ is not None:
            self._main_v_layout_.setContentsMargins(self._border_width, self._border_width, self._border_width, self._border_width)

    border_width_ = Property(str, fget=border_width, fset=set_border_width)

    def border_indicator_width(self):
        return self._border_indicator_width

    def set_border_indicator_width(self, width):
        self._border_indicator_width = parse_pix_width(width)

    border_indicator_width_ = Property(str, fget=border_indicator_width, fset=set_border_indicator_width)

    def mouseMoveEvent(self, event):
        """ mouseMoveEvent(self, event:PySide2.QtGui.QMouseEvent) """
        if self._enabled_drag:
            if self.isMaximized() is not True and self.isFullScreen() is not True:
                self._set_cursor_shape(self._calc_cursor_pos(event.pos(), self._calc_cursor_col(event.pos())))
            if self._mouse_left_button_pressed and MousePosition.CenterPos != self._cursor_calc_type:
                self._drag_resize()
        super(StyleWindow, self).mouseMoveEvent(event)

    def _set_cursor_shape(self, pos):
        """setCurSorShape(self, pos:StyleWindow.MousePosition)"""
        cursor_shape = Qt.ArrowCursor
        if MousePosition.TopLeftPos == pos or MousePosition.BottomRightPos == pos:
            cursor_shape = Qt.SizeFDiagCursor
        elif MousePosition.LeftPos == pos or MousePosition.RightPos == pos:
            cursor_shape = Qt.SizeHorCursor
        elif MousePosition.BottomLeftPos == pos or MousePosition.TopRightPos == pos:
            cursor_shape = Qt.SizeBDiagCursor
        elif MousePosition.BottomPos == pos or MousePosition.TopPos == pos:
            cursor_shape = Qt.SizeVerCursor
        self.setCursor(cursor_shape)

    def _calc_cursor_col(self, pt):
        """calCursorCol(self, pt:PySide2.QtCore.QPoint)"""
        res = 3
        x = pt.x()
        if x < self.border_indicator_width():
            res = 1
        elif x < self.width() - self.border_indicator_width():
            res = 2
        return res

    def _calc_cursor_pos(self, pt, bit):
        """calCursorCol(self, pt:PySide2.QtCore.QPoint, bit)"""
        result = bit
        y = pt.y()
        if y < self.border_indicator_width():
            result += 10
        elif y > self.height() - self.border_indicator_width():
            result += 30
        else:
            result += 20

        return result

    def mousePressEvent(self, event):
        """ mousePressEvent(self, event:PySide2.QtGui.QMouseEvent) """
        if self._enabled_drag:
            self.set_calc_mouse_type(self._calc_cursor_pos(event.pos(), self._calc_cursor_col(event.pos())))
            if Qt.LeftButton == event.button() and MousePosition.CenterPos != self._cursor_calc_type:
                self._mouse_left_button_pressed = True
            self._rt_pre_geometry = self.geometry()
            self._mouse_move_pre_pos = event.globalPos()
        super(StyleWindow, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """ mousePressEvent(self, event:PySide2.QtGui.QMouseEvent) """
        self._mouse_left_button_pressed = False
        QApplication.restoreOverrideCursor()
        super(StyleWindow, self).mouseReleaseEvent(event)

    def _drag_resize(self):
        mouse_cur_pos = QCursor.pos()
        move_pos = mouse_cur_pos - self._mouse_move_pre_pos
        after_resize_geometry = self._rt_pre_geometry
        if MousePosition.TopLeftPos == self._cursor_calc_type:
            after_resize_geometry.setTopLeft(self._rt_pre_geometry.topLeft() + move_pos)
        elif MousePosition.LeftPos == self._cursor_calc_type:
            after_resize_geometry.setLeft(self._rt_pre_geometry.left() + move_pos.x())
        elif MousePosition.BottomLeftPos == self._cursor_calc_type:
            after_resize_geometry.setBottomLeft(self._rt_pre_geometry.bottomLeft() + move_pos)
        elif MousePosition.BottomPos == self._cursor_calc_type:
            after_resize_geometry.setBottom(self._rt_pre_geometry.bottom() + move_pos.y())
        elif MousePosition.BottomRightPos == self._cursor_calc_type:
            after_resize_geometry.setBottomRight(self._rt_pre_geometry.bottomRight() + move_pos)
        elif MousePosition.RightPos == self._cursor_calc_type:
            after_resize_geometry.setRight(self._rt_pre_geometry.right() + move_pos.x())
        elif MousePosition.TopRightPos == self._cursor_calc_type:
            after_resize_geometry.setTopRight(self._rt_pre_geometry.topRight() + move_pos)
        elif MousePosition.TopPos == self._cursor_calc_type:
            after_resize_geometry.setTop(self._rt_pre_geometry.top() + move_pos.y())

        self.setGeometry(after_resize_geometry)
        self._mouse_move_pre_pos = mouse_cur_pos
        self._rt_pre_geometry = after_resize_geometry

    def background_color(self):
        return self._background_color

    def set_background_color(self, clr):
        self._background_color = clr

    background_color_ = Property(QColor, fget=background_color, fset=set_background_color)

    def border_color(self):
        return self._border_color

    def set_border_color(self, clr):
        self._border_color = clr

    border_color_ = Property(QColor, fget=border_color, fset=set_border_color)

    def border_radius(self):
        return self._border_radius

    def set_border_radius(self, radius):
        self._border_radius = parse_pix_width(radius)

    border_radius_ = Property(str, fget=border_radius, fset=set_border_radius)

    def paint_border_background(self, painter):
        """paint_border_background(self, painter:PySide2.QtGui.QPainter)"""
        painter.save()
        pen = QPen()
        pen.setColor(self.border_color())
        pen.setWidth(self.border_width())
        painter.setPen(pen)
        brush = QBrush(self.background_color())
        painter.setBrush(brush)
        painter.setOpacity(self.opacity())
        # painter.setRenderHint(QPainter.Antialiasing)
        rc = self.rect()
        paint_path = QPainterPath()
        # adjust shadow
        if self._shadow is not None:
            rc.adjust(self.shadow_blur(), self.shadow_blur(), -self.shadow_blur(), -self.shadow_blur())

        # self._calc_background_path(rc, paint_path)
        if self._calc_background_path(rc, paint_path):
            painter.setRenderHint(QPainter.Antialiasing)

        if self.border_width() > 0:
            painter.drawPath(paint_path)
        else:
            painter.fillPath(paint_path, brush)

        painter.restore()

    def set_opacity(self, opacity):
        self._opacity = opacity

    def opacity(self) -> float:
        return self._opacity

    opacity_ = Property(float, fget=opacity, fset=set_opacity)

    def resizeEvent(self, event):
        super(StyleWindow, self).resizeEvent(event)
        # self.setGeometry(5, 5, self.width() - 5, self.height() - 5)

    def set_shadow(self, on):
        if on:
            self._shadow = QGraphicsDropShadowEffect(self)
            self._shadow.setOffset(0.0, 0.0)
            self._shadow.color()
            self.setGraphicsEffect(self._shadow)
            self.setGeometry(5, 5, self.width() - 5, self.height() - 5)

    def shadow(self):
        return self._shadow

    shadow_on_ = Property(bool, fget=shadow, fset=set_shadow)

    def shadow_color(self):
        if self._shadow is not None:
            return self._shadow.color()

    def set_shadow_color(self, color):
        if self._shadow is not None:
            self._shadow.setColor(color)

    shadow_color_ = Property(QColor, fget=shadow_color, fset=set_shadow_color)

    def shadow_blur(self):
        if self._shadow is not None:
            return self._shadow.blurRadius()
        return 0

    def set_shadow_blur(self, pix_blur):
        if self._shadow is not None:
            blur = parse_pix_width(pix_blur)
            self._shadow.setBlurRadius(blur)
            self.set_border_indicator_width(blur + self.border_indicator_width())
            if self._main_v_layout_ is not None:
                self._main_v_layout_.setContentsMargins(blur + self.border_width(), blur + self.border_width(),
                                                        blur - 1 + self.border_width(), blur + self.border_width())

    shadow_blur_ = Property(str, fget=shadow_blur, fset=set_shadow_blur)

    def _init_default_layout(self):
        """setting a default QVBoxLayout"""
        self._main_v_layout_ = QVBoxLayout(self)
        self._main_v_layout_.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._main_v_layout_)

    def set_left_top_border_radius(self, radius):
        self._left_top_border_radius = parse_pix_width(radius)

    def left_top_border_radius(self):
        if self._left_top_border_radius:
            return self._left_top_border_radius
        return self.border_radius()

    left_top_border_radius_ = Property(str, fget=left_top_border_radius, fset=set_left_top_border_radius)

    def set_left_bottom_border_radius(self, radius):
        self._left_bottom_border_radius = parse_pix_width(radius)

    def left_bottom_border_radius(self):
        if self._left_bottom_border_radius:
            return self._left_bottom_border_radius
        return self.border_radius()

    left_bottom_border_radius_ = Property(str, fget=left_bottom_border_radius, fset=set_left_bottom_border_radius)

    def set_right_top_border_radius(self, radius):
        self._right_top_border_radius = parse_pix_width(radius)

    def right_top_border_radius(self):
        if self._right_top_border_radius:
            return self._right_top_border_radius
        return self.border_radius()

    right_top_border_radius_ = Property(str, fget=right_top_border_radius, fset=set_right_top_border_radius)

    def set_right_bottom_border_radius(self, radius):
        self._right_bottom_border_radius = parse_pix_width(radius)

    def right_bottom_border_radius(self):
        if self._right_bottom_border_radius:
            return self._right_bottom_border_radius
        return self.border_radius()

    right_bottom_border_radius_ = Property(str, fget=right_bottom_border_radius, fset=set_right_bottom_border_radius)

    def _calc_background_path(self, rc, painter_path):

        render_hint = False
        if self.border_radius():
            painter_path.addRoundedRect(rc, self.border_radius(), self.border_radius())
            render_hint = True
        else:
            if self.left_top_border_radius() or self.left_bottom_border_radius() \
                    or self.right_top_border_radius() or self.right_bottom_border_radius():
                # add radius
                render_hint = True
            radius_angle = 90.0
            rotate_angle = 90.0
            painter_path.moveTo(rc.left(), rc.top())
            painter_path.arcTo(rc.left(), rc.top(), self.left_top_border_radius(), self.left_top_border_radius(),
                               rotate_angle, radius_angle)
            painter_path.lineTo(rc.left(), rc.bottom() - self.left_bottom_border_radius() / 2)
            painter_path.arcTo(rc.left(), rc.bottom() - self.left_bottom_border_radius(),
                               self.left_bottom_border_radius(), self.left_bottom_border_radius(), rotate_angle * 2,
                               radius_angle)
            painter_path.lineTo(rc.right() - self.right_bottom_border_radius() / 2, rc.bottom())
            painter_path.arcTo(rc.right() - self.right_bottom_border_radius(),
                               rc.bottom() - self.right_bottom_border_radius(), self.right_bottom_border_radius(),
                               self.right_bottom_border_radius(), rotate_angle * 3, radius_angle)
            painter_path.lineTo(rc.right(), rc.top() - self.right_top_border_radius() / 2)
            painter_path.arcTo(rc.right() - self.right_top_border_radius(), rc.top(), self.right_top_border_radius(),
                               self.right_top_border_radius(), rotate_angle * 4 % rotate_angle, radius_angle)
            painter_path.lineTo(rc.left() + self.left_top_border_radius() / 2, rc.top())

        return render_hint

    def set_layout(self, layout):
        if self._main_v_layout_ is not None:
            self._main_v_layout_.addLayout(layout)

    @property
    def mouse_drag_enabled(self):
        return self._enabled_drag

    @mouse_drag_enabled.setter
    def mouse_drag_enabled(self, drag):
        self._enabled_drag = drag

    def _mouse_drag_is_center_type(self):
        if self._cursor_calc_type == MousePosition.CenterPos:
            return True
        return False

    def set_calc_mouse_type(self, mouse_type: MousePosition):
        self._cursor_calc_type = mouse_type
