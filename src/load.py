import os
from typing import List, Dict, Any
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@cluster0.qok8d3w.mongodb.net/?appName=Cluster0"

class Load:
    """Classe para carregar dados do IBGE diretamente no MongoDB Atlas."""

    def __init__(self) -> None:
        pass

    def _transform_ibge_to_list(self, ibge_raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Transforma o JSON complexo do IBGE em uma lista de documentos simples.
        """
        flat_data = []
        
        if not ibge_raw_data:
            return flat_data

        resultados = ibge_raw_data[0].get('resultados', [])
        
        for res in resultados:
            categoria = list(res['classificacoes'][0]['categoria'].values())[0]
            serie = res['series'][0]['serie']
            
            for periodo, valor in serie.items():
                try:
                    valor_num = float(valor) if valor != "..." else None
                except (ValueError, TypeError):
                    valor_num = None

                flat_data.append({
                    "categoria": categoria,
                    "periodo": periodo,
                    "taxa_desocupacao": valor_num,
                    "localidade": "Pernambuco"
                })
        
        return flat_data

    def insert_in_mongo(self, ibge_raw_data: List[Dict], db_name: str, collection_name: str):
        """Prepara e insere a série temporal no MongoDB Atlas."""
        
        client = MongoClient(uri, server_api=ServerApi('1'))
        
        try:
            db = client[db_name]
            collection = db[collection_name]

            # Transformação antes da carga
            dados_processados = self._transform_ibge_to_list(ibge_raw_data)

            if dados_processados:
                collection.delete_many({}) 
                
                collection.insert_many(dados_processados)
            else:
                print("Aviso: Nenhum dado processado para inserção.")
        
        except Exception as e:
            print(f"Erro na carga para o MongoDB: {e}")
        
        finally:
            client.close()