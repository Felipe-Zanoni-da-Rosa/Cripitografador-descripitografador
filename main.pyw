import os
import hashlib
import secrets
from tkinter import Tk, Label, Button, Entry, StringVar, filedialog, messagebox, simpledialog
from tkinter.ttk import Style, Progressbar
from cryptography.fernet import Fernet
from pathlib import Path

KEY_FILE = 'key.key'

class App:
    def __init__(self, master):
        self.master = master
        master.title("Criptografia e Descriptografia de Arquivos")

        style = Style()
        style.configure('TButton', font=('Helvetica', 14))
        style.configure('TLabel', font=('Helvetica', 16))

        self.encrypt_button = Button(master, text="Criptografar arquivo", command=self.start_encryption)
        self.encrypt_button.pack(pady=10)

        self.decrypt_button = Button(master, text="Descriptografar arquivo", command=self.start_decryption)
        self.decrypt_button.pack(pady=10)

        self.progress_label = Label(master, text="")
        self.progress_label.pack(pady=10)

        self.progress_bar = Progressbar(master, orient='horizontal', length=200, mode='determinate')
        self.progress_bar.pack(pady=10)

    def get_key(self):
        if os.path.exists(KEY_FILE):
            with open(KEY_FILE, 'rb') as f:
                key = f.read()
        else:
            key_choice = messagebox.askyesno("Gerar chave aleatória", "Deseja gerar uma chave aleatória de 50 dígitos?")
            if key_choice:
                key = Fernet.generate_key()
            else:
                key = simpledialog.askstring("Escolha a chave", "Digite a chave a ser usada:").encode()
            with open(KEY_FILE, 'wb') as f:
                f.write(key)
        return key

    def calculate_file_hash(self, file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
        file_hash = hashlib.sha256(data).hexdigest()
        return file_hash

    def start_encryption(self):
        file_path = filedialog.askopenfilename(filetypes=[('Arquivos de Texto', '*.txt')])
        if file_path:
            self.encrypt_file(file_path)
        else:
            messagebox.showerror("Erro", 'Nenhum arquivo selecionado.')

    def encrypt_file(self, file_path):
        key = self.get_key()
        original_hash = self.calculate_file_hash(file_path)
        messagebox.showinfo("Hash Original", f'Hash do arquivo original: {original_hash}')
        with open(file_path, 'rb') as f:
            data = f.read()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)

        original_extension = '.txt'
        encrypted_with_extension = encrypted + original_extension.encode()

        encrypted_file_path = filedialog.asksaveasfilename(defaultextension='.enc')
        if encrypted_file_path:
            with open(encrypted_file_path, 'wb') as f:
                f.write(encrypted_with_extension)
            encrypted_hash = self.calculate_file_hash(encrypted_file_path)
            messagebox.showinfo("Hash Criptografado", f'Hash do arquivo criptografado: {encrypted_hash}')
            messagebox.showinfo("Sucesso", f'Arquivo criptografado salvo em {encrypted_file_path}!')

            # Alterar a extensão do arquivo para .enc
            encrypted_file_path = self._change_file_extension(encrypted_file_path, '.enc')

            # Remover o arquivo de texto original
            os.remove(file_path)
        else:
            messagebox.showerror("Erro", 'Nenhum local selecionado para salvar o arquivo criptografado.')

    def start_decryption(self):
        file_path = filedialog.askopenfilename(filetypes=[('Arquivos Criptografados', '*.enc')])
        if file_path:
            self.decrypt_file(file_path)
        else:
            messagebox.showerror("Erro", 'Nenhum arquivo selecionado.')

    def decrypt_file(self, file_path):
        key = self.get_key()
        encrypted_hash = self.calculate_file_hash(file_path)
        messagebox.showinfo("Hash Criptografado", f'Hash do arquivo criptografado: {encrypted_hash}')
        with open(file_path, 'rb') as f:
            data = f.read()
        fernet = Fernet(key)
        try:
            original_extension = '.txt'
            encrypted_data = data[:-4]
            decrypted = fernet.decrypt(encrypted_data)

            decrypted_file_path = filedialog.asksaveasfilename(defaultextension='.txt')
            if decrypted_file_path:
                with open(decrypted_file_path, 'wb') as f:
                    f.write(decrypted)
                decrypted_hash = self.calculate_file_hash(decrypted_file_path)
                messagebox.showinfo("Hash Descriptografado", f'Hash do arquivo descriptografado: {decrypted_hash}')
                messagebox.showinfo("Sucesso", f'Arquivo descriptografado salvo em {decrypted_file_path}!')

                # Alterar a extensão do arquivo para .txt
                decrypted_file_path = self._change_file_extension(decrypted_file_path, '.txt')

                # Remover o arquivo criptografado
                os.remove(file_path)
            else:
                messagebox.showerror("Erro", 'Nenhum local selecionado para salvar o arquivo descriptografado.')
        except:
            messagebox.showerror("Erro", 'Senha incorreta ou arquivo inválido.')

    def _change_file_extension(self, file_path, new_extension):
        file_name = Path(file_path).stem  # Obter o nome do arquivo sem a extensão
        new_file_path = file_name + new_extension  # Novo caminho de arquivo com a nova extensão
        return new_file_path

def main():
    root = Tk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()
