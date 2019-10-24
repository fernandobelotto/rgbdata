# Esse programa importa um vídeo qualquer e exporta os valores médios de rgb para cada frame de uma seleção de interesse

# Por: Fernando Bosco

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import xlsxwriter
from tkinter import filedialog
import os
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from PIL import Image
from PIL import ImageTk
from threading import Thread
from scipy import stats


def analise():
    statuslabel.config(text='Status:', background='', foreground='')
    if metodo.get() == 0:
        statuslabel.config(text='Status: Select a method first!', background='#E32B2F', foreground='white')
    if metodo.get() == 1:
        selecionar_area()
        thread.start()
    if metodo.get() == 2:
        selecionar_area()
        thread2.start()
    if metodo.get() == 3:
        selecionar_area()
        thread3.start()
    if metodo.get() == 4:
        selecionar_area()
        thread4.start()
    if metodo.get() == 5:
        selecionar_area()
        thread5.start()

#Função que abre e lê o arquivo de vídeo do usuário
def abrir_video():
    # show an "Open" dialog box and return the path to the selected file
    statuslabel.config(text='Status:', background='', foreground='')
    filename = askopenfilename()
    global nome_arquivo
    nome_arquivo = os.path.basename(filename)
    arquivo.config(text='File: {}'.format(os.path.basename(filename)))
    global vd
    vd = cv2.VideoCapture(filename)
    # pega o número de frames no vídeo
    global tamanho
    tamanho = vd.get(7)

    global lista_dos_frames
    lista_dos_frames = range(int(tamanho)-1)

    global lista_dos_segundos
    lista_dos_segundos = []
    for i in lista_dos_frames:
        lista_dos_segundos.append(i / (vd.get(cv2.CAP_PROP_FPS)))

    print(vd.get(3))
    print(vd.get(4))

#função que abre a janela de analise
def analisar():

    root3 = tk.Toplevel(root)
    root3.title('Select analysis properties')


    #cria um botão para o usuario selecionar o frame
    bttn2 = ttk.Button(root3, text='FRAME SELECTION', command=mostrar_frame).pack(side='top', pady=5, padx=25, fill='x')

    # seleciona o médoto de análise, seja por média ou valor máximo na área
    global metodo
    metodo = tk.IntVar()
    ttk.Radiobutton(root3, text='Average', variable=metodo, value=1).pack(anchor='w', padx=25)
    ttk.Radiobutton(root3, text='Maximum', variable=metodo, value=2).pack(anchor='w', padx=25)
    ttk.Radiobutton(root3, text='Standard deviation', variable=metodo, value=3).pack(anchor='w', padx=25)
    ttk.Radiobutton(root3, text='Median', variable=metodo, value=4).pack(anchor='w', padx=25)
    ttk.Radiobutton(root3, text='Mode', variable=metodo, value=5).pack(anchor='w', padx=25)

    bttn3 = ttk.Button(root3, text='SELECT AREA', command=analise).pack(side='top', pady=5, fill='x', padx=25)
    bttn2 = ttk.Button(root3, text='FULL FRAME ANALYSIS', command=vai_fullframe).pack(side='top', pady=5, padx=25, fill='x')
    # mostra os gráficos da análise
    bttn6 = ttk.Button(root3, text='SHOW PLOT', command=mostrar_graficos).pack(side='top', pady=5, fill='x', padx=25)

