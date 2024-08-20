FROM python:3.10
EXPOSE 5000

# Copie o código da aplicação para o diretório /app
ADD . /app
WORKDIR /app

# Instale as dependências
RUN pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install -e .[all]

# Copie o script de inicialização para o contêiner
COPY init_env.py /app/

# Execute o script de inicialização (garanta que o Docker esteja configurado corretamente)
RUN python init_env.py || true

# Defina o comando padrão para executar a aplicação Flask
CMD ["flask", "run", "--host", "0.0.0.0"]
