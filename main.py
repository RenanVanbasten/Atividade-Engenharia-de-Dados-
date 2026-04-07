from src.extract import Extract
from typing import List, Dict, Any
from src.load import Load

ext: Extract = Extract()
ld = Load()

raw_data: List[Dict[str, Any]] = ext.extract_desocupacao()

if raw_data:
    resultados = raw_data[0].get('resultados', [])
    
    
    for res in resultados:
        categoria = res['classificacoes'][0]['categoria']
        pontos_na_serie = len(res['series'][0]['serie'])
        
        print(f"- Categoria: {list(categoria.values())[0]} | Pontos coletados: {pontos_na_serie}")


ld.insert_in_mongo(
    ibge_raw_data=raw_data, 
    db_name="projeto_ibge", 
    collection_name="taxa_desocupacao_sexo"
)