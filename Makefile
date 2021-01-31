build:
	docker build -t assemler ./

run:
	xhost +
	docker run -v $(PWD)/:/usr/src/app -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY -e DISPLAY=:0.0 -p 8266:8266 -t assemler