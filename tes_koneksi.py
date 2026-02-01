from netmiko import ConnectHandler
import time

# 1. Konfigurasi Akses Router (Alpine FRR)
router_alpine = {
    'device_type': 'linux',
    'host': '172.17.0.100',
    'username': 'root',
    'password': '1', # GANTI SESUAI PASSWORD YANG KAMU BUAT
    'port': 22,
}

def jalankan_otomasi():
    new_hostname = "RizkiCoding"
    
    try:
        print(f"🚀 Memulai koneksi ke {router_alpine['host']}...")
        
        # Membuka koneksi
        with ConnectHandler(**router_alpine) as ssh:
            print("✅ Login Berhasil!")
            print("-" * 45)

            # --- BAGIAN 1: MENGUBAH HOSTNAME DI LEVEL SISTEM (ALPINE) ---
            print(f"📡 Mengubah System Hostname menjadi: {new_hostname}")
            
            # Kita gunakan expect_string=r'#' agar Netmiko hanya mencari tanda pagar,
            # sehingga tidak error saat nama router di depannya berubah.
            ssh.send_command(f"echo '{new_hostname}' > /etc/hostname", expect_string=r'#')
            ssh.send_command(f"hostname {new_hostname}", expect_string=r'#')

            # --- BAGIAN 2: MENGUBAH HOSTNAME DI LEVEL ROUTING (FRR/VTYSH) ---
            print("⚙️  Mengonfigurasi FRR via vtysh...")
            # Menjalankan perintah vtysh secara langsung dari shell Linux
            ssh.send_command(f'vtysh -c "conf t" -c "hostname {new_hostname}"', expect_string=r'#')
            ssh.send_command('vtysh -c "write mem"', expect_string=r'#')

            # Beri jeda 1 detik agar sistem sinkron
            time.sleep(1)

            # --- BAGIAN 3: VERIFIKASI AKHIR ---
            print("-" * 45)
            print("🔍 HASIL VERIFIKASI:")
            
            # Cek identitas di level OS dan Config FRR
            # Gunakan expect_string lagi karena prompt sudah berubah permanen
            check_os = ssh.send_command("hostname", expect_string=r'#')
            check_frr = ssh.send_command('vtysh -c "show running-config" | grep hostname', expect_string=r'#')

            print(f"   > OS Hostname  : {check_os}")
            print(f"   > FRR Config   : {check_frr}")
            
            if new_hostname in check_os:
                print("\n✨ SEMUA BERHASIL DIUBAH! ✨")
            else:
                print("\n⚠️  Cek kembali, sepertinya ada konfigurasi yang belum sinkron.")

    except Exception as e:
        # Menampilkan pesan error yang lebih bersih
        print(f"\n❌ TERJADI KESALAHAN: {e}")

if __name__ == "__main__":
    jalankan_otomasi()