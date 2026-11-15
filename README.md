# Simulacro AMIB Figura 3

Simulacro de estudio en terminal para la certificación AMIB Figura 3 (Asesor en Estrategias de Inversión). Python 3.8+, sin dependencias.

> **Aviso:** las preguntas son de elaboración propia con fines de estudio. No son reactivos oficiales, no reflejan el examen real y este proyecto no tiene relación con la AMIB. Verifica siempre los temas y datos contra el manual de estudio vigente.

## Uso

```bash
python simulacro.py                       # 20 preguntas, modo estudio
python simulacro.py -n 40 --modo examen   # resultados hasta el final
python simulacro.py -m deuda              # solo un módulo
python simulacro.py --tiempo 60           # límite de 60 minutos
python simulacro.py --listar              # módulos y número de preguntas
```

- **Modo estudio:** te dice si acertaste y por qué después de cada pregunta.
- **Modo examen:** no hay retroalimentación hasta el final.
- Al terminar muestra tu puntaje por módulo y repasa las preguntas falladas con su explicación.

## Módulos del banco

Fondos de inversión, Análisis económico, Análisis financiero, Normatividad y ética, Deuda, Capitales, Derivados y riesgos.

## Agregar preguntas

Edita `preguntas.json` y agrega objetos con este formato. `correcta` es el índice (desde 0) de la opción correcta; el orden de las opciones se mezcla en cada ejecución.

```json
{
  "modulo": "Deuda",
  "pregunta": "Texto de la pregunta",
  "opciones": ["A", "B", "C", "D"],
  "correcta": 0,
  "explicacion": "Por qué es correcta."
}
```

## Subir a GitHub

```bash
git init
git add .
git commit -m "Simulacro AMIB Figura 3"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/simulacro-amib-f3.git
git push -u origin main
```
