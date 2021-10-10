@echo off
if not exist ./win_venv/ python -m venv win_venv
.\win_venv\Scripts\pip install -r requirements.txt
.\win_venv\Scripts\python main.py
