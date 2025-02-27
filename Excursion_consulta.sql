SELECT 
    EXCURSION.FECHA, 
    GRADO.GRADO, 
    GRADO.SECCION, 
    'Alumno' AS Tipo, 
    alumnos.APELLIDO, 
    alumnos.NOMBRE,
    EXCURSION.LOCALIDAD,
    EXCURSION.LOCALIDAD_ESCUELA,
    EXCURSION.ESCUELA,
    1 AS Orden -- Prioridad para los alumnos
FROM EXCURSION
JOIN GRADO ON EXCURSION.IdGRADO = GRADO.IdGRADO
JOIN alumnos ON EXCURSION.IdEXCURSION = alumnos.IdEXCURSION
WHERE EXCURSION.FECHA = '24/10/2024'

UNION ALL

SELECT 
    EXCURSION.FECHA, 
    GRADO.GRADO, 
    GRADO.SECCION, 
    'Acompañante' AS Tipo, 
    acompanantes.APELLIDO, 
    acompanantes.NOMBRE,
    EXCURSION.LOCALIDAD,
    EXCURSION.LOCALIDAD_ESCUELA,
    EXCURSION.ESCUELA,
    2 AS Orden -- Prioridad para los acompañantes
FROM EXCURSION
JOIN GRADO ON EXCURSION.IdGRADO = GRADO.IdGRADO
JOIN acompanantes ON EXCURSION.IdEXCURSION = acompanantes.IdEXCURSION
WHERE EXCURSION.FECHA = '24/10/2024'

ORDER BY Orden ASC, APELLIDO ASC;
