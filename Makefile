SERVICE_NAME := game_table.service

.PHONY: run logs clean copy-service

run: copy-service
	@echo "Starting game table service..."
	sudo systemctl daemon-reload
	sudo systemctl restart $(SERVICE_NAME)
	sudo systemctl enable $(SERVICE_NAME)
	sudo systemctl start $(SERVICE_NAME)

logs:
	@echo "Showing game table service logs..."
	sudo journalctl -u $(SERVICE_NAME) -f

clean:
	@echo "Stopping game table service..."
	sudo systemctl stop $(SERVICE_NAME)

copy-service:
	@echo "Copying game table service..."
	sudo cp $(SERVICE_NAME) /etc/systemd/system/
