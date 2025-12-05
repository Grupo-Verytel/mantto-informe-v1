from datetime import datetime
from typing import Dict, Any, Optional
from src.services.database import get_database


async def get_section2(anio: int, mes: int, user_id: int, name_file: str):
    db = get_database()
    collection = db["section2"]
    
    document = await collection.find_one({"anio": anio, "mes": mes})
    
    if not document:
        await build_section2(anio, mes, user_id, name_file)
        document = await collection.find_one({"anio": anio, "mes": mes})
    
    return document    




# ESTE ES EL ESQUEMA BASE DEL DOCUMENTO EN CASO QUE NO EXISTA #
async def build_section2(anio: int, mes: int , user_id: int, name_file: str):

    db = get_database()
    datetime_now = datetime.now()    
    collection = db["section2"]
    user_created = user_id    
    document = await collection.insert_one(
        { 
        "section": "2",
        "title": "INFORME DE MESA DE SERVICIO",
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
                "id": "2",
                "level": 1,
                "title": "2. INFORME DE MESA DE SERVICIO",
                "content": {                    
                    "image": "",                    
                },
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,
                "updated_at": datetime_now,
            },
            {
                "id": "2.1",
                "level": 2,
                "title": "2.1 INFORME DE MESA DE SERVICIO",
                "content": {
                    "route": "",      
                    "image": "",    
                    "table_1": [
                        {"item": "" , "fecha": "" , "referencia": "" , "radicado": "" , "estado": "", "aprobacion": ""}
                    ],
                    "table_2": [
                        {"subsistema": "" , "diagnostico": "" , "diagnostico_subsistema": "" , "limpieza_acrilico": "" , "mto_acometida": "" , "mto_correctivo": "" , "mto_correctivo_subsistema": "" , "plan_de_choque": "" , "total": ""}
                    ]                       
                },
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,
                "updated_at": datetime_now,
            },
            {
                "id": "2.2",
                "level": 2,
                "title": "HERRAMIENTAS DE TRABAJO",
                "content": {
                    "email": "ergrodz@etb.com.co",
                },
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,     
                "updated_at": datetime_now,
            },
            {
                "id": "2.3",
                "level": 2,
                "title": "VISITAS DE DIAGNÓSTICOS A SUBSISTEMAS",
                "content": {
                    "table_1": [
                        {"subsistema": "" , "ejecutadas": ""}
                    ],
                    "comunicacion": "",
                    "oficio": "",
                },
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,
                "updated_at": datetime_now,
            },
            {
                "id": "2.4",
                "level": 2,
                "title": "INFORME CONSOLIDADO DEL ESTADO DE LOS TICKETS ADMINISTRATIVOS",
                "content": {
                    "table_1": [
                        {"subsistema": "" , "diagnostico": "" , "diagnostico_subsistema": "" , "limpieza_acrilico": "" , "mto_acometida": "" , "mto_correctivo": "" , "mto_correctivo_subsistema": "" , "plan_de_choque": "" , "total": ""}                        
                    ],
                    "name_document": "",
                    "table_2": [
                        {"subsistema": "" , "cerrado": "" , "en_curso_asignada": "" , "en_curso_planificada": "" , "en_espera": "" , "resueltas": "" , "total": ""}                        
                    ]
                },
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,
                "updated_at": datetime_now,
            },
            {
                "id": "2.5",
                "level": 2,
                "title": "ESCALAMIENTOS",
                "content": {
                    "table_1": [
                        {"escalamiento": "" , "cantidad": ""}
                    ]
                },
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,
                "updated_at": datetime_now,
            },
            {
                "id": "2.5.1",
                "level": 3,
                "title": "ENEL",
                "content": {
                    "table_1": [
                        {"item": "" , "codigo_punto": "" , "ticket_enel": "" , "fecha_escalamiento": "" , "ticket_glpi": ""}
                    ]                    
                },
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,
                "updated_at": datetime_now,
            },
            {
                "id": "2.5.2",
                "level": 3,
                "title": "CAÍDA MASIVA",
                "content": {
                    "table_1": [                        
                        {"item": "" , "punto": "" , "localidad": "" , "cav": "" , "fecha": "" , "consecutivo_caida": ""}
                    ]                    
                },
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,
                "updated_at": datetime_now,
            },
            {
                "id": "2.5.3",
                "level": 3,
                "title": "CONECTIVIDAD",
                "content": {
                    "table_1": [                        
                        {"item": "" , "codigo_punto": "" , "ticket_etb": "" , "fecha_escalamiento": "" , "ticket_glpi": ""}
                    ]                    
                },
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,
                "updated_at": datetime_now,
            },
            {
                "id": "2.6",
                "level": 2,
                "title": "INFORME ACTUALIZADO DE HOJAS DE VIDA DE LOS PUNTOS Y SUBSISTEMAS DE VIDEO VIGILANCIA",
                "content": {
                    "name_document": "",
                },
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,
                "updated_at": datetime_now,
            },
            {
                "id": "2.7",
                "level": 2,
                "title": "INFORME EJECUTIVO DEL ESTADO DEL SISTEMA",
                "content": {
                    "table_1": [
                        {"estado": "" , "cantidad": ""}
                    ],
                    "image": "",
                    "section_1": "",
                    "section_2": "",
                    "table_2": [
                        {"responsable": "" , "cantidad": ""}
                    ],
                    "section_3": "",
                    "table_3": [
                        {"subsistema": "" , "caida_masiva": "" , "fuera_de_servicio": "" , "operativa": "" , "operativa_con_novedad": "" , "total": ""}                        
                    ],
                    "name_document": "",
                },
                "user_created": 1,
                "user_updated": 1,
                "created_at": datetime_now,
                "updated_at": datetime_now,
            }
        ],
        }
    )
    return document