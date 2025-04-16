# Dockerfile

FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install flask joblib scikit-learn numpy
EXPOSE 5000
CMD ["python", "api.py"]