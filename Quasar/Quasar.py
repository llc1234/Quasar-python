#"""
import time
import socket
import tkinter
import threading
import tkinter.ttk



class Quasar():
    def __init__(self, root, WindowSize, WindowTitle):
        self.root = root
        self.WindowSize = WindowSize
        self.WindowTitle = WindowTitle

        self.root.title(WindowTitle)
        self.SetWindowCentered()
        

        self.socket_timeout_Server = 5
        self.socket_timeout_clients = 5

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(self.socket_timeout_Server)

        lo = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        lo.connect(("8.8.8.8", 80))

        self.IP = lo.getsockname()[0]
        self.PORT = 5050

        self.columns = ("IP Address", "Tag", "User@PC", "Version", "Status", "User Status", "Country", "Operating System", "Account Type")
        self.columns_width = (110, 65, 150, 50, 70, 70, 110, 230, 100)

        self.data_clients = [
            # [0, "192.168.10.177", "Office-PC", "Admin@DESKTOP1", "1.4.0", "Connected", "Idle", "USA", "Windows 10", "Admin"],
            # [0, "192.168.10.155", "Laptop", "Kevin@LAPTOP", "1.3.8", "Connected", "Active", "Germany", "Windows 11", "User"]

            #
            #[
            #    conn,
            #    "IP Address", 
            #    "Tag", 
            #    "User@PC", 
            #    "Version", 
            #    "Status", 
            #    "User Status", 
            #    "Country", 
            #    "Operating System", 
            #    "Account Type",
                
            #    "RX: CMD"
            #]
        ]

        self.running = True
        self.isListening = False

        threading.Thread(target=self.ListeningForClients).start()

        self.CreatMenu()
        self.create_treeview()


    def SetWindowCentered(self):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width // 2) - (self.WindowSize[0] // 2)
        y = (screen_height // 2) - (self.WindowSize[1] // 2)

        self.root.geometry(f"{self.WindowSize[0]}x{self.WindowSize[1]}+{x}+{y}")


    def CreatMenu(self):
        menubar = tkinter.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tkinter.Menu(menubar, tearoff=0)
        settings_menu = tkinter.Menu(menubar, tearoff=0)
        builder_menu = tkinter.Menu(menubar, tearoff=0)
        about_menu = tkinter.Menu(menubar, tearoff=0)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Settings", command=self.TabSettings) # menu=settings_menu
        menubar.add_cascade(label="Builder", menu=builder_menu)
        menubar.add_cascade(label="About", menu=about_menu)

        file_menu.add_command(label="Exit", command=lambda: exit())
        about_menu.add_command(label="About Quasar GUI")
        # settings_menu.add_command(command=self.TabSettings)

        self.status_label = tkinter.Label(self.root, text="Listening: False", anchor="w", padx=10)
        self.status_label.pack(side=tkinter.BOTTOM, fill=tkinter.X)

    
    def create_treeview(self):
        self.tree = tkinter.ttk.Treeview(self.root, columns=self.columns, show="headings", style="Treeview")
        self.tree.pack(fill=tkinter.BOTH, expand=True)

        for col in range(len(self.columns)):
            self.tree.heading(self.columns[col], text=self.columns[col])
            self.tree.column(self.columns[col], width=self.columns_width[col])
        
        #for client in self.data_clients:
        #    self.tree.insert("", "end", values=client[1:])

        self.tree.bind("<Button-3>", self.show_context_menu)

    
    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            menu = tkinter.Menu(self.root, tearoff=0)
            menu.add_command(label="Open CMD", command=lambda: print("CMD"))
            menu.add_command(label="Open File Manager", command=lambda: print("File Manager"))
            menu.add_command(label="Live Screen View", command=lambda: print("Live Screen"))
            menu.add_command(label="Disconnect", command=self.on_disconnect)
            menu.tk_popup(event.x_root, event.y_root)

    
    def on_disconnect(self):
        selected_items = self.tree.selection()
        if selected_items:
            item_id = selected_items[0]
            index = self.tree.index(item_id)
            self.tree.delete(item_id)

            print(f"Remove: index: {index}")


    def TabSettings(self):
        r = tkinter.Tk()
        r.title("Settings")
        # r.geometry("310x330")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width // 2) - (310 // 2)
        y = (screen_height // 2) - (330 // 2)

        r.geometry(f"{310}x{330}+{x}+{y}")

        tp_text = tkinter.Label(r, text="IP:")
        tp_text.place(x=5, y=20)
        ip = tkinter.Entry(r)
        ip.place(x=50, y=20)
        ip.insert(0, self.IP)

        port_text = tkinter.Label(r, text="PORT:")
        port_text.place(x=5, y=50)
        port = tkinter.Entry(r)
        port.place(x=50, y=50)
        port.insert(0, str(self.PORT))

        self.start_server_button = tkinter.ttk.Button(r, text="Start Server", command=self.StartUpServer)
        self.start_server_button.place(x=5, y=80)

        self.stop_server_button = tkinter.ttk.Button(r, text="Stop Server", state=tkinter.DISABLED, command=self.StopServer) 
        self.stop_server_button.place(x=85, y=80)

        #if self.isListening:
        #    self.start_server_button.config(state=tkinter.DISABLED)
        #    self.stop_server_button.config(state=tkinter.NORMAL)

        r.mainloop()

    
    def StartUpServer(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(self.socket_timeout_Server)

        self.s.bind((self.IP, self.PORT))
        self.s.listen()

        self.isListening = True

        self.status_label.config(text=f'Listening: {self.IP}:{self.PORT}')

        self.start_server_button.config(state=tkinter.DISABLED)
        self.stop_server_button.config(state=tkinter.NORMAL)

    
    def StopServer(self):
        self.s.close()
        self.isListening = False

        self.status_label.config(text=f'Listening: False')

        self.stop_server_button.config(state=tkinter.DISABLED)
        self.start_server_button.config(state=tkinter.NORMAL)

        for pp in self.data_clients:
            pp[0].close()
            self.data_clients.remove(pp)
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            # self.AddLogs(f"disconnect client {item}")


    def ListeningToClient(self, conn, addr):
        while self.running:
            pass

    
    def ListeningForClients(self):
        while self.running:
            if self.isListening:
                try:
                    try:
                        conn, addr = self.s.accept()
                        conn.settimeout(self.socket_timeout_clients)  # 2 seconds timeout

                        print(f"Client Connected: {addr[0]}")

                        threading.Thread(target=lambda: self.ListeningToClient(conn, addr)).start()

                        data = [
                            conn,
                            addr[0], 
                            "Unknown", 
                            "Unknown", 
                            "Unknown", 
                            "Unknown", 
                            "Unknown", 
                            "Unknown", 
                            "Unknown", 
                            "Unknown"
                        ]
                        
                        self.data_clients.append(data)
                        self.tree.insert('', tkinter.END, values=data[1:10])

                    except socket.timeout:
                        pass
                except:
                    pass
            else:
                time.sleep(2)


if __name__ == "__main__":
    root = tkinter.Tk()
    app = Quasar(root, (1020, 435), "Quasar 0.1.0")
    root.mainloop()
    print("exit")
    root.running = False
    root.isListening = False
    exit()

#"""
















"""

import tkinter as tk
from tkinter import ttk, Menu

class QuasarGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quasar RAT Replica - Tkinter")
        self.geometry("1010x420")
        # self.configure(bg="#1e1e1e")

        self.create_menu()
        self.create_treeview()
        self.populate_clients()

    def create_menu(self):
        menubar = Menu(self)
        self.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        settings_menu = Menu(menubar, tearoff=0)
        builder_menu = Menu(menubar, tearoff=0)
        about_menu = Menu(menubar, tearoff=0)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        menubar.add_cascade(label="Builder", menu=builder_menu)
        menubar.add_cascade(label="About", menu=about_menu)

        file_menu.add_command(label="Exit", command=self.quit)
        about_menu.add_command(label="About Quasar GUI", command=lambda: print("Quasar Replica in Tkinter"))

        self.status_label = tk.Label(self, text="Listening: False", anchor="w",
                                 padx=10)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def create_treeview(self):
        columns = (
            "IP Address", "Tag", "User@PC", "Version",
            "Status", "User Status", "Country",
            "Operating System", "Account Type"
        )

        style = ttk.Style(self)
        style.theme_use("default")

        self.tree = ttk.Treeview(self, columns=columns, show="headings", style="Treeview")
        self.tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=120)

        self.tree.bind("<Button-3>", self.show_context_menu)

    def populate_clients(self):
        clients = [
            ["192.168.1.5", "Office-PC", "Admin@DESKTOP1", "1.4.0", "Connected", "Idle", "USA", "Windows 10", "Admin"],
            ["10.0.0.8", "Laptop", "Kevin@LAPTOP", "1.3.8", "Connected", "Active", "Germany", "Windows 11", "User"],
            ["172.16.5.2", "Home", "Netx@HOME-PC", "1.4.0", "Connected", "Idle", "Norway", "Windows 10", "Admin"],
            ["192.168.1.5", "Office-PC", "Admin@DESKTOP1", "1.4.0", "Connected", "Idle", "USA", "Windows 10", "Admin"],
            ["10.0.0.8", "Laptop", "Kevin@LAPTOP", "1.3.8", "Connected", "Active", "Germany", "Windows 11", "User"],
            ["172.16.5.2", "Home", "Netx@HOME-PC", "1.4.0", "Connected", "Idle", "Norway", "Windows 10", "Admin"]
        ]

        for client in clients:
            self.tree.insert("", "end", values=client)

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            menu = Menu(self, tearoff=0)
            menu.add_command(label="Open CMD", command=lambda: print("CMD"))
            menu.add_command(label="Open File Manager", command=lambda: print("File Manager"))
            menu.add_command(label="Live Screen View", command=lambda: print("Live Screen"))
            menu.add_command(label="Disconnect", command=self.on_disconnect)
            menu.tk_popup(event.x_root, event.y_root)

    
    def on_disconnect(self):
        selected_items = self.tree.selection()
        if selected_items:
            item_id = selected_items[0]
            index = self.tree.index(item_id)
            self.tree.delete(item_id)

            print(f"Remove: index: {index}")


if __name__ == "__main__":
    app = QuasarGUI()
    app.mainloop()
"""