#essa função mostra o frame e permite selecioná-lô
def mostrar_frame():

    try:
        root2 = tk.Toplevel(root)
        root2.title('Select the frame of interest')
        # root2.iconbitmap('icone.ico')
        imageFrame = tk.Frame(root2)
        imageFrame.pack()
        lmain = tk.Label(imageFrame)
        lmain.pack(padx=20, pady=20)

        global selec_var_x
        selec_var_x = tk.IntVar()

        global selec_var_y
        selec_var_y = tk.DoubleVar()
        selec_var_y.set('0.5')

        def mostrar_frame_selecionado():
            vd.set(1, selec_var_x.get())
            global frame_select
            _, frame_select = vd.read()
            if vd.get(3) >= 1920.0 and vd.get(4) >= 1080.0:
                frame_select = cv2.resize(frame_select, None, fx=selec_var_y.get(), fy=selec_var_y.get())
            cv2image = cv2.cvtColor(frame_select, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10, mostrar_frame_selecionado)
        try:
            mostrar_frame_selecionado()
        except ValueError:
            statuslabel.config(text='Status: Open a video first!', background='red')

        def fechar_janela():
            root2.destroy()

        slider1 = ttk.Scale(root2, variable=selec_var_x, from_=0, to=(vd.get(7) - 1), length=(np.shape(frame_select)[1]))
        slider1.pack()

        confirmar = ttk.Button(root2, command=fechar_janela, text='CONFIRM FRAME')
        confirmar.pack(pady=10)
        # variavel_ate = (root.winfo_screenwidth()/2)/(vd.get(3))
        # slider2 = ttk.Scale(root2, variable=selec_var_y, from_=0.5, to=variavel_ate, length=200)
        # slider2.pack()

    except NameError:
        statuslabel.config(text='Status: Open a video first!', background='red')

# essa função recebe um vídeo como parâmetro e retorna 3 listas com as médias de rgb

def vai_fullframe():
    thread6.start()

def fullframe():
    #lê o primeiro frame do vídeo

    global qw_list
    qw_list = [1]
    global analises
    analises = []
    vd.set(1, 1)
    cv2.destroyAllWindows()
    # cria uma lista para guardar as médias de rgb
    med_red = []
    med_blue = []
    med_green = []

    # loop por cada frame, corta a área de interesse, separa os valores de r g b, tira a média deles e adiciona as listas
    i=1
    while i!=tamanho:
        ret, frame1 = vd.read()
        g, b, r = cv2.split(frame1)
        med_red.append(np.average(r))
        med_blue.append(np.average(g))
        med_green.append(np.average(b))
        i = i + 1

    medias = [med_red, med_green, med_blue]
    analises.append(medias)

    statuslabel.config(text='Status: Finished!', background ='#0FAF98', foreground='white')


def average():
    #lê o primeiro frame do vídeo
    try:
        global analises
        analises = []
        for qw in qw_list:
            print(qw)
            vd.set(1, 1)
            cv2.destroyAllWindows()
            # cria uma lista para guardar as médias de rgb
            med_red = []
            med_blue = []
            med_green = []

            # loop por cada frame, corta a área de interesse, separa os valores de r g b, tira a média deles e adiciona as listas
            i=1
            while i!=tamanho:
                ret, frame1 = vd.read()
                ROI = frame1[int(qw[1]):int(qw[1] + qw[3]), int(qw[1]):int(qw[1] + qw[2])]
                g, b, r = cv2.split(ROI)
                med_red.append(np.average(r))
                med_blue.append(np.average(g))
                med_green.append(np.average(b))
                i = i + 1
                p.step(100/tamanho/len(qw_list))
            medias = [med_red, med_green, med_blue]
            analises.append(medias)

        statuslabel.config(text='Status: Finished!', background ='#0FAF98', foreground='white')

    except NameError:
        statuslabel.config(text='Status: Select a frame first!', background='#E32B2F', foreground='white')

def maximum():
    #lê o primeiro frame do vídeo
    try:
        global analises
        analises = []
        for qw in qw_list:
            print(qw)
            # lê o primeiro frame do vídeo
            # ret, frame1 = vd.read()
            vd.set(1, 1)
            cv2.destroyAllWindows()
            # cria uma lista para guardar as médias de rgb
            max_red = []
            max_blue = []
            max_green = []

            # loop por cada frame, corta a área de interesse, separa os valores de r g b, tira a média deles e adiciona as listas
            i=1
            while i!=tamanho:
                ret, frame1 = vd.read()
                ROI = frame1[int(qw[1]):int(qw[1] + qw[3]), int(qw[1]):int(qw[1] + qw[2])]
                g, b, r = cv2.split(ROI)
                max_red.append(np.max(r))
                max_blue.append(np.max(g))
                max_green.append(np.max(b))
                i = i + 1

            maximos = [max_red, max_green, max_blue]
            analises.append(maximos)
        print(len(analises))

        statuslabel.config(text='Status: Finished!', background ='#0FAF98', foreground='white')

    except NameError:

        statuslabel.config(text='Status: Select a frame first!', background='#E32B2F', foreground='white')

    return
