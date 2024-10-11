import tkinter as tk
from tkinter import messagebox, ttk

class Estudiante:
    def __init__(self, nombre, notas):
        self.nombre = nombre
        self.notas = notas
        self.conocimientos_basicos = {
            "Multiplicación": 1,
            "División": 1,
            "Factorización": 0,
        }
        self.progreso = {
            "Ecuaciones Cuadráticas": {"Multiplicación": 1, "División": 1, "Potenciación": 0, "Factorización": 0},
            "Matrices": {"Suma": 1, "Multiplicación": 0, "Determinantes": 1, "Inversión de matrices": 0},
            "Cálculo Diferencial": {"Derivación": 1, "Reglas de Derivación": 0, "Límites": 0, "Funciones continuas": 1},
        }

    def evaluar_progreso(self):
        resumen = {}
        for tema, bases in self.progreso.items():
            faltantes = [base for base, estado in bases.items() if estado == 0]
            if faltantes:
                resumen[tema] = faltantes
        return resumen

    def obtener_nota_promedio(self):
        return sum(self.notas.values()) / len(self.notas)

    def necesita_repasar(self, tema, umbral=7):
        # Solo sugerir repaso si la nota es menor que el umbral
        if tema in self.notas and self.notas[tema] < umbral:
            return True
        return False

class GrafoConocimiento:
    def __init__(self):
        self.grafo = {}

    def agregar_relacion(self, tema, concepto):
        if tema not in self.grafo:
            self.grafo[tema] = []
        self.grafo[tema].append(concepto)

    def obtener_conceptos(self, tema):
        return self.grafo.get(tema, [])

class MotorReglas:
    def __init__(self, grafo_conocimiento):
        self.grafo_conocimiento = grafo_conocimiento

    def evaluar_necesidades(self, estudiante, umbral=7):
        sugerencias = []
        for tema in estudiante.progreso.keys():
            if estudiante.necesita_repasar(tema, umbral):
                conceptos = self.grafo_conocimiento.obtener_conceptos(tema)
                if conceptos:
                    for concepto in conceptos:
                        if estudiante.conocimientos_basicos.get(concepto, 0) == 0:
                            sugerencias.append(f"{estudiante.nombre} necesita repasar '{tema}' porque no domina '{concepto}'.")
        return sugerencias

