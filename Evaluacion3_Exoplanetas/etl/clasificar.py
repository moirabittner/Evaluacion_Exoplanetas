"""
Módulo de clasificación de exoplanetas.
Clasifica planetas según su radio en radios de Júpiter.
"""

def clasificar_planeta(radio: float) -> str:
    """
    Clasifica el tipo de planeta según su radio en radios de Júpiter.

    Parámetros:
        radio (float): Radio del planeta en radios de Júpiter.

    Retorna:
        str: Tipo de planeta:
            - 'Rocoso'          si radio < 0.16
            - 'Neptuniano'      si radio < 0.28
            - 'Gigante Gaseoso' si radio >= 0.28
            - 'Desconocido'     si el valor es nulo
    """
    if radio is None:
        return "Desconocido"
    if radio < 0.16:
        return "Rocoso"
    elif radio < 0.28:
        return "Neptuniano"
    else:
        return "Gigante Gaseoso"