### SERVER
# ¯¯¯¯¯¯¯¯¯¯¯


server.build: ## Build server
	docker-compose build webcrawler

server.start: server.services server.build  ## Start server
	docker-compose up webcrawler

server.services: ## Start main services except the server (for development uses)
	docker-compose up -d webcrawler-main-services

server.sh: ## Connect to server to lauch commands
	docker-compose exec webcrawler sh

server.daemon: ## Start daemon server in its docker container
	docker-compose up --build -d webcrawler

server.stop: ## Stop server
	docker-compose stop

server.remove: ## Stop server and remove volumes
	docker-compose down -v

server.logs: ## Display server logs
	docker-compose logs -f -t --tail=1000