docker build -t assemler ./
docker run -d -v $(pwd)/:/home -p 8266:8266 -t assemler