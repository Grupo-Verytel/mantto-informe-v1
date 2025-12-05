import calendar   
def _construir_ruta_mes( mes: int, anio: int) -> str:
        """
        Construye la ruta en formato '01OCT – 31OCT' basándose en el mes y año.
        
        Args:
            mes: Número del mes (1-12)
            anio: Año (ej: 2025)
            
        Returns:
            String en formato '01OCT – 31OCT'
        """
        # Abreviaciones de meses en mayúsculas
        meses_abrev = {
            1: "ENE", 2: "FEB", 3: "MAR", 4: "ABR",
            5: "MAY", 6: "JUN", 7: "JUL", 8: "AGO",
            9: "SEP", 10: "OCT", 11: "NOV", 12: "DIC"
        }
        
        # Obtener el último día del mes
        ultimo_dia = calendar.monthrange(anio, mes)[1]
        
        # Construir la ruta
        mes_abrev = meses_abrev.get(mes, "")
        ruta = f"01{mes_abrev} – {ultimo_dia:02d}{mes_abrev}"
        
        return ruta
