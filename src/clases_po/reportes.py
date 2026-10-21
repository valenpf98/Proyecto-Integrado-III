"""Generación de reportes de DataFrames."""
from __future__ import annotations

from pathlib import Path
import pandas as pd


class Reportes:
    """Imprime y guarda un resumen legible y descriptivo de un DataFrame."""

    def generar_reporte(self, df: pd.DataFrame) -> str:
        """Genera el contenido textual del reporte."""
        self._validar_dataframe(df)
        numericas = df.select_dtypes(include="number")
        categoricas = df.select_dtypes(include="object")

        lineas = [
            "REPORTE DEL DATAFRAME",
            "=" * 60,
            f"Filas: {len(df)}",
            f"Columnas: {len(df.columns)}",
            f"Duplicados: {int(df.duplicated().sum())}",
            "",
            "Columnas y tipos:",
            *[f"- {columna}: {tipo}" for columna, tipo in df.dtypes.items()],
            "",
            "Valores nulos por columna:",
            *[f"- {columna}: {cantidad}" for columna, cantidad in df.isna().sum().items()],
        ]

        # Estadísticas numéricas
        if not numericas.empty:
            lineas += [
                "",
                "Estadísticas numéricas:",
                numericas.describe().round(3).to_string(),
                "",
                "Mediana de columnas numéricas:",
                str(numericas.median().round(3)),
            ]

        # Valores únicos en columnas categóricas
        if not categoricas.empty:
            lineas += [
                "",
                "Valores únicos por columna categórica:",
                *[f"- {col}: {df[col].nunique()}" for col in categoricas.columns],
            ]

            # Ejemplo de distribución en columnas clave si existen
            for col in ["difficulty", "body_focus"]:
                if col in df.columns:
                    lineas += [
                        "",
                        f"Distribución de {col}:",
                        str(df[col].value_counts().head()),
                    ]

        return "\n".join(lineas) + "\n"

    def imprimir_reporte(self, df: pd.DataFrame) -> None:
        """Imprime en la consola el reporte del DataFrame."""
        print(self.generar_reporte(df), end="")

    def guardar_reporte(self, df: pd.DataFrame, ruta: str | Path) -> Path:
        """Guarda el reporte en un archivo de texto y devuelve su ruta."""
        path = Path(ruta)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.generar_reporte(df), encoding="utf-8")
        return path

    @staticmethod
    def _validar_dataframe(df: pd.DataFrame) -> None:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df debe ser un pandas.DataFrame.")
