# _*_ coding:utf-8 _*_

from qtcomponent import StyleWindow
from PySide2.QtWidgets import QHBoxLayout

class HomePage(StyleWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.init_page()
    
    def init_page(self):
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins()
        self.set_layout(main_layout)
        
        