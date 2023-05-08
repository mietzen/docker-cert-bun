FROM python:3.11.3-slim

COPY certbun.py /certbun.py

VOLUME [ "/ssl" ]

CMD [ "python", "/certbun.py" ]
