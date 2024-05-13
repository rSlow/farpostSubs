FROM python:3.12 as builder

WORKDIR /app

# copy any python requirements file into the install directory and install all python requirements.
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

# copy the source code into /app and move into that directory.
COPY . .

## start base stage.
# this is the image this is run.
FROM builder

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ./entrypoint.sh
