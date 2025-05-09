"""
Основной файл для запуска анализа сайта sportrent.kz
"""
import os
import sys
import argparse
import logging
import time
from datetime import datetime

# Импорт модулей проекта
from modules.scraper import Scraper
from modules.structure import StructureAnalyzer
from modules.seo import SeoAnalyzer
from modules.performance import PerformanceAnalyzer
from modules.report import ReportGenerator
from utils.logger import setup_logger
import config

def parse_arguments():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(description="Анализатор сайта sportrent.kz")
    parser.add_argument("--module", choices=["scraper", "structure", "seo", "performance", "report", "all"],
                        default="all", help="Запуск конкретного модуля анализа")
    parser.add_argument("--output", help="Путь для сохранения отчета")
    parser.add_argument("--verbose", action="store_true", help="Подробный вывод")
    return parser.parse_args()

def main():
    """Основная функция запуска анализа"""
    # Парсинг аргументов
    args = parse_arguments()
    
    # Настройка логирования
    log_level = logging.DEBUG if args.verbose else getattr(logging, config.LOG_LEVEL)
    logger = setup_logger(log_level, config.LOG_FILE)
    
    logger.info("Начало анализа сайта sportrent.kz")
    start_time = time.time()
    
    # Определение выходного пути для отчета
    output_path = args.output if args.output else os.path.join(
        config.REPORTS_DIR, 
        config.REPORT_FILENAME.format(date=datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    )
    
    # Создание экземпляров анализаторов
    scraper = Scraper(config.BASE_URL, config.USER_AGENT, config.TIMEOUT, config.MAX_RETRIES)
    structure_analyzer = StructureAnalyzer()
    seo_analyzer = SeoAnalyzer(config.SEO_KEYWORDS)
    performance_analyzer = PerformanceAnalyzer()
    report_generator = ReportGenerator(config.REPORT_TEMPLATE)
    
    # Выполнение анализа в зависимости от выбранного модуля
    if args.module in ["all", "scraper"]:
        logger.info("Запуск скрапинга сайта...")
        pages_data = scraper.scrape_site(
            max_pages=config.MAX_PAGES,
            crawl_delay=config.CRAWL_DELAY,
            respect_robots_txt=config.RESPECT_ROBOTS_TXT
        )
        logger.info(f"Скрапинг завершен. Собрано {len(pages_data)} страниц.")
        
        # Сохранение собранных данных
        scraper.save_data(os.path.join(config.DATA_DIR, "scraped_data.json"))
    else:
        # Загрузка данных, если скрапинг не выполняется
        pages_data = scraper.load_data(os.path.join(config.DATA_DIR, "scraped_data.json"))
    
    if args.module in ["all", "structure"]:
        logger.info("Анализ структуры сайта...")
        structure_data = structure_analyzer.analyze(pages_data)
        logger.info("Анализ структуры сайта завершен.")
    
    if args.module in ["all", "seo"]:
        logger.info("SEO-анализ...")
        seo_data = seo_analyzer.analyze(pages_data)
        logger.info("SEO-анализ завершен.")
    
    if args.module in ["all", "performance"]:
        logger.info("Анализ производительности...")
        performance_data = performance_analyzer.analyze(pages_data)
        logger.info("Анализ производительности завершен.")
    
    if args.module in ["all", "report"]:
        logger.info("Генерация отчета...")
        # Сбор всех данных для отчета
        report_data = {
            "site_url": config.BASE_URL,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pages_count": len(pages_data),
            "structure": structure_data if "structure_data" in locals() else None,
            "seo": seo_data if "seo_data" in locals() else None,
            "performance": performance_data if "performance_data" in locals() else None
        }
        
        # Генерация и сохранение отчета
        report_generator.generate(report_data, output_path)
        logger.info(f"Отчет сохранен в: {output_path}")
    
    # Завершение анализа
    elapsed_time = time.time() - start_time
    logger.info(f"Анализ завершен. Затраченное время: {elapsed_time:.2f} секунд.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
