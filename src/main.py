# _*_ coding:utf-8 _*_


import sys, os
from PySide2.QtWidgets import QApplication, QWidget
# from qtcomponent.style_window import StyleWindow
from ui_video.main_window import MainWindow

def set_style_sheet_file(app):
    with open("style/style.css", 'r+', encoding='UTF-8') as f:
        content = f.read()
        app.setStyleSheet(content)


def main():
    app = QApplication(sys.argv)
    set_style_sheet_file(app)
    # window init info
    main_wnd = MainWindow()
    main_wnd.setFixedSize(1280, 800)
    main_wnd.show()
    main_wnd.move_center()
    app.exec_()

if __name__ == '__main__':
    main()
