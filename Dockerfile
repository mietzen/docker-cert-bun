FROM python:3.11.4-slim

COPY certbun.py /certbun.py

VOLUME [ "/ssl" ]

CMD [ "python", "/certbun.py" ]
