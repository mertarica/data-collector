from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import RawDataResponse, ProcessedDataResponse
from app.services.data_ingestion.ine.factory import INEProviderFactory
from app.api.deps import get_ine_factory

router = APIRouter()


@router.get("/raw/{dataset_code}", response_model=RawDataResponse)
async def get_raw_data(
    dataset_code: str,
    factory: INEProviderFactory = Depends(get_ine_factory)
):
    """Fetch raw data from INE API for given dataset code"""
    try:
        # Create provider
        provider = factory.create_provider(dataset_code)

        # Fetch raw data
        raw_data = await provider.fetch_raw_data()

        return RawDataResponse(
            codigo=dataset_code,
            dataset_name=provider.dataset_name,
            record_count=len(raw_data) if isinstance(raw_data, list) else 1,
            raw_data=raw_data,
            message=f"Successfully fetched raw data for {dataset_code}"
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch raw data: {str(e)}"
        )


@router.get("/processed/{dataset_code}", response_model=ProcessedDataResponse)
async def get_processed_data(
    dataset_code: str,
    factory: INEProviderFactory = Depends(get_ine_factory)
):
    """Fetch and process data from INE API for given dataset code"""
    try:
        # Create provider
        provider = factory.create_provider(dataset_code)

        # Fetch raw data
        raw_data = await provider.fetch_raw_data()

        # Process to DataFrame
        df = provider.parse_to_dataframe(raw_data)

        return ProcessedDataResponse(
            codigo=dataset_code,
            dataset_name=provider.dataset_name,
            record_count=len(df),
            processed_data=df.to_dict('records'),
            columns=df.columns.tolist(),
            message=f"Successfully processed {len(df)} records for {dataset_code}"
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process data: {str(e)}"
        )


@router.get("/info/{dataset_code}")
async def get_provider_info(
    dataset_code: str,
    factory: INEProviderFactory = Depends(get_ine_factory)
):
    """Get provider information for a dataset"""
    try:
        provider = factory.create_provider(dataset_code)
        return provider.get_api_info()

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get provider info: {str(e)}"
        )
