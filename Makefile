MICRO_CONTRILLER_SERVICE_NAME := controller.service
APP_SERVICE_NAME := app.service

.PHONY: run logs clean copy-service

run: copy-service
	@echo "Starting game table services..."
	sudo systemctl daemon-reload
	sudo systemctl restart $(MICRO_CONTRILLER_SERVICE_NAME) $(APP_SERVICE_NAME)
	sudo systemctl enable $(MICRO_CONTRILLER_SERVICE_NAME) $(APP_SERVICE_NAME)
	sudo systemctl start $(MICRO_CONTRILLER_SERVICE_NAME) $(APP_SERVICE_NAME)

microcontroller-logs:
	@echo "Showing game table controller service logs..."
	sudo journalctl -u $(MICRO_CONTRILLER_SERVICE_NAME) -f

app-logs:
	@echo "Showing game table app service logs..."
	sudo journalctl -u $(APP_SERVICE_NAME) -f

nginx-logs:
	@echo "Showing game table nginx logs..."
	sudo journalctl -u nginx -f

clean:
	@echo "Stopping game table services..."
	sudo systemctl stop $(MICRO_CONTRILLER_SERVICE_NAME) $(APP_SERVICE_NAME)
	sudo systemctl stop nginx

copy-services:
	@echo "Copying game table services..."
	sudo cp $(MICRO_CONTRILLER_SERVICE_NAME) $(APP_SERVICE_NAME) /etc/systemd/system/
