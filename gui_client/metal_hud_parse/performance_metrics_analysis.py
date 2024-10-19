# 데이터를 분리합니다.
def split_performance_data(hud_raw_data:dict, get_calculate_conditions:dict, get_data:dict, get_error_data:dict, decimal_places:int) -> None:
    
    # 소수점 자리 처리 조건문
    adjusted_decimal = decimal_places if decimal_places <= 2 else 2
    
    for line in hud_raw_data:
        if get_calculate_conditions["overlapCheckData"] != line[0]:
            get_calculate_conditions["overlapCheckData"] = line[0]
            get_calculate_conditions["missedFrame"] = float(line[1])
            
            # 메모리 데이터
            get_data["memoryData"].append(round(float(line[2]), adjusted_decimal))
            
            for i in range(3, len(line)):
                # 일부 데이터의 소수점 자리가 <...>로 들어올 때가 있어서 제거 처리
                if ("<" not in line[i]):
                    if (line[i] != ""):
                        if i % 2 == 1:
                            # 성능 시간 데이터
                            get_data["frameTimeData"].append(round(float(line[i]), adjusted_decimal))
                            
                        else:
                            # GPU 시간 데이터
                            get_data["gpuTimeData"].append(round(float(line[i]), adjusted_decimal))

                else:
                    if i % 2 == 1:
                        get_calculate_conditions["frametimeError"] += 1
                        get_error_data["frametimeErrorData"].append(line[i])
                    else:
                        get_calculate_conditions["gpuTimeError"] += 1
                        get_error_data["gpuTimeErrorData"].append(line[i])
        else:
            continue

# 성능 데이터의 계산식 함수입니다.
def _calculate_performance_fps(get_calculate_conditions:dict, decimal_places:int) -> float:
    return round(
        (get_calculate_conditions["frameCount"] * 
        get_calculate_conditions["benchmarkBasedTime"] / 
        get_calculate_conditions["secondSum"]) * 
        1000 / 
        get_calculate_conditions["benchmarkBasedTime"],
        decimal_places
        )

# 성능 데이터의 frametime를 fps로 변환하는 함수입니다.
def convert_frametime_to_fps(get_calculate_conditions:dict, get_data:dict, decimal_places:int) -> None:
    # 자투리 시간 오차를 줄이기 위해 추가. 이게 없으면 1초당 약 1/FPS 만큼의 오차가 생김
    overTempFrameTimeSum = 0.0
    
    for i in range(len(get_data["frameTimeData"])):
        get_calculate_conditions["secondSum"] += float(get_data["frameTimeData"][i])
        get_calculate_conditions["frameCount"] += 1
        
        if get_calculate_conditions["secondSum"] >= get_calculate_conditions["benchmarkBasedTime"] - overTempFrameTimeSum:
            get_data["FPSData"].append(_calculate_performance_fps(get_calculate_conditions, decimal_places))
            
            # 반복 할때마다 초기화
            overTempFrameTimeSum = get_calculate_conditions["secondSum"] - (1000 - overTempFrameTimeSum)
            get_calculate_conditions["frameCount"] = 0
            get_calculate_conditions["secondSum"] = 0


# 마지막으로 남은 자투리 데이터를 처리하는 함수입니다.
def calculate_fps_from_remainder(get_calculate_conditions:dict, get_data:dict, decimal_places:int) -> None:
    # 분모가 0일때 예외처리
    if get_calculate_conditions["secondSum"] != 0:
        get_data["FPSData"].append(_calculate_performance_fps(get_calculate_conditions, decimal_places))