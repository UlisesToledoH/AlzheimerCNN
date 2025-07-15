import customtkinter
import os
from tkinter import filedialog, messagebox
import numpy as np
from PIL import Image, ImageGrab
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from keras.models import load_model
from tkintermapview import TkinterMapView
from CTkPDFViewer import *
import tkinter as tk
#import tkPDFViewer
#from tkPDFViewer import tkPDFViewer as pdf

modelo = load_model('modelo9967.h5')

clases = {
    0: "Demencia leve",
    1: "Demencia moderada",
    2: "Sin demencia",
    3: "Demencia muy leve",
}
def save_img():
    if app.home_frame:
        try:
            # Obtener el área del widget que se desea capturar
            x = app.home_frame.winfo_rootx()
            y = app.home_frame.winfo_rooty()
            w = app.home_frame.winfo_width()
            h = app.home_frame.winfo_height()
            
            # Capturar la imagen del área especificada
            imagen_capturada = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            
            # Guardar la imagen capturada en la ubicación seleccionada por el usuario
            ruta_guardado = filedialog.asksaveasfilename(defaultextension=".png",
                                                         filetypes=(("PNG files", "*.png"),
                                                                    ("JPEG files", "*.jpg"),
                                                                    ("All files", "*.*")),
                                                         title="Guardar captura como")
            if ruta_guardado:
                imagen_capturada.save(ruta_guardado)
                messagebox.showinfo("Guardado", "Captura de pantalla guardada exitosamente.")
        except Exception as e:
            print(f"Error al guardar la captura de pantalla: {e}")  # Depuración: Imprimir error
            messagebox.showerror("Error", f"No se pudo guardar la captura de pantalla: {e}")
    else:
        messagebox.showwarning("Advertencia", "No hay captura de pantalla para guardar.")

