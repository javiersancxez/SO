import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import threading
import time


# ─── CLASE PROCESO (PCB) ───────────────────────────────────────────────────────

class Proceso:
    def __init__(self, nombre, tiempo):
        self.nombre = nombre
        self.tiempo_restante = tiempo
        self.tiempo_total = tiempo
        self.estado = "LISTO"


# ─── INTERFAZ GRÁFICA ──────────────────────────────────────────────────────────

class KernelSimulatorApp:
    # Paleta de colores (tema oscuro tipo terminal)
    BG_DARK   = "#010204"
    BG_PANEL  = "#111827"
    BG_INPUT  = "#060a0f"
    FG_GREEN  = "#4ade80"
    FG_YELLOW = "#fbbf24"
    FG_RED    = "#f87171"
    FG_BLUE   = "#818cf8"
    FG_GRAY   = "#6b7280"
    FG_WHITE  = "#e5e7eb"
    BORDER    = "#1e2a38"

    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de un Sistema Operativo Básico")
        self.root.configure(bg=self.BG_DARK)
        self.root.resizable(True, True)
        self.root.minsize(820, 560)

        self.procesos = []
        self.corriendo = False

        self._build_ui()
        self._log("Sistema iniciado. Listo.", color=self.FG_GREEN)

    # ── CONSTRUCCIÓN DE LA UI ─────

    def _build_ui(self):
        # Barra de título
        title_bar = tk.Frame(self.root, bg=self.BG_DARK, pady=10)
        title_bar.pack(fill="x", padx=18)

        dots_frame = tk.Frame(title_bar, bg=self.BG_DARK)
        dots_frame.pack(side="left")
        for color in ("#ee09ad", "#d2aa32", "#1e3ce4"):
            tk.Label(dots_frame, text="●", fg=color, bg=self.BG_DARK,
                     font=("Courier New", 12)).pack(side="left", padx=2)

        tk.Label(title_bar, text="SIMULADOR DE PROCESOS VINKOPRO 1TB",
                 fg=self.FG_GREEN, bg=self.BG_DARK,
                 font=("Courier New", 12, "bold")).pack(side="left")

        sep = tk.Frame(self.root, bg=self.BORDER, height=1)
        sep.pack(fill="x", padx=18, pady=(0, 10))

        # Contenedor principal
        main = tk.Frame(self.root, bg=self.BG_DARK)
        main.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=2)
        main.rowconfigure(0, weight=1)

        self._build_left(main)
        self._build_right(main)

    def _panel(self, parent, title, row=0, col=0, rowspan=1, pady_bottom=10):
        frame = tk.LabelFrame(
            parent, text=f"  {title}  ",
            fg=self.FG_GRAY, bg=self.BG_PANEL,
            font=("Courier New", 8), bd=1,
            relief="flat", highlightbackground=self.BORDER,
            highlightthickness=1, padx=12, pady=10
        )
        frame.grid(row=row, col=col if False else None, column=col,
                   rowspan=rowspan, sticky="nsew",
                   padx=(0 if col > 0 else 0, 8 if col == 0 else 0),
                   pady=(0, pady_bottom))
        return frame

    def _label(self, parent, text, color=None, font_size=11, bold=False):
        font = ("Courier New", font_size, "bold" if bold else "normal")
        return tk.Label(parent, text=text, fg=color or self.FG_WHITE,
                        bg=self.BG_PANEL, font=font, anchor="w")

    def _entry(self, parent, textvariable=None, width=18):
        e = tk.Entry(parent, textvariable=textvariable, width=width,
                     bg=self.BG_INPUT, fg=self.FG_WHITE,
                     insertbackground=self.FG_GREEN,
                     relief="flat", font=("Courier New", 11),
                     highlightbackground=self.BORDER,
                     highlightthickness=1, highlightcolor=self.FG_GREEN)
        e.configure(bd=0)
        return e

    def _btn(self, parent, text, cmd, color=None, hover=None):
        color = color or self.FG_GREEN
        hover = hover or "#0fb153"
        btn = tk.Button(parent, text=text, command=cmd,
                        bg=self.BG_PANEL, fg=color,
                        activebackground=hover, activeforeground=color,
                        relief="flat", font=("Courier New", 10),
                        cursor="hand2", pady=6,
                        highlightbackground=color, highlightthickness=1)
        btn.bind("<Enter>", lambda e: btn.config(bg=hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.BG_PANEL))
        return btn

    # ── PANEL IZQUIERDO ────────────────────────────────────────────────────────

    def _build_left(self, parent):
        left = tk.Frame(parent, bg=self.BG_DARK)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left.rowconfigure(0, weight=0)
        left.rowconfigure(1, weight=0)
        left.rowconfigure(2, weight=0)

        # ── Crear proceso
        p_crear = tk.LabelFrame(left, text="  CREAR PROCESO  ",
                                fg=self.FG_GRAY, bg=self.BG_PANEL,
                                font=("Courier New", 8), relief="flat",
                                highlightbackground=self.BORDER,
                                highlightthickness=1, padx=12, pady=10)
        p_crear.pack(fill="x", pady=(0, 8))

        self._label(p_crear, "> nombre:", self.FG_GREEN, 10).pack(anchor="w")
        self.var_nombre = tk.StringVar()
        self._entry(p_crear, self.var_nombre).pack(fill="x", pady=(2, 8))

        self._label(p_crear, "> tiempo (seg):", self.FG_GREEN, 10).pack(anchor="w")
        self.var_tiempo = tk.StringVar()
        self._entry(p_crear, self.var_tiempo).pack(fill="x", pady=(2, 8))

        self._btn(p_crear, "+ CREAR PROCESO", self.crear_proceso).pack(fill="x")

        # ── Eliminar proceso
        p_del = tk.LabelFrame(left, text="  ELIMINAR PROCESO  ",
                              fg=self.FG_GRAY, bg=self.BG_PANEL,
                              font=("Courier New", 8), relief="flat",
                              highlightbackground=self.BORDER,
                              highlightthickness=1, padx=12, pady=10)
        p_del.pack(fill="x", pady=(0, 8))

        self._label(p_del, "> selecciona un proceso:", self.FG_RED, 10).pack(anchor="w")
        self.var_del = tk.StringVar()
        self.combo_del = ttk.Combobox(p_del, textvariable=self.var_del,
                                      state="readonly", font=("Courier New", 11))
        self._style_combobox()
        self.combo_del.pack(fill="x", pady=(2, 8))
        self._btn(p_del, "× ELIMINAR", self.eliminar_proceso,
                  color=self.FG_RED, hover="#1a0606").pack(fill="x")

        # ── Planificación
        p_sched = tk.LabelFrame(left, text="  PLANIFICACIÓN  ",
                                fg=self.FG_GRAY, bg=self.BG_PANEL,
                                font=("Courier New", 8), relief="flat",
                                highlightbackground=self.BORDER,
                                highlightthickness=1, padx=12, pady=10)
        p_sched.pack(fill="x", pady=(0, 0))

        self._btn(p_sched, "▶  EJECUTAR FCFS", self.ejecutar_fcfs,
                  color=self.FG_YELLOW, hover="#1c1204").pack(fill="x", pady=(0, 8))

        self._label(p_sched, "> quantum (Round Robin):", self.FG_BLUE, 10).pack(anchor="w")
        self.var_quantum = tk.StringVar()
        self._entry(p_sched, self.var_quantum).pack(fill="x", pady=(2, 8))
        self._btn(p_sched, "↺  EJECUTAR ROUND ROBIN", self.ejecutar_rr,
                  color=self.FG_BLUE, hover="#1e1b4b").pack(fill="x")

    # ── PANEL DERECHO ─────────

    def _build_right(self, parent):
        right = tk.Frame(parent, bg=self.BG_DARK)
        right.grid(row=0, column=1, sticky="nsew")
        right.rowconfigure(0, weight=1)
        right.rowconfigure(1, weight=0)

        # Tabla PCB
        p_pcb = tk.LabelFrame(right, text="  TABLA DE PROCESOS (PCB)  ",
                              fg=self.FG_GRAY, bg=self.BG_PANEL,
                              font=("Courier New", 8), relief="flat",
                              highlightbackground=self.BORDER,
                              highlightthickness=1, padx=12, pady=10)
        p_pcb.grid(row=0, column=0, sticky="nsew", pady=(0, 8))

        style = ttk.Style()
        style.theme_use("default")
        style.configure("PCB.Treeview",
                        background=self.BG_PANEL, foreground=self.FG_WHITE,
                        fieldbackground=self.BG_PANEL,
                        font=("Courier New", 11), rowheight=28)
        style.configure("PCB.Treeview.Heading",
                        background=self.BG_DARK, foreground=self.FG_GRAY,
                        font=("Courier New", 9), relief="flat")
        style.map("PCB.Treeview",
                  background=[("selected", "#1e2a38")],
                  foreground=[("selected", self.FG_WHITE)])

        cols = ("Nombre", "Total", "Restante", "Estado")
        self.tree = ttk.Treeview(p_pcb, columns=cols, show="headings",
                                 style="PCB.Treeview", selectmode="none")
        for col, w in zip(cols, (140, 70, 90, 100)):
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=w, anchor="w")

        scrollbar = ttk.Scrollbar(p_pcb, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Log del sistema
        p_log = tk.LabelFrame(right, text="  LOG DEL SISTEMA  ",
                              fg=self.FG_GRAY, bg=self.BG_PANEL,
                              font=("Courier New", 8), relief="flat",
                              highlightbackground=self.BORDER,
                              highlightthickness=1, padx=12, pady=10)
        p_log.grid(row=1, column=0, sticky="nsew")
        right.columnconfigure(0, weight=1)

        self.log_text = tk.Text(p_log, height=8, bg=self.BG_INPUT,
                                fg=self.FG_GRAY, font=("Courier New", 10),
                                relief="flat", state="disabled",
                                wrap="word", highlightthickness=0)
        self.log_text.pack(fill="both", expand=True)
        self.log_text.tag_config("ok",   foreground=self.FG_GREEN)
        self.log_text.tag_config("warn", foreground=self.FG_YELLOW)
        self.log_text.tag_config("err",  foreground=self.FG_RED)
        self.log_text.tag_config("info", foreground=self.FG_BLUE)

    # ── HELPERS ────────────────────────────────────────────────────────────────

    def _style_combobox(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TCombobox",
                        fieldbackground=self.BG_INPUT,
                        background=self.BG_INPUT,
                        foreground=self.FG_WHITE,
                        arrowcolor=self.FG_GRAY,
                        selectbackground=self.BG_INPUT,
                        selectforeground=self.FG_WHITE)

    def _log(self, msg, color=""):
        tag = {"green": "ok", "yellow": "warn", "red": "err", "blue": "info"}.get(
            {self.FG_GREEN: "green", self.FG_YELLOW: "yellow",
             self.FG_RED: "red", self.FG_BLUE: "blue"}.get(color, ""), "")
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"> {msg}\n", tag or None)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _actualizar_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        estado_colors = {
            "LISTO":     self.FG_GREEN,
            "EJECUTANDO": self.FG_YELLOW,
            "TERMINADO": self.FG_RED,
        }
        for p in self.procesos:
            color = estado_colors.get(p.estado, self.FG_WHITE)
            self.tree.insert("", "end", values=(
                p.nombre, f"{p.tiempo_total}s",
                f"{p.tiempo_restante}s", p.estado
            ), tags=(p.estado,))
            self.tree.tag_configure(p.estado, foreground=color)

        # Actualizar combobox de eliminación
        nombres = [p.nombre for p in self.procesos if p.estado != "TERMINADO"]
        self.combo_del["values"] = nombres
        if self.var_del.get() not in nombres:
            self.var_del.set("")

    # ── LÓGICA DEL SISTEMA ─────────────────────────────────────────────────────

    def crear_proceso(self):
        if self.corriendo:
            self._log("Sistema ocupado. Espera a que termine la ejecución.", self.FG_RED)
            return
        nombre = self.var_nombre.get().strip()
        tiempo_str = self.var_tiempo.get().strip()

        if not nombre:
            self._log("Error: el nombre no puede estar vacío.", self.FG_RED); return
        if any(p.nombre == nombre for p in self.procesos):
            self._log(f"Error: ya existe un proceso '{nombre}'.", self.FG_RED); return
        try:
            tiempo = int(tiempo_str)
            if tiempo <= 0: raise ValueError
        except ValueError:
            self._log("Error: tiempo inválido. Debe ser un entero > 0.", self.FG_RED); return

        self.procesos.append(Proceso(nombre, tiempo))
        self._log(f"Proceso '{nombre}' añadido. Tiempo: {tiempo}s", self.FG_GREEN)
        self.var_nombre.set("")
        self.var_tiempo.set("")
        self._actualizar_tabla()

    def eliminar_proceso(self):
        if self.corriendo:
            self._log("Sistema ocupado.", self.FG_RED); return
        nombre = self.var_del.get()
        if not nombre:
            self._log("Selecciona un proceso para eliminar.", self.FG_RED); return
        self.procesos = [p for p in self.procesos if p.nombre != nombre]
        self._log(f"Proceso '{nombre}' eliminado.", self.FG_YELLOW)
        self._actualizar_tabla()

    def _run_in_thread(self, target):
        t = threading.Thread(target=target, daemon=True)
        t.start()

    # ── FCFS ──────────────────────────────────────────────────────────────────

    def ejecutar_fcfs(self):
        if self.corriendo:
            self._log("Ya hay un algoritmo en ejecución.", self.FG_RED); return
        listos = [p for p in self.procesos if p.estado != "TERMINADO"]
        if not listos:
            self._log("No hay procesos pendientes.", self.FG_YELLOW); return
        self._run_in_thread(lambda: self._fcfs_thread(listos))

    def _fcfs_thread(self, listos):
        self.corriendo = True
        self.root.after(0, self._log, "--- Iniciando FCFS ---", self.FG_BLUE)
        for p in listos:
            p.estado = "EJECUTANDO"
            self.root.after(0, self._log, f"CPU: ejecutando '{p.nombre}'...", self.FG_YELLOW)
            self.root.after(0, self._actualizar_tabla)
            time.sleep(1)
            p.tiempo_restante = 0
            p.estado = "TERMINADO"
            self.root.after(0, self._log, f"Finalizado: '{p.nombre}'", self.FG_GREEN)
            self.root.after(0, self._actualizar_tabla)
            time.sleep(0.2)
        self.root.after(0, self._log, "--- FCFS completado ---", self.FG_BLUE)
        self.corriendo = False

    # ── ROUND ROBIN ───────────────────────────────────────────────────────────

    def ejecutar_rr(self):
        if self.corriendo:
            self._log("Ya hay un algoritmo en ejecución.", self.FG_RED); return
        try:
            quantum = int(self.var_quantum.get())
            if quantum <= 0: raise ValueError
        except ValueError:
            self._log("Error: quantum inválido. Debe ser un entero > 0.", self.FG_RED); return
        listos = [p for p in self.procesos if p.estado != "TERMINADO"]
        if not listos:
            self._log("No hay procesos pendientes.", self.FG_YELLOW); return
        self._run_in_thread(lambda: self._rr_thread(listos, quantum))

    def _rr_thread(self, listos, quantum):
        self.corriendo = True
        self.root.after(0, self._log, f"--- Iniciando Round Robin (quantum={quantum}s) ---", self.FG_BLUE)
        cola = deque(listos)
        while cola:
            p = cola.popleft()
            p.estado = "EJECUTANDO"
            ejecutado = min(p.tiempo_restante, quantum)
            self.root.after(0, self._log,
                f"CPU: '{p.nombre}' | restante: {p.tiempo_restante}s | ejecuta: {ejecutado}s",
                self.FG_YELLOW)
            self.root.after(0, self._actualizar_tabla)
            time.sleep(0.5 + ejecutado * 0.15)
            p.tiempo_restante -= ejecutado
            if p.tiempo_restante > 0:
                p.estado = "LISTO"
                self.root.after(0, self._log,
                    f"Quantum agotado. '{p.nombre}' reingresa. Restante: {p.tiempo_restante}s",
                    self.FG_BLUE)
                cola.append(p)
            else:
                p.estado = "TERMINADO"
                self.root.after(0, self._log, f"'{p.nombre}' terminado.", self.FG_GREEN)
            self.root.after(0, self._actualizar_tabla)
            time.sleep(0.15)
        self.root.after(0, self._log, "--- Round Robin completado ---", self.FG_BLUE)
        self.corriendo = False


if __name__ == "__main__":
    root = tk.Tk()
    app = KernelSimulatorApp(root)
    root.mainloop()
