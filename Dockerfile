FROM python:3
ADD bot.py /
ADD bugs_handler.py /
ADD bugzilla_call.py /
ADD config.yml /
ADD configuration.py /
RUN pip install python-bugzilla
RUN pip install pyyaml
RUN pip install pymongo
RUN pip install telegram
RUN pip install validate_email
CMD [ "python", "./bot.py" ]