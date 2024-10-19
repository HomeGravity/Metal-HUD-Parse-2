# 성능 계산 조건식
def get_calculate_conditions():
    return {
        "benchmarkBasedTime": 1000,
        "missedFrame": 0.0,  # 누락된 프레임 갯수
        "frametimeError": 0,  # 소수점 자리가 <...>로 입력된 프레임타임
        "gpuTimeError": 0,  # 소수점 자리가 <...>로 입력된 GPU타임
        "secondSum": 0,
        "frameCount": 0,
        "overlapCheckData": "temp"
    }

# 성능 데이터
def get_data():
    return {
        "FPSData": [], # 프레임타임을 FPS로 바꾼 것
        "frameTimeData":[], # 프레임타임 데이터 (ms)
        "gpuTimeData":[], # GPU타임 데이터 (ms)
        "memoryData":[] # 메모리 사용량 저장
    }

# 성능 오류 데이터
def get_error_data():
    return {
        "frametimeErrorData":[],
        "gpuTimeErrorData":[]
    }