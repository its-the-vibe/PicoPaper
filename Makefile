PORT ?= 4002
MPREMOTE = mpremote connect port:rfc2217://localhost:$(PORT)

.PHONY: deploy

bootstrap:
	mpremote fs cp secrets.py :secrets.py
	mpremote mip install github:its-the-vibe/TinyUpdater/updater.py
	mpremote run bootstrap.py
	
deploy:
	mpremote fs cp main.py :main.py
	mpremote fs cp secrets.py :secrets.py
	mpremote fs cp network_requests.py :network_requests.py
	mpremote fs cp wifi.py :wifi.py
	mpremote fs cp my_config.py :my_config.py
	mpremote fs cp util.py :util.py
	mpremote mip install github:its-the-vibe/TinyUpdater/updater.py
	mpremote run main.py

dev:
	$(MPREMOTE) fs cp main.py :main.py
	$(MPREMOTE) fs cp secrets_dev.py :secrets.py
	$(MPREMOTE) fs cp mock_network_requests.py :network_requests.py
	$(MPREMOTE) fs cp wifi.py :wifi.py
	$(MPREMOTE) fs cp my_config.py :my_config.py
	$(MPREMOTE) fs cp util.py :util.py
	$(MPREMOTE) run main.py
