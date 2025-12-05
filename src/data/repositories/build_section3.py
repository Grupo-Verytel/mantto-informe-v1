from datetime import datetime
from typing import Dict, Any, Optional
from src.services.database import get_database


async def get_section3(anio: int, mes: int, user_id: int, name_file: str):
    db = get_database()
    collection = db["section3"]
    
    document = await collection.find_one({"anio": anio, "mes": mes})
    
    if not document:
        await build_section3(anio, mes, user_id, name_file)
        document = await collection.find_one({"anio": anio, "mes": mes})
    
    return document    


# ESTE ES EL ESQUEMA BASE DEL DOCUMENTO EN CASO QUE NO EXISTA #
async def build_section3(anio: int, mes: int , user_id: int, name_file: str):

    db = get_database()
    datetime_now = datetime.now()    
    collection = db["section3"]
    user_created = user_id    
    document = await collection.insert_one(
        { 
        "section": "3",
        "title": "INFORMES DE MEDICIÓN DE NIVELES DE SERVICIO (ANS)",
        "anio": anio, 
        "mes": mes,  
        "name_file": name_file,
        "level": 1,      
        "created_at": datetime_now,
        "updated_at": datetime_now,
        "user_created": user_created,
        "user_updated": user_created,
        "index": [
             {
                "id": "3",
                "level": 1,
                "title": "3. INFORMES DE MEDICIÓN DE NIVELES DE SERVICIO (ANS)",
                "content": {
                    "mes": mes,
                    "anio": anio,
                    "cant_disponibilidad_sistema": None,
                    "valor_disponibilidad_sistema": None,
                    "cant_calidad_informes_1": None,
                    "valor_calidad_informes_1": None,
                    "cant_calidad_informes_2": None,
                    "valor_calidad_informes_2": None,
                    "cant_calidad_informes_3": None,
                    "valor_calidad_informes_3": None,
                    "cant_calidad_informes_4": None,
                    "valor_calidad_informes_4": None,
                    "cant_oportunidad_informes": None,
                    "valor_oportunidad_informes": None,
                    "cant_rto_1": None,
                    "valor_rto_1": None,
                    "cant_rto_2": None,
                    "valor_rto_2": None,
                    "cant_rto_3": None,
                    "valor_rto_3": None,
                    "cant_rto_4": None,
                    "valor_rto_4": None,
                    "cant_tiempo_restauracion": None,
                    "valor_tiempo_restauracion": None,
                    "cant_oportunidad_actividades": None,
                    "valor_oportunidad_actividades": None,
                    "valor_total": None,
                },
                "user_created": user_id,
                "user_updated": user_id,
                "created_at": datetime_now,
                "updated_at": datetime_now,
            }
        ],
        }
    )
    return document

