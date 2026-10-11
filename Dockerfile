
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYGAME_HIDE_SUPPORT_PROMPT=1 \
    SDL_VIDEODRIVER=dummy

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libsdl2-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY game.py game_logic.py ./
COPY tests ./tests

CMD ["python", "game.py"]
