import os
import shutil
import tkinter as tk
from tkinter import ttk, Listbox, messagebox, filedialog, Label, Scrollbar, MULTIPLE
from fnmatch import fnmatch
from datetime import datetime

class Config:
    config_file_path = "config.txt"
    folder_facturadas_prosegur = ""
    folder_nofacturadas_prosegur = ""
    folder_facturadas_brinks = ""
    folder_nofacturadas_brinks = ""

    @classmethod
    def load_config(cls):
        if os.path.exists(cls.config_file_path):
            with open(cls.config_file_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    key, value = line.strip().split("=")
                    setattr(cls, key, value)
        else:
            # Create the config file with default values if it doesn't exist
            cls.save_config()

    @classmethod
    def save_config(cls):
        with open(cls.config_file_path, "w") as file:
            file.write(f"folder_nofacturadas_prosegur={cls.folder_facturadas_prosegur}\n")
            file.write(f"folder_facturadas_prosegur={cls.folder_nofacturadas_prosegur}\n")
            file.write(f"folder_nofacturadas_brinks={cls.folder_facturadas_brinks}\n")
            file.write(f"folder_facturadas_brinks={cls.folder_nofacturadas_brinks}\n")

    @classmethod
    def update_config(cls, folder_facturadas_prosegur, folder_nofacturadas_prosegur,
                      folder_facturadas_brinks, folder_nofacturadas_brinks):
        cls.folder_facturadas_prosegur = folder_facturadas_prosegur
        cls.folder_nofacturadas_prosegur = folder_nofacturadas_prosegur
        cls.folder_facturadas_brinks = folder_facturadas_brinks
        cls.folder_nofacturadas_brinks = folder_nofacturadas_brinks

        # Save the updated configuration
        cls.save_config()

class FileMoverApp:
    def __init__(self, root):
        Config.load_config()  # Cargar la configuración desde el archivo
        self.root = root
        self.root.title("File Mover App")
        self.init_main_ui()

    def init_main_ui(self):
        # Utilizar el estilo ttk para obtener un aspecto más moderno
        style = ttk.Style()
        style.configure('TButton', font=('calibri', 14, 'bold'), borderwidth='4')
        style.configure('TListbox', font=('calibri', 14), borderwidth='2', relief='sunken')

        # Interfaz principal con dos botones
        btn_prosegur = ttk.Button(self.root, text="Prosegur", command=lambda: self.open_interface_prosegur())
        btn_brinks = ttk.Button(self.root, text="Brinks", command=lambda: self.open_interface_brinks())

        # Colocar botones en la interfaz principal
        btn_prosegur.grid(row=0, column=0, padx=10, pady=10)
        btn_brinks.grid(row=0, column=1, padx=10, pady=10)

        # Centrar la interfaz en la pantalla
        self.center_window()
    def seleccionar_facturadas_prosegur(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            Config.update_config(folder_facturadas_prosegur=folder_selected)
            Config.save_config()
            self.actualizar_lista_prosegur()


    def seleccionar_nofacturadas_prosegur(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            Config.update_config(folder_nofacturadas_prosegur=folder_selected)
            Config.save_config()
            self.actualizar_lista_prosegur()

    def seleccionar_facturadas_brinks(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            Config.update_config(folder_facturadas_brinks=folder_selected)
            Config.save_config()
            self.actualizar_lista_brinks()

    def seleccionar_nofacturadas_brinks(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            Config.update_config(folder_nofacturadas_brinks=folder_selected)
            Config.save_config()
            self.actualizar_lista_brinks()

    def open_interface_prosegur(self):
        # Cerrar la interfaz principal
        self.root.destroy()

        # Crear una nueva interfaz para Prosegur
        root_prosegur = tk.Tk()
        root_prosegur.title("File Mover App - Prosegur")
        app_prosegur = FileMoverAppSpecific(root_prosegur, "Prosegur")
        app_prosegur.center_window()
        root_prosegur.mainloop()

    def open_interface_brinks(self):
        # Cerrar la interfaz principal
        self.root.destroy()

        # Crear una nueva interfaz para Brinks
        root_brinks = tk.Tk()
        root_brinks.title("File Mover App - Brinks")
        app_brinks = FileMoverAppSpecific(root_brinks, "Brinks")
        app_brinks.center_window()
        root_brinks.mainloop()

    def center_window(self):
        # Centrar la ventana en la pantalla
        width = 600
        height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def actualizar_lista_prosegur(self):
        messagebox.showinfo("Actualizado", "Lista de Prosegur actualizada.")

    def actualizar_lista_brinks(self):
        messagebox.showinfo("Actualizado", "Lista de Brinks actualizada.")

class FileMoverAppSpecific:
    def __init__(self, root, company_name):
        self.root = root
        self.root.title(f"File Mover App - {company_name}")
        self.folder_facturadas = ""
        self.folder_nofacturadas = ""
        self.company_name = company_name  # Agregamos el nombre de la empresa
        self.load_folders_from_config()  # Cargamos las carpetas desde la configuración
        self.init_ui()

    def init_ui(self):
        # Utilizar el estilo ttk para obtener un aspecto más moderno
        style = ttk.Style()
        style.configure('TButton', font=('calibri', 14, 'bold'), borderwidth='4')
        style.configure('TListbox', font=('calibri', 12), borderwidth='2', relief='sunken')  # Ajusta el tamaño de la fuente
        style.configure('TEntry', font=('calibri', 14), borderwidth='2', relief='sunken')

        self.listbox_facturadas = Listbox(self.root, selectmode=MULTIPLE, height=20, width=35, font=('calibri', 12))
        self.listbox_nofacturadas = Listbox(self.root, selectmode=MULTIPLE, height=20, width=35, font=('calibri', 12))

        # Agregar archivos de ejemplo a las listas
        self.load_files_into_listbox(self.folder_facturadas, self.listbox_facturadas)
        self.load_files_into_listbox(self.folder_nofacturadas, self.listbox_nofacturadas)

        # Crear botones de selección de archivos
        btn_seleccionar_facturadas = ttk.Button(self.root, text="Seleccionar No Facturadas", command=self.seleccionar_facturadas)
        btn_seleccionar_nofacturadas = ttk.Button(self.root, text="Seleccionar Facturadas", command=self.seleccionar_nofacturadas)

        # Botón para eliminar archivos seleccionados
        btn_eliminar_seleccion = ttk.Button(self.root, text="Eliminar Archivos", command=self.eliminar_seleccion)
        btn_eliminar_seleccion.grid(row=3, column=5, padx=10, pady=10)

        # Crear botones de flechas y botón de guardar
        btn_right = ttk.Button(self.root, text="<-", command=self.move_files_right)
        btn_left = ttk.Button(self.root, text="->", command=self.move_files_left)
        btn_guardar = ttk.Button(self.root, text="Guardar", command=self.guardar_cambios)
        btn_back = ttk.Button(self.root, text="Volver", command=self.volver)

        # Etiquetas y entrada para el buscador
        lbl_facturadas = Label(self.root, text="Cotizaciones-No Facturadas", font=('calibri', 14))
        lbl_nofacturadas = Label(self.root, text="Cotizaciones-Facturadas", font=('calibri', 14))
        lbl_search = Label(self.root, text="Buscar:", font=('calibri', 14))
        self.entry_search = ttk.Entry(self.root, font=('calibri', 14))
        btn_search = ttk.Button(self.root, text="Buscar", command=self.search_files)

        # Botones de borrar selección
        btn_borrar_seleccion_facturadas = ttk.Button(self.root, text="Borrar Selección", command=self.borrar_seleccion_facturadas)
        btn_borrar_seleccion_nofacturadas = ttk.Button(self.root, text="Borrar Selección", command=self.borrar_seleccion_nofacturadas)

        # Botones de seleccionar todas
        btn_seleccionar_todas_facturadas = ttk.Button(self.root, text="Seleccionar Todas", command=lambda: self.listbox_select_all(self.listbox_facturadas))
        btn_seleccionar_todas_nofacturadas = ttk.Button(self.root, text="Seleccionar Todas", command=lambda: self.listbox_select_all(self.listbox_nofacturadas))

        # Botón de actualizar lista
        btn_actualizar = ttk.Button(self.root, text="Actualizar", command=self.actualizar_lista)

        # Colocar widgets en la interfaz
        self.listbox_facturadas.grid(row=1, column=0, padx=10, pady=10, rowspan=3)
        lbl_facturadas.grid(row=0, column=0, padx=10, pady=10)
        lbl_nofacturadas.grid(row=0, column=3, padx=10, pady=10)
        btn_right.grid(row=2, column=1, padx=10, pady=10)
        btn_left.grid(row=2, column=2, padx=10, pady=10)
        self.listbox_nofacturadas.grid(row=1, column=3, padx=10, pady=10, rowspan=3)
        btn_guardar.grid(row=1, column=5, padx=10, pady=10)
        btn_back.grid(row=2, column=5, padx=10, pady=10)
        lbl_search.grid(row=10, column=0, padx=10, pady=10)
        self.entry_search.grid(row=10, column=1, padx=10, pady=10)
        btn_search.grid(row=10, column=2, padx=10, pady=10)
        btn_borrar_seleccion_facturadas.grid(row=3, column=1, padx=10, pady=10)
        btn_borrar_seleccion_nofacturadas.grid(row=3, column=2, padx=10, pady=10)
        btn_seleccionar_todas_facturadas.grid(row=5, column=1, padx=10, pady=10)
        btn_seleccionar_todas_nofacturadas.grid(row=5, column=2, padx=10, pady=10)
        btn_actualizar.grid(row=10, column=3, padx=10, pady=10)
        btn_seleccionar_facturadas.grid(row=5, column=0, padx=10, pady=10)
        btn_seleccionar_nofacturadas.grid(row=5, column=3, padx=10, pady=10)

        # Configurar scrollbars
        scrollbar_facturadas = Scrollbar(self.root, orient='vertical', command=self.listbox_facturadas.yview)
        scrollbar_nofacturadas = Scrollbar(self.root, orient='vertical', command=self.listbox_nofacturadas.yview)

        scrollbar_facturadas_x = Scrollbar(self.root, orient='horizontal', command=self.listbox_facturadas.xview)
        scrollbar_nofacturadas_x = Scrollbar(self.root, orient='horizontal', command=self.listbox_nofacturadas.xview)

        self.listbox_facturadas.config(xscrollcommand=scrollbar_facturadas_x.set)
        self.listbox_nofacturadas.config(xscrollcommand=scrollbar_nofacturadas_x.set)

        scrollbar_facturadas_x.grid(row=4, column=0, columnspan=3, sticky='ew')
        scrollbar_nofacturadas_x.grid(row=4, column=3, columnspan=3, sticky='ew')

        self.listbox_facturadas.config(yscrollcommand=scrollbar_facturadas.set)
        self.listbox_nofacturadas.config(yscrollcommand=scrollbar_nofacturadas.set)

        scrollbar_facturadas.grid(row=1, column=1, sticky='ns', pady=10)
        scrollbar_nofacturadas.grid(row=1, column=4, sticky='ns', pady=10)

        # Configurar eventos de doble clic en la lista
        self.listbox_facturadas.bind("<Double-1>", self.open_file)
        self.listbox_nofacturadas.bind("<Double-1>", self.open_file)

        # Centrar la interfaz en la pantalla
        self.center_window()

    def eliminar_seleccion(self):
        # Obtener los índices seleccionados en ambas listas
        indices_facturadas = self.listbox_facturadas.curselection()
        indices_nofacturadas = self.listbox_nofacturadas.curselection()

        # Eliminar archivos seleccionados en la lista de facturadas
        for index in reversed(indices_facturadas):
            file_name = self.listbox_facturadas.get(index)
            file_path = os.path.join(self.folder_facturadas, file_name)
            os.remove(file_path)

        # Eliminar archivos seleccionados en la lista de nofacturadas
        for index in reversed(indices_nofacturadas):
            file_name = self.listbox_nofacturadas.get(index)
            file_path = os.path.join(self.folder_nofacturadas, file_name)
            os.remove(file_path)

        # Actualizar las listas después de eliminar los archivos
        self.actualizar_lista()

    def load_files_into_listbox(self, folder, listbox):
        # Verificar si la carpeta existe
        if os.path.exists(folder):
            # Obtener la lista de archivos en la carpeta
            files = os.listdir(folder)

            # Agregar archivos a la lista
            for file in files:
                file_path = os.path.join(folder, file)
                file_date = datetime.fromtimestamp(os.path.getmtime(file_path))
                formatted_date = file_date.strftime('%d-%m-%Y %H:%M:%S')
                listbox.insert(tk.END, f"{file} ({formatted_date})")

    def seleccionar_facturadas(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_facturadas = folder_selected
            if self.company_name.lower() == "prosegur":
                Config.update_config(
                    folder_facturadas_prosegur=self.folder_facturadas,
                    folder_nofacturadas_prosegur=Config.folder_nofacturadas_prosegur,
                    folder_facturadas_brinks=Config.folder_facturadas_brinks,
                    folder_nofacturadas_brinks=Config.folder_nofacturadas_brinks
                )
            elif self.company_name.lower() == "brinks":
                Config.update_config(
                    folder_facturadas_prosegur=Config.folder_facturadas_prosegur,
                    folder_nofacturadas_prosegur=Config.folder_nofacturadas_prosegur,
                    folder_facturadas_brinks=self.folder_facturadas,
                    folder_nofacturadas_brinks=Config.folder_nofacturadas_brinks
                )
            Config.save_config()  # Save the updated configuration
            self.actualizar_lista()

    def seleccionar_nofacturadas(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_nofacturadas = folder_selected
            if self.company_name.lower() == "prosegur":
                Config.update_config(
                    folder_facturadas_prosegur=Config.folder_facturadas_prosegur,
                    folder_nofacturadas_prosegur=self.folder_nofacturadas,
                    folder_facturadas_brinks=Config.folder_facturadas_brinks,
                    folder_nofacturadas_brinks=Config.folder_nofacturadas_brinks
                )
            elif self.company_name.lower() == "brinks":
                Config.update_config(
                    folder_facturadas_prosegur=Config.folder_facturadas_prosegur,
                    folder_nofacturadas_prosegur=Config.folder_nofacturadas_prosegur,
                    folder_facturadas_brinks=Config.folder_facturadas_brinks,
                    folder_nofacturadas_brinks=self.folder_nofacturadas
                )
            Config.save_config()  # Save the updated configuration
            self.actualizar_lista()


    def load_folders_from_config(self):
        # Cargar carpetas específicas de Prosegur o Brinks desde la configuración
        if self.company_name.lower() == "prosegur":
            self.folder_facturadas = Config.folder_facturadas_prosegur
            self.folder_nofacturadas = Config.folder_nofacturadas_prosegur
        elif self.company_name.lower() == "brinks":
            self.folder_facturadas = Config.folder_facturadas_brinks
            self.folder_nofacturadas = Config.folder_nofacturadas_brinks

    def save_folders_to_config(self):
        # Guardar carpetas específicas de Prosegur o Brinks en la configuración
        if self.company_name.lower() == "prosegur":
            Config.folder_facturadas_prosegur = self.folder_facturadas
            Config.folder_nofacturadas_prosegur = self.folder_nofacturadas
        elif self.company_name.lower() == "brinks":
            Config.folder_facturadas_brinks = self.folder_facturadas
            Config.folder_nofacturadas_brinks = self.folder_nofacturadas

    def move_files_right(self):
        selected_indices = self.listbox_nofacturadas.curselection()
        for index in selected_indices:
            # Obtener el nombre del archivo seleccionado
            file_name = self.listbox_nofacturadas.get(index)

            date_position = file_name.rfind('(')
            if date_position != -1:
                # Eliminar la información de la fecha
                file_name = file_name[:date_position].strip()

            # Verificar si el elemento es un archivo (y no una carpeta)
            file_path = os.path.join(self.folder_nofacturadas, file_name)
            if os.path.isfile(file_path):
                # Mover el archivo de "nofacturadas" a "facturadas"
                shutil.move(file_path, os.path.join(self.folder_facturadas, file_name))

        # Actualizar las listas y guardar cambios
        self.actualizar_lista()
        self.save_folders_to_config()

    def move_files_left(self):
        selected_indices = self.listbox_facturadas.curselection()
        for index in selected_indices:
            # Obtener el nombre del archivo seleccionado
            file_name = self.listbox_facturadas.get(index)
            date_position = file_name.rfind('(')
            if date_position != -1:
                # Eliminar la información de la fecha
                file_name = file_name[:date_position].strip()

            # Verificar si el elemento es un archivo (y no una carpeta)
            file_path = os.path.join(self.folder_facturadas, file_name)
            if os.path.isfile(file_path):
                # Mover el archivo de "facturadas" a "nofacturadas"
                shutil.move(file_path, os.path.join(self.folder_nofacturadas, file_name))

        # Actualizar las listas y guardar cambios
        self.actualizar_lista()
        self.save_folders_to_config()

    def guardar_cambios(self):
        messagebox.showinfo("HECHO", "Cambios guardados correctamente.")

    def volver(self):
        # Cerrar la interfaz actual
        self.root.destroy()

        # Crear una nueva interfaz principal
        root_main = tk.Tk()
        app_main = FileMoverApp(root_main)
        app_main.center_window()
        root_main.mainloop()

    def search_files(self):
        search_term = self.entry_search.get().lower()

        # Buscar archivos en facturadas
        self.listbox_facturadas.delete(0, tk.END)
        self.load_files_into_listbox_filtered(self.folder_facturadas, self.listbox_facturadas, search_term)

        # Buscar archivos en nofacturadas
        self.listbox_nofacturadas.delete(0, tk.END)
        self.load_files_into_listbox_filtered(self.folder_nofacturadas, self.listbox_nofacturadas, search_term)

    def load_files_into_listbox_filtered(self, folder, listbox, search_term):
        # Verificar si la carpeta existe
        if os.path.exists(folder):
            # Obtener la lista de archivos en la carpeta
            files = os.listdir(folder)

            # Filtrar archivos por término de búsqueda
            filtered_files = [file for file in files if fnmatch(file.lower(), f'*{search_term}*')]

            # Agregar archivos a la lista
            for file in filtered_files:
                listbox.insert(tk.END, file)

    def borrar_seleccion_facturadas(self):
        # Desmarcar la selección en la lista de facturadas
        self.listbox_facturadas.selection_clear(0, tk.END)

    def borrar_seleccion_nofacturadas(self):
        # Desmarcar la selección en la lista de nofacturadas
        self.listbox_nofacturadas.selection_clear(0, tk.END)

    def listbox_select_all(self, listbox):
        # Seleccionar todas las entradas en la lista
        listbox.select_set(0, tk.END)

    def actualizar_lista(self):
        self.listbox_facturadas.delete(0, tk.END)
        self.load_files_into_listbox(self.folder_facturadas, self.listbox_facturadas)

        # Actualizar la lista de archivos en nofacturadas
        self.listbox_nofacturadas.delete(0, tk.END)
        self.load_files_into_listbox(self.folder_nofacturadas, self.listbox_nofacturadas)

    def open_file(self, event):
    # Obtener el índice del elemento seleccionado
        widget = event.widget
        selected_index = widget.curselection()

        if selected_index:
            # Obtener el nombre del archivo seleccionado
            file_name_with_date = widget.get(selected_index[0])

            # Extraer solo el nombre del archivo sin la información de la fecha
            file_name, file_extension = os.path.splitext(file_name_with_date)

            # Buscar la posición de la última ocurrencia del patrón de fecha en el nombre del archivo
            date_position = file_extension.rfind('(')
            if date_position != -1:
                # Eliminar la información de la fecha
                file_extension = file_extension[:date_position].strip()

            # Obtener la carpeta correcta según la lista
            if widget is self.listbox_facturadas:
                folder_path = self.folder_facturadas
            elif widget is self.listbox_nofacturadas:
                folder_path = self.folder_nofacturadas
            else:
                return

            # Construir la ruta completa al archivo
            file_path = os.path.join(folder_path, file_name + file_extension)

            # Usar el método adecuado según la plataforma para abrir el archivo
            try:
                os.startfile(file_path)  # Para Windows
            except AttributeError:
                # En sistemas no Windows, utilizar 'open' de acuerdo al tipo de archivo
                import subprocess
                subprocess.run(['open', file_path], check=True)


    def center_window(self):
        # Obtener dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Establecer el tamaño deseado de la ventana (ajusta según sea necesario)
        width = int(screen_width * 0.8)
        height = int(screen_height * 0.8)

        # Calcular la posición para centrar la ventana
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Configurar el tamaño y la posición de la ventana
        self.root.geometry(f'{width}x{height}+{x}+{y}')

root_main = tk.Tk()
app_main = FileMoverApp(root_main)
app_main.center_window()  # Llamar a la función para establecer el tamaño y posición de la ventana
root_main.mainloop()
