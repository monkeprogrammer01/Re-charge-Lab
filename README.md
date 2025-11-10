
## ⚙️ Установка и запуск

```bash
# Клонировать репозиторий
git clone https://github.com/monkeprogrammer01/Re-charge-Lab.git
cd Re-charge-Lab

# Создать виртуальное окружение
python -m venv venv

# Активировать окружение
# MacOS / Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Запустить сервер
python manage.py runserver