def deviation():
    #lê o primeiro frame do vídeo
    try:
        global analises
        analises = []
        for qw in qw_list:
            print(qw)
            # lê o primeiro frame do vídeo
            # ret, frame1 = vd.read()
            vd.set(1, 1)
            cv2.destroyAllWindows()
            # cria uma lista para guardar as médias de rgb
            max_red = []
            max_blue = []
            max_green = []

            # loop por cada frame, corta a área de interesse, separa os valores de r g b, tira a média deles e adiciona as listas
            i=1
            while i!=tamanho:
                ret, frame1 = vd.read()
                ROI = frame1[int(qw[1]):int(qw[1] + qw[3]), int(qw[1]):int(qw[1] + qw[2])]
                g, b, r = cv2.split(ROI)
                max_red.append(np.std(r))
                max_blue.append(np.std(g))
                max_green.append(np.std(b))
                i = i + 1

            maximos = [max_red, max_green, max_blue]
            analises.append(maximos)
        print(len(analises))

        statuslabel.config(text='Status: Finished!', background ='#0FAF98', foreground='white')

    except NameError:

        statuslabel.config(text='Status: Select a frame first!', background='#E32B2F', foreground='white')
def median():
    #lê o primeiro frame do vídeo
    try:
        global analises
        analises = []
        for qw in qw_list:
            print(qw)
            # lê o primeiro frame do vídeo
            # ret, frame1 = vd.read()
            vd.set(1, 1)
            cv2.destroyAllWindows()
            # cria uma lista para guardar as médias de rgb
            max_red = []
            max_blue = []
            max_green = []

            # loop por cada frame, corta a área de interesse, separa os valores de r g b, tira a média deles e adiciona as listas
            i=1
            while i!=tamanho:
                ret, frame1 = vd.read()
                ROI = frame1[int(qw[1]):int(qw[1] + qw[3]), int(qw[1]):int(qw[1] + qw[2])]
                g, b, r = cv2.split(ROI)
                max_red.append(np.median(r))
                max_blue.append(np.median(g))
                max_green.append(np.median(b))
                i = i + 1

            maximos = [max_red, max_green, max_blue]
            analises.append(maximos)
        print(len(analises))

        statuslabel.config(text='Status: Finished!', background ='#0FAF98', foreground='white')

    except NameError:

        statuslabel.config(text='Status: Select a frame first!', background='#E32B2F', foreground='white')
def mode():
    #lê o primeiro frame do vídeo
    try:
        global analises
        analises = []
        for qw in qw_list:
            print(qw)
            # lê o primeiro frame do vídeo
            # ret, frame1 = vd.read()
            vd.set(1, 1)
            cv2.destroyAllWindows()
            # cria uma lista para guardar as médias de rgb
            max_red = []
            max_blue = []
            max_green = []

            # loop por cada frame, corta a área de interesse, separa os valores de r g b, tira a média deles e adiciona as listas
            i=1
            while i!=tamanho:
                ret, frame1 = vd.read()
                ROI = frame1[int(qw[1]):int(qw[1] + qw[3]), int(qw[1]):int(qw[1] + qw[2])]
                g, b, r = cv2.split(ROI)
                max_red.append(stats.mode(r))
                print(str(stats.mode(r)))
                max_blue.append(stats.mode(g))
                max_green.append(stats.mode(b))
                i = i + 1

            maximos = [max_red, max_green, max_blue]
            analises.append(maximos)
        print(len(analises))

        statuslabel.config(text='Status: Finished!', background ='#0FAF98', foreground='white')

    except NameError:

        statuslabel.config(text='Status: Select a frame first!', background='#E32B2F', foreground='white')

def selecao_precisa():
    root10 = tk.Toplevel(root)
    root10.title('Precision selection')
    root10.geometry("300x600+900+200")
    global e
    e = tk.Entry(root10)
    a = tk.Label(root10, text='Altura').grid()
    e.grid(row=1)
