@echo off

rem Install pip, the package manager for Python
python -m ensurepip --upgrade

rem Install the dependencies listed in requirements.txt
pip install -r requirements.txt
