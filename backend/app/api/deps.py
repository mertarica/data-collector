from app.services.data_ingestion.ine.factory import INEProviderFactory


def get_ine_factory() -> INEProviderFactory:
    """Dependency to get INE factory instance"""
    return INEProviderFactory()
