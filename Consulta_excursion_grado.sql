SELECT 
    e.FECHA, 
    e.LUGAR, 
    e.DISTRITO, 
    g.GRADO, 
    g.SECCION, 
    g.TURNO,
	a.NOMBRE,
	a.APELLIDO
FROM 
    excursion e
INNER JOIN  
    grado g ON e.IdGRADO = g.IdGRADO
INNER JOIN  	
	alumnos a ON e.IdEXCURSION = a.IdEXCURSION
WHERE 
    g.IdGRADO = 6;
