-include .env

HA_HOST ?= homeassistant.local
HA_PATH ?= /config

DEST = $(HA_HOST):$(HA_PATH)/custom_components/duco_modbus/
SSH_CMD = ssh $(HA_HOST)

.PHONY: test venv install deploy sync restart logs

venv:
	python3 -m venv .venv

install: venv
	.venv/bin/python -m pip install -r requirements_test.txt

test:
	.venv/bin/pytest

deploy:
	rsync -avz --delete \
		--exclude '__pycache__' \
		--exclude '*.pyc' \
		custom_components/duco_modbus/ $(DEST)

sync: deploy

restart:
	$(SSH_CMD) "ha core restart"

logs:
	$(SSH_CMD) "ha core logs | grep duco_modbus"
