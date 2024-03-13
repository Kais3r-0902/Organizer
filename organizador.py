import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar, Style  # Importar Style desde ttk
from PIL import Image, ImageTk  # Importar Image y ImageTk desde PIL

def organize_files(source_directory, target_directory, progress_bar):
    # Inicializar variables para el registro de actividad y el progreso
    activity_log = []
    total_files = sum(len(files) for _, _, files in os.walk(source_directory))
    progress_bar["maximum"] = total_files

    # Recorrer el directorio de origen y organizar archivos
    for root, _, files in os.walk(source_directory):
        for file in files:
            source_file_path = os.path.join(root, file)
            target_file_path = os.path.join(target_directory, file)

            # Manejar archivos duplicados
            if os.path.exists(target_file_path):
                target_file_path = handle_duplicate_file(target_file_path)

            # Mover el archivo al directorio de destino
            shutil.move(source_file_path, target_file_path)

            # Actualizar el registro de actividad y la barra de progreso
            activity_log.append(f"Movido: {source_file_path} -> {target_file_path}")
            progress_bar["value"] += 1
            root.update_idletasks()

            # Verificar si se ha solicitado detener la organización de archivos
            if stopped:
                activity_log.append("Organización de archivos detenida.")
                break

    # Mostrar mensaje de finalización y registro de actividad
    if not stopped:
        activity_log.append("Organización de archivos completada.")
    messagebox.showinfo("Información", "\n".join(activity_log))

def handle_duplicate_file(target_file_path):
    # Lógica para manejar archivos duplicados (puedes personalizar según tus necesidades)
    # Aquí simplemente agregamos un sufijo '_copy' al nombre del archivo duplicado
    base_name, ext = os.path.splitext(target_file_path)
    counter = 1
    while os.path.exists(target_file_path):
        target_file_path = f"{base_name}_copy{counter}{ext}"
        counter += 1
    return target_file_path

def browse_source_directory():
    directory = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, directory)

def browse_target_directory():
    directory = filedialog.askdirectory()
    target_entry.delete(0, tk.END)
    target_entry.insert(0, directory)

def organize_button_click():
    try:
        # Obtener los parámetros de la GUI
        source_directory = source_entry.get()
        target_directory = target_entry.get()

        # Confirmar con el usuario antes de iniciar la organización de archivos
        confirm_message = f"¿Estás seguro de que deseas organizar los archivos de '{source_directory}' en '{target_directory}'?"
        if messagebox.askyesno("Confirmar Organización", confirm_message):
            # Restablecer la barra de progreso y la variable global 'stopped'
            progress_bar["value"] = 0
            global stopped
            stopped = False

            # Mostrar la barra de progreso
            progress_bar.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

            # Organizar archivos
            organize_files(source_directory, target_directory, progress_bar)
    except Exception as e:
        messagebox.showerror("Error", f"Se produjo un error: {str(e)}")

def stop_button_click():
    global stopped
    stopped = True

# Crear la ventana principal
root = tk.Tk()
root.title("Organizer by Poisoner Aphotecarius")
root.configure(bg="#f0f0f0")  # Cambiar el fondo a gris claro

# Etiquetas y campos de entrada para los directorios de origen y destino
source_label = tk.Label(root, text="Directorio de Origen:", bg="#f0f0f0", fg="black")  # Cambiar el color de fondo a gris claro y el texto a negro
source_label.grid(row=0, column=0, sticky="w")
source_entry = tk.Entry(root, width=50)
source_entry.grid(row=0, column=1, padx=5, pady=5)
browse_source_button = tk.Button(root, text="Examinar", command=browse_source_directory)
browse_source_button.grid(row=0, column=2)

target_label = tk.Label(root, text="Directorio de Destino:", bg="#f0f0f0", fg="black")  # Cambiar el color de fondo a gris claro y el texto a negro
target_label.grid(row=1, column=0, sticky="w")
target_entry = tk.Entry(root, width=50)
target_entry.grid(row=1, column=1, padx=5, pady=5)
browse_target_button = tk.Button(root, text="Examinar", command=browse_target_directory)
browse_target_button.grid(row=1, column=2)

# Botones de organización y detención
organize_icon = Image.open("organize_icon.png")  # Ruta al archivo de icono de organización
organize_icon = ImageTk.PhotoImage(organize_icon)
organize_button = tk.Button(root, text="Organizar", image=organize_icon, compound=tk.LEFT, command=organize_button_click)
organize_button.grid(row=3, column=0, padx=5, pady=5)

stop_icon = Image.open("stop_icon.png")  # Ruta al archivo de icono de detención
stop_icon = ImageTk.PhotoImage(stop_icon)
stop_button = tk.Button(root, text="Detener", image=stop_icon, compound=tk.LEFT, command=stop_button_click)
stop_button.grid(row=3, column=1, padx=5, pady=5)

# Barra de progreso
style = Style()  # Instanciar la clase Style
style.theme_use("default")
style.configure("blue.Horizontal.TProgressbar", background="blue")  # Cambiar el color a azul
progress_bar = Progressbar(root, style="blue.Horizontal.TProgressbar", orient="horizontal", length=300, mode="determinate")

# Ejecutar la aplicación
root.mainloop()
