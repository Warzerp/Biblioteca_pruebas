Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py makemigrations usuarios catalogo prestamos multas
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser --noinput --username admin --email admin@example.com
cd frontend
cmd /c npm install
cd ..

