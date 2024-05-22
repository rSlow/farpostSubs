taskiq worker \
  --ack-type when_executed \
  --workers 8 \
  --max-prefetch 1 \
  apps.subs.mq.broker:ads_broker \
  -fsd
