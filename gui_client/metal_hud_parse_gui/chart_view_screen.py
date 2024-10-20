from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtWidgets import QSpacerItem, QSizePolicy
from PyQt6.QtWidgets import QLabel, QPushButton
from PyQt6.QtWidgets import QWidget, QFileDialog
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

import sys
import os
import numpy as np

# 현재 파일의 경로를 기준으로 상위 디렉토리 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from metal_hud_parse.metal_hud_parse import run_performance_analysis, get_csv_data

class ChartViewScreenStyle():
    def __init__(self) -> None:
        pass
    
    def chart_view_label_style(self):
        return """
QLabel {
    font-size: 17px;
    font-weight: bold;
    color: #2e7ad1;
    padding: 5px;  /* 여백 설정 */
    border-radius: 10px;  /* 둥근 모서리 */
}
QLabel:hover {
    background-color: #232a96;  /* 마우스 오버 시 색상 */
}
"""

    def time_and_fps_label_style(self):
        return """
QLabel {
    font-size: 14px;
    font-weight: bold;
    color: #2e7ad1;
    padding: 5px;  /* 여백 설정 */
    border-radius: 10px;  /* 둥근 모서리 */
}
QLabel:hover {
    background-color: #232a96;  /* 마우스 오버 시 색상 */
}
"""

    def change_button_style(self):
        return """
QPushButton {
    font-size: 16px;
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

# 데이터를 차트로 표현합니다.
class ChartViewScreen(QWidget):
    def __init__(self, parent=None):
        super(ChartViewScreen, self).__init__(parent)
        
        self.chart_view_screen_style = ChartViewScreenStyle()
        self.parent = parent
        self.set_data = self.parent.set_data
    
    def setup_view_ui(self):
        """UI 구성 요소를 설정합니다."""
        # 프레임 생성
        self.chart_view_frame = QFrame()
        
        # 수직 레이아웃 생성
        chart_view_layout = QVBoxLayout()

        # 버튼 전용 수평 레이아웃 생성
        button_layout = QHBoxLayout()

        # 레이블 생성 및 중앙 정렬
        chart_view_label = QLabel("Chart By Metal Hud Parse-Python")
        chart_view_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_view_label.setStyleSheet(self.chart_view_screen_style.chart_view_label_style())  # 스타일 추가
        # 크기를 텍스트에 맞게 자동 조절
        chart_view_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        chart_view_label.adjustSize()
        chart_view_layout.addWidget(chart_view_label, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        
        
        # 차트의 시간과 FPS를 표시하는 레이블 생성
        self.time_and_fps_label = QLabel("시간과 FPS를 표시합니다.")
        self.time_and_fps_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_and_fps_label.setStyleSheet(self.chart_view_screen_style.time_and_fps_label_style())  # 스타일 추가
        # 크기를 텍스트에 맞게 자동 조절
        self.time_and_fps_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.time_and_fps_label.adjustSize()
        chart_view_layout.addWidget(self.time_and_fps_label, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
    
        # Figure와 Canvas 생성 - 차트 크기 조정
        self.figure = Figure(figsize=(18, 18))  # 너비 18인치, 높이 18인치로 설정
        self.canvas = FigureCanvas(self.figure)

        # 레이아웃에 Canvas 추가
        chart_view_layout.addWidget(self.canvas, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        # 차트의 전체 시간과 평균 FPS를 표시하는 레이블 생성
        self.total_time_and_avg_fps_label = QLabel("전체 시간과 평균 FPS를 표시합니다.")
        self.total_time_and_avg_fps_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total_time_and_avg_fps_label.setStyleSheet(self.chart_view_screen_style.time_and_fps_label_style())  # 스타일 추가
        # 크기를 텍스트에 맞게 자동 조절
        self.total_time_and_avg_fps_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.total_time_and_avg_fps_label.adjustSize()
        chart_view_layout.addWidget(self.total_time_and_avg_fps_label, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
    
        # 버튼 레이아웃 위에 여백 추가 
        chart_view_layout.addSpacing(10)
    
        # 파일 변경하기 버튼 생성
        change_button = QPushButton("파일 변경하기")
        change_button.setMaximumWidth(400)  # 버튼의 최대 너비 설정
        change_button.setStyleSheet(self.chart_view_screen_style.change_button_style())  # 버튼 스타일 추가
        # change_button.clicked.connect(self.load_file)  # 버튼 클릭 시 load_file 함수 호출
        
        button_layout.addWidget(change_button, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 중앙 정렬
        chart_view_layout.addLayout(button_layout)

        self.chart_view_frame.setLayout(chart_view_layout)
        return self.chart_view_frame

        # 차트에 데이터를 표시합니다
    def update_chart(self):
        if self.set_data["file_name"] is not None:
            data = get_csv_data(self.set_data["file_name"])
            _get_calculate_conditions, _get_data, _get_error_data = run_performance_analysis(data, 2)
            
            fps_data = np.array(_get_data["frameTimeData"])
            fps_data_length = len(fps_data)
            avg_fps = np.mean(fps_data)

            # 차트 업데이트
            self.figure.clf()  # 이전 플롯을 지움
            self.ax = self.figure.add_subplot(111)  # 새로운 Axes 추가

            # 데이터 플로팅
            x = np.arange(1, fps_data_length + 1)  # x축: 시간 (초 단위)
            y = fps_data  # y축: FPS 데이터

            self.line, = self.ax.plot(x, y, label='FPS', color='blue', linewidth=1)

            # 레이블 설정
            self.ax.set_xlabel('Time (m:s)')
            self.ax.set_ylabel('FPS')
            self.ax.legend()

            # x축 자동 설정
            self.ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x // 60)}m {int(x % 60)}s"))

            # y축 설정: 0에서 최대 FPS까지 표시
            max_fps = np.max(fps_data)  # 최대 FPS 값에 따른 y축 범위 설정
            self.ax.set_ylim(0, max_fps)
            self.ax.yaxis.set_ticks(np.arange(0, max_fps * 2, 20))  # y축 눈금 설정
            
            # Canvas 업데이트
            self.canvas.draw()
            
            # 레이블 업데이트
            self.total_time_and_avg_fps_label.setText(f"Total testing time: {fps_data_length // 60}m {fps_data_length % 60}s / AVG FPS: {avg_fps:.2f}")

    def vline_event(self):
        # 수직선 초기화
        self.vline = self.ax.axvline(x=0, color='red', linestyle='-')  # 초기 수직선 설정

        # 마우스 이벤트 연결
        self.figure.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)


    def on_mouse_move(self, event):
        if event.inaxes is not None:  # 마우스 포인터가 Axes 안에 있는지 확인
            # x 좌표에 해당하는 인덱스를 찾기
            x_data = self.line.get_xdata()
            y_data = self.line.get_ydata()

            # 마우스 x 좌표에 가장 가까운 데이터 포인트 찾기 (최적화)
            closest_index = np.searchsorted(x_data, event.xdata)  # 이진 탐색을 사용하여 인덱스 찾기

            # 경계 조건 체크
            if closest_index == len(x_data):  # 인덱스가 x_data의 크기와 같으면
                closest_index = len(x_data) - 1  # 마지막 인덱스 사용
            elif closest_index > 0 and np.abs(event.xdata - x_data[closest_index - 1]) < np.abs(event.xdata - x_data[closest_index]):
                closest_index -= 1  # 왼쪽 인덱스가 더 가까운 경우

            # 해당 포인트의 x, y 값
            closest_x = x_data[closest_index]
            closest_y = y_data[closest_index]

            # 마우스 포인터가 선 위에 있을 때만 출력
            if np.abs(event.xdata - closest_x) < 0.1:  # 허용 오차 설정
                # x축을 분과 초로 변환
                minutes = int(closest_x // 60)
                seconds = int(closest_x % 60)
                
                # 레이블에 출력
                self.time_and_fps_label.setText(f"time: {minutes}m {seconds}s, FPS: {closest_y:.2f}")

                # 수직선 위치 업데이트
                self.vline.set_xdata([closest_x, closest_x])  # x 데이터를 리스트로 설정

            # Canvas 업데이트
            self.canvas.draw_idle()  # UI 업데이트 최적화


# 차트 뷰 스레드를 생성합니다.
class ChartViewThread(QThread):
    update_chart = pyqtSignal()
    vline_event = pyqtSignal()
    
    def __init__(self, parent=None):
        super(ChartViewThread, self).__init__(parent)
    
    def start(self):
        self.update_chart.emit()
        self.vline_event.emit()
        