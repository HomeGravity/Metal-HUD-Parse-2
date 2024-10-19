import sys
import os

# 현재 파일의 경로를 기준으로 상위 디렉토리 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from metal_hud_parse.metal_hud_parse import run_performance_analysis, get_csv_data

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QSpacerItem, QSizePolicy
from PyQt6.QtWidgets import QPushButton, QLabel
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout

from welcome_screen import WelcomeScreen


class MetalHudParse(QWidget):
    def __init__(self):
        super().__init__() #QWidget()
        
        # 디스플레이 사이즈 인스턴스 변수
        self.set_display = {
            "width": 1400,
            "height": 700,
        }
        
        self.init_ui()
        self.center()
        
        # 초기 화면
        welcome_screen = WelcomeScreen()
        self.setLayout(welcome_screen.setup_ui())

    def init_ui(self):
        self.resize(self.set_display["width"], self.set_display["height"])
        self.setWindowTitle("Main Window in PyQt")
        self.show() # Display the window on the screen
        
    # gui의 위치를 중앙에 배치합니다.
    def center(self):
        # 화면 크기 가져오기
        qr = self.frameGeometry()
        screen = QApplication.primaryScreen()
        cp = screen.availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    


def main():
    app = QApplication(sys.argv)
    window = MetalHudParse()
    app.exec()

if __name__ == '__main__':
    main()