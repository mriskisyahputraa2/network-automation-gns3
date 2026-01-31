from netmiko import ConnectHandler
import time

# 1. Konfigurasi Akses Router (Alpine FRR)
# Pastikan IP dan password sesuai dengan yang kamu buat di GNS3
router_alpine = {
    'device_type': 'linux',
    'host': '172.17.0.100',
    'username': 'root',
    'password': 'admin123', # GANTI DENGAN PASSWORD KAMU
    'port': 22,
}

def jalankan_otomasi():
    new_hostname = "Router-Otomasi-Riski"
    
    try:
        print(f"🚀 Memulai koneksi ke {router_alpine['host']}...")
        
        # Membuka koneksi menggunakan context manager (otomatis close)
        with ConnectHandler(**router_alpine) as ssh:
            print("✅ Login Berhasil!")
            print("-" * 40)

            # --- BAGIAN 1: MENGUBAH HOSTNAME DI LEVEL SISTEM (ALPINE) ---
            print(f"📡 Mengubah System Hostname menjadi: {new_hostname}")
            ssh.send_command(f"echo '{new_hostname}' > /etc/hostname")
            ssh.send_command(f"hostname {new_hostname}")

            # --- BAGIAN 2: MENGUBAH HOSTNAME DI LEVEL ROUTING (FRR/VTYSH) ---
            print("⚙️  Mengonfigurasi FRR via vtysh...")
            # Mengirimkan rangkaian perintah konfigurasi
            cmd_vtysh = [
                f'vtysh -c "conf t" -c "hostname {new_hostname}"',
                'vtysh -c "write mem"'
            ]
            for cmd in cmd_vtysh:
                ssh.send_command(cmd)

            # Memberi jeda sebentar agar sistem memproses
            time.sleep(1)

            # --- BAGIAN 3: VERIFIKASI AKHIR ---
            print("-" * 40)
            print("🔍 HASIL VERIFIKASI:")
            
            # Cek nama di level OS
            check_os = ssh.send_command("hostname")
            # Cek nama di level Config FRR
            check_frr = ssh.send_command('vtysh -c "show running-config" | grep hostname')

            print(f"   > OS Hostname  : {check_os}")
            print(f"   > FRR Config   : {check_frr}")
            
            if new_hostname in check_os and new_hostname in check_frr:
                print("\n✨ SEMUA BERHASIL DIUBAH! ✨")
            else:
                print("\n⚠️  Ada bagian yang belum berubah, cek kembali perintahnya.")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    jalankan_otomasi()