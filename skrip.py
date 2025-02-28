import os
import random
import time
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Konfigurasi RPC Monad Testnet dengan timeout
RPC_URL = "https://testnet-rpc.monad.xyz/"
web3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={'timeout': 60}))

# Cek apakah terhubung ke jaringan
if not web3.is_connected():
    print("[ERROR] Tidak dapat terhubung ke RPC Monad Testnet.")
    exit()

# Private key dari .env
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
if not PRIVATE_KEY:
    print("[ERROR] PRIVATE_KEY tidak ditemukan di .env!")
    exit()

WALLET_ADDRESS = web3.eth.account.from_key(PRIVATE_KEY).address
print(f"[INFO] Wallet Address: {WALLET_ADDRESS}")

# Kontrak Wrapped MONAD (wMONAD) Testnet
WMONAD_CONTRACT = "0x760AfE86e5de5fa0Ee542fc7B7B713e1c5425701"  # Gantilah dengan alamat kontrak wMONAD

# ABI wMONAD (Minimal untuk wrap)
WMONAD_ABI = '[{"inputs":[],"name":"deposit","outputs":[],"stateMutability":"payable","type":"function"}]'

# Fungsi untuk mensimulasikan delay manusia
def human_like_delay():
    delay = random.uniform(30, 120)  # Jeda antara 30 detik hingga 5 menit
    print(f"[INFO] Menunggu {delay:.2f} detik sebelum melanjutkan...")
    time.sleep(delay)

# Fungsi untuk wrap MONAD ke wMONAD dengan variasi acak
def wrap_monad():
    try:
        contract = web3.eth.contract(address=WMONAD_CONTRACT, abi=WMONAD_ABI)
        amount = random.uniform(0.00001, 0.00099)  # Random di bawah 0.001 MONAD
        print(f"[INFO] Mencoba melakukan wrap {amount:.6f} MONAD ke wMONAD...")

        tx = contract.functions.deposit().build_transaction({
            'from': WALLET_ADDRESS,
            'value': web3.to_wei(amount, 'ether'),
            'gas': random.randint(90000, 110000),  # Variasi gas agar lebih realistis
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(WALLET_ADDRESS)
        })

        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"[SUCCESS] wMONAD | TX Sent: {web3.to_hex(tx_hash)}")
    
    except Exception as e:
        print(f"[ERROR] Gagal melakukan transaksi: {str(e)}")

    human_like_delay()

# Loop utama
tx_count = 0

while True:
    try:
        wrap_monad()
        tx_count += 1

        if 30 <= tx_count <= 50:
            long_sleep_time = random.randint(3600, 14400)  # Jeda acak antara 1 hingga 4 jam
            print(f"[INFO] Telah mencapai {tx_count} transaksi, menunggu {long_sleep_time} detik sebelum melanjutkan...")
            time.sleep(long_sleep_time)
            tx_count = 0  # Reset counter setelah jeda panjang
        else:
            sleep_time = random.randint(0, 120)  # Jeda acak antara 2 hingga 10 menit
            print(f"[INFO] Menunggu {sleep_time} detik sebelum transaksi berikutnya...")
            time.sleep(sleep_time)

    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan dalam loop utama: {str(e)}")
        time.sleep(300)  # Tunggu 5 menit sebelum mencoba lagi
