"""
Конфигурационный файл для настройки параметров анализа сайта sportrent.kz
"""
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Основные настройки
BASE_URL = "https://sportrent.kz"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
TIMEOUT = 30  # Таймаут для HTTP-запросов в секундах
MAX_RETRIES = 3  # Максимальное количество повторных попыток для HTTP-запросов

# Настройки скрапинга
MAX_PAGES = 100  # Максимальное количество страниц для сканирования
CRAWL_DELAY = 1  # Задержка между запросами в секундах
RESPECT_ROBOTS_TXT = True  # Уважать директивы robots.txt

# Настройки SEO-анализа
SEO_KEYWORDS = [
    "аренда спортивного инвентаря",
    "прокат спортивного оборудования",
    "спортивный инвентарь Казахстан",
    "аренда лыж",
    "прокат велосипедов",
    "спортивное снаряжение"
]

# Настройки анализа производительности
PERFORMANCE_METRICS = [
    "load_time",
    "page_size",
    "requests_count",
    "mobile_friendly"
]

# Пути к директориям
REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# Создание директорий, если они не существуют
for directory in [REPORTS_DIR, DATA_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Настройки отчета
REPORT_TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "report_template.html")
REPORT_FILENAME = "sportrent_analysis_report_{date}.html"

# Настройки логирования
LOG_LEVEL = "INFO"
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "analysis.log")
