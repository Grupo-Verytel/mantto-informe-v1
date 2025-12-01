"""
Generador de Informes Mensuales ETB
Punto de entrada principal
"""
import argparse
from pathlib import Path
from datetime import datetime
import config
from src.generadores.seccion_1_info_general import GeneradorSeccion1
from src.generadores.seccion_2_mesa_servicio import GeneradorSeccion2
from src.generadores.seccion_3_ans import GeneradorSeccion3
from src.generadores.seccion_4_bienes import GeneradorSeccion4
from src.generadores.seccion_5_laboratorio import GeneradorSeccion5
from src.generadores.seccion_6_visitas import GeneradorSeccion6
from src.generadores.seccion_7_siniestros import GeneradorSeccion7
from src.generadores.seccion_8_presupuesto import GeneradorSeccion8
from src.generadores.seccion_9_riesgos import GeneradorSeccion9
from src.generadores.seccion_10_sgsst import GeneradorSeccion10
from src.generadores.seccion_11_valores import GeneradorSeccion11
from src.generadores.seccion_12_conclusiones import GeneradorSeccion12
from src.generadores.seccion_13_anexos import GeneradorSeccion13
from src.generadores.seccion_14_control_cambios import GeneradorSeccion14

# Importar otros generadores conforme se vayan creando
# ...

def generar_informe(anio: int, mes: int, version: int = 1):
    """
    Genera el informe mensual completo
    
    Args:
        anio: Año del informe (ej: 2025)
        mes: Mes del informe (1-12)
        version: Versión del documento
    """
    print(f"\n{'='*60}")
    print(f">>> GENERADOR DE INFORMES MENSUALES ETB")
    print(f"   Contrato: {config.CONTRATO['numero']}")
    print(f"   Periodo: {config.get_periodo_texto(anio, mes)}")
    print(f"{'='*60}\n")
    
    # Validar rango de fechas
    if not validar_periodo(anio, mes):
        print("[ERROR] Periodo fuera del rango del contrato")
        print(f"   Rango válido: Noviembre 2024 - Octubre 2025")
        return
    
    # Crear directorio de salida si no existe
    output_dir = config.OUTPUT_DIR / f"{anio}" / f"{mes:02d}_{config.MESES[mes]}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Lista de generadores a ejecutar
    generadores = [
        GeneradorSeccion1(anio, mes),
        GeneradorSeccion2(anio, mes),
        GeneradorSeccion3(anio, mes),
        GeneradorSeccion4(anio, mes),
        GeneradorSeccion5(anio, mes),
        GeneradorSeccion6(anio, mes),
        GeneradorSeccion7(anio, mes),
        GeneradorSeccion8(anio, mes),
        GeneradorSeccion9(anio, mes),
        GeneradorSeccion10(anio, mes),
        GeneradorSeccion11(anio, mes),
        GeneradorSeccion12(anio, mes),
        GeneradorSeccion13(anio, mes),
        GeneradorSeccion14(anio, mes),
        # Agregar más generadores conforme se desarrollen
        # ...
    ]
    
    # Generar cada sección
    secciones_generadas = []
    for generador in generadores:
        try:
            print(f"[*] Generando: {generador.nombre_seccion}...")
            output_file = output_dir / f"{generador.template_file}"
            generador.guardar(output_file)
            secciones_generadas.append(output_file)
        except Exception as e:
            print(f"[ERROR] Error en {generador.nombre_seccion}: {e}")
    
    # TODO: Combinar todas las secciones en un solo documento
    # combinar_secciones(secciones_generadas, output_dir, anio, mes, version)
    
    print(f"\n{'='*60}")
    print(f"[OK] Proceso completado")
    print(f"   Secciones generadas: {len(secciones_generadas)}")
    print(f"   Ubicación: {output_dir}")
    print(f"{'='*60}\n")

def validar_periodo(anio: int, mes: int) -> bool:
    """Valida que el periodo esté dentro del rango del contrato"""
    fecha = datetime(anio, mes, 1)
    fecha_inicio = datetime(2024, 11, 1)  # Noviembre 2024
    fecha_fin = datetime(2025, 10, 31)    # Octubre 2025
    
    return fecha_inicio <= fecha <= fecha_fin

def main():
    """Punto de entrada con argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(
        description="Generador de Informes Mensuales ETB - Contrato SCJ-1809-2024"
    )
    parser.add_argument(
        "--anio", "-a",
        type=int,
        default=datetime.now().year,
        help="Año del informe (default: año actual)"
    )
    parser.add_argument(
        "--mes", "-m",
        type=int,
        default=datetime.now().month,
        help="Mes del informe 1-12 (default: mes actual)"
    )
    parser.add_argument(
        "--version", "-v",
        type=int,
        default=1,
        help="Versión del documento (default: 1)"
    )
    
    args = parser.parse_args()
    
    # Validar mes
    if not 1 <= args.mes <= 12:
        print("[ERROR] El mes debe estar entre 1 y 12")
        return
    
    generar_informe(args.anio, args.mes, args.version)

