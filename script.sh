#!/bin/bash


python_script="c:/Users/yuram/OneDrive/Рабочий стол/update/test.py"

# Перевірка чи файл існує
if [ -f "$python_script" ]; then
    echo "Запускаю Python скрипт $python_script"
    python "$python_script" # Запускаємо Python скрипт
else
    echo "Помилка: файл $python_script не знайдено або не може бути запущений."
    exit 1
fi
