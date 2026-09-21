# Stage 1: Build the frontend
FROM node:20 AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Serve with Python
FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code, ml scripts, and models
COPY backend/ ./backend/
COPY ml/ ./ml/
COPY models/ ./models/

# Copy the pre-existing SQLite database (if needed for the demo)
# In production on Render, you should use a managed PostgreSQL database, 
# as the local disk is ephemeral and the SQLite database will be reset on every deploy.
COPY stocksense.db .

# Copy the built frontend from the builder stage
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Set the port environment variable
ENV PORT=8000
EXPOSE 8000

# Start the application
CMD uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
