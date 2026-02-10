python -m venv venv
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
& .\venv\Scripts\Activate.ps1
python -m ensurepip --upgrade
pip install -r requirements.txt
if (-Not (Test-Path "database.db")) { New-Item -Path . -Name "database.db" -ItemType "file" }
python init_db.py
python app.py # RUN this again to restart the server after first time setup is complete.