def selecionar_area():

    root3 = tk.Toplevel(root)
    root3.title('Select the frame of interest')

    selecao_precisa()

    # root2.iconbitmap('icone.ico')
    imageFrame = tk.Frame(root3)
    imageFrame.pack()
    lmain = tk.Label(imageFrame)
    lmain.pack()


    # _, frame_select = vd.read()
    print(np.shape(frame_select))
    cv2image = cv2.cvtColor(frame_select, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk

    print(imgtk.height())
    print(imgtk.width())

    global qw_list
    qw_list = []
    def start_ret(event):
        global a, b
        a = event.x
        b = event.y
        global meu
        meu = canv.create_rectangle(event.x, event.y, event.x, event.y, fill=[], outline='green2', width=2, tag='go')
        qw_list.append(canv.coords(meu))
        print(qw_list)


    # essa função permite o redimensionamento do retangulo criado na função start_ret
    def mov_ret(event):
        canv.coords(meu, a, b, event.x, event.y)
        e.insert(0, str(canv.coords(meu)))

    # implementa uma linha pontilhada para target do cursor
    def linhas_pontilhadas(event):
        global x, y
        kill_xy()
        dashes = [2, 2]
        x = canv.create_line(event.x, 0, event.x, 1000, dash=dashes, tags='no')
        y = canv.create_line(0, event.y, 1000, event.y, dash=dashes, tags='no')

    def kill_xy(event=None):  # essa função evita das linhas ficarem no gui, não apague ela
        canv.delete('no')

    def limpar():
        canv.delete("go")
        qw_list.clear()

    # tamanho_frame_x = np.shape(frame_select)[0]
    # tamanho_frame_y = np.shape(frame_select)[1]

    canv = tk.Canvas(root3, width=np.shape(frame_select)[1] , height=np.shape(frame_select)[0])
    canv.config(bd=4, highlightbackground='black')

    canv.create_image(imgtk.width()/2,imgtk.height()/2, image=imgtk)



    canv.bind('<Motion>', linhas_pontilhadas)
    canv.bind('<Button-1>', start_ret)

    # canv.bind('<Button-1>', insere_img)
    canv.bind('<B1-Motion>', mov_ret)
    canv.pack()

    meu_botao = ttk.Button(root3, text="Clear All", command=limpar).pack(anchor='center', side='left')

    var = tk.IntVar()
    button = ttk.Button(root3, text="Finish Selection", command=lambda: var.set(1))
    button.pack(side='right')
    button.wait_variable(var)

    global p
    p = ttk.Progressbar(root, mode='determinate', maximum=100, length=190)
    p.pack(pady=10)


#essa funçao recebe uma lista de 3 elementos contendo os dados de r, g e b da análise
# e plota
def plot_analysis(rgb, type):
    # Cria uma janela nova para colocar os gráficos
    root2 = tk.Tk()
    root2.title('CVA')
    # root2.iconbitmap('icone.ico')

    # cria as abas para colocar os vários tipos de gráficos
    notebook = ttk.Notebook(root2)
    notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    frame1 = ttk.Frame(notebook)
    frame2 = ttk.Frame(notebook)
    frame3 = ttk.Frame(notebook)
    frame4 = ttk.Frame(notebook)
    notebook.add(frame1, text='RGB')
    notebook.add(frame2, text='RED')
    notebook.add(frame3, text='GREEN')
    notebook.add(frame4, text='BLUE')

    # trasforma as listas com as médias em numpy arrays para plot

    med_red = rgb[0]
    med_green = rgb[1]
    med_blue = rgb[2]

    #cria uma figura com 3 gráficos (rgb) em pilhaR
    fig, ax = plt.subplots(3, 1, sharex=True, sharey=True)
    ax[0].plot(lista_dos_segundos, med_red, color='red')
    ax[1].plot(lista_dos_segundos, med_green, color='green')
    ax[2].plot(lista_dos_segundos, med_blue, color='blue')
    #coloca os título dos eixos
    fig.text(0.5, 0.04, 'SECONDS', ha='center')
    fig.text(0.04, 0.5, '{} OF PIXELS VALUE'.format(str(type)), va='center', rotation='vertical')
    # Adiciona o gráfico criado a janela to tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame1)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, frame1)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    # Cria o gráfico para RED
    fig, ax = plt.subplots()
    ax.plot(lista_dos_segundos, med_red, color='red')
    #coloca os título dos eixos
    fig.text(0.5, 0.04, 'SECONDS', ha='center')
    fig.text(0.04, 0.5, '{} OF PIXELS VALUE'.format(str(type)), va='center', rotation='vertical')
    # Adiciona o gráfico criado a janela to tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame2)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, frame2)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Cria o gráfico para GREEN
    fig, ax = plt.subplots()
    ax.plot(lista_dos_segundos, med_green, color='green')
    #coloca os título dos eixos
    fig.text(0.5, 0.04, 'SECONDS', ha='center')
    fig.text(0.04, 0.5, '{} OF PIXELS VALUE'.format(str(type)), va='center', rotation='vertical')
    # Adiciona o gráfico criado a janela to tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame3)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, frame3)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Cria o gráfico para Blue
    fig, ax = plt.subplots()
    ax.plot(lista_dos_segundos, med_blue, color='blue')
    #coloca os título dos eixos
    fig.text(0.5, 0.04, 'SECONDS', ha='center')
    fig.text(0.04, 0.5, '{} OF PIXELS VALUE'.format(str(type)), va='center', rotation='vertical')
    # Adiciona o gráfico criado a janela to tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame4)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, frame4)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
#escolhe o tipo de gráfico com base no type
def mostrar_graficos():

    if metodo.get() == 1:
        for l,n in enumerate(qw_list):
            plot_analysis(analises[l], 'AVERAGE')
            l = l + 1
    if metodo.get() == 2:
        for l,n in enumerate(qw_list):
            plot_analysis(analises[l], 'MAXIMUM')
            l = l + 1
    if metodo.get() == 3:
        for l,n in enumerate(qw_list):
            plot_analysis(analises[l], 'STARDAND DEVIATION')
            l = l + 1
    if metodo.get() == 4:
        for l,n in enumerate(qw_list):
            plot_analysis(analises[l], 'MEDIAN')
            l = l + 1
    if metodo.get() == 5:
        for l,n in enumerate(qw_list):
            plot_analysis(analises[l], 'MODE')
            l = l + 1





#escreve os dados para um excel
def escrita_excel(rgb):
    # transforma todos os numpy arrays em arrays normal do python

    salvar_arquivo = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[("Excel File", '*.xlsx')])

    med_green = rgb[1]
    med_blue = rgb[2]
    med_red = rgb[0]
    x = range(len(med_red))

    # Cria um arquivo xlsx, cria uma worksheet(planilha) e cria uma formação bold para ser usada depois
    workbook = xlsxwriter.Workbook(salvar_arquivo)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})

    # escreve o cabeçalho na primeira linha da worksheet
    worksheet.write('A1', 'Segundos', bold)
    worksheet.write('B1', 'Frame', bold)
    worksheet.write('C1', 'Red', bold)
    worksheet.write('D1', 'Green', bold)
    worksheet.write('E1', 'Blue', bold)


    # loopa pelos valores escrevendo eles na planilha
    linha = 1
    coluna = 0
    for i in lista_dos_segundos:
        worksheet.write(linha, coluna, i)
        linha += 1

    linha = 1
    coluna = 0
    for i in x:
        worksheet.write(linha, coluna+1, i)
        linha += 1

    linha = 1
    coluna = 0
    for i in med_red:
        worksheet.write(linha, coluna+2, i)
        linha += 1

    linha = 1
    coluna = 0
    for i in med_green:
        worksheet.write(linha, coluna+3, i)
        linha += 1

    linha = 1
    coluna = 0
    for i in med_blue:
        worksheet.write(linha, coluna+4, i)
        linha += 1


    workbook.close()
    statuslabel.config(text='Status: Saved!',background='#007E99', foreground='white')
