import tkinter as tk
import csv
import random
from tkinter import messagebox

# Variables del juego
vidas = 3
puntos = 0
numero_pregunta = 0
preguntas_juego = []
variables = []
frame_juego = None
frame_inicio = None
aciertos = 0
fallos = 0
respondida = False

# Funcion para cargar preguntas
def cargar_preguntas():
    preguntas = []

    # Leer el archivo
    try:
        with open("preguntas.csv", "r", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            next(lector, None)

            for fila in lector:
                if len(fila) >= 6:
                    preguntas.append(fila)

    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo no encontrado")
        return None

    # Seleccion de preguntas
    if len(preguntas) < 5:
        messagebox.showerror("Error", "Se necesitan al menos 5 preguntas")
        return None

    return random.sample(preguntas, 5)


# Ventana
ventana = tk.Tk()
ventana.title("Quiz de Historia de México")
ventana.geometry("600x450")
ventana.config(bg="#00AAFF")


def crear_pantalla_inicio():
    global frame_inicio, entrada_nombre, preguntas_juego

    frame_inicio = tk.Frame(ventana, bg="#00AAFF")
    frame_inicio.pack(fill="both", expand=True)

    titulo = tk.Label(frame_inicio, text="¿Cuánto sabes de la historia de México? (Escribe tu nombre)", fg="white", bg="#AB9900")
    titulo.pack()

    entrada_nombre = tk.Entry(frame_inicio, bg="white")
    entrada_nombre.pack()

    boton_comenzar = tk.Button(frame_inicio, text="Comenzar", command=comenzar_partida)
    boton_comenzar.pack()


def comenzar_partida():
    global preguntas_juego, frame_juego, respuesta_selec, nombre_jugador
    global vidas_juego, puntos_juego, boton_responder
    global etiqueta_pregunta, boton_respuesta1, boton_respuesta2
    global boton_respuesta3, boton_respuesta4

    nombre_jugador = entrada_nombre.get()

    if nombre_jugador == "":
        messagebox.showwarning(title="Aviso", message="El apartado de nombre está vacío")
        return

    preguntas_juego = cargar_preguntas()

    if preguntas_juego is None:
        return

    # Pantalla de juego
    frame_inicio.pack_forget()

    frame_juego = tk.Frame(ventana, bg="#00AAFF")
    frame_juego.pack(fill="both", expand=True)

    # Centrar las columnas
    frame_juego.columnconfigure(0, weight=1)
    frame_juego.columnconfigure(1, weight=1)

    # Etiqueta vidas
    vidas_juego = tk.Label(frame_juego, text=f"Vidas: {vidas}", fg="black", bg="white")
    vidas_juego.grid(row=0, column=0, columnspan=2, pady=5)

    # Etiqueta puntos
    puntos_juego = tk.Label(frame_juego, text=f"Puntos: {puntos}", fg="black", bg="white")
    puntos_juego.grid(row=1, column=0, columnspan=2, pady=5)

    # Pregunta
    etiqueta_pregunta = tk.Label(frame_juego, text=preguntas_juego[0][0], fg="white", bg="#AB9900")
    etiqueta_pregunta.grid(row=2, column=0, columnspan=2, pady=15)

    # Botones de respuesta
    respuesta_selec = tk.StringVar()

    boton_respuesta1 = tk.Radiobutton(frame_juego, text=preguntas_juego[0][1], variable=respuesta_selec, value=preguntas_juego[0][1], fg="black", bg="#00FFF1")
    boton_respuesta1.grid(row=3, column=0, padx=10, pady=10)

    boton_respuesta2 = tk.Radiobutton(frame_juego, text=preguntas_juego[0][2], variable=respuesta_selec, value=preguntas_juego[0][2], fg="black", bg="#00FFF1")
    boton_respuesta2.grid(row=3, column=1, padx=10, pady=10)

    boton_respuesta3 = tk.Radiobutton(frame_juego, text=preguntas_juego[0][3], variable=respuesta_selec, value=preguntas_juego[0][3], fg="black", bg="#00FFF1")
    boton_respuesta3.grid(row=4, column=0, padx=10, pady=10)

    boton_respuesta4 = tk.Radiobutton(frame_juego, text=preguntas_juego[0][4], variable=respuesta_selec, value=preguntas_juego[0][4], fg="black", bg="#00FFF1")
    boton_respuesta4.grid(row=4, column=1, padx=10, pady=10)

    # Boton responder
    boton_responder = tk.Button(frame_juego, text="Responder", command=comprobar_respuesta, fg="white", bg="green")
    boton_responder.grid(row=5, column=0, columnspan=2, pady=10)

    # Boton siguiente
    boton_siguiente = tk.Button(frame_juego, text="Siguiente", command=avanzar_pregunta, fg="white", bg="green")
    boton_siguiente.grid(row=6, column=0, columnspan=2, pady=5)


# Comprobacion de respuestas
def comprobar_respuesta():
    global respuesta_selec, puntos, vidas, respondida, fallos, aciertos

    respuesta_usuario = respuesta_selec.get()

    # Comprobar que haya seleccionado algo
    if respuesta_usuario == "":
        messagebox.showwarning("Aviso", "Selecciona una respuesta")
        return

    respondida = True

    # Desactivar boton para evitar respuestas repetidas
    boton_responder.config(state="disabled")

    # Comprobar si la respuesta es correcta
    if respuesta_usuario == preguntas_juego[numero_pregunta][5]:
        puntos += 10
        aciertos += 1
        puntos_juego.config(text=f"Puntos: {puntos}")
        messagebox.showinfo("¡Correcto!", "Tu respuesta es correcta")

    else:
        vidas -= 1
        fallos += 1
        vidas_juego.config(text=f"Vidas: {vidas}")
        messagebox.showinfo("¡Incorrecto!", f"Te restan: {vidas}, vidas")

        if vidas == 0:
            messagebox.showinfo("Fin del juego", "Te has quedado sin vidas")
            ver_resultados()
            return


# Avanzar a la siguiente pregunta
def avanzar_pregunta():
    global numero_pregunta, respondida

    # Comprobar si ya respondio
    if not respondida:
        messagebox.showwarning("Aviso", "Primero debes responder la pregunta")
        return

    if numero_pregunta >= len(preguntas_juego) - 1:
        ver_resultados()
        return

    numero_pregunta += 1
    respondida = False

    # Actualizar pregunta
    etiqueta_pregunta.config(text=preguntas_juego[numero_pregunta][0])

    # Actualizar respuestas
    boton_respuesta1.config(text=preguntas_juego[numero_pregunta][1], value=preguntas_juego[numero_pregunta][1])
    boton_respuesta2.config(text=preguntas_juego[numero_pregunta][2], value=preguntas_juego[numero_pregunta][2])
    boton_respuesta3.config(text=preguntas_juego[numero_pregunta][3], value=preguntas_juego[numero_pregunta][3])
    boton_respuesta4.config(text=preguntas_juego[numero_pregunta][4], value=preguntas_juego[numero_pregunta][4])

    # Limpiar respuesta seleccionada
    respuesta_selec.set("")

    # Volver a activar el boton de responder
    boton_responder.config(state="normal")


# Mostrar resultados
def ver_resultados():
    global frame_resultados

    frame_juego.pack_forget()

    frame_resultados = tk.Frame(ventana, bg="#00AAFF")
    frame_resultados.pack(fill="both", expand=True)

    etiqueta_nombre = tk.Label(frame_resultados, text=f"Jugador: {nombre_jugador}")
    etiqueta_nombre.pack()

    etiqueta_puntos = tk.Label(frame_resultados, text=f"Puntaje final: {puntos}")
    etiqueta_puntos.pack()

    etiqueta_aciertos = tk. Label(frame_resultados, text=f"Aciertos: {aciertos}")
    etiqueta_aciertos.pack()

    etiqueta_fallos = tk. Label(frame_resultados, text=f"Fallos: {fallos}")
    etiqueta_fallos.pack()
    

    boton_reiniciar = tk.Button(frame_resultados, text="Volver a jugar", command=reiniciar_partida)
    boton_reiniciar.pack()


# Reiniciar partida
def reiniciar_partida():
    global vidas, puntos, numero_pregunta, respondida, fallos , aciertos

    vidas = 3
    puntos = 0
    numero_pregunta = 0
    fallos = 0
    aciertos = 0
    respondida = False

    frame_resultados.pack_forget()

    crear_pantalla_inicio()


crear_pantalla_inicio()
ventana.mainloop()