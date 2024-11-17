import serial
import time
import tkinter as tk
from tkinter import messagebox, ttk
import serial.tools.list_ports

# ================== Configuration ==================
# Command mappings
COMMANDS = {
    'W': 'F',  # Forward
    'A': 'L',  # Left
    'S': 'B',  # Back
    'D': 'R',  # Right
    'Stop': 'S'  # Stop
}
# =====================================================

class BluetoothCarController:
    def __init__(self, master):
        self.master = master
        self.master.title("Bluetooth Car Controller")
        self.master.resizable(False, False)

        # Initialize serial connection variables
        self.ser = None
        self.connected = False

        # Configure the grid
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_rowconfigure(3, weight=1)
        self.master.grid_rowconfigure(4, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)

        # Create UI elements
        self.create_port_selection()
        self.create_buttons()
        self.create_status_label()

        # Bind keyboard events
        self.master.bind('<KeyPress>', self.on_key_press)
        self.master.bind('<KeyRelease>', self.on_key_release)

    def create_port_selection(self):
        frame = tk.Frame(self.master)
        frame.grid(row=0, column=0, columnspan=3, pady=10)

        lbl_port = tk.Label(frame, text="Select Serial Port:")
        lbl_port.pack(side=tk.LEFT, padx=5)

        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(frame, textvariable=self.port_var, state="readonly", width=40)
        self.port_combo['values'] = self.get_serial_ports()
        self.port_combo.pack(side=tk.LEFT, padx=5)

        btn_refresh = tk.Button(frame, text="Refresh", command=self.refresh_ports)
        btn_refresh.pack(side=tk.LEFT, padx=5)

        btn_connect = tk.Button(frame, text="Connect", command=self.connect_serial)
        btn_connect.pack(side=tk.LEFT, padx=5)

    def create_buttons(self):
        button_font = ("Helvetica", 16, "bold")

        # Forward Button
        btn_forward = tk.Button(self.master, text="↑", command=self.forward, width=5, height=2, font=button_font, bg="lightgreen")
        btn_forward.grid(row=1, column=1, padx=10, pady=10)

        # Left Button
        btn_left = tk.Button(self.master, text="←", command=self.left, width=5, height=2, font=button_font, bg="lightblue")
        btn_left.grid(row=2, column=0, padx=10, pady=10)

        # Stop Button
        btn_stop = tk.Button(self.master, text="Stop", command=self.stop, width=5, height=2, font=button_font, bg="red", fg="white")
        btn_stop.grid(row=2, column=1, padx=10, pady=10)

        # Right Button
        btn_right = tk.Button(self.master, text="→", command=self.right, width=5, height=2, font=button_font, bg="lightblue")
        btn_right.grid(row=2, column=2, padx=10, pady=10)

        # Back Button
        btn_back = tk.Button(self.master, text="↓", command=self.back, width=5, height=2, font=button_font, bg="lightgreen")
        btn_back.grid(row=3, column=1, padx=10, pady=10)

        # Disable control buttons until connected
        for btn in [btn_forward, btn_back, btn_left, btn_right, btn_stop]:
            btn.config(state=tk.DISABLED)
        self.control_buttons = [btn_forward, btn_back, btn_left, btn_right, btn_stop]

    def create_status_label(self):
        self.status_var = tk.StringVar()
        self.status_var.set("Not Connected")
        self.status_label = tk.Label(self.master, textvariable=self.status_var, fg="red")
        self.status_label.grid(row=4, column=0, columnspan=3, pady=10)

    def get_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        port_list = []
        for port in ports:
            port_desc = port.description
            port_device = port.device
            port_list.append(f"{port_device} - {port_desc}")
        return port_list

    def refresh_ports(self):
        self.port_combo['values'] = self.get_serial_ports()
        if self.port_combo['values']:
            self.port_combo.current(0)

    def connect_serial(self):
        selection = self.port_var.get()
        if not selection:
            messagebox.showwarning("No Port Selected", "Please select a serial port.")
            return
        # Extract the device name before the ' - '
        port = selection.split(' - ')[0]
        try:
            self.ser = serial.Serial(port, 9600, timeout=1)
            time.sleep(2)  # Wait for the connection to initialize
            self.connected = True
            self.status_var.set(f"Connected to {port}")
            self.status_label.config(fg="green")
            # Enable control buttons
            for btn in self.control_buttons:
                btn.config(state=tk.NORMAL)
            print(f"Connected to {port} at 9600 baud.")
        except serial.SerialException as e:
            messagebox.showerror("Serial Port Error", f"Cannot open serial port {port}.\n{e}")
            self.status_var.set("Connection Failed")
            self.status_label.config(fg="red")

    def send_command(self, command):
        if self.connected and self.ser and self.ser.is_open:
            try:
                self.ser.write(command.encode())
                print(f"Sent command: {command}")
            except serial.SerialException as e:
                messagebox.showerror("Serial Communication Error", f"Failed to send command '{command}'.\n{e}")
        else:
            messagebox.showwarning("Not Connected", "Please connect to a serial port first.")

    # Command Functions
    def forward(self):
        self.send_command(COMMANDS['W'])

    def back(self):
        self.send_command(COMMANDS['S'])

    def left(self):
        self.send_command(COMMANDS['A'])

    def right(self):
        self.send_command(COMMANDS['D'])

    def stop(self):
        self.send_command(COMMANDS['Stop'])

    # Keyboard Event Handlers
    def on_key_press(self, event):
        key = event.keysym.upper()
        if key in COMMANDS and key != 'STOP':
            self.send_command(COMMANDS[key])

    def on_key_release(self, event):
        self.stop()

    def on_closing(self):
        # Close serial port on exit
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Serial port closed.")
        self.master.destroy()

def main():
    root = tk.Tk()
    app = BluetoothCarController(root)
    # Refresh ports initially
    app.refresh_ports()
    # Select the first port if available
    if app.port_combo['values']:
        app.port_combo.current(0)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