#escreve os dados para um csv
def escrita_csv(rgb):

    salvar_arquivo = filedialog.asksaveasfilename(defaultextension='.csv',filetypes=[("Comma Separated Values", '*.csv')])

    arquivo = open(salvar_arquivo, mode='w')
    arquivo.write('segundos, frame, red, green, blue\n')

    med_red = rgb[0]
    med_green = rgb[1]
    med_blue = rgb[2]

    i = 0
    for i in range(int(tamanho-1)):
        arquivo.write(str(lista_dos_segundos[i])+','+str(i)+','+str(med_red[i]) +',' + str(med_green[i]) +','+ str(med_blue[i])+'\n')
        i = i + 1

    arquivo.close()
    statuslabel.config(text='Status: Saved!', background='#007E99', foreground='white')
#função que faz a exportação com base na escolha do usuário
def exportar():


    if excel.get() == 1:
        i=0
        while i < len(analises):
            escrita_excel(analises[i])
            i = i + 1

    if CSV.get() == 1:
        k = 0
        while k < len(analises):
            escrita_csv(analises[k])
            k = k + 1


    if CSV.get() ==0 and excel.get() == 0:
        statuslabel.config(text='Status: Select a option first', background='', foreground='')


#cria uma gui simples para usuário interagir
root = tk.Tk()
root.title('CVA') #define o título da janela
# root.iconbitmap('icone.ico') #define o icone da janela

