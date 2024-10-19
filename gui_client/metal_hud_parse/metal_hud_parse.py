from .performance_metrics_analysis import *
from .performance_metrics_condition import *
from .get_csv_data import *
import numpy as np


# 성능 분석을 실행하는 함수입니다.
def run_performance_analysis(hud_raw_data:dict, decimal_places:int) -> dict:
    _get_calculate_conditions = get_calculate_conditions()
    _get_data = get_data()
    _get_error_data = get_error_data()

    # 데이터를 분리합니다.
    split_performance_data(hud_raw_data, _get_calculate_conditions, _get_data, _get_error_data, decimal_places)

    # 성능 데이터의 frametime를 fps로 변환하는 함수입니다.
    convert_frametime_to_fps(_get_calculate_conditions, _get_data, decimal_places)

    # 마지막으로 남은 자투리 데이터를 처리하는 함수입니다.
    calculate_fps_from_remainder(_get_calculate_conditions, _get_data, decimal_places)
    
    return _get_calculate_conditions, _get_data, _get_error_data
    

if __name__ == "__main__":
    data = get_csv_data("output1.csv")
    _get_calculate_conditions, _get_data, _get_error_data = run_performance_analysis(data, 2)

    print(_get_calculate_conditions["benchmarkBasedTime"])
    print(np.mean(_get_data["frameTimeData"]))
    print(np.mean(_get_data["gpuTimeData"]))
    print(np.mean(_get_data["memoryData"]))
    print(_get_error_data["frametimeErrorData"])
    print(_get_error_data["gpuTimeErrorData"])

