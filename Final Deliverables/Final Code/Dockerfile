# FROM python
# WORKDIR /app
# COPY . .
# RUN pip install -r requirements.txt
# CMD ["python3","app.py"]
# EXPOSE 5000

FROM python:3.10.6
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install ibm_db
COPY . .
EXPOSE 5000
CMD ["python","./app.py"]


