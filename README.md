# Автоматизированный фотоальбом

Этот проект предназначен для создания фотоальбомов с использованием нейронных сетей и семантического анализа.

## Структура проекта

- **backend**: содержит все серверные модули.
  - `ai_module`: содержит модули для обработки изображений и создания альбомов.
  - `app.py`: основной файл приложения.
  - `requirements.txt`: зависимости проекта.
- **frontend**: содержит все фронтенд файлы.
  - `public`: статические файлы.
  - `src`: исходные файлы приложения.

## Установка и запуск

### Установка и запуск серверной части


1. Создайте и активируйте виртуальное окружение (в директории `backend`):
    ```bash
    cd backend
    python -m venv venv
    ```

    Для Windows:
    ```bash
    venv\Scripts\activate
    ```

    Для macOS и Linux:
    ```bash
    source venv/bin/activate
    ```

2. Установите необходимые библиотеки:
    ```bash
    pip install -r requirements.txt
    ```

3. Запустите серверную часть:
    ```bash
    python app.py
    ```
### Установка и запуск фронтенд части

1. Перейдите в директорию `frontend`:
    ```bash
    cd frontend
    ```

2. Установите зависимости:
    ```bash
    npm install(для работы этой команды необходимо иметь node.js - v14.21.3 и npm - 6.14.18, либо совместимые с этими версиями)
    ```

3. Запустите фронтенд приложение:
    ```bash
    npm start
    ```

