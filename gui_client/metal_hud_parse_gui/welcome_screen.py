from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtWidgets import QSpacerItem, QSizePolicy
from PyQt6.QtWidgets import QLabel, QPushButton
from PyQt6.QtWidgets import QWidget, QFileDialog
from PyQt6.QtCore import Qt, QTimer

from chart_view_screen import ChartViewScreen, ChartViewThread

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
    font-size: 20px;
    background-color: #2e7ad1;  /* 버튼 배경색 */
    color: white;  /* 버튼 텍스트 색상 */
    border: none;  /* 테두리 없애기 */
    padding: 15px;  /* 여백 설정 */
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
        self.set_data = self.parent.set_data
        self.main_layout = self.parent.main_layout
        
        # 스타일 객체를 생성합니다.
        self.welcome_screen_style = WelcomeScreenStyle()
        # 차트 뷰 객체를 생성합니다.
        self.chart_view_screen = ChartViewScreen(self.parent)
        
    def setup_ui(self):
        """UI 구성 요소를 설정합니다."""
        # 프레임 생성
        self.welcome_frame = QFrame()
        
        # 수직 레이아웃 생성
        welcome_layout = QVBoxLayout()

        # 버튼 전용 수평 레이아웃 생성
        button_layout = QHBoxLayout()

        # 위쪽 스페이서 추가
        welcome_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # 레이블 생성 및 중앙 정렬
        self.welcome_label = QLabel("환영합니다.")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setStyleSheet(self.welcome_screen_style.welcome_label_style())  # 스타일 추가
        # 크기를 텍스트에 맞게 자동 조절
        self.welcome_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.welcome_label.adjustSize()
        welcome_layout.addWidget(self.welcome_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 중앙 여백 추가 
        welcome_layout.addSpacing(10)
        
        # 파일 불러오기 버튼 생성
        load_button = QPushButton("파일 불러오기")
        load_button.setMaximumWidth(400)  # 버튼의 최대 너비 설정
        load_button.setStyleSheet(self.welcome_screen_style.load_button_style())  # 버튼 스타일 추가
        load_button.clicked.connect(self.load_file)  # 버튼 클릭 시 load_file 함수 호출
        
        button_layout.addWidget(load_button, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 중앙 정렬
        welcome_layout.addLayout(button_layout)

        # 아래쪽 스페이서 추가
        welcome_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # 프레임에 레이아웃 설정
        self.welcome_frame.setLayout(welcome_layout)
        
        return self.welcome_frame

    # 파일을 선택하는 함수입니다.
    def load_file(self):
        # 파일 불러오기 기능 구현
        file_name, _ = QFileDialog.getOpenFileName(self.parent, "open csv file", "", "csv files (*.csv);;all files (*)")
        # 파일 포맷을 검사합니다.
        if file_name:
            if file_name.lower().endswith(".csv"):
                print(f"선택한 파일: {file_name}")  # 선택한 파일 경로 출력
                
                # welcome_label 텍스트를 변경합니다
                self.welcome_label.setText(f"선택한 파일: {file_name}")
                self.set_data["file_name"] = file_name
                
                # 2초간 비동기 대기 후 main_frame 를 삭제합니다.
                QTimer.singleShot(2000, self.welcome_frame.deleteLater)
                QTimer.singleShot(2000, lambda: self.main_layout.addWidget(self.chart_view_screen.setup_view_ui()))
                QTimer.singleShot(3000, self.start_chart_view_thread)
                
                
            else:
                print(f"파일 포맷이 *.csv 가 아닙니다.")
                
                # welcome_label 텍스트를 변경합니다
                self.welcome_label.setText("파일 포맷이 *.csv 가 아닙니다.")
                self.set_data["file_name"] = None

    def start_chart_view_thread(self):
        chart_view_thread = ChartViewThread()
        chart_view_thread.update_chart.connect(self.chart_view_screen.update_chart)  # 데이터 로드 후 차트 업데이트
        chart_view_thread.vline_event.connect(self.chart_view_screen.vline_event)
        chart_view_thread.start()  # 스레드 시작