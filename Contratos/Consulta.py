import pyodbc
from datetime import datetime

anio_actual = datetime.now().year


class Consulta:

    # CREATE='''
    # 		CREATE TABLE empleado (
    # 		ID INTEGER PRIMARY KEY AUTOINCREMENT,
    # 		NOMBRE VARCHAR(50) NOT NULL,
    # 		CARGO VARCHAR(50) NOT NULL,
    # 		SALARIO INT NOT NULL)
    # 		'''

    # DELETE_TABLE="DROP TABLE empleado"

    # INSERT = "INSERT INTO empleado VALUES(NULL,?,?,?)"

    # SELECT = "SELECT * FROM AL_ALUMNOS_EMAIL"

    SELECT = """
            Select DISTINCT al_docentes.docente_id, al_docentes.combo As docente, AL_PLANES_EST_CARRE.Combo As carrera, AL_COMISIONES.Comision_ID, al_comisiones.anio, al_comisiones.division,AL_TURNOS.Descripcion As turno, al_materias.descripcion As materia, tg_dias.nombredia, al_docentes.contratado
            From al_comisiones_mate
            INNER Join al_comisiones_mate_horarios ON al_comisiones_mate.comisionmate_id = al_comisiones_mate_horarios.comisionmate_id
            INNER Join al_comisiones ON al_comisiones_mate.comision_id = al_comisiones.comision_id
            INNER Join al_carreras ON al_comisiones.carrera_id = al_carreras.carrera_id
            INNER Join al_docentes ON al_docentes.Docente_ID = al_comisiones_mate.docente_id
            INNER Join TG_TIPOS_DOCUMENTO on TG_TIPOS_DOCUMENTO.TIPO_DOCUMENTO_ID = al_docentes.TipoDoc_ID
            INNER Join tg_dias ON tg_dias.Dia_ID = al_comisiones_mate_horarios.Dia_ID
            INNER Join tg_sexos ON tg_sexos.Sexo_ID = al_docentes.Sexo_ID
            INNER Join al_materias ON al_materias.materia_id = al_comisiones_mate.materia_id
            INNER Join al_horarios ON al_horarios.Horario_ID = al_comisiones_mate_horarios.Horario_ID
            INNER Join AL_CICLOS_LECTIVOS_MODULOS ON AL_CICLOS_LECTIVOS_MODULOS.CicloLectModulo_ID = al_comisiones.CicloLectModulo_ID
            INNER Join AL_CICLOS_LECTIVOS ON AL_CICLOS_LECTIVOS.CicloLectivo_ID = AL_CICLOS_LECTIVOS_MODULOS.CicloLectivo_ID
            INNER Join AL_TURNOS ON AL_TURNOS.Turno_ID=AL_COMISIONES.Turno_ID
            INNER Join AL_PLANES_EST_CARRE_MATE ON AL_PLANES_EST_CARRE_MATE.Materia_ID=AL_MATERIAS.materia_ID
    		INNER JOIN AL_PLANES_EST_CARRE ON AL_PLANES_EST_CARRE.PlanEstCarrera_ID=AL_PLANES_EST_CARRE_MATE.PlanEstCarrera_ID
            WHERE
            AL_CICLOS_LECTIVOS.Descripcion = ?
            And AL_CICLOS_LECTIVOS_MODULOS.Modulo_ID = ?
            And al_comisiones.carrera_id = ?
            And al_docentes.Docente_ID <> 5130
            And  al_docentes.Docente_ID <> 99999999
            GROUP BY
           al_docentes.docente_id,
           al_docentes.combo,
           AL_PLANES_EST_CARRE.Combo,
           al_turnos.Descripcion,
           AL_COMISIONES.Comision_ID,
           al_comisiones.anio,
           al_comisiones.division,
           al_materias.descripcion,
           tg_dias.nombredia,
           al_docentes.contratado
           order by docente asc, carrera asc, anio asc,Division asc ,turno asc, nombreDia asc
    """

    UPDATE = "UPDATE al_comisiones SET division = ? WHERE comision_id = ?"

    # DELETE = "DELETE FROM empleado WHERE ID="

    BUSCAR = """
SELECT DISTINCT 
    al_docentes.docente_id, 
    al_docentes.combo AS docente, 
    AL_PLANES_EST_CARRE.NombreCompleto AS carrera, 
    AL_COMISIONES.Comision_ID, 
    al_comisiones.anio, 
    al_comisiones.division, 
    AL_TURNOS.Descripcion AS turno, 
    al_materias.descripcion AS materia, 
    tg_dias.nombredia, 
    al_docentes.contratado,
    TG_TIPOS_DOCUMENTO.NOMBRE_ABR AS tipo_doc, 
    AL_DOCENTES.NumDoc AS DNI
FROM 
    al_comisiones_mate
INNER JOIN 
    al_comisiones_mate_horarios ON al_comisiones_mate.comisionmate_id = al_comisiones_mate_horarios.comisionmate_id
INNER JOIN 
    al_comisiones ON al_comisiones_mate.comision_id = al_comisiones.comision_id
INNER JOIN 
    al_carreras ON al_comisiones.carrera_id = al_carreras.carrera_id
INNER JOIN 
    al_docentes ON al_docentes.Docente_ID = al_comisiones_mate.docente_id
INNER JOIN 
    TG_TIPOS_DOCUMENTO ON TG_TIPOS_DOCUMENTO.TIPO_DOCUMENTO_ID = al_docentes.TipoDoc_ID
INNER JOIN 
    tg_dias ON tg_dias.Dia_ID = al_comisiones_mate_horarios.Dia_ID
INNER JOIN 
    tg_sexos ON tg_sexos.Sexo_ID = al_docentes.Sexo_ID
INNER JOIN 
    al_materias ON al_materias.materia_id = al_comisiones_mate.materia_id
INNER JOIN 
    al_horarios ON al_horarios.Horario_ID = al_comisiones_mate_horarios.Horario_ID
INNER JOIN 
    AL_CICLOS_LECTIVOS_MODULOS ON AL_CICLOS_LECTIVOS_MODULOS.CicloLectModulo_ID = al_comisiones.CicloLectModulo_ID
INNER JOIN 
    AL_CICLOS_LECTIVOS ON AL_CICLOS_LECTIVOS.CicloLectivo_ID = AL_CICLOS_LECTIVOS_MODULOS.CicloLectivo_ID
INNER JOIN 
    AL_TURNOS ON AL_TURNOS.Turno_ID = AL_COMISIONES.Turno_ID
INNER JOIN 
    AL_PLANES_EST_CARRE_MATE ON AL_PLANES_EST_CARRE_MATE.Materia_ID = AL_MATERIAS.materia_ID
INNER JOIN 
    AL_PLANES_EST_CARRE ON AL_PLANES_EST_CARRE.PlanEstCarrera_ID = AL_PLANES_EST_CARRE_MATE.PlanEstCarrera_ID
WHERE 
    AL_CICLOS_LECTIVOS.Descripcion = ?
AND 
    AL_CICLOS_LECTIVOS_MODULOS.Modulo_ID = ?
AND 
    al_comisiones.carrera_id = ?
AND 
    al_docentes.Docente_ID <> 5130
AND 
    al_docentes.Docente_ID <> 99999999
AND 
    al_docentes.combo LIKE ?
GROUP BY
    al_docentes.docente_id,
    al_docentes.combo,
    AL_PLANES_EST_CARRE.NombreCompleto,
    AL_TURNOS.Descripcion,
    AL_COMISIONES.Comision_ID,
    al_comisiones.anio,
    al_comisiones.division,
    al_materias.descripcion,
    tg_dias.nombredia,
    al_docentes.contratado,
    TG_TIPOS_DOCUMENTO.NOMBRE_ABR,
    AL_DOCENTES.NumDoc
ORDER BY 
    docente ASC, 
    carrera ASC, 
    anio ASC, 
    division ASC, 
    turno ASC, 
    nombredia ASC
"""

    BUSCAR_CARRERA = """
    SELECT DISTINCT al_comisiones.carrera_id, AL_CARRERAS.NombreCompleto
    FROM al_comisiones_mate
    INNER JOIN al_comisiones_mate_horarios ON al_comisiones_mate.comisionmate_id = al_comisiones_mate_horarios.comisionmate_id
    INNER JOIN al_comisiones ON al_comisiones_mate.comision_id = al_comisiones.comision_id
    INNER JOIN al_carreras ON al_comisiones.carrera_id = al_carreras.carrera_id
    INNER JOIN al_docentes ON al_docentes.Docente_ID = al_comisiones_mate.docente_id
    INNER JOIN al_materias ON al_materias.materia_id = al_comisiones_mate.materia_id
    INNER JOIN al_horarios ON al_horarios.Horario_ID = al_comisiones_mate_horarios.Horario_ID
    INNER JOIN AL_CICLOS_LECTIVOS_MODULOS ON AL_CICLOS_LECTIVOS_MODULOS.CicloLectModulo_ID = al_comisiones.CicloLectModulo_ID
    INNER JOIN AL_CICLOS_LECTIVOS ON AL_CICLOS_LECTIVOS.CicloLectivo_ID = AL_CICLOS_LECTIVOS_MODULOS.CicloLectivo_ID
    INNER JOIN AL_TURNOS ON AL_TURNOS.Turno_ID = AL_COMISIONES.Turno_ID
    INNER JOIN AL_PLANES_EST_CARRE_MATE ON AL_PLANES_EST_CARRE_MATE.Materia_ID = AL_MATERIAS.materia_ID
    INNER JOIN AL_PLANES_EST_CARRE ON AL_PLANES_EST_CARRE.PlanEstCarrera_ID = AL_PLANES_EST_CARRE_MATE.PlanEstCarrera_ID
    WHERE AL_CICLOS_LECTIVOS.Descripcion = ?
    AND AL_CICLOS_LECTIVOS_MODULOS.Modulo_ID = ?
    AND al_docentes.Docente_ID <> 5130
    AND al_docentes.Docente_ID <> 99999999
    ORDER BY al_comisiones.carrera_id ASC, AL_CARRERAS.NombreCompleto
"""

    Docente_materias = """
    select distinct
    com.Combo2 as Comisión,car.NombreCompleto as Carrera  ,mat.combo,dia.NombreDia,doc.Combo as Docente
    from AL_ALUMNOS_MATERIAS al
    inner join al_comisiones_mate comat on al.Comision_ID=comat.Comision_ID and al.Materia_ID=comat.Materia_ID --and EstadoMateria_ID in (1,2,3,4,5,9)
    inner join al_comisiones com on al.Comision_ID=com.Comision_ID
    inner join AL_PLANES_EST_CARRE car on al.Carrera_ID=car.Carrera_ID and al.PlanEstudio_ID=car.PlanEstudio_ID
    inner join AL_MATERIAS mat on al.materia_ID=mat.Materia_ID
    inner join AL_CICLOS_LECTIVOS ciclo on al.CicloLectivo_ID=ciclo.CicloLectivo_ID
    inner join AL_COMISIONES_MATE_HORARIOS comath on comat.ComisionMate_ID = comath.ComisionMate_ID
    inner join TG_DIAS dia on dia.Dia_ID=comath.Dia_ID
    inner join AL_DOCENTES doc on doc.Docente_ID=comat.Docente_ID
    where ciclo.Descripcion = ? al.Modulo_ID = ?
    and comat.Docente_ID  = 5165 --99999999
    and com.Activo = 'S'

    order by dia.NombreDia --doc.Combo,2,1,3
"""
