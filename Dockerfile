FROM python:3.10-slim

# Set up working directory
WORKDIR /app

# Copy code and requirements
COPY . /app

# Optionally copy prebuilt data (uncomment if needed)
COPY filings/ /app/filings/
COPY mag7_filing_metadata.json /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# (Optional) For production, you might want to specify a user for security:
# RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
# USER appuser

# Entrypoint: run your main app script (change as needed)
CMD ["python", "app.py"]
# For Streamlit, use:
# CMD ["streamlit", "run", "app.py"]

# Expose port for web apps (e.g. Streamlit, FastAPI)
EXPOSE 8501
