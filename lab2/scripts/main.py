# Assuming you have imported your SQLAlchemy Repo from the DAL repository
from data_access.repositories import SqlAlchemyRepository
from business.services import ProcessingService
from data_access.interfaces import ConsolePresentation

def main():
    conn_str = "mssql+pyodbc://@DESKTOP-33IR0JT/rental_service?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    repo = SqlAlchemyRepository(db_url=conn_str)

    service = ProcessingService(repository=repo)
    
    ui = ConsolePresentation()
    
    ui.show_message("Starting Data Import System...")
    file_to_load = "data/data_source.csv"
    
    try:
        result = service.run_import_pipeline(file_to_load)
        ui.show_message(result)
    except Exception as e:
        ui.show_error(str(e))

if __name__ == "__main__":
    main()