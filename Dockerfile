FROM python:3

WORKDIR /app

COPY . .

RUN apt update && \
    apt upgrade -y && \
    apt install -y python3 python3-pip

RUN python3 -m pip install -r requirements.txt

RUN python3 setup.py clean

RUN python3 setup.py build_ext --inplace

RUN python3 setup.py install

CMD ["hyperscript", "--help"]
