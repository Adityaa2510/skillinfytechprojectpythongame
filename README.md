# Snake Arena — Python DevSecOps CI Project

## Setup (Windows PowerShell)
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -v
python game.py
```

## Local security checks
```powershell
python -m bandit -r game.py game_logic.py tests
python -m pip_audit -r requirements.txt
```

GitHub Actions runs tests, syntax validation, Bandit, pip-audit, and Gitleaks.
See the separate Phase ZIPs for step-by-step instructions.
