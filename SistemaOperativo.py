# =========================================
# PROYECTO FINAL - SISTEMA OPERATIVO BÁSICO
# =========================================

# Instrucciones:
# Completa las funciones marcadas con TODO
# y mejora el sistema agregando lógica propia

import time

# ----------------------------
# Clase Proceso
# ----------------------------
class Proceso:
    def __init__(self, nombre, tiempo):
        self.nombre = nombre
        self.tiempo = tiempo
        self.estado = "Listo"  # Listo, Ejecutando, Terminado

    def __str__(self):
        return f"{self.nombre} | Tiempo: {self.tiempo} | Estado: {self.estado}"


# ----------------------------
# Sistema Operativo
# ----------------------------
class SistemaOperativo:
    def __init__(self):
        self.procesos = []

    # ----------------------------
    # Crear proceso
    # ----------------------------
    def crear_proceso(self):
        nombre = input("Nombre del proceso: ")
        tiempo = int(input("Tiempo de ejecución: "))

        nuevo = Proceso(nombre, tiempo)
        self.procesos.append(nuevo)

        print(f"Proceso {nombre} creado.\n")

    # ----------------------------
    # Mostrar procesos
    # ----------------------------
    def mostrar_procesos(self):
        print("\nLista de procesos:")

        # TODO: recorrer la lista e imprimir procesos
        for p in self.procesos:
            print(p)

        print()

    # ----------------------------
    # Eliminar proceso
    # ----------------------------
    def eliminar_proceso(self):
        nombre = input("Nombre del proceso a eliminar: ")

        # TODO: eliminar proceso de la lista
        self.procesos = [p for p in self.procesos if p.nombre != nombre]

        print("Proceso eliminado.\n")

    # ----------------------------
    # Planificación FCFS
    # ----------------------------
    def ejecutar_fcfs(self):
        print("\nEjecutando FCFS...\n")

        # TODO: recorrer procesos en orden
        for p in self.procesos:
            p.estado = "Ejecutando"
            print(f"Ejecutando {p.nombre}...")

            time.sleep(1)  # Simula ejecución

            p.estado = "Terminado"

        print("\nTodos los procesos terminaron.\n")

    # ----------------------------
    # Planificación Round Robin
    # ----------------------------
    def ejecutar_rr(self):
        print("\nRound Robin\n")

        quantum = int(input("Ingresa el quantum: "))

        # TODO: implementar lógica de Round Robin
        # Pista:
        # - recorrer procesos
        # - restar tiempo
        # - volver a agregar si no termina

        for p in self.procesos:
            print(f"Procesando {p.nombre}... (falta implementar lógica completa)")

        print("\nSimulación incompleta (debes terminarla)\n")

    # ----------------------------
    # Menú principal (I/O)
    # ----------------------------
    def menu(self):
        while True:
            print("==== SISTEMA OPERATIVO ====")
            print("1. Crear proceso")
            print("2. Ver procesos")
            print("3. Eliminar proceso")
            print("4. Ejecutar FCFS")
            print("5. Ejecutar Round Robin")
            print("6. Salir")

            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                self.crear_proceso()

            elif opcion == "2":
                self.mostrar_procesos()

            elif opcion == "3":
                self.eliminar_proceso()

            elif opcion == "4":
                self.ejecutar_fcfs()

            elif opcion == "5":
                self.ejecutar_rr()

            elif opcion == "6":
                print("Saliendo...")
                break

            else:
                print("Opción inválida\n")


# ----------------------------
# Programa principal
# ----------------------------
if __name__ == "__main__":
    sistema = SistemaOperativo()
    sistema.menu()