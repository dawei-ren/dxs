FROM python:3.6


WORKDIR /dxs

COPY requirement.txt .
RUN pip install -r requirement.txt

COPY . /dxs
RUN cd /dxs

# CMD ["gunicorn", "start:app", "-c", "./gunicorn.conf.py"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
# CMD ["bin/sh"]