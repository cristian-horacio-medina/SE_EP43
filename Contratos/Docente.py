class Docente:

    # constructor
    def __init__(self, docente_id, docente, carrera,comision_id, division):
        self.__docente_id = docente_id
        self.__docente = docente
        self.__carrera = carrera
        self.__comision_id = comision_id
        self.__division = division
            
    #retornar Docente
    def info(self):
        return self.__docente_id,self.__docente,self.__carrera, self.__comision_id, self.__division
#prueba
# docente=Docente(821,"Juan","Marketing",1203)
# print(docente.info())