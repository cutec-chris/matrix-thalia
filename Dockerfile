from python:3.8.0
RUN mkdir /bot
RUN mkdir /bot/source
RUN mkdir /data
COPY source/* /bot/source/
RUN pip3 install -r /bot/source/requirements.txt
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download de_core_news_sm
WORKDIR /data/
CMD [ "python3", "/bot/source/bot.py" ]