# cria uma label explicando o programa
# imagem = Image.open('logo2.png')
# imgtk = ImageTk.PhotoImage(imagem)
# label1 = tk.ttk.Label(root, image=imgtk)
# label1.pack(pady=10, padx=20, anchor='w', side='left')
# label1.image = imgtk

#define os estilos para o programa
fontsizeglobal = 16
style = ttk.Style()
style.configure("TButton", font=('Segoe UI', fontsizeglobal))
style.configure("TLabel", font=('Segoe UI', fontsizeglobal))
style.configure("TRadiobutton", font=('Segoe UI', fontsizeglobal))
style.configure("TCheckbutton", font=('Segoe UI', fontsizeglobal))

#cria uma label para mostrar o nome do arquivo
filename = ''
arquivo = tk.ttk.Label(root, text='File: {}'.format(filename), anchor='w')
arquivo.pack(fill='x', padx=20)
# criar uma label para mostrar o status da analise
status = ''
statuslabel = ttk.Label(root, text='Status: {}'.format(status), anchor='w')
statuslabel.pack(pady=5, padx=20, fill='x')


#cria os 3 botões do programa, 'abrir', 'analisar' e 'salvar'
bttn1 = ttk.Button(root,text='OPEN VIDEO', command=abrir_video).pack(padx=25, pady =5 ,side='top', fill='x')
bttn1 = ttk.Button(root,text='ANALYSIS', command=analisar).pack(padx=25, pady =5 ,side='top', fill='x')
# bttn2 = ttk.Button(root,text='New roi selection', command=selecionar_area).pack(side='top', pady =5, padx=25, fill='x')

# Cria uma label mostrando o status da análise


#escolha do método de export
excel = tk.IntVar()
CSV = tk.IntVar()
ttk.Checkbutton(root,text='Excel', variable=excel, onvalue=1, offvalue=0).pack(anchor='w', padx=25)
ttk.Checkbutton(root,text='CSV', variable=CSV, onvalue=1, offvalue=0).pack(anchor='w', padx=25)


bttn8 = ttk.Button(root,text='EXPORT DATA', command=exportar, style="TButton")
bttn8.pack(side='top',pady =5, padx=25, fill='x')

thread = Thread(target=average)
thread2 = Thread(target=maximum)
thread3 = Thread(target=deviation)
thread4 = Thread(target=median)
thread5 = Thread(target=mode)
thread6 = Thread(target=fullframe)


thread.setDaemon(True)
thread2.setDaemon(True)
thread3.setDaemon(True)
thread4.setDaemon(True)
thread5.setDaemon(True)
thread6.setDaemon(True)


#descubra o nome para usar no styling!


if __name__ == '__main__':
    root.mainloop()