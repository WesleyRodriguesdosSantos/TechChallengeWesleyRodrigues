# Importação necessárias
import logging
import sys
from pythonjsonlogger import jsonlogger
# Função para configurar o logger da aplicação
def setup_logger():
    # Obtém o logger raiz do Pyth
    logger = logging.getLogger()
    # Define o nível de log como INFO (pode ser DEBUG, WARNING, ERROR, etc.
    logger.setLevel(logging.INFO)
    # Cria um manipulador de log que envia as mensagens para a saída padrão (console)
    logHandler = logging.StreamHandler(sys.stdout)
    # Define o formato dos logs em JSON, incluindo data/hora, nível, nome do logger e mensagem
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    logHandler.setFormatter(formatter)
     # Adiciona o manipulador ao logger
    logger.addHandler(logHandler)
