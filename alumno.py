"""
Pau Pont

Tractament de fitxers de notes d'alumnes.
Inclou la classe Alumno i la funció leeAlumnos().
"""

import re


class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        return Alumno(self.nombre, self.numIden,
                      self.notas + [other])

    def media(self):
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'


def leeAlumnos(ficAlum):
    """
    Lee un fichero de alumnos y devuelve un diccionario cuya
    clave es el nombre del alumno y el valor el objeto Alumno.

    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171     Blanca Agirrebarrenetse 9.5
    23      Carles Balcells de Lara 4.9
    68      David Garcia Fuster 7.0
    """

    alumnos = {}

    patron = re.compile(
        r'^(\d+)\s+(.+?)\s+((?:\d+(?:\.\d+)?(?:\s+|$))+)$'
    )

    with open(ficAlum, encoding="utf-8") as fichero:

        for linea in fichero:

            linea = linea.strip()

            if not linea:
                continue

            coincidencia = patron.match(linea)

            if coincidencia:

                identificador = int(coincidencia.group(1))
                nombre = coincidencia.group(2)

                notas = [
                    float(nota)
                    for nota in re.findall(
                        r'\d+(?:\.\d+)?',
                        coincidencia.group(3)
                    )
                ]

                alumnos[nombre] = Alumno(
                    nombre,
                    identificador,
                    notas
                )

    return alumnos


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)