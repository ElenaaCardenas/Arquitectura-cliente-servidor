import socket

# Funciones para comunicarse con el servidor
def buscar_nombre(cliente, nombre):
    cliente.send('BN'.encode('utf-8'))
    cliente.send(nombre.encode('utf-8'))
    respuesta = cliente.recv(1024).decode('utf-8')
    print(respuesta)

def buscar_correo(cliente, correo):
    cliente.send('BC'.encode('utf-8'))
    cliente.send(correo.encode('utf-8'))
    respuesta = cliente.recv(1024).decode('utf-8')
    print(respuesta)

def buscar_edad(cliente, edad):
    cliente.send('BE'.encode('utf-8'))
    cliente.send(str(edad).encode('utf-8'))
    respuesta = cliente.recv(1024).decode('utf-8')
    print(respuesta)

def buscar_genero(cliente, genero):
    cliente.send('BG'.encode('utf-8'))
    cliente.send(genero.encode('utf-8'))
    respuesta = cliente.recv(1024).decode('utf-8')
    print(respuesta)

def agregar_nuevos_datos(cliente, nuevos_datos):
    cliente.send('AN'.encode('utf-8'))

    num_nuevos = str(len(nuevos_datos))
    cliente.send(num_nuevos.encode('utf-8'))

    for datos in nuevos_datos:
        cliente.send(datos['Nombre'].encode('utf-8'))
        cliente.send(datos['Password'].encode('utf-8'))
        cliente.send(datos['Genero'].encode('utf-8'))
        cliente.send(str(datos['Edad']).encode('utf-8'))
        cliente.send(datos['Correo'].encode('utf-8'))

    respuesta = cliente.recv(1024).decode('utf-8')
    print(respuesta)

def desconectar(cliente):
    cliente.send('S'.encode('utf-8'))
    cliente.close()


# socket del cliente
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 50007))

while True:
    print("\nMenú de opciones:")
    print("1. Busqueda por nombre")
    print("2. Busqueda por correo")
    print("3. Busqueda por edad")
    print("4. Busqueda por genero")
    print("5. Añadir nuevos datos")
    print("6. Desconectar")

    opcion = input("Ingrese el número de la opción deseada: ")

    if opcion == '1':
        nombre = input("Ingrese el nombre a buscar: ")
        buscar_nombre(cliente, nombre)

    elif opcion == '2':
        correo = input("Ingrese el correo a buscar: ")
        buscar_correo(cliente, correo)

    elif opcion == '3':
        edad = int(input("Ingrese la edad a buscar: "))
        buscar_edad(cliente, edad)

    elif opcion == '4':
        genero = input("Ingrese el genero a buscar: ")
        buscar_genero(cliente, genero)

    elif opcion == '5':
        num_nuevos = int(input("Ingrese la cantidad de nuevos datos a añadir: "))
        nuevos_datos = []

        for _ in range(num_nuevos):
            nuevo_nombre = input("Nuevo Nombre: ")
            nuevo_password = input("Nueva Password: ")
            nuevo_genero = input("Nuevo Género: ")
            nueva_edad = int(input("Nueva Edad: "))
            nuevo_correo = input("Nuevo Correo: ")

            nuevos_datos.append({
                'Nombre': nuevo_nombre,
                'Password': nuevo_password,
                'Genero': nuevo_genero,
                'Edad': nueva_edad,
                'Correo': nuevo_correo
            })

        agregar_nuevos_datos(cliente, nuevos_datos)

    elif opcion == '6':
        desconectar(cliente)
        break

    else:
        print("Opción no válida. Inténtelo de nuevo.")
