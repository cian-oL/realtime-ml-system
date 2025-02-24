run-dev:
	uv run python3 run.py

# dockerize trade producer 
build:
	docker build -f Dockerfile -t trades .

# run the up-to-date build
# replace external broker address with internal
run: build
	docker run -it \
		--name trades-service \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda-0:9092 \
		-e KAFKA_TOPIC=trades \
		-e PAIRS='["BTC/USD"]' \
		trades