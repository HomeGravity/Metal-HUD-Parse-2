from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtWidgets import QSpacerItem, QSizePolicy
from PyQt6.QtWidgets import QLabel, QPushButton
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt

class WelcomeScreenStyle():
    def __init__(self) -> None:
        pass
    
    def welcome_label_style(self):
        return """
QLabel {
    font-size: 24px;
    font-weight: bold;
    color: #2e7ad1;
    padding: 10px;  /* 여백 설정 */
    border-radius: 10px;  /* 둥근 모서리 */
}
QLabel:hover {
    background-color: #232a96;  /* 마우스 오버 시 색상 */
}
"""

    def load_button_style(self):
        return """
QPushButton {
    font-size: 18px;
    font-weight: bold;
    background-color: #2e7ad1;  /* 버튼 배경색 */
    color: white;  /* 버튼 텍스트 색상 */
    border: none;  /* 테두리 없애기 */
    padding: 10px;  /* 여백 설정 */
    border-radius: 10px;  /* 둥근 모서리 */
}
QPushButton:hover {
    background-color: #232a96;  /* 마우스 오버 시 색상 */
}
"""

# 초기화면 입니다. 
# 간단한 라벨과 파일을 불러올 수 있는 기능을 구현합니다.
class WelcomeScreen(QWidget):
    def __init__(self, parent=None):
        super(WelcomeScreen, self).__init__(parent)
        self.parent = parent
        
        self.welcome_screen_style = WelcomeScreenStyle()
        
    def setup_ui(self):
        """UI 구성 요소를 설정합니다."""
        # 수직 레이아웃 생성
        main_layout = QVBoxLayout()

        # 버튼 전용 수평 레이아웃 생성
        button_layout = QHBoxLayout()

        # 위쪽 스페이서 추가
        main_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # 레이블 생성 및 중앙 정렬
        welcome_label = QLabel("환영합니다.", self)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet(self.welcome_screen_style.welcome_label_style())  # 스타일 추가
        # 크기를 텍스트에 맞게 자동 조절
        welcome_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        welcome_label.adjustSize()
        main_layout.addWidget(welcome_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 중앙 여백 추가 
        main_layout.addSpacing(10)
        
        # 파일 불러오기 버튼 생성
        load_button = QPushButton("파일 불러오기", self)
        load_button.setMaximumWidth(400)  # 버튼의 최대 너비 설정
        load_button.setStyleSheet(self.welcome_screen_style.load_button_style())  # 버튼 스타일 추가
        button_layout.addWidget(load_button, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 중앙 정렬
        main_layout.addLayout(button_layout)

        # 아래쪽 스페이서 추가
        main_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        return main_layout