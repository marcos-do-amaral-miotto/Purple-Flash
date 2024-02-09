import tkinter as tk

def configurar_largura(widget, porcentagem):
    largura_janela = root.winfo_width()
    print(largura_janela)
    largura_desejada = int(largura_janela * (porcentagem / 100))
    widget.config(width=largura_desejada)

root = tk.Tk()
root.title("Exemplo de Largura de Widget")

# Criar um widget (por exemplo, um botão)
meu_widget = tk.Button(root, text="Meu Widget")

# Adicionar o widget à janela
meu_widget.pack(pady=20)  # pady é o espaço vertical ao redor do widget

# Configurar a largura do widget para 80% da largura da janela
configurar_largura(meu_widget, 10)

# Iniciar o loop principal
root.mainloop()
