import ttkbootstrap as tb
from tkinter import LEFT, RIGHT, BOTH, X
import tkinter as tk
import sys
import os
from datetime import datetime
import time

# Agregar el directorio raiz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.doctor_controller import DoctorController
from controllers.paciente_controller import PacienteController
from controllers.cita_controller import CitaController

class DashboardView:
    def __init__(self, parent):
        for widget in parent.winfo_children():
            widget.destroy()
        self.parent = parent
        self.frame = tb.Frame(parent)
        self.frame.pack(fill=BOTH, expand=True)

        # Titulos y colores
        colores = ["danger", "warning", "info"]
        iconos = ["👨‍⚕️", "🙎‍♂️🙎‍♀️", "📅"]
        titulos = ["Total Doctores", "Total Pacientes", "Total Citas"]

        # Obtener datos
        total_doctores = DoctorController().contar()
        total_pacientes = PacienteController().contar()
        total_citas = CitaController().contar()
        totales = [total_doctores, total_pacientes, total_citas]

        # Crear estilos personalizados para los totales
        style = tb.Style()
        style.configure("TotalDanger.TLabel", background="#dc3545", foreground="white", font=("Arial", 14, "bold"), anchor="center")
        style.configure("TotalWarning.TLabel", background="#ffc107", foreground="white", font=("Arial", 14, "bold"), anchor="center")
        style.configure("TotalInfo.TLabel", background="#008cba", foreground="white", font=("Arial", 14, "bold"), anchor="center")

        # Footer personalizado
        style.configure("FooterAzul.TLabel", background="#007bff", foreground="white", font=("Arial", 10), anchor="center")

        # Tarjetas resumen
        cards_frame = tb.Frame(self.frame)
        cards_frame.pack(pady=20)

        for i, (color, icono, titulo, total) in enumerate(zip(colores, iconos, titulos, totales)):
            # Card con estilo de color
            card = tb.Frame(cards_frame, style=f"{color}.TFrame", width=220, height=130)
            card.pack(side=LEFT, padx=10)
            card.pack_propagate(False)

            # Obtener color real del estilo
            style = tb.Style()
            card_bg = style.lookup(f"{color}.TFrame", "background")
            if not card_bg or card_bg in ("", "SystemButtonFace", None):
                card_bg = "#dc3545" if color=="danger" else ("#ffc107" if color=="warning" else "#0dcaf0")

            # Contenedor principal con padding
            main_frame = tb.Frame(card, style=f"{color}.TFrame")
            main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

            # Contenedor para el icono
            icon_frame = tb.Frame(main_frame, style=f"{color}.TFrame")
            icon_frame.pack(fill=X, pady=(0,5))

            # Icono (más pequeño)
            tb.Label(icon_frame, text=icono, font=("Arial", 28),
                    style=f"{color}.Inverse.TLabel").pack()

            # Contenedor para titulo y total
            info_frame = tb.Frame(main_frame, style=f"{color}.TFrame")
            info_frame.pack(fill=X, pady=(5,0))

            # Titulo
            tb.Label(info_frame, text=titulo, font=("Arial", 11, "bold"),
                    style=f"{color}.Inverse.TLabel").pack()
        
            # Total debajo del título con estilo personalizado
            total_frame = tb.Frame(info_frame, style=f"{color}.TFrame")
            total_frame.pack(fill=X, pady=(5,0))
            total_style = "TotalDanger.TLabel" if color=="danger" else ("TotalWarning.TLabel" if color=="warning" else "TotalInfo.TLabel")
            tb.Label(total_frame, text=str(total), style=total_style).pack(fill=X)

        # Tablas de recientes
        tablas_frame = tb.Frame(self.frame)
        tablas_frame.pack(pady=20, fill=X)

        # Doctores recientes
        doctores = DoctorController().listar(por_pagina=5)
        tabla_doc_frame = tb.LabelFrame(tablas_frame, text="Doctores Recientes", bootstyle="info")
        tabla_doc_frame.pack(side=LEFT, padx=20, fill=X, expand=True)
        tabla_doc = tb.Treeview(tabla_doc_frame, columns=("nombre", "departamento", "telefono", "estado"),
                        show="headings", height=6, bootstyle="Success")
        tabla_doc.heading("nombre", text="Nombre")
        tabla_doc.heading("departamento", text="Departamento")
        tabla_doc.heading("telefono", text="Teléfono")
        tabla_doc.heading("estado", text="Estado")
        tabla_doc.column("nombre", width=120)
        tabla_doc.column("departamento", width=120)
        tabla_doc.column("telefono", width=90)
        tabla_doc.column("estado", width=80)
        tabla_doc.pack(fill=X, padx=5, pady=5)

        for d in doctores:
            tabla_doc.insert("", "end", values=(d["nombre"], d["departamento"], d["telefono"], d["estado"]))

        # Pacientes recientes
        pacientes = PacienteController().listar(por_pagina=5)
        tabla_pac_frame = tb.LabelFrame(tablas_frame, text="Pacientes Recientes", bootstyle="info")
        tabla_pac_frame.pack(side=RIGHT, padx=20, fill=X, expand=True)
        tabla_pac = tb.Treeview(tabla_pac_frame, columns=("nombre", "sintomas", "telefono", "direccion", "estado"),
                            show="headings", height=6, bootstyle="secondary")
        tabla_pac.heading("nombre", text="Nombre")
        tabla_pac.heading("sintomas", text="Síntomas")
        tabla_pac.heading("telefono", text="Teléfono")
        tabla_pac.heading("direccion", text="Dirección")
        tabla_pac.heading("estado", text="Estado")
        tabla_pac.column("nombre", width=120)
        tabla_pac.column("sintomas", width=120)
        tabla_pac.column("telefono", width=90)
        tabla_pac.column("direccion", width=120)
        tabla_pac.column("estado", width=80)
        tabla_pac.pack(fill=X, padx=5, pady=5)
        
        for p in pacientes:
            tabla_pac.insert("", "end", values=(p["nombre"], p["sintomas"], p["telefono"], p["direccion"], p["estado"]))

        # Footer
        footer_frame = tb.Frame(self.frame)
        footer_frame.pack(side="bottom", fill=X, pady=10)
        self.footer_label = tb.Label(footer_frame, text="Sistema de Gestión de Clínica - Dashboard", style="")
        self.footer_label.pack(fill="x")

    def update_footer(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.footer_label.config(
            text=f"Usuario: {{self.usuario['nombre']}} | Fecha y hora: {{now}} | © 2025 Soluciones Tecnologicas"
        )
        self.parent.after(1000, self.update_footer)

        time.sleep(2) # Esperar 2 segundos