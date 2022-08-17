#IMPORTAMOS LIBRERIAS NECESARIAS
from os import terminal_size
from re import split
import tkinter as tk
from tkinter.constants import BOTTOM, END, INSERT, LEFT, RIGHT, TRUE, WORD, X, Y

from tkinter import Frame, Menu, PhotoImage, Scrollbar, font
from PIL import ImageTk, Image
import os
import speech_recognition as sr
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import colorchooser
from pydub import AudioSegment
from pydub.silence import split_on_silence
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
import pyaudio
import wave
from pprint import pprint
import json
from librosa import display
import librosa as librosa
import scipy
import scipy.fftpack as fftpk
import librosa.core as lc 
from mpl_toolkits.axes_grid1 import make_axes_locatable

#Variables globales
global selected,filepath,texto3 #, texto 
selected = False
#Inicio obejecto de reconocimiento
r = sr.Recognizer()
texto=" "
texto2=" "    
def grabar():
    duracion=3
    messagebox.showinfo(message="Tienes"+ str(duracion) + " segundos para tu audio, la grabacion empezara despues de dar clic en aceptar", title="Mensaje")
    FORMAT=pyaudio.paInt16
    CHANNELS=1
    RATE=44100
    CHUNK=1024
    
    archivo="grabacion.wav"
    #INICIAMOS "pyaudio"
    audio=pyaudio.PyAudio ()
    stream=audio.open (format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    #INICIAMOS GRABACIÓN
    print ("grabando...")
    frames=[]
    for i in range (0, int (RATE/CHUNK*duracion)):
        data=stream.read (CHUNK)
        frames. append (data)
    print ("grabación terminada")
    #DETENEMOS GRABACIÓN
    stream.stop_stream ()
    stream.close ()
    audio.terminate ()
    #CREAMOS/GUARDAMOS EL ARCHIVO DE AUDIO
    waveFile = wave.open (archivo, 'wb')
    waveFile.setnchannels (CHANNELS)
    waveFile.setsampwidth (audio.get_sample_size (FORMAT))
    waveFile.setframerate (RATE)
    waveFile.writeframes (b''.join (frames))
    waveFile.close()
    messagebox.showinfo(message="Tu audio ha sido guardado con exito como grabacion.wav , para decodificarlo abrelo con el icono de carpeta", title="Mensaje")

def voz_texto():
    global texto
    sampleRateHertz=44100

    with sr.Microphone() as source:
        print("Habla..-")
        messagebox.showinfo(message="Se empezará a grabar", title="Mensaje")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio_text = r.listen(source)
        print("Tiempo finalizado, gracias")
        
   
        # Usamos la API de Google
        
        
        texto=str(r.recognize_google(audio_text, language = "es-EC"))
        texto=f"{texto.capitalize()}."+" "
        messagebox.showinfo(message="Texto Decodificado", title="Mensaje")
        txt_edit.insert(END, texto);
        print("Google Speech Recognition results:")
        pprint(r.recognize_google(audio_text, language = "es-EC", show_all=True))
   # except:
         #print("Sorry, I did not get that")

def info():
    #GRAFICO ESPECTRO DE SONIDO
    filepath="grabacion.wav"
    samples , sampling_rate=librosa.load (filepath, sr = None, mono = True, offset = 0.0, duration = None)                 
    len(samples), sampling_rate
    duration_of_sound=len(samples)/sampling_rate 
    plt.figure (1)
    plt_0=plt.subplot(311)
    plt.title('Señal Analogica de Audio')
    librosa.display.waveplot (y = samples, sr = sampling_rate)
    plt_0.set_xlabel("Time (seconds) -->")
    plt_0.set_ylabel("Amplitude")
    
    #FFT
    s_rate, signal= wavfile.read(filepath)
    FFT = abs(fftpk.fft(signal))
    freqs = fftpk.fftfreq(len(FFT), (1.0/s_rate))
    plt_1=plt.subplot(312)
    plt.title('FFT de Audio')
    plt_1.plot(freqs[range(len(FFT)//2)], FFT[range(len(FFT)//2)])                                                          
    plt_1.set_xlabel('Frequency (Hz)')
    plt_1.set_ylabel('Amplitude')

    #ESPECTROGRAMA
    plt.subplot(313)
    fs, y_ = wavfile.read(filepath)                # Lee la frecuencia de muestreo del archivo
    fs = fs       
    n_fft = 1024         #FFTLongitud
    y, sr = librosa.load(filepath, sr=fs)
    #Obtener espectrograma de banda ancha
    mag = np.abs(lc.stft(y, n_fft=n_fft, hop_length=10, win_length=40, window='hamming'))                # Realice la transformada de Fourier de corta duración y obtenga la amplitud
    D = librosa.amplitude_to_db(mag, ref=np.max)        #Amplitud convertida a unidad db
    librosa.display.specshow(D, sr=fs, hop_length=10, x_axis='s', y_axis='linear')                          #      
    
    plt.colorbar( format='%+2.0f')
    plt.title('Espectrograma')
    plt.savefig('broader.png')
    #plt.show()

    ventana3(texto3)
    plt.tight_layout()
    plt.show()
      
def file_texto():
    global texto2, filepath, texto3
    
    #abrir archivo
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.wav"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    messagebox.showinfo(message="Decodificando... esto puede tardar unos segundos...", title="Mensaje")
    sonido=AudioSegment.from_wav(filepath)
    #separar aduio cuando haya silencios de 700 ms o mas
    chunks = split_on_silence(sonido,
        # experiment with this value for your target audio file
        min_silence_len = 1000,
        # adjust this per requirement
        silence_thresh = sonido.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=1000,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # ciclo para cortar los audios 
    for i, audio_chunk in enumerate(chunks, start=1):
        # exportar el audio recortado
        # creamos una carpeta para guardar los audios recortados
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")


        with sr.AudioFile(chunk_filename) as source:
            recorded_audio = r.listen(source)
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Recognizing the text")
            texto2 = r.recognize_google(
                    recorded_audio, 
                    language="es-EC"
                )
            
            print("Google Speech Recognition results:")
            pprint(r.recognize_google(recorded_audio, language = "es-EC", show_all=True))
            texto3=r.recognize_google(recorded_audio, language = "es-EC", show_all=True)

            texto2=f"{texto2.capitalize()}."
            whole_text += texto2 + " "
    messagebox.showinfo(message="Texto Decodificado", title="Mensaje")
    txt_edit.insert(END, whole_text);

def open_file():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete(1.0, tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"PROYECTO COMUNICACIÓN DIGITAL - {filepath}")

def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_edit.get(1.0, tk.END)
        output_file.write(text)
    window.title(f"Text Editor Application - {filepath}")

def nuevo():
    txt_edit.delete("1.0", END)
    
def inser_texto():
    txt_edit=Text(texto)
    print (texto)

def cortar(e):
    global selected
    if e:
        selected = window.clipboard_get()
    else:
        if txt_edit.selection_get():
            selected = txt_edit.selection_get()
            txt_edit.delete("sel.first", "sel.last")
            #limpiar el portapales para nuvamente usar
            window.clipboard_clear()
            window.clipboard_append(selected)

def copiar(e):
    global selected
    #reviso si se ha usado los shortcuts
    if e:
        selected = window.clipboard_get()

    if txt_edit.selection_get():
        selected = txt_edit.selection_get()
        #limpiar el portapales para nuvamente usar
        window.clipboard_clear()
        window.clipboard_append(selected)

def pegar(e):
    global selected
    #reviso si se ha usado los shortcuts
    if e:
        selected = window.clipboard_get()
    else:
        if selected:
            position = txt_edit.index(INSERT)
            txt_edit.insert(position, selected)

def negrita():
    bold_font=font.Font(txt_edit, txt_edit.cget("font"))
    bold_font.configure(weight="bold")

    txt_edit.tag_configure("bold", font=bold_font)

    current_tags = txt_edit.tag_names("sel.first")

    if "bold" in current_tags:
        txt_edit.tag_remove("bold", "sel.first", "sel.last")
    else: 
        txt_edit.tag_add("bold","sel.first", "sel.last" )

def italica():
    italics_font=font.Font(txt_edit, txt_edit.cget("font"))
    italics_font.configure(slant="italic")

    txt_edit.tag_configure("italic", font=italics_font)

    current_tags = txt_edit.tag_names("sel.first")

    if "italic" in current_tags:
        txt_edit.tag_remove("italic", "sel.first", "sel.last")
    else: 
        txt_edit.tag_add("italic","sel.first", "sel.last" )

def deshacer():
    pass

def rehacer():
    pass

def txt_color():
    my_color=colorchooser.askcolor()[1]

    if my_color:

        color_font=font.Font(txt_edit, txt_edit.cget("font"))
    

        txt_edit.tag_configure("colored", font=color_font, foreground=my_color)

        current_tags = txt_edit.tag_names("sel.first")

        if "italic" in current_tags:
            txt_edit.tag_remove("colored", "sel.first", "sel.last")
        else: 
            txt_edit.tag_add("colored","sel.first", "sel.last" )

def bg_color():
    my_color=colorchooser.askcolor()[1]

    if my_color:
        txt_edit.config(background=my_color)

def todo_txt():
    my_color=colorchooser.askcolor()[1]

    if my_color:
        txt_edit.config(foreground=my_color)

def txt_centrar():
    
    txt_edit.tag_configure("center", justify="center")

    current_tags1 = txt_edit.tag_names("sel.first")

    if "center" in current_tags1:
        txt_edit.tag_remove("center", "sel.first", "sel.last")
    else: 
        txt_edit.tag_add("center","sel.first", "sel.last" )

def txt_izquierda():
    
    txt_edit.tag_configure("left", justify="left")

    current_tags2 = txt_edit.tag_names("sel.first")

    if "left" in current_tags2:
        txt_edit.tag_remove("left", "sel.first", "sel.last")
    else: 
        txt_edit.tag_add("left","sel.first", "sel.last" )

def txt_derecha():
    
    txt_edit.tag_configure("right", justify="right")

    current_tags3 = txt_edit.tag_names("sel.first")

    if "right" in current_tags3:
        txt_edit.tag_remove("right", "sel.first", "sel.last")
    else: 
        txt_edit.tag_add("right","sel.first", "sel.last" )
   

#def prueba_color():
    
    #txt_edit.configure(foreground="red")

def ventana2():
    newWindow = tk.Toplevel(window) 
    newWindow.geometry("400x400+400+100")
    newWindow.title('Información') 
    #información
    btn_neg = tk.Button(newWindow, image=imagen_uta, command=negrita)
    label_1 = tk.Label(newWindow,text="Proyecto de Comunicación Digital")
    label_2 = tk.Label(newWindow,text="Editor de Texto - Voz a texto")
    label_3 = tk.Label(newWindow,text="Integrantes:")
    label_4 = tk.Label(newWindow,text="Gavilanez Wendy")
    label_5 = tk.Label(newWindow,text="Lema John")
    label_6 = tk.Label(newWindow,text="Sanchez Francis")
    label_7 = tk.Label(newWindow,text="Alexis Veloz")

    label_1.config(font=("Verdana",16))
    label_2.config(font=("Verdana",15))
    label_3.config(font=("Verdana",14))
    label_4.config(font=("Verdana",13))
    label_5.config(font=("Verdana",13))
    label_6.config(font=("Verdana",13))
    label_7.config(font=("Verdana",13))


    btn_neg.pack()
    label_1.pack()
    label_2.pack()
    label_3.pack()
    label_4.pack()
    label_5.pack()
    label_6.pack()
    label_7.pack()

def ventana3(texto3):
    
    result = json.dumps(texto3, ensure_ascii=False)
    result1=result[17:len(result)]
    result2=result1.replace(',','\n')
    result2=result2.replace('transcript','transcripción')
    
    longitud=len(result2[1])
    print(longitud)
    newWindow = tk.Toplevel(window) 
    newWindow.geometry("400x400+400+100")
    newWindow.title('Información') 
    #información
    label_1 = tk.Label(newWindow,text="Posibles Resultados")
    label_2 = tk.Label(newWindow,text=result2,wraplength=400, justify=LEFT)
    label_1.config(font=("Verdana",13))
    label_2.config(font=("Verdana",10))
    label_1.pack()    
    label_2.pack()

########################################################
# Configuración de GUI
########################################################
window = tk.Tk()
window.title("Proyecto Comunicaciones Digitales")
window.geometry("1000x600+150+20")
window.resizable(False, False)
mi_menu=Menu(window)
window.config(menu=mi_menu)
window.rowconfigure(0, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

frame_scroll=Frame(window)
frame_hscroll=Frame(window)

txt_scroll = Scrollbar(frame_scroll)
txt_scroll.pack(side=RIGHT, fill=Y)

hor_scroll = Scrollbar(frame_hscroll, orient='horizontal')
hor_scroll.pack(side=BOTTOM, fill=X)

#Menu archivos
file_menu = tk.Menu(mi_menu, tearoff=False)
mi_menu.add_cascade(label="Archivo", menu=file_menu)
file_menu.add_command(label="Nuevo", command=nuevo)
file_menu.add_command(label="Abrir", command=open_file)
file_menu.add_command(label="Guardar", command=save_file)

#Menu edicion
edit_menu = tk.Menu(mi_menu, tearoff=False)
mi_menu.add_cascade(label="Editar", menu=edit_menu)
edit_menu.add_command(label="Cortar", command= lambda: cortar(False), accelerator="(Ctrl+X)")
edit_menu.add_command(label="Copiar", command=lambda: copiar(False), accelerator="(Ctrl+Y)")
edit_menu.add_command(label="Pegar", command=lambda: pegar(False), accelerator="(Ctrl+Z)")
#edit_menu.add_separator()
#edit_menu.add_command(label="Deshacer", command=lambda: deshacer(False), accelerator="(Ctrl+Z)")
#edit_menu.add_command(label="Rehacer", command=lambda: rehacer(False), accelerator="(Ctrl+Y)")

#Menu colores
edit_colors = tk.Menu(mi_menu, tearoff=False)
mi_menu.add_cascade(label="Colores", menu=edit_colors)
edit_colors.add_command(label="Texto Seleccionado", command= txt_color)
edit_colors.add_command(label="Todo el texto ", command=todo_txt)
edit_colors.add_command(label="Fondo", command=bg_color)



#Menu info
mas_menu = tk.Menu(mi_menu, tearoff=False)
mi_menu.add_cascade(label="Más", menu=mas_menu)
mas_menu.add_command(label="Sobre el programa", command= ventana2)

#shortcuts para pegar, copiar y cortar
window.bind('<Control-Key-x>', cortar)
window.bind('<Control-Key-c>', copiar)
window.bind('<Control-Key-v>', pegar)
window.bind('<Control-Key-g>', voz_texto)

#imagenes
fisei=PhotoImage(file=r"C:\Users\HP\Documents\7\Digitales\Voz2texto\fisei.gif")
grabar2=PhotoImage(file=r"C:\Users\HP\Documents\7\Digitales\Voz2texto\micro2.gif")
cargar=PhotoImage(file=r"C:\Users\HP\Documents\7\Digitales\Voz2texto\cargar.gif")
izquierda=PhotoImage(file=r"C:\Users\HP\Documents\7\Digitales\Voz2texto\izqu.gif")
derecha=PhotoImage(file=r"C:\Users\HP\Documents\7\Digitales\Voz2texto\der.gif")
centrar=PhotoImage(file=r"C:\Users\HP\Documents\7\Digitales\Voz2texto\cent.gif")
cursiva=PhotoImage(file=r"C:\Users\HP\Documents\7\Digitales\Voz2texto\cur.gif")
negrita2=PhotoImage(file=r"C:\Users\HP\Documents\7\Digitales\Voz2texto\negr.gif")
colores=PhotoImage(file=r"C:\Users\HP\Documents\7\Digitales\Voz2texto\color.gif")
imagen_uta = PhotoImage(file=r"C:\Users\HP\Documents\7\Digitales\Voz2texto\uta.gif")
record = PhotoImage(file=r"C:\Users\HP\Documents\7\Digitales\Voz2texto\record.gif")
info2 = PhotoImage(file=r"C:\Users\HP\Documents\7\Digitales\Voz2texto\info.gif")

txt_edit = tk.Text(window, font=("Helvetica", 14), undo=True,  yscrollcommand=txt_scroll.set, xscrollcommand=hor_scroll.set,  wrap=WORD)

txt_scroll.config(command=txt_edit.yview) 
hor_scroll.config(command=txt_edit.xview) 
#frame para botones
fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=3)
fr_edit = tk.Frame(window, relief=tk.RAISED, bd=3)
#botones grabar,guardar y abrir
btn_grabar = tk.Button(fr_buttons, image=grabar2, command=voz_texto)
btn_cargar = tk.Button(fr_buttons, image=cargar, command=file_texto)
btn_imagen = tk.Button(fr_buttons, image=fisei, command=ventana2)
btn_micro = tk.Button(fr_buttons, image=record, command=grabar)
btn_info = tk.Button(fr_buttons, image=info2, command=info)
#btn_open = tk.Button(fr_buttons, text="Open", command=open_file)
#btn_save = tk.Button(fr_buttons, text="Save As...", command=save_file)

#frame para botones de edición y color

btn_neg = tk.Button(fr_edit, image=negrita2, command=negrita)
btn_neg.grid(row=0, column=2, sticky="ew", padx=5, pady=5)

btn_curs = tk.Button(fr_edit, image=cursiva, command=italica)
btn_curs.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

#color
btn_color = tk.Button(fr_edit, image=colores, command=txt_color)
btn_color.grid(row=0, column=4, sticky="ew", padx=5, pady=5)

#izquierda
btn_izquierda = tk.Button(fr_edit, image=izquierda, command=txt_izquierda)
btn_izquierda.grid(row=0, column=6, sticky="ew", padx=5, pady=5)

#centrar
btn_centrar = tk.Button(fr_edit, image=centrar, command=txt_centrar)
btn_centrar.grid(row=0, column=5, sticky="ew", padx=5, pady=5)

#derecha
btn_derecha = tk.Button(fr_edit, image=derecha, command=txt_derecha)
btn_derecha.grid(row=0, column=7, sticky="ew", padx=5, pady=5)

#botones para grabar, guardar y abrir
btn_imagen.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_grabar.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
btn_cargar.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
btn_micro.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
btn_info.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
#btn_open.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
#btn_save.grid(row=2, column=0, sticky="ew", padx=5)

fr_buttons.grid(row=1, column=0, sticky="ns")
fr_edit.grid(row=0, column=1, sticky="nwne")
txt_edit.grid(row=1, column=1, sticky="nsew")
frame_scroll.grid(row=1, column=2, sticky="ns")
frame_hscroll.grid(row=2, column=1, sticky="swse")
######################################################
# listening the speech and store in audio_text variable

window.mainloop()
