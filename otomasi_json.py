import json
from netmiko import ConnectHandler

def jalankan_otomasi_json():
    # 1. Membaca file JSON (Ibarat Fetching API)
    try:
        with open('perangkat.json', 'r') as file:
            perangkat_list = json.load(file)
    except FileNotFoundError:
        print("❌ Error: File perangkat.json tidak ditemukan!")
        return

    print(f"📂 Berhasil memuat {len(perangkat_list)} perangkat dari JSON.")

    # 2. Looping untuk konfigurasi
    for device in perangkat_list:
        try:
            print(f"\n--- Menghubungkan ke: {device['host']} ---")
            with ConnectHandler(**device) as ssh:
                # Mengambil angka belakang IP untuk nama unik
                ip_ujung = device['host'].split('.')[-1]
                nama_baru = f"Router-JSON-{ip_ujung}"
                
                print(f"📡 Mengubah Hostname menjadi: {nama_baru}")
                ssh.send_command(f"hostname {nama_baru}", expect_string=r'#')
                ssh.send_command(f'vtysh -c "conf t" -c "hostname {nama_baru}"', expect_string=r'#')
                
                print(f"✅ Sukses mengonfigurasi {nama_baru}")

        except Exception as e:
            print(f"❌ Gagal pada {device['host']}: {e}")

if __name__ == "__main__":
    jalankan_otomasi_json()