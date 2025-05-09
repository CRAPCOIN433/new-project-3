# SportRent.kz Сайт-анализатор

Этот проект предназначен для автоматизированного анализа сайта sportrent.kz. Он включает в себя следующие функции:

- Скрапинг и сбор данных с сайта
- Анализ структуры сайта
- SEO-анализ
- Анализ производительности
- Генерация подробного отчета

## Установка

1. Клонируйте репозиторий:
git clone https://github.com/yourusername/sportrent-analyzer.git
cd sportrent-analyzer

2. Создайте виртуальное окружение и активируйте его:
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate     # Для Windows

3. Установите зависимости:
pip install -r requirements.txt

## Использование

Для запуска полного анализа:

python main.py

Для запуска отдельных модулей:

python main.py --module scraper    # Только скрапинг
python main.py --module seo        # Только SEO-анализ
python main.py --module performance # Только анализ производительности
python main.py --module report     # Только генерация отчета

## Структура проекта

sportrent-analyzer/
├── main.py                 # Основной файл запуска
├── config.py               # Конфигурационный файл
├── requirements.txt        # Зависимости проекта
├── modules/
│   ├── scraper.py          # Модуль для скрапинга сайта
│   ├── structure.py        # Анализ структуры сайта
│   ├── seo.py              # SEO-анализ
│   ├── performance.py      # Анализ производительности
│   └── report.py           # Генерация отчета
├── utils/
│   ├── helpers.py          # Вспомогательные функции
│   └── logger.py           # Логирование
└── reports/                # Директория для сохранения отчетов

## Результаты

После завершения анализа в директории `reports/` будет создан HTML-отчет с подробной информацией о сайте sportrent.kz, включая:

- Карту сайта
- SEO-рекомендации
- Анализ скорости загрузки
- Анализ мобильной версии
- Рекомендации по улучшению