def open_img():
    ruta_imagen = filedialog.askopenfilename(initialdir="/", title="Seleccionar Imagen",
                                             filetypes=(("Archivos de Imagen", "*.png *.jpg *.jpeg"), ("Todos los archivos", "*.*")))
    if ruta_imagen:
        try:
            imagen = Image.open(ruta_imagen)
            imagen = imagen.convert("L")
            imagen = imagen.resize((128, 128))
            imagen = np.array(imagen) / 255.0
            imagen = np.expand_dims(imagen, axis=0)

            img = Image.open(ruta_imagen)
            #img = img.resize((250, 250))
            img = customtkinter.CTkImage(img, size=(250,250))
            panel = customtkinter.CTkLabel(master=app.image_graph_frame, image=img, text="")
            panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            # Realizar la predicción utilizando el modelo
            prediccion = modelo.predict(imagen)
            clase_predicha = np.argmax(prediccion)
            # Obtener el nombre de la clase predicha
            nombre_clase_predicha = clases.get(clase_predicha, "Clase Desconocida")
            # Calcular la precisión de la predicción
            precision = prediccion[0][clase_predicha] * 100

            # Crear la figura
            fig = plt.figure(figsize=(3.8, 4.5))
            colores = ['#5DADE2', '#A0568A', '#A09156', '#50AF50']
            bars = plt.bar(clases.values(), prediccion.flatten()*100, width=0.3, color=colores)

            # Agregar etiquetas con porcentajes en cada barra
            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}%', ha='center', va='bottom')
            plt.xlabel('Clase', fontsize=10)
            plt.ylabel('Acertividad (%)', fontsize=12)
            plt.title('Acertividad de la predicción por clase', fontsize=10)
            plt.xticks(rotation=45, ha='right', fontsize=10)
            plt.tight_layout()

            # Incrustar la gráfica en el frame inicio
            canvas = FigureCanvasTkAgg(fig, master=app.image_graph_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

            # Crear un nuevo frame para el texto de la clase predicha y el porcentaje de acertividad
            prediction_frame = customtkinter.CTkFrame(master=app.image_graph_frame)
            prediction_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

            # Mostrar el resultado de la predicción en la interfaz gráfica
            label_resultado = customtkinter.CTkLabel(master=prediction_frame, text=f"Clase Predicha: {nombre_clase_predicha}", font=customtkinter.CTkFont(size=16, weight="bold"))
            label_resultado.grid(row=0, column=0, padx=10, pady=10)

            # Mostrar el porcentaje de asertividad en un label
            label_porcentaje_acertividad = customtkinter.CTkLabel(master=prediction_frame, text=f"  Porcentaje de Acertividad: {precision:.2f}%", font=customtkinter.CTkFont(size=16, weight="bold"))
            label_porcentaje_acertividad.grid(row=0, column=1, padx=10, pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar la imagen: {e}")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Alzheimer")
        self.geometry("780x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "escudo.png")), size=(40, 40))
        
        self.large_test_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "poli_n.png")),
                                                            dark_image=Image.open(os.path.join(image_path, "poli_b.png")), size=(150, 110))
        
        #Imagenes de botones de inicio
        self.imagen_subir = customtkinter.CTkImage(Image.open(os.path.join(image_path, "R.png")), size=(20, 20))
        self.imagen_guardado = customtkinter.CTkImage(Image.open(os.path.join(image_path, "guardar.png")), size=(20, 20))
        self.imagen_recomendacion = customtkinter.CTkImage(Image.open(os.path.join(image_path, "ayuda.png")), size=(20, 20))
        self.imagen_nuevo = customtkinter.CTkImage(Image.open(os.path.join(image_path, "nuevo.png")), size=(20, 20))
        #-----imagenes Frames
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(30, 30))
        self.directorio_img = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "directorio_n.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "directorio_b.png")), size=(30, 30))
        self.manual_img = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "manual_n.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "manual_b.png")), size=(30, 30))

        self.salir_img = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "salir_n.png")),
                                                            dark_image=Image.open(os.path.join(image_path, "salir_b.png")), size=(30, 30))
                
        #-----------------------        
                # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=" ESIME ZACATENCO", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Inicio",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.directorio_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Directorio",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.directorio_img, anchor="w", command=self.directorio_button_event)
        self.directorio_button.grid(row=2, column=0, sticky="ew")
        
        

        self.manual_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Manual",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.manual_img, anchor="w", command=self.manual_button_event)
        self.manual_button.grid(row=3, column=0, sticky="ew")
        
        self.frame_salir = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Salir",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.salir_img, anchor="w", command=self.quit)
        self.frame_salir.grid(row=5, column=0, sticky="ew")
        

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],  fg_color="#7DC488", text_color="black",
                                                                button_color="#4E7B55", button_hover_color="#B4BAB5",
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame es el de la grafica
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0,weight=0)
        self.home_frame.grid_columnconfigure(1,weight=0)
        self.home_frame.grid_columnconfigure(2,weight=0)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image )
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10, columnspan=1)
        self.titulo_proy = customtkinter.CTkLabel(self.home_frame, text="Diagnóstico de Alzheimer Mediante Redes Neuronales Convolucionales\n" 
                                                  "Aplicadas al Análisis de Resonancias Magnéticas",
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.titulo_proy.grid(row=0, column=1, padx=20, pady=20, columnspan= 6)

        #Botones del frame inicio-------------
        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="Subir resonancia", image=self.imagen_subir,fg_color="#7DC488", text_color="black", command=open_img, hover_color="#B4BAB5")
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="Guardar Diagnostico", image=self.imagen_guardado, fg_color="#7DC488", text_color="black", command=save_img, hover_color="#B4BAB5")
        self.home_frame_button_2.grid(row=1, column=1, padx=20, pady=10)
        self.home_frame_button_3 = customtkinter.CTkButton(self.home_frame, text="Recomendaciones", image=self.imagen_recomendacion, fg_color="#7DC488", text_color="black", hover_color="#B4BAB5")
        self.home_frame_button_3.grid(row=1, column=2, padx=20, pady=10)
        self.home_frame_button_3 = customtkinter.CTkButton(self.home_frame, text="Nuevo Diagnostico", image=self.imagen_nuevo, fg_color="#7DC488", text_color="black",command=open_img , hover_color="#B4BAB5")
        self.home_frame_button_3.grid(row=1, column=3, padx=20, pady=10)
        
        #==================================================
         # Frame de directorio
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=0)
        self.second_frame.grid_columnconfigure(1, weight=0)
        self.second_frame.grid_columnconfigure(2, weight=0)
        
        # Crea los botones para seleccionar cada frame
        self.frame_buttons = customtkinter.CTkFrame(self.second_frame, corner_radius=0, fg_color="transparent")
        self.frame_buttons.grid(row=1, column=0, columnspan=4, pady=10)

        self.second_frame_1_button = customtkinter.CTkButton(self.frame_buttons, text="Talita", command=lambda: self.select_second_frame("second_frame_1"))
        self.second_frame_1_button.grid(row=0, column=0, padx=10)
    
        self.second_frame_2_button = customtkinter.CTkButton(self.frame_buttons, text="Frame 2", command=lambda: self.select_second_frame("second_frame_2"))
        self.second_frame_2_button.grid(row=0, column=1, padx=10)

        self.second_manual_button = customtkinter.CTkButton(self.frame_buttons, text="Frame 3", command=lambda: self.select_second_frame("second_frame_3"))
        self.second_manual_button.grid(row=0, column=2, padx=10)

        self.second_frame_4_button = customtkinter.CTkButton(self.frame_buttons, text="Frame 4", command=lambda: self.select_second_frame("second_frame_4"))
        self.second_frame_4_button.grid(row=0, column=3, padx=10)

        self.second_frame_5_button = customtkinter.CTkButton(self.frame_buttons, text="Frame 5", command=lambda: self.select_second_frame("second_frame_5"))
        self.second_frame_5_button.grid(row=0, column=4, padx=10)
        

        # Crea los 5 frames adicionales
        self.second_frame_1 = customtkinter.CTkFrame(self.second_frame, corner_radius=0, fg_color="transparent")
        self.second_frame_2 = customtkinter.CTkFrame(self.second_frame, corner_radius=0, fg_color="transparent")
        self.second_frame_3 = customtkinter.CTkFrame(self.second_frame, corner_radius=0, fg_color="transparent")
        self.second_frame_4 = customtkinter.CTkFrame(self.second_frame, corner_radius=0, fg_color="transparent")
        self.second_frame_5 = customtkinter.CTkFrame(self.second_frame, corner_radius=0, fg_color="transparent")

        # PARA LA PAGINA 1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.directorio_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "asilo.jpg")), size=(40, 40))
        self.directorio_label1=customtkinter.CTkLabel(self.second_frame_1, image=self.directorio_img, compound="left", text="")
        self.directorio_label1.grid(row=0, column=1, padx=10, pady=10)
        self.directorio_label1 = customtkinter.CTkLabel(self.second_frame_1, text=" TALITA\n RESIDENCIA Y CASA DE DIA PARA ALZHEIMER",
                                                             compound="center", font=customtkinter.CTkFont(size=22, weight="bold"))
        self.directorio_label1.grid(row=0, column=2, padx=10, pady=10, columnspan=5)
        self.directorio_label2 = customtkinter.CTkLabel(self.second_frame_1,compound="left", text="Dirección :", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.directorio_label2.grid(row=1, column=0, padx=0, pady=0)
        self.directorio_label3 = customtkinter.CTkLabel(self.second_frame_1,compound="left", text="Teléfono :", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.directorio_label3.grid(row=2, column=0, padx=10, pady=10)
        self.directorio_label4 = customtkinter.CTkLabel(self.second_frame_1,compound="left", text="E-mail :", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.directorio_label4.grid(row=3, column=0, padx=10, pady=0)
        
        self.directorio_label4 = customtkinter.CTkLabel(self.second_frame_1,compound="center", text="Mapa", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.directorio_label4.grid(row=5, column=2, padx=10, pady=10, columnspan=5)
         # Agrega el mapa
        self.mapa_1 = TkinterMapView(self.second_frame_1, width=620, height=400, corner_radius=0)
        self.mapa_1.grid(row=6, column=2, padx=10, pady=10, columnspan=5)
        self.mapa_1.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=26)
        self.mapa_1.set_marker(19.423090585856134, -99.23947021150305, text="Talita", text_color="black", font=("Consolas", 16,"bold")) #Coordenadas del marcador
        self.mapa_1.set_position(19.423090585856134, -99.23947021150305)  # Coordenadas de Ciudad de México
        # self.mapa_1.set_zoom(15)
        
       # PARA LA PAGINA 2 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.directorio_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "asilo.jpg")), size=(40, 40))
        self.directorio_label1=customtkinter.CTkLabel(self.second_frame_2, image=self.directorio_img, compound="left", text="")
        self.directorio_label1.grid(row=0, column=1, padx=10, pady=10)
        self.directorio_label1 = customtkinter.CTkLabel(self.second_frame_2, text=" Pagina 2",
                                                             compound="center", font=customtkinter.CTkFont(size=22, weight="bold"))
        self.directorio_label1.grid(row=0, column=2, padx=10, pady=10, columnspan=5)
        self.directorio_label2 = customtkinter.CTkLabel(self.second_frame_2,compound="left", text="Dirección :", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.directorio_label2.grid(row=1, column=0, padx=0, pady=0)
        self.directorio_label3 = customtkinter.CTkLabel(self.second_frame_2,compound="left", text="Teléfono :", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.directorio_label3.grid(row=2, column=0, padx=10, pady=10)
        self.directorio_label4 = customtkinter.CTkLabel(self.second_frame_2,compound="left", text="E-mail :", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.directorio_label4.grid(row=3, column=0, padx=10, pady=0)
        
        self.directorio_label4 = customtkinter.CTkLabel(self.second_frame_2,compound="center", text="Mapa", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.directorio_label4.grid(row=5, column=2, padx=10, pady=10, columnspan=5)
         # Agrega el mapa
        self.mapa_1 = TkinterMapView(self.second_frame_2, width=620, height=400, corner_radius=0)
        self.mapa_1.grid(row=6, column=2, padx=10, pady=10, columnspan=5)
        self.mapa_1.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=26)
        self.mapa_1.set_marker(19.423090585856134, -99.23947021150305, text="Talita", text_color="black", font=("Consolas", 16,"bold")) #Coordenadas del marcador
        self.mapa_1.set_position(19.423090585856134, -99.23947021150305)  # Coordenadas de Ciudad de México
        # self.mapa_1.set_zoom(15)
        
        #PARA LA PAGINA 3 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.directorio_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "asilo.jpg")), size=(40, 40))
        self.directorio_label1=customtkinter.CTkLabel(self.second_frame_3, image=self.directorio_img, compound="left", text="")
        self.directorio_label1.grid(row=0, column=1, padx=10, pady=10)
        self.directorio_label1 = customtkinter.CTkLabel(self.second_frame_3, text=" PAGINA",
                                                             compound="center", font=customtkinter.CTkFont(size=22, weight="bold"))
        self.directorio_label1.grid(row=0, column=2, padx=10, pady=10, columnspan=5)
        self.directorio_label2 = customtkinter.CTkLabel(self.second_frame_3,compound="left", text="Dirección :", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.directorio_label2.grid(row=1, column=0, padx=0, pady=0)
        self.directorio_label3 = customtkinter.CTkLabel(self.second_frame_3,compound="left", text="Teléfono :", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.directorio_label3.grid(row=2, column=0, padx=10, pady=10)
        self.directorio_label4 = customtkinter.CTkLabel(self.second_frame_3,compound="left", text="E-mail :", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.directorio_label4.grid(row=3, column=0, padx=10, pady=0)
        
        self.directorio_label4 = customtkinter.CTkLabel(self.second_frame_3,compound="center", text="Mapa", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.directorio_label4.grid(row=5, column=2, padx=10, pady=10, columnspan=5)
         # Agrega el mapa
        self.mapa_1 = TkinterMapView(self.second_frame_3, width=620, height=400, corner_radius=0)
        self.mapa_1.grid(row=6, column=2, padx=10, pady=10, columnspan=5)
        self.mapa_1.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=26)
        self.mapa_1.set_marker(19.423090585856134, -99.23947021150305, text="Talita", text_color="black", font=("Consolas", 16,"bold")) #Coordenadas del marcador
        self.mapa_1.set_position(19.423090585856134, -99.23947021150305)  # Coordenadas de Ciudad de México
        # self.mapa_1.set_zoom(15)
        
        #PARA LA PAGINA 4 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.directorio_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "asilo.jpg")), size=(40, 40))
        self.directorio_label1=customtkinter.CTkLabel(self.second_frame_4, image=self.directorio_img, compound="left", text="")
        self.directorio_label1.grid(row=0, column=1, padx=10, pady=10)
        self.directorio_label1 = customtkinter.CTkLabel(self.second_frame_4, text=" pag 4",
                                                             compound="center", font=customtkinter.CTkFont(size=22, weight="bold"))
        self.directorio_label1.grid(row=0, column=2, padx=10, pady=10, columnspan=5)
        self.directorio_label2 = customtkinter.CTkLabel(self.second_frame_4,compound="left", text="Dirección :", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.directorio_label2.grid(row=1, column=0, padx=0, pady=0)
        self.directorio_label3 = customtkinter.CTkLabel(self.second_frame_4,compound="left", text="Teléfono :", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.directorio_label3.grid(row=2, column=0, padx=10, pady=10)
        self.directorio_label4 = customtkinter.CTkLabel(self.second_frame_4,compound="left", text="E-mail :", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.directorio_label4.grid(row=3, column=0, padx=10, pady=0)
        
        self.directorio_label4 = customtkinter.CTkLabel(self.second_frame_4,compound="center", text="Mapa", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.directorio_label4.grid(row=5, column=2, padx=10, pady=10, columnspan=5)
         # Agrega el mapa
        self.mapa_1 = TkinterMapView(self.second_frame_4, width=620, height=400, corner_radius=0)
        self.mapa_1.grid(row=6, column=2, padx=10, pady=10, columnspan=5)
        self.mapa_1.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=26)
        self.mapa_1.set_marker(19.423090585856134, -99.23947021150305, text="Talita", text_color="black", font=("Consolas", 16,"bold")) #Coordenadas del marcador
        self.mapa_1.set_position(19.423090585856134, -99.23947021150305)  # Coordenadas de Ciudad de México
        # self.mapa_1.set_zoom(15)
        #PARA LA PAGINA 5 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.directorio_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "asilo.jpg")), size=(40, 40))
        self.directorio_label1=customtkinter.CTkLabel(self.second_frame_5, image=self.directorio_img, compound="left", text="")
        self.directorio_label1.grid(row=0, column=1, padx=10, pady=10)
        self.directorio_label1 = customtkinter.CTkLabel(self.second_frame_5, text=" pag 5",
                                                             compound="center", font=customtkinter.CTkFont(size=22, weight="bold"))
        self.directorio_label1.grid(row=0, column=2, padx=10, pady=10, columnspan=5)
        self.directorio_label2 = customtkinter.CTkLabel(self.second_frame_5,compound="left", text="Dirección :", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.directorio_label2.grid(row=1, column=0, padx=0, pady=0)
        self.directorio_label3 = customtkinter.CTkLabel(self.second_frame_5,compound="left", text="Teléfono :", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.directorio_label3.grid(row=2, column=0, padx=10, pady=10)
        self.directorio_label4 = customtkinter.CTkLabel(self.second_frame_5,compound="left", text="E-mail :", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.directorio_label4.grid(row=3, column=0, padx=10, pady=0)
        
        self.directorio_label4 = customtkinter.CTkLabel(self.second_frame_5,compound="center", text="Mapa", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.directorio_label4.grid(row=5, column=2, padx=10, pady=10, columnspan=5)
         # Agrega el mapa
        self.mapa_1 = TkinterMapView(self.second_frame_5, width=620, height=400, corner_radius=0)
        self.mapa_1.grid(row=6, column=2, padx=10, pady=10, columnspan=5)
        self.mapa_1.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=26)
        self.mapa_1.set_marker(19.423090585856134, -99.23947021150305, text="Talita", text_color="black", font=("Consolas", 16,"bold")) #Coordenadas del marcador
        self.mapa_1.set_position(19.423090585856134, -99.23947021150305)  # Coordenadas de Ciudad de México
        # self.mapa_1.set_zoom(15)

        self.current_frame = None  # Para almacenar el frame actual

        
        
        # create third frame
        #self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.manual_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent") 
        # self.manual_frame.grid_rowconfigure(2, weight=1)
        # self.manual_frame.grid_columnconfigure(10, weight=1)    
        self.manual_doc = CTkPDFViewer(self.manual_frame,file="Manual.pdf", height=900, width=400, page_separation_height= 2)
        self.manual_doc.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        #self.manual_doc.pack()
        # self.manual_doc.grid(row=2, column=20, padx=10, pady=10, columnspan= 10 , rowspan=6)
        # self.manual_doc.grid_configure(sticky="ew", ipadx=10, ipady= 10)
        

        # self.pdf_viewer = pdf.PDFViewer(self.manual_frame, pdf_location="V3_interfaz\\Manual.pdf", width=500, height=300)
        # self.pdf_viewer.pack(fill="both", expand=True)
        
        
        
        self.salir = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")
        self.image_graph_frame = customtkinter.CTkFrame(self.home_frame, fg_color='transparent')
        #self.image_graph_frame = customtkinter.CTkFrame(self.home_frame)
        self.image_graph_frame.grid(row=2, column=0, columnspan=4, rowspan=9 , padx=20, pady=10, sticky="nsew")
        self.image_graph_frame.grid_rowconfigure(0, weight=1)
        self.image_graph_frame.grid_columnconfigure(0, weight=1)
        self.image_graph_frame.grid_rowconfigure(1, weight=1)
        
       
    
       

    def select_second_frame(self, frame_name):
        if self.current_frame:
            self.current_frame.grid_forget()
        
        if frame_name == "second_frame_1":
            self.second_frame_1.grid(row=2, column=0, columnspan=4, pady=10, sticky="nsew")
            self.current_frame = self.second_frame_1
        elif frame_name == "second_frame_2":
            self.second_frame_2.grid(row=2, column=0, columnspan=4, pady=10, sticky="nsew")
            self.current_frame = self.second_frame_2
        elif frame_name == "second_frame_3":
            self.second_frame_3.grid(row=2, column=0, columnspan=4, pady=10, sticky="nsew")
            self.current_frame = self.second_frame_3
        elif frame_name == "second_frame_4":
            self.second_frame_4.grid(row=2, column=0, columnspan=4, pady=10, sticky="nsew")
            self.current_frame = self.second_frame_4
        elif frame_name == "second_frame_5":
            self.second_frame_5.grid(row=2, column=0, columnspan=4, pady=10, sticky="nsew")
            self.current_frame = self.second_frame_5
       
       
        #--------------------------
        #---------------------------

    
  

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.directorio_button.configure(fg_color=("gray75", "gray25") if name == "Directorio" else "transparent")
        self.manual_button.configure(fg_color=("gray75", "gray25") if name == "Manual" else "transparent")
        self.frame_salir.configure(fg_color=("gray75", "gray25") if name == "Salir" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "Directorio":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "Manual":
            self.manual_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.manual_frame.grid_forget()
        if name == "Salir":
            self.quit
        # else:
        #     self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def directorio_button_event(self):
        self.select_frame_by_name("Directorio")

    def manual_button_event(self):
        self.select_frame_by_name("Manual")
        
   

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.geometry("1025x700")
    app.mainloop()

