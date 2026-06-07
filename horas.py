"""
Pau Pont

Normalització d'expressions horàries utilitzant
expressions regulars.
"""

import re


def convertir_12h(hora, minuts, periode):
    """
    Converteix una hora en format de 12 hores
    amb període (matí, tarda, etc.) a format 24 hores.
    """

    if not (1 <= hora <= 12 and 0 <= minuts <= 59):
        return None

    if periode == "mañana":
        if 4 <= hora <= 12:
            return f"{hora % 12:02d}:{minuts:02d}"

    elif periode == "mediodía":
        if hora == 12:
            return f"12:{minuts:02d}"
        if 1 <= hora <= 3:
            return f"{hora + 12:02d}:{minuts:02d}"

    elif periode == "tarde":
        if 3 <= hora <= 8:
            return f"{hora + 12:02d}:{minuts:02d}"

    elif periode == "noche":
        if hora == 12:
            return f"00:{minuts:02d}"

        if 1 <= hora <= 4:
            return f"{hora:02d}:{minuts:02d}"

        if 8 <= hora <= 11:
            return f"{hora + 12:02d}:{minuts:02d}"

    elif periode == "madrugada":
        if 1 <= hora <= 6:
            return f"{hora:02d}:{minuts:02d}"

    return None


def normalizaHoras(ficText, ficNorm):
    """
    Lee un fichero de texto y genera otro en el que las
    expresiones horarias aparecen normalizadas en formato HH:MM.
    """

    def reemplazo_hora(match):

        hora = int(match.group(1))
        minuto = int(match.group(2))

        if 0 <= hora <= 23 and 0 <= minuto <= 59:
            return f"{hora:02d}:{minuto:02d}"

        return match.group(0)

    def reemplazo_hm(match):

        hora = int(match.group(1))

        if match.group(2):
            minuto = int(match.group(2))
        else:
            minuto = 0

        if 0 <= hora <= 23 and 0 <= minuto <= 59:
            return f"{hora:02d}:{minuto:02d}"

        return match.group(0)

    def reemplazo_frase(match):

        hora = int(match.group(1))
        expresion = match.group(2)
        periode = match.group(3)

        if expresion == "en punto":
            minuts = 0

        elif expresion == "y cuarto":
            minuts = 15

        elif expresion == "y media":
            minuts = 30

        elif expresion == "menos cuarto":
            hora -= 1

            if hora == 0:
                hora = 12

            minuts = 45

        else:
            return match.group(0)

        resultat = convertir_12h(hora, minuts, periode)

        return resultat if resultat else match.group(0)

    def reemplazo_simple(match):

        hora = int(match.group(1))
        periode = match.group(2)

        resultat = convertir_12h(hora, 0, periode)

        return resultat if resultat else match.group(0)

    with open(ficText, encoding="utf-8") as entrada, \
         open(ficNorm, "w", encoding="utf-8") as salida:

        for linea in entrada:

            linea = re.sub(
                r"\b(\d{1,2}):(\d{2})\b",
                reemplazo_hora,
                linea
            )

            linea = re.sub(
                r"\b(\d{1,2})h(?:([0-9]{1,2})m)?\b",
                reemplazo_hm,
                linea
            )

            linea = re.sub(
                r"\b(\d{1,2})\s*"
                r"(en punto|y cuarto|y media|menos cuarto)"
                r"\s+de la\s+"
                r"(mañana|tarde|noche|madrugada|mediodía)\b",
                reemplazo_frase,
                linea
            )

            linea = re.sub(
                r"\b(\d{1,2})\s+de la\s+"
                r"(mañana|tarde|noche|madrugada|mediodía)\b",
                reemplazo_simple,
                linea
            )

            salida.write(linea)