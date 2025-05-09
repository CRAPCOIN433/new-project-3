"""
Модуль для скрапинга сайта sportrent.kz
"""
import json
import logging
import time
import re
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import tqdm
from utils.helpers import is_valid_url

class Scraper:
    """Класс для скрапинга сайта sportrent.kz"""
    
    def __init__(self, base_url, user_agent, timeout=30, max_retries=3):
        """
        Инициализация класса скрапера
        
        Args:
            base_url (str): Базовый URL сайта
            user_agent (str): User-Agent для HTTP-запросов
            timeout (int): Таймаут для HTTP-запросов в секундах
            max_retries (int): Максимальное количество повторных попыток
        """
        self.base_url = base_url
        self.headers = {"User-Agent": user_agent}
        self.timeout = timeout
        self.max_retries = max_retries
        self.visited_urls = set()
        self.pages_data = []
        self.logger = logging.getLogger(__name__)
        
        # Проверка доступности сайта
        self._check_site_availability()
    
    def _check_site_availability(self):
        """Проверка доступности сайта"""
        try:
            response = requests.get(
                self.base_url, 
                headers=self.headers, 
                timeout=self.timeout
            )
            response.raise_for_status()
            self.logger.info(f"Сайт {self.base_url} доступен. Код ответа: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Сайт {self.base_url} недоступен. Ошибка: {str(e)}")
            raise
    
    def _get_robots_txt_rules(self):
        """Получение правил из robots.txt"""
        robots_url = urljoin(self.base_url, "/robots.txt")
        disallowed_paths = set()
        
        try:
            response = requests.get(robots_url, headers=self.headers, timeout=self.timeout)
            if response.status_code == 200:
                # Простой парсер robots.txt
                lines = response.text.split('\n')
                active_user_agent = False
                
                for line in lines:
                    line = line.strip().lower()
                    
                    # Проверка на user-agent
                    if line.startswith('user-agent:'):
                        agent = line.split(':', 1)[1].strip()
                        active_user_agent = agent == '*' or 'python' in agent
                    
                    # Если текущий user-agent применим к нам, собираем disallow правила
                    if active_user_agent and line.startswith('disallow:'):
                        path = line.split(':', 1)[1].strip()
                        if path:
                            disallowed_paths.add(path)
            
            self.logger.info(f"Получены правила robots.txt. Запрещено {len(disallowed_paths)} путей.")
            return disallowed_paths
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"Не удалось получить robots.txt: {str(e)}")
            return set()
    
    def _is_allowed_by_robots(self, url, disallowed_paths):
        """Проверка разрешения URL согласно правилам robots.txt"""