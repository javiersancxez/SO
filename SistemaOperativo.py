import time
from collections import deque


# CLASE PROCESO (PCB)

class Proceso:
    def __init__(self, nombre, tiempo):
        self.nombre = nombre
        self.tiempo_restante = tiempo
        self.tiempo_total = tiempo
        self.estado = "LISTO"

    def __str__(self):
        return f"[{self.nombre}] -> Total: {self.tiempo_total}s | Restante: {self.tiempo_restante}s | Estado: {self.estado}"



# SISTEMA OPERATIVO

class SistemaOperativo:
    def __init__(self):
        self.procesos = []

    def crear_proceso(self):
        print("\n--- [I/O] CREAR PROCESO ---")
        nombre = input("NOMBRE DEL PROCESO: ")
        try:
            tiempo = int(input("TIEMPO DE EJECUCIÓN (segundos): "))
            if tiempo <= 0:
                print("ERROR: EL TIEMPO DEBE SER MAYOR A 0.")
                return
            nuevo = Proceso(nombre, tiempo)
            self.procesos.append(nuevo)
            print(f"ÉXITO: PROCESO '{nombre}' AÑADIDO A LA COLA DE LISTOS.")
        except ValueError:
            print("ERROR: ENTRADA INVÁLIDA. INGRESA UN NÚMERO ENTERO PARA EL TIEMPO.")

    def mostrar_procesos(self):
        print("\n--- TABLA DE PROCESOS (PCB) ---")
        if not self.procesos:
            print("NO HAY PROCESOS EN EL SISTEMA.")
        else:
            for p in self.procesos:
                print(p)
        print("-" * 30)

    def eliminar_proceso(self):
        if not self.procesos:
            print("\nERROR: NO HAY PROCESOS PARA ELIMINAR.")
            return
        
        nombre = input("\nNOMBRE DEL PROCESO A ELIMINAR: ")
        encontrado = False
        for p in self.procesos:
            if p.nombre == nombre:
                self.procesos.remove(p)
                print(f"ÉXITO: PROCESO '{nombre}' ELIMINADO CORRECTAMENTE.")
                encontrado = True
                break
        if not encontrado:
            print(f"ERROR: NO SE ENCONTRÓ EL PROCESO '{nombre}'.")

    def ejecutar_fcfs(self):
        print("\n--- PLANIFICACIÓN FCFS (First-Come, First-Served) ---")
        procesos_listos = [p for p in self.procesos if p.estado != "TERMINADO"]
        
        if not procesos_listos:
            print("NO HAY PROCESOS PENDIENTES POR EJECUTAR.")
            return

        for p in procesos_listos:
            p.estado = "EJECUTANDO"
            print(f">> CPU: {p.nombre} en ejecución...")
            time.sleep(1) # SIMULACION DE RAFAGA DE CPU
            p.tiempo_restante = 0
            p.estado = "TERMINADO"
            print(f"<< FINALIZADO: {p.nombre}")

    def ejecutar_rr(self):
        print("\n--- PLANIFICACIÓN ROUND ROBIN ---")
        procesos_listos = [p for p in self.procesos if p.estado != "TERMINADO"]
        
        if not procesos_listos:
            print("NO HAY PROCESOS PENDIENTES POR EJECUTAR.")
            return

        try:
            quantum = int(input("INGRESA EL VALOR DEL QUANTUM: "))
            cola = deque(procesos_listos)

            while cola:
                p = cola.popleft()
                p.estado = "EJECUTANDO"
                print(f">> CPU: EJECUTANDO {p.nombre} (RESTANTE: {p.tiempo_restante}s)")

                # LOGICA DE DESCUENTO DEL TIEMPO DE EJECUCIÓN
                tiempo_ejecutado = min(p.tiempo_restante, quantum)
                time.sleep(0.5) 
                p.tiempo_restante -= tiempo_ejecutado

                if p.tiempo_restante > 0:
                    p.estado = "LISTO"
                    print(f"   ! QUANTUM AGOTADO. {p.nombre} REINGRESA A LA COLA.")
                    cola.append(p)
                else:
                    p.estado = "TERMINADO"
                    print(f"   * {p.nombre} HA TERMINADO SU EJECUCIÓN.")
            
            print("\n--- CICLO ROUND ROBIN COMPLETADO ---")
        except ValueError:
            print("ERROR: EL QUANTUM DEBE SER UN NÚMERO ENTERO.")

    
    # MENU PRINCIPAL
    
    def menu(self):
        while True:
            print("\n" + "="*30)
            print("    KERNEL SIMULATOR v1.0")
            print("="*30)
            print("1. CREAR PROCESO")
            print("2. VER TABLA DE PROCESOS (PCB)")
            print("3. ELIMINAR PROCESO")
            print("4. EJECUTAR PLANIFICACIÓN FCFS")
            print("5. EJECUTAR ROUND ROBIN")
            print("6. SALIR")
            print("="*30)

            opcion = input("SELECCIONA COMANDO: ")

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
                print("APAGANDO SISTEMA... BYE .I. ")
                break
            else:
                print("COMANDO NO RECONOCIDO. INTENTALO DE NUEVO.")


# INICIO DEL PROGRAMA

if __name__ == "__main__":
    simulador = SistemaOperativo()
    simulador.menu()