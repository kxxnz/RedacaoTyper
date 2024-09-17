import tkinter as tk
import keyboard
import time
import threading
import webbrowser
from PIL import Image, ImageTk
from tkinter import filedialog, simpledialog, messagebox

# Variável global para controlar a execução da digitação
typing_active = False
custom_start_shortcut = 'ctrl+shift+s'  # Atalho padrão para iniciar
custom_stop_shortcut = 'ctrl+shift+p'   # Atalho padrão para parar

def start_typing():
    global typing_active
    text = entry.get()
    if not text:
        return
    
    entry.config(state="disabled")  # Bloqueia o campo de entrada
    progress_label.config(text="Digitando...")  # Feedback visual

    time.sleep(2)  # Delay de 2 segundos antes de começar a digitar
    typing_active = True

    try:
        speed = float(speed_entry.get())  # Obtém o valor do campo de entrada
        if speed < 0.01 or speed > 1:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "A velocidade deve estar entre 0.01 e 1.")
        entry.config(state="normal")
        progress_label.config(text="")
        return

    for char in text:
        if not typing_active:
            break
        keyboard.write(char)
        time.sleep(speed)  # Ajusta a velocidade da digitação

    entry.config(state="normal")  # Reativa o campo de entrada
    progress_label.config(text="")  # Remove o feedback visual

def on_click_start():
    threading.Thread(target=start_typing).start()

def stop_typing():
    global typing_active
    typing_active = False  # Para a execução da digitação
    entry.config(state="normal")
    progress_label.config(text="")  # Remove o feedback visual

def open_link():
    webbrowser.open("https://chatgpt.com")

def open_instagram(event):
    webbrowser.open("https://www.instagram.com/joaowrlld/")

# Função para carregar e redimensionar a imagem
def load_icon(path, size):
    img = Image.open(path)
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

# Função para salvar o texto em um arquivo
def save_text():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(entry.get())

# Função para carregar o texto de um arquivo
def load_text():
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            entry.delete(0, tk.END)  # Limpa o campo de entrada
            entry.insert(0, file.read())  # Insere o texto carregado

# Função para definir atalhos personalizados
def set_shortcuts():
    global custom_start_shortcut, custom_stop_shortcut
    start_shortcut = simpledialog.askstring("Atalho de Início", "Digite o novo atalho para começar a digitar (ex: ctrl+shift+s):")
    stop_shortcut = simpledialog.askstring("Atalho de Parada", "Digite o novo atalho para parar a digitação (ex: ctrl+shift+p):")

    if start_shortcut and stop_shortcut:
        try:
            # Remove os atalhos antigos
            keyboard.remove_hotkey(custom_start_shortcut)
            keyboard.remove_hotkey(custom_stop_shortcut)

            # Atualiza os atalhos com os novos valores
            custom_start_shortcut = start_shortcut
            custom_stop_shortcut = stop_shortcut

            # Adiciona os novos atalhos
            keyboard.add_hotkey(custom_start_shortcut, on_click_start)
            keyboard.add_hotkey(custom_stop_shortcut, stop_typing)

            messagebox.showinfo("Sucesso", "Atalhos atualizados com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "Atalho inválido. Por favor, tente novamente.")

# Configuração da interface gráfica
root = tk.Tk()
root.title("RedaçãoTyper | @joaowrlld")
root.geometry("500x520")
root.minsize(500, 520)  # Ajuste do tamanho mínimo para comportar todos os widgets

# Ícone da janela
root.iconbitmap(r"C:\Users\João P. Reis\Desktop\Digitador Python\app_icon.ico")

# Definindo cores para a interface
bg_color = "#1c1c1c"
fg_color = "#ffffff"
button_color = "#4CAF50"
inactive_button_color = "#f44336"
entry_bg_color = "#333333"
entry_fg_color = "#ffffff"

root.config(bg=bg_color)

# Estilização dos widgets
label = tk.Label(root, text="Digite o texto para ser escrito:", font=("Helvetica", 12), bg=bg_color, fg=fg_color)
label.pack(pady=10)

entry = tk.Entry(root, width=50, font=("Helvetica", 10), bd=2, relief="solid", bg=entry_bg_color, fg=entry_fg_color)
entry.pack(pady=10)

# Carregar ícones
icon_start = load_icon(r"C:\Users\João P. Reis\Desktop\Digitador Python\start_icon.png", (20, 20))
icon_stop = load_icon(r"C:\Users\João P. Reis\Desktop\Digitador Python\stop_icon.png", (20, 20))
icon_link = load_icon(r"C:\Users\João P. Reis\Desktop\Digitador Python\link_icon.png", (20, 20))

# Botão para começar a digitar
button_start = tk.Button(root, text=" Começar a escrever", command=on_click_start, font=("Helvetica", 12), bg=button_color, fg="white", bd=0, relief="solid", image=icon_start, compound="left")
button_start.pack(pady=10)

# Botão para parar a digitação
button_stop = tk.Button(root, text=" Parar de escrever", command=stop_typing, font=("Helvetica", 12), bg=inactive_button_color, fg="white", bd=0, relief="solid", image=icon_stop, compound="left")
button_stop.pack(pady=10)

# Atalho para o site
link_button = tk.Button(root, text=" Atalho para conseguir seu texto", command=open_link, font=("Helvetica", 12), bg="#2196F3", fg="white", bd=0, relief="solid", image=icon_link, compound="left")
link_button.pack(pady=10)

# Campo de entrada para ajustar a velocidade da digitação
speed_label = tk.Label(root, text="Velocidade da digitação (entre 0.01 e 1):", font=("Helvetica", 12), bg=bg_color, fg=fg_color)
speed_label.pack(pady=5)

speed_entry = tk.Entry(root, width=10, font=("Helvetica", 10), bd=2, relief="solid", bg=entry_bg_color, fg=entry_fg_color)
speed_entry.insert(0, "0.1")  # Valor padrão
speed_entry.pack(pady=5)

# Botões de salvar e carregar texto
button_save = tk.Button(root, text="Salvar Texto", command=save_text, font=("Helvetica", 12), bg=button_color, fg="white", bd=0)
button_save.pack(pady=10)

button_load = tk.Button(root, text="Carregar Texto", command=load_text, font=("Helvetica", 12), bg=button_color, fg="white", bd=0)
button_load.pack(pady=10)

# Label para mostrar feedback visual
progress_label = tk.Label(root, text="", font=("Helvetica", 10), bg=bg_color, fg="yellow")
progress_label.pack(pady=10)

# Botão para definir atalhos personalizados
button_shortcuts = tk.Button(root, text="Definir Atalhos Personalizados", command=set_shortcuts, font=("Helvetica", 12), bg="#FF9800", fg="white", bd=0)
button_shortcuts.pack(pady=10)

# Créditos ao criador com link clicável para o Instagram
credit = tk.Label(root, text="Criado por @joaowrlld | 2024©", font=("Helvetica", 9), fg="lightblue", bg=bg_color, cursor="hand2")
credit.pack(side="bottom", pady=10)
credit.bind("<Button-1>", open_instagram)

# Adiciona os atalhos de teclado
keyboard.add_hotkey(custom_start_shortcut, on_click_start)
keyboard.add_hotkey(custom_stop_shortcut, stop_typing)

root.mainloop()
