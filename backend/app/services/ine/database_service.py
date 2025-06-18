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
            
    async def search_ine_datasets(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search INE datasets by name or external_id"""
        conn = await self.get_connection()
        try:
            sql = """
            SELECT * FROM ine_datasets 
            WHERE (name ILIKE $1 OR external_id ILIKE $1) 
            AND active = true
            ORDER BY name
            LIMIT $2
            """
            rows = await conn.fetch(sql, f"%{query}%", limit)
            return [dict(row) for row in rows]
        finally:
            await conn.close()

    async def get_dataset_raw_data(self, dataset_code: str) -> List[Dict[str, Any]]:
        """Get raw data for a dataset from ine_metadata and ine_data_points tables"""
        conn = await self.get_connection()
        try:
            rows = await conn.fetch("""
                SELECT 
                    m.code,
                    m.name,
                    m.unit_id,
                    m.scale_id,
                    json_agg(
                        json_build_object(
                            'value', ROUND(dp.value,2),
                            'is_secret', dp.is_secret,
                            'period_id', dp.period_id,
                            'year', dp.year,
                            'data_type_id', dp.data_type_id,
                            'timestamp_ms', dp.timestamp_ms
                        ) ORDER BY dp.period_index
                    ) as data_points
                FROM ine_metadata m
                LEFT JOIN ine_data_points dp ON m.id = dp.metadata_id
                WHERE m.dataset_external_id = $1
                GROUP BY m.id, m.code, m.name, m.unit_id, m.scale_id
                ORDER BY m.code
            """, dataset_code)
            
            result = []
            for row in rows:
                data_item = {
                    'code': row['code'],
                    'name': row['name'],
                    'unit_id': row['unit_id'],
                    'scale_id': row['scale_id'],
                    'data_points': row['data_points'] if row['data_points'] and row['data_points'] != [None] else []
                }
                result.append(data_item)
            
            return result
        finally:
            await conn.close()

    async def get_dataset_processed_data(self, dataset_code: str) -> List[Dict[str, Any]]:
        """Get processed data for a dataset - simplified format"""
        conn = await self.get_connection()
        try:
            rows = await conn.fetch("""
                SELECT 
                    m.dataset_external_id,
                    m.code,
                    m.name as indicator_name,
                    m.unit_id,
                    u.name as unit_description,
                    e.name as scale_description,
                    dp.period_index,
                    f.name,
                    dp.year,
                    ROUND(dp.value,2) as value,
                    CASE 
                        WHEN dp.is_secret = true THEN 'Confidential — not publicly shown'
                        ELSE 'Public data — freely available'
                    END as data_confidentiality,
                    m.created_at as metadata_created,
                    m.updated_at as metadata_updated,
                    dp.created_at as data_point_created
                FROM ine_data_points dp
                INNER JOIN ine_metadata m ON dp.metadata_id = m.id
                LEFT JOIN ine_def_frequencies f ON CAST (dp.period_id AS INTEGER) = f.ref_id
                LEFT JOIN ine_def_units u ON CAST(m.unit_id AS INTEGER) = u.ref_id
                LEFT JOIN ine_def_scales e ON CAST(m.scale_id AS INTEGER) = e.ref_id
                WHERE m.dataset_external_id = $1
                ORDER BY m.code, dp.year, dp.period_id;
            """, dataset_code)
            
            result = []
            for row in rows:
                processed_item = {
                    'code': row['code'],
                    'name': row['name'],
                    'total_data_points': row['total_data_points'],
                    'year_range': {
                        'min': row['min_year'],
                        'max': row['max_year']
                    },
                    'statistics': {
                        'average_value': float(row['avg_value']) if row['avg_value'] else None
                    },
                    'last_updated': row['updated_at'].isoformat() if row['updated_at'] else None
                }
                result.append(processed_item)
            
            return result
        finally:
            await conn.close()

    async def get_dataset_metadata(self, dataset_code: str) -> List[Dict[str, Any]]:
        """Get just metadata information for a dataset"""
        conn = await self.get_connection()
        try:
            rows = await conn.fetch("""
                SELECT 
                    m.code,
                    m.name,
                    m.unit_id,
                    m.scale_id,
                    m.created_at,
                    m.updated_at,
                    COUNT(dp.id) as data_points_count
                FROM ine_metadata m
                LEFT JOIN ine_data_points dp ON m.id = dp.metadata_id
                WHERE m.dataset_external_id = $1
                GROUP BY m.id, m.code, m.name, m.unit_id, m.scale_id, m.created_at, m.updated_at
                ORDER BY m.code
            """, dataset_code)
            
            return [dict(row) for row in rows]
        finally:
            await conn.close()

database_service = DatabaseService()