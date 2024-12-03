class Alumno:

	#constructor
	def __init__(self,apellidos,nombres,fechanac):
		self.__apellidos=apellidos
  		self.__nombres=nombres
		self.__fechanac=fechanac

	def info(self):
		return self.__nombres,self.__apellidos,self.__fechanac