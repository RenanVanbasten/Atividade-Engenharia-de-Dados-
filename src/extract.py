import requests
from typing import List, Dict, Any

class Extract:
    """Classe para extrair dados da PNAD Contínua (IBGE)."""

    def __init__(self) -> None:
        pass

    def extract_desocupacao(self) -> List[Dict[str, Any]]:
        """Extrai a série temporal da taxa de desocupação por sexo."""
        
        base_url = "https://servicodados.ibge.gov.br/api/v3/agregados/4093/periodos/201201-202504/variaveis/4099"

        parametros = {
            "localidades": "N3[26]",
            "classificacao": "2[all]"
        }
        
        response = requests.get(base_url, params=parametros)
        
        response.raise_for_status()
        
        data = response.json()
        
        return data