class SistemaTutorMatematicas:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Inteligente de Tutoría")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f0f0")

        # Crear un grafo de conocimiento
        self.grafo_conocimiento = GrafoConocimiento()
        self.configurar_grafo_conocimiento()

        # Motor de reglas
        self.motor_reglas = MotorReglas(self.grafo_conocimiento)

        # Estudiantes con notas predeterminadas
        self.estudiantes = [
            Estudiante("Juan", {"Ecuaciones Cuadráticas": 7, "Matrices": 5, "Cálculo Diferencial": 8, 
                                "Cálculo Integral": 4, "Álgebra Lineal": 6}),
            Estudiante("Ana", {"Ecuaciones Cuadráticas": 5, "Matrices": 3, "Cálculo Diferencial": 6,
                                "Cálculo Integral": 5, "Álgebra Lineal": 7}),
            Estudiante("Pedro", {"Ecuaciones Cuadráticas": 8, "Matrices": 6, "Cálculo Diferencial": 9,
                                "Cálculo Integral": 7, "Álgebra Lineal": 8}),
            Estudiante("Lucía", {"Ecuaciones Cuadráticas": 4, "Matrices": 5, "Cálculo Diferencial": 5,
                                "Cálculo Integral": 2, "Álgebra Lineal": 3}),
            Estudiante("María", {"Ecuaciones Cuadráticas": 6, "Matrices": 7, "Cálculo Diferencial": 6,
                                "Cálculo Integral": 5, "Álgebra Lineal": 6})
        ]
        
        # Título y Descripción
        tk.Label(self.root, text="Sistema Inteligente de Tutoría Multiasignatura", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=10)
        tk.Label(self.root, text="Evaluación personalizada para estudiantes.", font=("Helvetica", 10), bg="#f0f0f0").pack(pady=5)

        # Lista de estudiantes
        self.lista_estudiantes = tk.Listbox(self.root, height=10, width=30, font=("Helvetica", 12))
        self.lista_estudiantes.pack(pady=20)
        self.actualizar_lista_estudiantes()

        # Botones de Interacción
        frame_botones = tk.Frame(self.root, bg="#f0f0f0")
        frame_botones.pack(pady=20)

        self.boton_ver_notas = tk.Button(frame_botones, text="Ver Notas", command=self.ver_notas, bg="#4CAF50", fg="white", font=("Helvetica", 12))
        self.boton_ver_notas.grid(row=0, column=0, padx=10)

        self.boton_repaso_general = tk.Button(frame_botones, text="Repaso General", command=self.repaso_general, bg="#2196F3", fg="white", font=("Helvetica", 12))
        self.boton_repaso_general.grid(row=0, column=1, padx=10)

        self.boton_sugerir_tema = tk.Button(frame_botones, text="Sugerir Temas a Estudiar", command=self.sugerir_tema, bg="#FF9800", fg="white", font=("Helvetica", 12))
        self.boton_sugerir_tema.grid(row=0, column=2, padx=10)

    def configurar_grafo_conocimiento(self):
        # Agregar relaciones entre temas y conceptos básicos
        self.grafo_conocimiento.agregar_relacion("Ecuaciones Cuadráticas", "Multiplicación")
        self.grafo_conocimiento.agregar_relacion("Ecuaciones Cuadráticas", "División")
        self.grafo_conocimiento.agregar_relacion("Matrices", "Suma")
        self.grafo_conocimiento.agregar_relacion("Matrices", "Multiplicación")
        self.grafo_conocimiento.agregar_relacion("Cálculo Diferencial", "Derivación")
        self.grafo_conocimiento.agregar_relacion("Cálculo Integral", "Integración")

    def actualizar_lista_estudiantes(self):
        self.lista_estudiantes.delete(0, tk.END)
        for estudiante in self.estudiantes:
            self.lista_estudiantes.insert(tk.END, estudiante.nombre)

    def ver_notas(self):
        seleccion = self.lista_estudiantes.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un estudiante.")
            return

        indice = seleccion[0]
        estudiante = self.estudiantes[indice]
        
        notas_ventana = tk.Toplevel(self.root)
        notas_ventana.title(f"Notas de {estudiante.nombre}")
        notas_ventana.geometry("600x400")

        tabla = ttk.Treeview(notas_ventana, columns=["Tema", "Nota"], show="headings")
        tabla.heading("Tema", text="Tema")
        tabla.heading("Nota", text="Nota")

        for tema, nota in estudiante.notas.items():
            tabla.insert("", tk.END, values=[tema, nota])

        tabla.pack(fill=tk.BOTH, expand=True)
        tk.Button(notas_ventana, text="Cerrar", command=notas_ventana.destroy, bg="#F44336", fg="white").pack(pady=10)

    def repaso_general(self):
        repaso = {}
        
        for estudiante in self.estudiantes:
            progreso = estudiante.evaluar_progreso()
            for tema, faltas in progreso.items():
                # Solo considerar temas donde los estudiantes tienen notas bajas
                if tema in estudiante.notas and estudiante.notas[tema] < 7:
                    if tema not in repaso:
                        repaso[tema] = set(faltas)
                    else:
                        repaso[tema].intersection_update(faltas)

        temas_a_repasar = sorted(repaso.keys(), key=lambda x: len(repaso[x]), reverse=True)[:3]

        if temas_a_repasar:
            mensaje = "Temas comunes para el repaso general:\n"
            for tema in temas_a_repasar:
                notas_temario = [estudiante.notas[tema] for estudiante in self.estudiantes if tema in estudiante.notas and estudiante.notas[tema] < 7]
                if notas_temario:
                    promedio = sum(notas_temario) / len(notas_temario)
                    mensaje += f"- {tema}: El promedio es {promedio:.2f}\n"
                else:
                    mensaje += f"- {tema}: No hay notas registradas o suficientes problemas.\n"
            razones_finales = "Los estudiantes deben repasar estos temas porque sus notas en estos cursos son bajas."
            mensaje += razones_finales
        else:
            mensaje = "Todos los estudiantes están al día."

        messagebox.showinfo("Repaso General", mensaje)

    def sugerir_tema(self):
        tema_sugerido = {}
        razones = []

        for estudiante in self.estudiantes:
            progreso = estudiante.evaluar_progreso()
            temas_con_fallas = list(progreso.keys())

            if temas_con_fallas:
                # Solo sugerir temas donde el promedio es menor al umbral
                temas_a_repasar = [t for t in temas_con_fallas if estudiante.necesita_repasar(t)]
                if temas_a_repasar:
                    tema_especifico = temas_a_repasar[0]
                    faltas = progreso[tema_especifico]

                    razon = f"{estudiante.nombre} debería repasar '{tema_especifico}' porque tiene problemas en: {', '.join(faltas)}. " \
                            f"Su nota promedio en este tema es {estudiante.notas.get(tema_especifico, 'N/A')}."
                    tema_sugerido[estudiante.nombre] = tema_especifico
                    razones.append(razon)

        mensaje = "Sugerencia para repasar:\n"
        for nombre, tema in tema_sugerido.items():
            mensaje += f"{nombre}: Repasar '{tema}'\n"
        mensaje += "\nRazones para el repaso:\n" + "\n".join(razones)

        messagebox.showinfo("Sugerencias de Estudio", mensaje)

    def calcular_importancia(self, estudiante, tema):
        nota = estudiante.notas.get(tema, 0)
        faltas = len(estudiante.progreso[tema]) - len(estudiante.progreso[tema].keys())
        return faltas + (10 - nota)

    def mostrar_info(self):
        messagebox.showinfo("Acerca de", "Sistema Inteligente de Tutoría - Versión 1.0\n"
                                            "Desarrollado para ayudar a los estudiantes en matemáticas, física, química y programación.\n"
                                            "Este sistema utiliza algoritmos de inferencia para adaptar el contenido a las necesidades de los estudiantes.")

# Configuración de la ventana principal
root = tk.Tk()
app = SistemaTutorMatematicas(root)
root.mainloop()
