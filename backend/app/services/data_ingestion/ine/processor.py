import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from app.core.config import settings
import logging

class INEDataProcessor:
    """Process raw INE data and enrich with metadata"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.metadata = self._load_metadata()
        self.units = self._load_units()
        self.logger.info(f"INEDataProcessor initialized with metadata: {bool(self.metadata)}, units: {bool(self.units)}")
    
    def _load_metadata(self) -> Dict[str, Dict[str, str]]:
        """Load ice_metadata.json"""
        try:
            possible_paths = [
                os.path.join(settings.SHARED_DATA_PATH, "ice_metadata.json"),
                "../../shared/data/ice_metadata.json",
                "../shared/data/ice_metadata.json",
                "shared/data/ice_metadata.json"
            ]
            
            self.logger.info(f"Looking for ice_metadata.json in paths: {possible_paths}")
            
            for path in possible_paths:
                full_path = os.path.abspath(path)
                self.logger.debug(f"Checking path: {full_path}")
                if os.path.exists(full_path):
                    self.logger.info(f"Found ice_metadata.json at: {full_path}")
                    with open(full_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                        self.logger.info(f"Loaded metadata with keys: {list(metadata.keys())}")
                        return metadata
            
            self.logger.warning("⚠️  ice_metadata.json not found, using empty metadata")
            return {}
            
        except Exception as e:
            self.logger.error(f"❌ Error loading ice_metadata.json: {e}")
            return {}

    def _load_units(self) -> Dict[str, str]:
        """Load units.json and create id to name mapping"""
        try:
            possible_paths = [
                os.path.join(settings.SHARED_DATA_PATH, "units.json"),
                "../../shared/data/units.json",
                "../shared/data/units.json",
                "shared/data/units.json"
            ]
            
            self.logger.info(f"Looking for units.json in paths: {possible_paths}")
            
            for path in possible_paths:
                full_path = os.path.abspath(path)
                self.logger.debug(f"Checking path: {full_path}")
                if os.path.exists(full_path):
                    self.logger.info(f"Found units.json at: {full_path}")
                    with open(full_path, 'r', encoding='utf-8') as f:
                        units_list = json.load(f)
                        # Create mapping from Id to Nombre
                        units_dict = {
                            str(unit.get('Id')): unit.get('Nombre', f"Unit {unit.get('Id')}")
                            for unit in units_list
                            if unit.get('Id')
                        }
                        self.logger.info(f"Loaded {len(units_dict)} units")
                        return units_dict
            
            self.logger.warning("⚠️  units.json not found, using empty units")
            return {}
            
        except Exception as e:
            self.logger.error(f"❌ Error loading units.json: {e}")
            return {}
    
    def process_raw_data(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process raw INE data and add enriched metadata"""
        try:
            self.logger.info(f"Processing {len(raw_data)} raw data items")
            processed_data = []
            
            for i, item in enumerate(raw_data):
                self.logger.debug(f"Processing item {i}: {list(item.keys()) if item else 'None'}")
                
                processed_item = {
                    "COD": item.get("COD"),
                    "Nombre": item.get("Nombre"),
                    "FK_Unidad": item.get("FK_Unidad"),
                    "FK_Escala": item.get("FK_Escala"),
                    # Use units.json for unit descriptions
                    "Unidad_Descripcion": self._get_unit_description(item.get("FK_Unidad")),
                    "Escala_Descripcion": self._get_metadata_value("FK_Escala", item.get("FK_Escala")),
                    "Data": []
                }
                
                # Process data points
                if item.get("Data"):
                    self.logger.debug(f"Processing {len(item['Data'])} data points for item {i}")
                    for j, data_point in enumerate(item["Data"]):
                        processed_point = {
                            "Fecha": data_point.get("Fecha"),
                            "Fecha_Legible": self._format_timestamp(data_point.get("Fecha")),
                            "FK_TipoDato": data_point.get("FK_TipoDato"),
                            "TipoDato_Descripcion": self._get_metadata_value("FK_TipoDato", data_point.get("FK_TipoDato")),
                            "FK_Periodo": data_point.get("FK_Periodo"),
                            "Periodo_Descripcion": self._get_metadata_value("FK_Periodo", data_point.get("FK_Periodo")),
                            "Anyo": data_point.get("Anyo"),
                            "Valor": data_point.get("Valor"),
                            "Secreto": data_point.get("Secreto"),
                            "Secreto_Descripcion": self._get_metadata_value("Secreto", str(data_point.get("Secreto", "false")).lower())
                        }
                        processed_item["Data"].append(processed_point)
                
                processed_data.append(processed_item)
            
            self.logger.info(f"Successfully processed {len(processed_data)} items")
            return processed_data
            
        except Exception as e:
            self.logger.error(f"Error processing raw data: {e}", exc_info=True)
            raise

    def _get_unit_description(self, unit_id: Any) -> Optional[str]:
        """Get unit description from units.json"""
        try:
            if not self.units:
                return f"No units data available"
            
            str_unit_id = str(unit_id) if unit_id is not None else ""
            
            if str_unit_id in self.units:
                return self.units[str_unit_id]
            else:
                return f"Unknown unit (ID: {str_unit_id})"
                
        except Exception as e:
            self.logger.error(f"Error getting unit description for {unit_id}: {e}")
            return f"Error: {str(e)}"
    
    def _get_metadata_value(self, field_name: str, field_value: Any) -> Optional[str]:
        """Get human-readable description for a metadata field"""
        try:
            if not self.metadata or field_name not in self.metadata:
                return f"No metadata for {field_name}"
            
            field_map = self.metadata[field_name]
            str_value = str(field_value) if field_value is not None else ""
            
            return field_map.get(str_value, f"Unknown ({str_value})")
        except Exception as e:
            self.logger.error(f"Error getting metadata value for {field_name}={field_value}: {e}")
            return f"Error: {str(e)}"
    
    def _format_timestamp(self, timestamp: Optional[int]) -> Optional[str]:
        """Convert timestamp to human-readable date"""
        if timestamp is None:
            return None
        
        try:
            # Convert milliseconds to seconds
            dt = datetime.fromtimestamp(timestamp / 1000)
            return dt.strftime("%Y-%m-%d")
        except (ValueError, OSError) as e:
            self.logger.error(f"Error formatting timestamp {timestamp}: {e}")
            return f"Invalid timestamp: {timestamp}"
    
    def get_processing_summary(self, processed_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of processed data"""
        try:
            total_series = len(processed_data)
            total_data_points = sum(len(item.get("Data", [])) for item in processed_data)
            
            # Count by data types
            tipo_dato_counts = {}
            periodo_counts = {}
            unit_counts = {}
            
            for item in processed_data:
                # Count units
                unit_desc = item.get("Unidad_Descripcion", "Unknown")
                unit_counts[unit_desc] = unit_counts.get(unit_desc, 0) + 1
                
                for data_point in item.get("Data", []):
                    # Count data types
                    tipo = data_point.get("TipoDato_Descripcion", "Unknown")
                    tipo_dato_counts[tipo] = tipo_dato_counts.get(tipo, 0) + 1
                    
                    # Count periods
                    periodo = data_point.get("Periodo_Descripcion", "Unknown")
                    periodo_counts[periodo] = periodo_counts.get(periodo, 0) + 1
            
            summary = {
                "total_series": total_series,
                "total_data_points": total_data_points,
                "data_type_distribution": tipo_dato_counts,
                "period_distribution": periodo_counts,
                "unit_distribution": unit_counts,
                "metadata_enriched": bool(self.metadata),
                "units_enriched": bool(self.units)
            }
            
            self.logger.info(f"Generated processing summary: {summary}")
            return summary
            
        except Exception as e:
            self.logger.error(f"Error generating processing summary: {e}", exc_info=True)
            return {
                "total_series": 0,
                "total_data_points": 0,
                "data_type_distribution": {},
                "period_distribution": {},
                "unit_distribution": {},
                "metadata_enriched": False,
                "units_enriched": False,
                "error": str(e)
            }