import time
from collections import deque # Usamos deque para una cola eficiente

class Proceso:
    def __init__(self, nombre, tiempo):
        self.nombre = nombre
        self.tiempo_restante = tiempo # Tiempo que le falta por ejecutar
        self.tiempo_total = tiempo
        self.estado = "Listo"

    def __str__(self):
        return f"{self.nombre} | Restante: {self.tiempo_restante}s | Estado: {self.estado}"

class SistemaOperativo:
    def __init__(self):
        self.procesos = []

    def crear_proceso(self):
        try:
            nombre = input("Nombre del proceso: ")
            tiempo = int(input("Tiempo de ejecución (segundos): "))
            self.procesos.append(Proceso(nombre, tiempo))
            print(f"Proceso {nombre} creado.\n")
        except ValueError:
            print("Error: El tiempo debe ser un número entero.\n")

    def mostrar_procesos(self):
        print("\n--- Lista de Procesos ---")
        if not self.procesos: print("No hay procesos.")
        for p in self.procesos:
            print(p)
        print()

    def eliminar_proceso(self):
        nombre = input("Nombre del proceso a eliminar: ")
        original_count = len(self.procesos)
        self.procesos = [p for p in self.procesos if p.nombre != nombre]
        if len(self.procesos) < original_count:
            print("Proceso eliminado.\n")
        else:
            print("No se encontró el proceso.\n")

    def ejecutar_fcfs(self):
        print("\n--- Planificación FCFS ---")
        for p in self.procesos:
            if p.estado != "Terminado":
                p.estado = "Ejecutando"
                print(f"Ejecutando {p.nombre} por {p.tiempo_restante}s...")
                time.sleep(1) 
                p.tiempo_restante = 0
                p.estado = "Terminado"
        print("Planificación finalizada.\n")

    def ejecutar_rr(self):
        print("\n--- Planificación Round Robin ---")
        if not self.procesos: return
        
        try:
            quantum = int(input("Ingresa el valor del Quantum: "))
        except: return

        # Filtramos solo los que no han terminado y los metemos a una cola
        cola = deque([p for p in self.procesos if p.estado != "Terminado"])

        while cola:
            p = cola.popleft() # Sacamos el primero de la cola
            p.estado = "Ejecutando"
            print(f"Ejecutando {p.nombre} (Restante: {p.tiempo_restante}s)")

            tiempo_a_ejecutar = min(p.tiempo_restante, quantum)
            time.sleep(0.5) # Simulación rápida
            p.tiempo_restante -= tiempo_a_ejecutar

            if p.tiempo_restante > 0:
                p.estado = "Listo"
                print(f"  -> Quantum agotado. {p.nombre} regresa a la cola.")
                cola.append(p) # Vuelve al final
            else:
                p.estado = "Terminado"
                print(f"  -> {p.nombre} FINALIZADO.")
        
        print("\nTodos los procesos en la cola han terminado.\n")

    def menu(self):
        # ... (Tu menú original está bien, solo asegúrate de llamar a estas funciones)
        pass

if __name__ == "__main__":
    sistema = SistemaOperativo()
    # Para probar rápido, descomenta el menú o llama a los métodos
    sistema.crear_proceso()
    sistema.ejecutar_rr()