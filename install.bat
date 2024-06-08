@echo off
cd "interpreter/Portable Python-3.10.5 x64/App/Python"

python.exe -m pip install --upgrade pip
python.exe -m pip install pygame
python.exe -m pip install openpyxl

pause