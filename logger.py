import logging
import pytz
from datetime import datetime

# 로거 설정
logger = logging.getLogger('steveLogger')
logger.setLevel(logging.DEBUG)

# 콘솔 핸들러 설정
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 파일 핸들러 설정
timezone = pytz.timezone(('Asia/Seoul'))
current_time = datetime.now(timezone).strftime('%Y%m%d%H%M')
log_name = f"debug-{current_time}.log"
# file_handler = logging.FileHandler(log_name)
# file_handler.setLevel(logging.DEBUG)

# 포맷터 설정
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
# file_handler.setFormatter(formatter)

# 핸들러를 로거에 추가
logger.addHandler(console_handler)
# logger.addHandler(file_handler)

# print와 동시에 로그 기록 함수
def print_and_log(message):
    # print(message)
    logger.debug(message)

def log_debug(message):
    print(message)
    logger.debug(message)

def log_info(message):
    print(message)
    logger.info(message)

def log_warning(message):
    print(message)
    logger.warning(message)

def log_error(message):
    print(message)
    logger.error(message)

def log_critical(message):
    print(message)
    logger.critical(message)
