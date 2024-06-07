import socket
import pandas as pd
import threading

# Función para cargar el archivo CSV en un DataFrame
def cargar_datos():
    try:
        # Intenta cargar el archivo existente
        df = pd.read_csv('DB.csv')
    except FileNotFoundError:
        # Si el archivo no existe, crea uno nuevo con las columnas
        df = pd.DataFrame(columns=['Nombre', 'Password', 'Genero', 'Edad', 'Correo'])

    # Añade nuevos datos al DataFrame
    nuevos_datos = pd.DataFrame({
        'Nombre': ['Elena', 'Omar', 'Carlo', 'Mau', 'Isis', 'Feregrino', 'Emiliano'],
        'Password': [12345] * 7,  # Supongamos que todos tienen la misma contraseña
        'Genero': ['Femenino', 'Masculino', 'Masculino', 'Masculino', 'Femenino', 'Masculino', 'Masculino'],
        'Edad': [22, 21, 20, 21, 22, 19, 20],
        'Correo': ['elena@gmai.com', 'omar@gmail.com', 'carlo@gmail.com', 'mau@gmail.com', 'isis@gmail.com', 'Fere@gmail.com', 'emi@gmail.com'] 
    })

    # Concatena el DataFrame existente con los nuevos datos
    df = pd.concat([df, nuevos_datos], ignore_index=True)

    # Guarda el DataFrame actualizado en el archivo CSV
    df.to_csv('DB.csv', index=False)

    return df


# Función para añadir nuevos datos al DataFrame y al archivo CSV
def agregar_nuevos_datos(df, nuevos_datos):
    # Añade nuevos datos al DataFrame
    df = pd.concat([df, nuevos_datos], ignore_index=True)

    # Esto guarda el DataFrame actualizado en el archivo CSV
    df.to_csv('DB.csv', index=False)

    return df

# Función para buscar por nombre o correo
def buscar(df, col, val):
    result = df[df[col] == val]
    return result.to_string(index=False) if not result.empty else "Cliente no encontrado."

# Función para buscar por edad
def buscar_edad(df, edad):
    result = df[df['Edad'] == edad]
    return result.to_string(index=False) if not result.empty else "Clientes no encontrados para la edad especificada."

# Función para buscar por género
def buscar_genero(df, genero):
    result = df[df['Genero'] == genero]
    return result.to_string(index=False) if not result.empty else "Clientes no encontrados para el género especificado."

# Función para manejar las solicitudes de los clientes
def manejar_solicitud(cliente, df):
    while True:
        solicitud = cliente.recv(1024).decode('utf-8')

        if solicitud == 'BN':
            nombre = cliente.recv(1024).decode('utf-8')
            respuesta = buscar(df, 'Nombre', nombre)

        elif solicitud == 'BC':
            correo = cliente.recv(1024).decode('utf-8')
            respuesta = buscar(df, 'Correo', correo)

        elif solicitud == 'BE':
            edad = int(cliente.recv(1024).decode('utf-8'))
            respuesta = buscar_edad(df, edad)

        elif solicitud == 'BG':
            genero = cliente.recv(1024).decode('utf-8')
            respuesta = buscar_genero(df, genero)

        elif solicitud == 'AN':  #Para añadir nuevos datos
            num_nuevos = int(cliente.recv(1024).decode('utf-8'))
            nuevos_datos = []

            for _ in range(num_nuevos):
                nuevo_nombre = cliente.recv(1024).decode('utf-8')
                nuevo_password = cliente.recv(1024).decode('utf-8')
                nuevo_genero = cliente.recv(1024).decode('utf-8')
                nueva_edad = int(cliente.recv(1024).decode('utf-8'))
                nuevo_correo = cliente.recv(1024).decode('utf-8')

                nuevos_datos.append({
                    'Nombre': nuevo_nombre,
                    'Password': nuevo_password,
                    'Genero': nuevo_genero,
                    'Edad': nueva_edad,
                    'Correo': nuevo_correo
                })

            df = agregar_nuevos_datos(df, pd.DataFrame(nuevos_datos))
            respuesta = "Datos añadidos exitosamente."

        elif solicitud == 'S':
            print("Cliente desconectado.")
            break

        cliente.send(respuesta.encode('utf-8'))


# socket del servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('127.0.0.1', 5555))
servidor.listen()

print("Servidor escuchando")

while True:
    cliente, direccion = servidor.accept()
    print(f"Conexión establecida con")
    
    df = cargar_datos()

    # Inicia un hilo para manejar la comunicación con el cliente
    cliente_handler = threading.Thread(target=manejar_solicitud, args=(cliente, df))
    cliente_handler.start()
