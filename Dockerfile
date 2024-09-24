FROM python:3.12.3-alpine3.20

WORKDIR /app

# Install OpenAL soft
RUN apk add --no-cache openal-soft-libs \
    && cp /usr/lib/libopenal.so.1 ./openal.so

# Install python dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -i https://test.pypi.org/simple/ pyftg==2.2b1

COPY ./data ./data
COPY ./src ./src
COPY ./main.py .

ENTRYPOINT [ "python", "main.py" ]