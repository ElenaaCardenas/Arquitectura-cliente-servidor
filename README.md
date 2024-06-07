En este primer examen harán un programa con la arquitectura cliente-servidor en dos archivos. El objetivo es
evaluar su conocimiento a la hora de implementar esta arquitectura y para esto realizarán las siguientes
actividades:
1. Crear un servidor como lo hemos visto en clase que se comunique con un cliente.
2. El servidor leerá un archivo llamado DB.csv como lo vimos en clase, este archivo se los voy a
proporcionar.
a. El archivo es separado por comas y lo van a leer con pandas.
b. Las columnas del archivo son:
i. Nombre
ii. Password
iii. Genero
iv. Edad
v. Email

3. El servidor debe ser capaz de leerlo y de editarlo para añadir nuevos datos.
a. Estos datos pueden provenir de uno o más clientes como lo vimos en el programa del chat.
4. El servidor debe poder realizar las siguientes búsquedas y entregarlas a uno o más clientes:
a. Buscar por nombre y entregar los datos del renglón que se busca:
i. Ejemplo:
Cliente: Buscar “Adrián”
Respuesta del servidor: “Adrián,12345,Masculino,30,ejemplo@.com”

b. Aplicar lo mismo para la columna email.
c. Buscar todos los clientes que cumplan con un criterio de edad.
d. Buscar todos los clientes que cumplan con un criterio de género.
5. Ambos deben de funcionar en diferentes consolas.
