import os
import time
import subprocess
import pyautogui
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

class ASTP:
    def __init__(self, root):
        self.root = root
        self.root.title("ASTP — Auto Script TXT › PY")
        self.root.geometry("600x450")
        self.root.resizable(False, False)
        self.root.configure(bg="#2D2D2D")
        
        self.current_file = None
        self.is_running = False
        
        self.create_ui()
        self.center_window()
    
    def create_ui(self):
        main_frame = tk.Frame(self.root, bg="#2D2D2D")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="ASTP", 
                font=("Consolas", 26, "bold"), 
                bg="#2D2D2D", fg="#FFFFFF").pack(pady=(0, 5))
        
        tk.Label(main_frame, text="auto script txt → py", 
                font=("Consolas", 10), 
                bg="#2D2D2D", fg="#888888").pack(pady=(0, 15))
        
        tk.Frame(main_frame, bg="#444444", height=2).pack(fill="x", pady=5)
        
        self.status = tk.Label(main_frame, text="> файл не выбран", 
                               font=("Consolas", 10), 
                               bg="#2D2D2D", fg="#4CAF50")
        self.status.pack(pady=(12, 8))
        
        # Прогресс
        self.progress = tk.Canvas(main_frame, height=4, bg="#444444", highlightthickness=0)
        self.progress.pack(fill="x", pady=(0, 10))
        self.progress_bar = None
        
        # Лог
        log_header = tk.Frame(main_frame, bg="#2D2D2D")
        log_header.pack(fill="x", pady=(5, 0))
        
        tk.Label(log_header, text="> console", 
                font=("Consolas", 8), 
                bg="#2D2D2D", fg="#888888").pack(side="left")
        
        clear_btn = tk.Button(log_header, text="🗑", 
                             command=self.clear_log,
                             bg="#2D2D2D", fg="#888888",
                             font=("Consolas", 8),
                             relief="flat", bd=0,
                             cursor="hand2")
        clear_btn.pack(side="right")
        
        log_frame = tk.Frame(main_frame, bg="#000000", bd=1, relief="solid")
        log_frame.pack(fill="both", expand=True, pady=(5, 15))
        
        self.log_text = tk.Text(log_frame, height=8, bg="#1E1E1E", fg="#00FF00",
                                font=("Consolas", 9), wrap="word", bd=0,
                                insertbackground="#FFFFFF")
        self.log_text.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Кнопки
        btn_frame = tk.Frame(main_frame, bg="#2D2D2D")
        btn_frame.pack(fill="x", pady=5)
        
        self.action_btn = tk.Button(btn_frame, text="▶  EXECUTE", 
                                    command=self.assemble,
                                    bg="#3D3D3D", fg="white",
                                    font=("Consolas", 10, "bold"),
                                    relief="flat", bd=1,
                                    padx=20, pady=8,
                                    cursor="hand2")
        self.action_btn.pack(side="left", padx=(0, 10), expand=True, fill="x")
        
        tk.Button(btn_frame, text="📂  SELECT .PY", 
                 command=self.select_file,
                 bg="#3D3D3D", fg="white",
                 font=("Consolas", 10),
                 relief="flat", bd=1,
                 padx=20, pady=8,
                 cursor="hand2").pack(side="left", expand=True, fill="x")
        
        tk.Label(main_frame, text="> ctrl+alt+shift+p  |  select file", 
                font=("Consolas", 8), 
                bg="#2D2D2D", fg="#666666").pack(pady=(12, 0))
    
    def clear_log(self):
        self.log_text.delete(1.0, "end")
    
    def show_progress(self):
        if self.progress_bar:
            self.progress.delete(self.progress_bar)
        self.progress_bar = self.progress.create_rectangle(0, 0, 0, 4, fill="#4CAF50", width=0)
        self.animate_progress(0)
    
    def animate_progress(self, step):
        if self.is_running and step <= 100:
            width = (step / 100) * self.progress.winfo_width()
            self.progress.coords(self.progress_bar, 0, 0, width, 4)
            self.root.after(30, lambda: self.animate_progress(step + 2))
        elif not self.is_running and self.progress_bar:
            self.progress.coords(self.progress_bar, 0, 0, 0, 4)
    
    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 300
        y = (self.root.winfo_screenheight() // 2) - 225
        self.root.geometry(f"600x450+{x}+{y}")
    
    def log(self, msg):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {msg}\n")
        self.log_text.see("end")
    
    def select_file(self):
        filepath = filedialog.askopenfilename(
            title="select .py file",
            filetypes=[("Python files", "*.py")]
        )
        if filepath:
            self.current_file = filepath
            self.status.config(text=f"> {os.path.basename(filepath)}", fg="#4CAF50")
            self.log(f"selected: {os.path.basename(filepath)}")
    
    def assemble(self):
        if self.is_running:
            self.log("busy...")
            return
        if not self.current_file:
            messagebox.showwarning("error", "select .py file first")
            return
        if not os.path.exists(self.current_file):
            messagebox.showerror("error", "file not found")
            return
        
        self.is_running = True
        self.action_btn.config(state="disabled")
        self.show_progress()
        
        def run():
            try:
                # Проверяем расширение
                if not self.current_file.endswith('.py'):
                    self.log("error: file is not .py")
                    return
                
                # Путь для .txt
                base = self.current_file[:-3]  # убираем .py
                txt_path = base + ".txt"
                
                self.log(f"renaming: {os.path.basename(self.current_file)} → .txt")
                os.rename(self.current_file, txt_path)
                self.log("→ .py → .txt")
                
                # Открываем в блокноте
                subprocess.Popen(["notepad.exe", txt_path])
                time.sleep(0.5)
                
                # Эмулируем нажатия
                self.log("pasting new code...")
                pyautogui.hotkey("ctrl", "a")
                time.sleep(0.05)
                pyautogui.press("delete")
                time.sleep(0.05)
                pyautogui.hotkey("ctrl", "v")
                time.sleep(0.05)
                pyautogui.hotkey("ctrl", "s")
                time.sleep(0.3)
                pyautogui.hotkey("alt", "f4")
                
                # Обратно в .py
                py_path = base + ".py"
                os.rename(txt_path, py_path)
                self.current_file = py_path
                
                self.log("← .txt → .py")
                self.log("✓ done")
                self.status.config(text=f"> {os.path.basename(py_path)}", fg="#4CAF50")
                messagebox.showinfo("success", "code replaced")
                
            except Exception as e:
                self.log(f"error: {str(e)}")
                messagebox.showerror("error", str(e))
            finally:
                self.is_running = False
                self.action_btn.config(state="normal")
        
        threading.Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = ASTP(root)
    
    try:
        import keyboard
        def hotkey_callback():
            if app.current_file and os.path.exists(app.current_file):
                app.assemble()
            else:
                app.log("select file first")
        keyboard.add_hotkey("ctrl+alt+shift+p", hotkey_callback)
        app.log("hotkey active: ctrl+alt+shift+p")
    except:
        app.log("hotkey unavailable")
    
    root.mainloop()