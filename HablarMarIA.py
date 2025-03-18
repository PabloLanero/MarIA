import tkinter as tk
from tkinter import ttk, Frame, Canvas, Scrollbar
import threading
import speech_recognition as sr
import pyttsx3
import ollama
from PIL import ImageTk, Image

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MarIA - Chat de Voz")
        self.root.geometry("800x600")
        self.root.minsize(400, 500)
        self.root.configure(bg="#e0f7fa")
        
        # Configuración de voz
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        
        # Cargar logo
        try:
            self.logo_image = ImageTk.PhotoImage(Image.open("Fotos/MarIA_Logo.png").resize((200, 200)))
        except Exception as e:
            print(f"Error cargando el logo: {e}")
            self.logo_image = None
        
        self.create_widgets()
        self.configure_styles()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Botones
        style.configure('TButton', font=('Arial', 10), background="#00acc1", 
                        foreground="white", borderwidth=0, padding=8)
        style.map('TButton', background=[('active', '#0097a7'), ('disabled', '#b2ebf2')])
        
        # Mensajes
        style.configure('User.TFrame', background="#e3f2fd", relief='flat')
        style.configure('Bot.TFrame', background="#ffffff", relief='flat')
        style.configure('User.TLabel', background="#0084ff", 
                        foreground="white", font=('Arial', 12), padding=12)
        style.configure('Bot.TLabel', background="#f0f4f7", 
                        foreground="#263238", font=('Arial', 12), padding=12)

    def create_widgets(self):
        main_frame = Frame(self.root, bg="#e0f7fa", padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Configurar escalabilidad
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Header
        header_frame = Frame(main_frame, bg="#e0f7fa")
        header_frame.grid(row=0, column=0, sticky="ew")

        if self.logo_image:
            logo_label = tk.Label(header_frame, image=self.logo_image, bg="#e0f7fa")
            logo_label.pack()

        # Área del chat
        chat_container = Frame(main_frame, bg="#e0f7fa")
        chat_container.grid(row=1, column=0, sticky="nsew")

        chat_container.grid_rowconfigure(0, weight=1)
        chat_container.grid_columnconfigure(0, weight=1)

        self.canvas = Canvas(chat_container, bg="#ffffff", highlightthickness=0)
        scrollbar = Scrollbar(chat_container, command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg="#ffffff", padx=5, pady=5)

        self.scrollable_frame.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Entrada de texto y botones
        input_frame = Frame(main_frame, bg="#e0f7fa")
        input_frame.grid(row=2, column=0, sticky="ew", pady=10)

        self.user_input = ttk.Entry(input_frame, font=('Arial', 12))
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.user_input.bind("<Return>", lambda event: self.send_text_message())

        btn_frame = Frame(input_frame, bg="#e0f7fa")
        btn_frame.pack(side=tk.RIGHT)

        ttk.Button(btn_frame, text="🎤", command=self.start_voice_recognition, width=3).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="↑", command=self.send_text_message, width=3).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="✖", command=self.clear_chat, width=3).pack(side=tk.LEFT, padx=2)

    def add_message(self, sender, message):
        frame = ttk.Frame(self.scrollable_frame, style='User.TFrame' if sender == "user" else 'Bot.TFrame')
        frame.pack(fill=tk.X, pady=4, padx=5)

        ttk.Label(
            frame,
            text=message,
            style='User.TLabel' if sender == "user" else 'Bot.TLabel',
            wraplength=self.root.winfo_width() - 100,
            justify=tk.LEFT if sender == "bot" else tk.RIGHT
        ).pack(padx=5, pady=2)

        self.canvas.yview_moveto(1)
        self.root.update_idletasks()

    def clear_chat(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def send_text_message(self):
        text = self.user_input.get().strip()
        if text:
            self.user_input.delete(0, tk.END)
            self.add_message("user", text)
            self.process_response(text)

    def process_response(self, text):
        try:
            response = ollama.generate(model='MarIA', prompt=text)
            if response and 'response' in response:
                self.add_message("bot", response['response'])
                self.speak(response['response'])
            else:
                self.add_message("bot", "No se recibió respuesta del modelo")
        except Exception as e:
            self.add_message("bot", f"Error: {str(e)}")

    def speak(self, text):
        def run_speech():
            self.engine.say(text)
            self.engine.runAndWait()
        threading.Thread(target=run_speech, daemon=True).start()

    def start_voice_recognition(self):
        threading.Thread(target=self.voice_recognition_thread, daemon=True).start()

    def voice_recognition_thread(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Escuchando...")
            try:
                audio = self.recognizer.listen(source, phrase_time_limit=50)
                text = self.recognizer.recognize_google(audio, language='es-ES')
                self.root.after(0, self.add_message, "user", text)
                self.root.after(0, self.process_response, text)
            except sr.UnknownValueError:
                self.root.after(0, self.add_message, "bot", "No se pudo entender el audio")
            except sr.RequestError:
                self.root.after(0, self.add_message, "bot", "Error en la solicitud al servicio de reconocimiento de voz")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()






'''
  

'''