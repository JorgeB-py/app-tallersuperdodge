import os
import shutil
import tkinter as tk
from tkinter import ttk, Listbox, Button, messagebox, Entry, Label, Scrollbar, MULTIPLE

class FileMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Mover App")
        self.init_main_ui()

    def init_main_ui(self):
        # Utilizar el estilo ttk para obtener un aspecto más moderno
        style = ttk.Style()
        style.configure('TButton', font=('calibri', 14, 'bold'), borderwidth='4')
        style.configure('TListbox', font=('calibri', 14), borderwidth='2', relief='sunken')

        # Interfaz principal con dos botones
        btn_brinks = ttk.Button(self.root, text="Brinks", command=lambda: self.open_interface("Brinks"))
        btn_prosegur = ttk.Button(self.root, text="Prosegur", command=lambda: self.open_interface("Prosegur"))

        # Colocar botones en la interfaz principal
        btn_brinks.grid(row=0, column=0, padx=10, pady=10)
        btn_prosegur.grid(row=0, column=1, padx=10, pady=10)

        # Centrar la interfaz en la pantalla
        self.center_window()

    def open_interface(self, company_name):
        # Cerrar la interfaz principal
        self.root.destroy()

        # Crear una nueva interfaz para la empresa específica
        root_company = tk.Tk()
        root_company.title(f"File Mover App - {company_name}")
        app_company = FileMoverAppSpecific(root_company, f"facturadas_{company_name.lower()}", f"nofacturadas_{company_name.lower()}")
        app_company.center_window()
        root_company.mainloop()

    def center_window(self):
        # Centrar la ventana en la pantalla
        width = 600
        height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

class FileMoverAppSpecific:
    def __init__(self, root, folder_facturadas, folder_nofacturadas):
        self.root = root
        self.root.title("File Mover App - Specific")
        self.folder_facturadas = folder_facturadas
        self.folder_nofacturadas = folder_nofacturadas
        self.init_ui()

    def init_ui(self):
        # Utilizar el estilo ttk para obtener un aspecto más moderno
        style = ttk.Style()
        style.configure('TButton', font=('calibri', 14, 'bold'), borderwidth='4')
        style.configure('TListbox', font=('calibri', 16), borderwidth='2', relief='sunken')  # Ajusta el tamaño de la fuente
        style.configure('TEntry', font=('calibri', 14), borderwidth='2', relief='sunken')

        self.listbox_facturadas = Listbox(self.root, selectmode=MULTIPLE, height=25, width=40, font=('calibri', 16))
        self.listbox_nofacturadas = Listbox(self.root, selectmode=MULTIPLE, height=25, width=40, font=('calibri', 16))

        # Agregar archivos de ejemplo a las listas
        self.load_files_into_listbox(self.folder_facturadas, self.listbox_facturadas)
        self.load_files_into_listbox(self.folder_nofacturadas, self.listbox_nofacturadas)

        # Crear botones de flechas y botón de guardar
        btn_right = ttk.Button(self.root, text="<-", command=self.move_files_right)
        btn_left = ttk.Button(self.root, text="->", command=self.move_files_left)
        btn_guardar = ttk.Button(self.root, text="Guardar", command=self.guardar_cambios)
        btn_back = ttk.Button(self.root, text="Volver", command=self.volver)

        # Etiquetas y entrada para el buscador
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
        btn_seleccionar_todas_facturadas.grid(row=4, column=1, padx=10, pady=10)
        btn_seleccionar_todas_nofacturadas.grid(row=4, column=2, padx=10, pady=10)
        btn_actualizar.grid(row=12, column=1, padx=10, pady=10)

        # Configurar scrollbars
        scrollbar_facturadas = Scrollbar(self.root, orient='vertical', command=self.listbox_facturadas.yview)
        scrollbar_nofacturadas = Scrollbar(self.root, orient='vertical', command=self.listbox_nofacturadas.yview)

        self.listbox_facturadas.config(yscrollcommand=scrollbar_facturadas.set)
        self.listbox_nofacturadas.config(yscrollcommand=scrollbar_nofacturadas.set)

        scrollbar_facturadas.grid(row=1, column=1, sticky='ns', pady=10)
        scrollbar_nofacturadas.grid(row=1, column=4, sticky='ns', pady=10)

        # Configurar eventos de doble clic en la lista
        self.listbox_facturadas.bind("<Double-1>", self.open_file)
        self.listbox_nofacturadas.bind("<Double-1>", self.open_file)

        # Centrar la interfaz en la pantalla
        self.center_window()

    def load_files_into_listbox(self, folder, listbox):
        # Verificar si la carpeta existe
        if os.path.exists(folder):
            # Obtener la lista de archivos en la carpeta
            files = os.listdir(folder)

            # Agregar archivos a la lista
            for file in files:
                listbox.insert(tk.END, file)

    def move_files_right(self):
        selected_indices = self.listbox_nofacturadas.curselection()
        for index in selected_indices:
            # Obtener el nombre del archivo seleccionado
            file_name = self.listbox_nofacturadas.get(index)

            # Verificar si el elemento es un archivo (y no una carpeta)
            file_path = os.path.join(self.folder_nofacturadas, file_name)
            if os.path.isfile(file_path):
                # Mover el archivo de "nofacturadas" a "facturadas"
                shutil.move(file_path, os.path.join(self.folder_facturadas, file_name))

        # Actualizar las listas
        self.actualizar_lista()

    def move_files_left(self):
        selected_indices = self.listbox_facturadas.curselection()
        for index in selected_indices:
            # Obtener el nombre del archivo seleccionado
            file_name = self.listbox_facturadas.get(index)

            # Verificar si el elemento es un archivo (y no una carpeta)
            file_path = os.path.join(self.folder_facturadas, file_name)
            if os.path.isfile(file_path):
                # Mover el archivo de "facturadas" a "nofacturadas"
                shutil.move(file_path, os.path.join(self.folder_nofacturadas, file_name))

        # Actualizar las listas
        self.actualizar_lista()

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
            filtered_files = [file for file in files if search_term in file.lower()]

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
        # Actualizar la lista de archivos en facturadas
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
            file_name = widget.get(selected_index[0])

            # Abrir el archivo
            file_path = os.path.join(self.folder_facturadas, file_name)
            os.system(f'start {file_path}')

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

