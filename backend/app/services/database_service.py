import asyncpg
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.connection_url =""
    
    async def get_connection(self):
        return await asyncpg.connect(self.connection_url)
    
    async def initialize_tables(self):
        """Create metadata and data tables if they don't exist"""
        conn = await self.get_connection()
        try:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS ine_metadata (
                    id SERIAL PRIMARY KEY,
                    dataset_external_id TEXT NOT NULL,
                    code TEXT NOT NULL,
                    name TEXT,
                    unit_id TEXT,
                    scale_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(dataset_external_id, code)
                );
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS ine_data_points (
                    id SERIAL PRIMARY KEY,
                    metadata_id INTEGER REFERENCES ine_metadata(id) ON DELETE CASCADE,
                    period_index INTEGER,
                    value NUMERIC,
                    is_secret BOOLEAN DEFAULT FALSE,
                    period_id INTEGER,
                    year INTEGER,
                    data_type_id INTEGER,
                    timestamp_ms BIGINT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_ine_data_points_metadata_id ON ine_data_points(metadata_id);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_ine_data_points_year_period ON ine_data_points(year, period_id);")
            
        finally:
            await conn.close()
    
    async def get_ine_data_source(self) -> Optional[Dict[str, Any]]:
        """Get INE data source configuration"""
        conn = await self.get_connection()
        try:
            row = await conn.fetchrow("SELECT * FROM data_sources WHERE adapter = $1", "ine")
            return dict(row) if row else None
        finally:
            await conn.close()
    
    async def get_ine_datasets(self) -> List[Dict[str, Any]]:
        """Get all INE datasets to collect"""
        conn = await self.get_connection()
        try:
            rows = await conn.fetch("SELECT * FROM ine_datasets ORDER BY id")
            return [dict(row) for row in rows]
        finally:
            await conn.close()
    
    async def save_dataset_data(self, dataset_external_id: str, data: List[Dict[str, Any]]):
        """Save dataset data with metadata and data points separation"""
        if not data:
            return {"records_inserted": 0}
        
        await self.initialize_tables()
        conn = await self.get_connection()
        
        try:
            total_records = 0
            
            async with conn.transaction():
                for item in data:
                    cod = item.get('COD')
                    if not cod:
                        continue
                    
                    # Upsert metadata
                    metadata_id = await conn.fetchval("""
                        INSERT INTO ine_metadata (dataset_external_id, code, name, unit_id, scale_id, updated_at)
                        VALUES ($1, $2, $3, $4, $5, CURRENT_TIMESTAMP)
                        ON CONFLICT (dataset_external_id, code) 
                        DO UPDATE SET name = EXCLUDED.name, unit_id = EXCLUDED.unit_id, 
                                     scale_id = EXCLUDED.scale_id, updated_at = CURRENT_TIMESTAMP
                        RETURNING id
                    """, 
                    dataset_external_id, cod, item.get('Nombre'), 
                    str(item.get('FK_Unidad', '')), str(item.get('FK_Escala', ''))
                    )
                    
                    # Clear existing data points
                    await conn.execute("DELETE FROM ine_data_points WHERE metadata_id = $1", metadata_id)
                    
                    # Insert new data points
                    data_array = item.get('Data', [])
                    if data_array:
                        batch_data = [
                            (metadata_id, index, dp.get('Valor'), dp.get('Secreto', False),
                             dp.get('FK_Periodo'), dp.get('Anyo'), dp.get('FK_TipoDato'), dp.get('Fecha'))
                            for index, dp in enumerate(data_array)
                        ]
                        
                        await conn.executemany("""
                            INSERT INTO ine_data_points 
                            (metadata_id, period_index, value, is_secret, period_id, year, data_type_id, timestamp_ms)
                            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                        """, batch_data)
                        
                        total_records += len(batch_data)
                
                logger.info(f"Saved {total_records} data points for dataset {dataset_external_id}")
                return {"records_inserted": total_records, "code": dataset_external_id}
            
        except Exception as e:
            logger.error(f"Error saving data for dataset {dataset_external_id}: {e}")
            raise
        finally:
            await conn.close()
    
    async def update_dataset_last_collected(self, dataset_id: int):
        """Update last collection timestamp for a dataset"""
        conn = await self.get_connection()
        try:
            timestamp = int(datetime.now().timestamp() * 1000)
            await conn.execute("UPDATE ine_datasets SET last_modified = $1 WHERE id = $2", timestamp, dataset_id)
        finally:
            await conn.close()

database_service = DatabaseService()