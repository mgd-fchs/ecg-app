
FROM python:3.8-slim
WORKDIR /app
COPY ./ /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run app.py when the container launches
CMD ["flask", "run"]
