import os
from datetime import datetime
from netmiko import ConnectHandler

# 1. Daftar pasukan router kamu
perangkat_list = [
    {'device_type': 'linux', 'host': '172.17.0.100', 'username': 'root', 'password': '1'},
    {'device_type': 'linux', 'host': '172.17.0.102', 'username': 'root', 'password': '1'},
    {'device_type': 'linux', 'host': '172.17.0.103', 'username': 'root', 'password': '1'},
]

def jalankan_backup():
    # Membuat folder 'backups' secara otomatis jika belum ada
    if not os.path.exists('backups'):
        os.makedirs('backups')
        print("📁 Folder 'backups' berhasil dibuat.")

    waktu_sekarang = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    print(f"🚀 Memulai Backup Massal pada: {waktu_sekarang}")

    for device in perangkat_list:
        try:
            print(f"\n--- Mengambil data dari: {device['host']} ---")
            with ConnectHandler(**device) as ssh:
                # 1. Ambil Nama Hostname
                hostname = ssh.send_command("hostname", expect_string=r'#').strip()
                
                # 2. Ambil Konfigurasi Jaringan & Routing
                print(f"💾 Menarik konfigurasi dari {hostname}...")
                config_linux = ssh.send_command("cat /etc/network/interfaces", expect_string=r'#')
                config_frr = ssh.send_command('vtysh -c "show run"', expect_string=r'#')

                # 3. Gabungkan Konfigurasi
                isi_backup = f"=== BACKUP {hostname} ({device['host']}) ===\n"
                isi_backup += f"Tanggal: {waktu_sekarang}\n\n"
                isi_backup += "--- [LINUX NETWORK CONFIG] ---\n" + config_linux + "\n\n"
                isi_backup += "--- [FRR ROUTING CONFIG] ---\n" + config_frr

                # 4. Simpan ke File .txt
                nama_file = f"backups/backup_{hostname}_{device['host']}_{waktu_sekarang}.txt"
                with open(nama_file, "w") as file:
                    file.write(isi_backup)
                
                print(f"✅ Tersimpan: {nama_file}")

        except Exception as e:
            print(f"❌ Gagal backup {device['host']}: {e}")

if __name__ == "__main__":
    jalankan_backup()