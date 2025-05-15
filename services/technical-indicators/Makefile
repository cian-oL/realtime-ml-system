run-dev:
	uv run python3 run.py

# # dockerize trade producer 
# build:
# 	docker build -f Dockerfile -t candles .

# # run the up-to-date build
# # replace external broker address with internal
# run: build
# 	docker run -it \
# 		--name candles-service \
# 		--network redpanda_network \
# 		-e KAFKA_BROKER_ADDRESS=redpanda-0:9092 \
# 		-e KAFKA_INPUT_TOPIC=trades \
# 		-e KAFKA_OUTPUT_TOPIC=candles \
# 		-e KAFKA_CONSUMER_GROUP=candles_consumer_group \
# 		-e CANDLE_SECONDS=60 \
# 		candles