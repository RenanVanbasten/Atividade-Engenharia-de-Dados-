from prefect import flow, task, get_run_logger
from src.extract import Extract
from src.load import Load

@task(retries=3, retry_delay_seconds=10)
def extract_task() -> list:
    """Task para extrair dados da PNAD Contínua (IBGE)."""
    logger = get_run_logger()
    extractor = Extract()
    
    logger.info("Iniciando extração de dados do IBGE...")
    data = extractor.extract_desocupacao()
    
    logger.info("Dados brutos extraídos com sucesso do IBGE.")
    return data

@task
def load_task(raw_data: list, db_name: str, collection_name: str):
    """Task para transformar e carregar os dados no MongoDB Atlas."""
    logger = get_run_logger()
    loader = Load()
    
    logger.info(f"Iniciando processo de carga no banco: {db_name}")
    loader.insert_in_mongo(raw_data, db_name, collection_name)
    logger.info("Carga finalizada com sucesso no MongoDB Atlas!")

@flow(name="ETL IBGE Desocupação Pernambuco", log_prints=True)
def ibge_etl_flow():
    """Flow principal que orquestra o pipeline de desocupação."""
    
    dados_brutos = extract_task()
    
    load_task(
        raw_data=dados_brutos, 
        db_name="ibge_data", 
        collection_name="taxa_desocupacao_pe"
    )

if __name__ == "__main__":
    ibge_etl_flow()