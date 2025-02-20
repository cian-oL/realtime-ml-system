run-dev:
	uv run python3 run.py

# dockerize trade producer 
build:
	docker build -f Dockerfile -t trades .

# run the up-to-date build
# replace external broker address with internal
run: build
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda-0:9092 \
		trades