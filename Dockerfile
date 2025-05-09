# Use a imagem oficial do Python como base
FROM python:3.11-slim

# Instalar dependências do PostgreSQL necessárias para compilar psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do contêiner
WORKDIR /src

# Copia o arquivo requirements.txt para o diretório de trabalho dentro do contêiner
COPY core/requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da pasta "core" do host para a pasta "core" dentro do contêiner
COPY ./ /src/

# Expõe a porta 8000
EXPOSE 8000

# Define o comando padrão para executar a aplicação
CMD ["uvicorn", "core.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
