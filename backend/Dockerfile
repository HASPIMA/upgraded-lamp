FROM python:3.9

# This is just so `stdout` and `stderr` are unbuffered by default
# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED
# This allows statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

WORKDIR /app

# Copy app files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Generate the Prisma client
RUN prisma generate

# Expose port imported from the environment
EXPOSE ${API_PORT}

# Start the app with uvicorn
CMD uvicorn main:app --host 0.0.0.0 --port ${API_PORT} --workers 1
