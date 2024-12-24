FROM python:3.10-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ROOT=/app \
    APP_RUNTIME=docker

# Set the working directory
WORKDIR ${APP_ROOT}

# Install UV dependency manager
RUN pip install --no-cache-dir uv==0.5.11

# Copy the dependency files for UV
COPY ./pyproject.toml ./uv.lock ./

# Sync dependencies using UV
RUN uv sync --no-dev

# Copy the application code
COPY . .

# Make the Gunicorn startup script executable (if applicable)
RUN chmod +x ./rungunicorn.sh

# Expose the application port (default Gunicorn/Uvicorn port)
EXPOSE 8000

# Entrypoint to use UV for dependency management
ENTRYPOINT ["uv", "run"]

# Default command to start the application with Gunicorn
CMD ["./rungunicorn.sh"]
