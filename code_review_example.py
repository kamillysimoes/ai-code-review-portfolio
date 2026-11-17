"""
Módulo de Exemplo: Validação e Processamento de Dados de Usuário
Foco: Demonstração de boas práticas, tratamento de exceções,
refatoração e eliminação de bugs lógicos (exigências para Code Review).
"""

import logging
from typing import Dict, List, Optional, Union

# Configuração de logging estruturado para rastreamento de erros
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class UserProcessor:
    """Classe responsável por processar e filtrar dados de usuários."""

    def __init__(self, user_list: List[Dict[str, Union[str, int]]]) -> None:
        self.user_list = user_list

    def filter_active_adults(self) -> List[Dict[str, Union[str, int]]]:
        """
        Filtra usuários ativos e maiores de idade (idade >= 18).
        
        Trata possíveis falhas de tipo e chaves ausentes no dicionário
        para evitar exceções em tempo de execução (KeyError, TypeError).
        """
        valid_users: List[Dict[str, Union[str, int]]] = []

        for index, user in enumerate(self.user_list):
            try:
                # Validação rigorosa de chaves obrigatórias
                if not isinstance(user, dict):
                    logger.warning("Item na posição %d não é um dicionário válido.", index)
                    continue

                is_active = user.get("is_active")
                age = user.get("age")

                # Verificação de tipos para evitar falhas lógicas de comparação
                if isinstance(is_active, bool) and is_active and isinstance(age, (int, float)):
                    if age >= 18:
                        valid_users.append(user)
            
            except Exception as e:
                logger.error("Erro inesperado ao processar o usuário no índice %d: %s", index, e)

        logger.info("Processamento concluído. %d usuários válidos encontrados.", len(valid_users))
        return valid_users


# Exemplo de uso prático demonstrando o funcionamento do script
if __name__ == "__main__":
    raw_data = [
        {"name": "Ana", "age": 25, "is_active": True},
        {"name": "Bruno", "age": 16, "is_active": True}, # Menor de idade (será filtrado)
        {"name": "Carla", "age": "trinta", "is_active": True}, # Erro de tipo proposital na idade
        {"name": "Daniel", "age": 30, "is_active": False}, # Inativo (será filtrado)
    ]

    processor = UserProcessor(raw_data)
    result = processor.filter_active_adults()
    print("Usuários filtrados com sucesso:", result)
