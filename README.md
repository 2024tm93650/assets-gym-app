# ACEest Fitness & Gym

Converted from desktop Tkinter app to Flask REST API for containerization and CI/CD.

## Endpoints
- `/` - Welcome message
- `/members` - List gym members
- `/members/<id>` - Get single member
- `/classes` - List gym classes
- `/bmi?weight=&height=` - BMI calculator
- `/health` - Health check

## Run
```bash
pip install -r requirements.txt
python app.py
```
