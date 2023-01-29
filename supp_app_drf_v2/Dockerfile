FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/supp_app_drf_v2

COPY ./requirements.txt /usr/src/supp_app_drf_v2/requirements.txt
RUN pip install -r /usr/src/supp_app_drf_v2/requirements.txt

COPY . /usr/src/supp_app_drf_v2

EXPOSE 8000
