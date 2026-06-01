from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet

from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

def generar_pdf_reporte(
    resultados,
    alertas,
    nombre_archivo = f"reportes/reporte_dengue_{timestamp}.pdf"
):

    doc = SimpleDocTemplate(nombre_archivo)

    styles = getSampleStyleSheet()

    elementos = []

    # =====================================
    # TÍTULO
    # =====================================
    elementos.append(
        Paragraph(
            "REPORTE DE PREDICCIÓN DE DENGUE",
            styles["Title"]
        )
    )

    elementos.append(Spacer(1, 12))

    # =====================================
    # FECHA
    # =====================================
    elementos.append(
        Paragraph(
            f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            styles["Normal"]
        )
    )

    elementos.append(Spacer(1, 12))

    # =====================================
    # RESUMEN
    # =====================================
    elementos.append(
        Paragraph(
            f"Total de predicciones: {len(resultados)}",
            styles["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Total de alertas: {len(alertas)}",
            styles["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            "Modelo utilizado: XGBoost",
            styles["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            "Objetivo: Predicción temprana de brotes de dengue",
            styles["Normal"]
        )
    )

    elementos.append(Spacer(1, 20))

    # =====================================
    # ALERTAS
    # =====================================
    if alertas:

        elementos.append(
            Paragraph(
                "Zonas con riesgo alto detectadas",
                styles["Heading2"]
            )
        )

        elementos.append(Spacer(1, 10))

        for alerta in alertas:

            texto = f"""
            Provincia: {alerta.get('provincia', 'N/A')}
            Distrito: {alerta.get('distrito', 'N/A')}
            Año: {alerta.get('ano', 'N/A')}
            Semana: {alerta.get('semana', 'N/A')}
            Casos estimados: {alerta.get('prediccion', 0)}
            """

            elementos.append(
                Paragraph(
                    texto,
                    styles["Normal"]
                )
            )

            elementos.append(
                Spacer(1, 10)
            )

    else:

        elementos.append(
            Paragraph(
                "No se detectaron zonas con riesgo alto.",
                styles["Normal"]
            )
        )

    elementos.append(PageBreak())

    # =====================================
    # TODAS LAS PREDICCIONES
    # =====================================
    elementos.append(
        Paragraph(
            "Detalle de Predicciones",
            styles["Heading1"]
        )
    )

    elementos.append(
        Spacer(1, 10)
    )

    for item in resultados:

        texto = f"""
        Provincia: {item.get('provincia')}<br/>
        Distrito: {item.get('distrito')}<br/>
        Año: {item.get('ano')}<br/>
        Semana: {item.get('semana')}<br/>
        Predicción: {round(float(item.get('prediccion', 0)), 2)}
        """

        elementos.append(
            Paragraph(
                texto,
                styles["Normal"]
            )
        )

        elementos.append(
            Spacer(1, 8)
        )

    doc.build(elementos)

    return nombre_archivo