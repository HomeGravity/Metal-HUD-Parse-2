from gui_client.metal_hud_parse.metal_hud_parse import run_performance_analysis, get_csv_data
import numpy as np

# dataStatus = "Total testing time : " + String(dataSet.fpsData.count / 60) + "m " + String(dataSet.fpsData.count % 60) + "s / AVG FPS : " + String(dataSet.avgFPS)
                            

if __name__ == "__main__":
    data = get_csv_data("output1.csv")
    if data is not None:
        _get_calculate_conditions, _get_data, _get_error_data = run_performance_analysis(data, 2)

        print(_get_calculate_conditions["benchmarkBasedTime"])
        print(_get_calculate_conditions["secondSum"])
        print(len(_get_data["FPSData"]) // 60, "m", len(_get_data["FPSData"]) % 60, "s", "avg fps:", np.mean(_get_data["FPSData"]))
        print(np.mean(_get_data["frameTimeData"]))
        print(np.mean(_get_data["gpuTimeData"]))
        print(np.mean(_get_data["memoryData"]))
        print(_get_error_data["frametimeErrorData"])
        print(_get_error_data["gpuTimeErrorData"])

    else:
        print("데이터가 없습니다.")