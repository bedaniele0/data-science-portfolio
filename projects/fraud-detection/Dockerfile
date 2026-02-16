# ============================================================================
# Dockerfile - Fraud Detection API Container
# ============================================================================
# Autor: Ing. Daniel Varela Perez
# Email: bedaniele0@gmail.com
# Metodología: DVP-PRO
# ============================================================================

FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Install package
RUN pip install -e .

# Expose ports
EXPOSE 8000 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run API
CMD ["fraud-api"]
