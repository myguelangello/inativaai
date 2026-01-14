APP_NAME=inativaai
DOCKER_IMAGE=inativaai:v1

# Cores para output
RESET = \033[0m
GREEN = \033[32m
YELLOW = \033[33m
RED = \033[31m

dev:
	@echo "$(YELLOW)Verificando se estou no diretório da $(APP_NAME_DEV)...$(RESET)"
	@echo "$(YELLOW)Diretório atual: $(shell pwd)$(RESET)"
	@echo "$(RED)Parando e removendo contêineres antigos...$(RESET)"
	docker compose down $(APP_NAME_DEV) || true
	docker rmi $(DOCKER_IMAGE_DEV) || true
	@echo "$(GREEN)Construindo a imagem do Docker...$(RESET)"
	docker compose -f compose.dev.yaml up -d --build
	@echo "$(GREEN)Aguardando o contêiner $(APP_NAME_DEV) iniciar...$(RESET)"
	@docker ps -a --filter "name=$(APP_NAME_DEV)" --format "Status: {{.Status}}\nPortas: {{.Ports}}\nImagem: {{.Image}}\n"
	@echo "Logs do contêiner $(APP_NAME_DEV):"
	docker logs -f $(APP_NAME_DEV) --tail 10

deploy:
	@echo "$(YELLOW)Verificando se estou no diretório da $(APP_NAME)...$(RESET)"
	@echo "$(YELLOW)Diretório atual: $(shell pwd)$(RESET)"
	@echo "$(RED)Parando e removendo contêineres antigos...$(RESET)"
	docker compose down $(APP_NAME) || true
	docker rmi $(DOCKER_IMAGE) || true
	@echo "$(GREEN)Construindo a imagem do Docker...$(RESET)"
	docker compose up -d --build
	@echo "$(GREEN)Aguardando o contêiner $(APP_NAME) iniciar...$(RESET)"
	@docker ps -a --filter "name=$(APP_NAME)" --format "Status: {{.Status}}\nPortas: {{.Ports}}\nImagem: {{.Image}}\n"
	@echo "Logs do contêiner $(APP_NAME):"
	docker logs -f $(APP_NAME) --tail 10