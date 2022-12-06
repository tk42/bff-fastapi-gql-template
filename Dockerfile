FROM python:3.11

WORKDIR /home
ADD requirements.txt ./
# requirements.txtにリストされたパッケージをインストールする
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]