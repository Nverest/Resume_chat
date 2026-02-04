FROM python:3.13-slim

WORKDIR /app

COPY frontend frontend

RUN pip install --no-cache-dir uv

WORKDIR /app/frontend

RUN uv sync --no-dev

CMD ["sh", "-c", "uv run streamlit run front_chat.py \
    --server.port=${PORT:-8501} \
    --server.address=0.0.0.0"]