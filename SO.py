import time

class Proceso:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.estado = "Listo"  # Estados: LISTO, EJECUTANDO, TERMINADO

class SimuladorSO:
    def __init__(self):
        self.procesos = []
        self.cola_listos = []

    def crear_proceso(self):
        print("\n--- Entrada/Salida (I/O) ---")
        nombre = input("Ingrese el nombre del proceso: ")
        nuevo_id = len(self.procesos) + 1
        nuevo_p = Proceso(nuevo_id, nombre)
        self.procesos.append(nuevo_p)
        self.cola_listos.append(nuevo_p)
        print(f"Proceso '{nombre}' creado con ID {nuevo_id}.")

    def mostrar_procesos(self):
        print("\n--- Lista de Procesos ---")
        for p in self.procesos:
            print(f"ID: {p.id} | Nombre: {p.nombre} | Estado: {p.estado}")

    def planificador_fcfs(self):
        """Simulación de planificación First-Come, First-Served"""
        print("\n--- Ejecutando Planificación (FCFS) ---")
        while self.cola_listos:
            p = self.cola_listos.pop(0) # TOMA EL PRIMERO QUE LLEGO
            p.estado = "Ejecutando"
            print(f"Proceso {p.id} ({p.nombre}) está en estado: {p.estado}...")
            time.sleep(1) # SIMULA TIEMPO DE CPU
            p.estado = "Terminado"
            print(f"Proceso {p.id} ha cambiado a: {p.estado}")

    def menu(self):
        while True:
            print("\n===== SIMULADOR DE SISTEMA OPERATIVO =====")
            print("1. CREAR PROCESO")
            print("2. MOSTRAR PROCESOS")
            print("3. EJECUTAR PLANIFICACIÓN (FCFS)")
            print("4. SALIR")
            opcion = input("SELECCIONE COMANDO: :D")

            if opcion == "1": self.crear_proceso()
            elif opcion == "2": self.mostrar_procesos()
            elif opcion == "3": self.planificador_fcfs()
            elif opcion == "4": break
            else: print("Comando no reconocido.")

if __name__ == "__main__":
    simulador = SimuladorSO()
    simulador.menu()