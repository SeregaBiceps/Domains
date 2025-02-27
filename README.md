# Проект Spider Domain

## Описание

Проект представляет собой инструмент для поиска и анализа доменов через API USPTO (United States Patent and Trademark Office). Основная цель проекта — автоматизация процесса сбора данных о доменах, связанных с торговыми марками, и их анализ на предмет доступности.

## Основные функции

1. **Поиск доменов**: Поиск доменов, связанных с торговыми марками, через API USPTO.
2. **Сбор данных**: Сбор данных о доменах, включая информацию о регистрации и сроке действия.
3. **Анализ доступности**: Определение доменов, которые скоро станут доступными для регистрации.
4. **Сохранение данных**: Сохранение собранных данных в формате HTML и JSON для дальнейшего анализа.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/spider-domain.git
   ```
2. Установите необходимые зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Использование

1. Запустите скрипт:
   ```bash
   python scripts/domains/spider_domain/init.py
   ```
2. Введите ключевое слово для поиска доменов.
3. Скрипт автоматически выполнит поиск, сбор данных и анализ доступности доменов.

## Зависимости

- `requests`
- `beautifulsoup4`
- `urllib3`
- `lxml`
