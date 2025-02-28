import os
import random
import time
import logging
from web3 import Web3
from dotenv import load_dotenv

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Watermark
WATERMARK = """


███╗░░░███╗░█████╗░███╗░░██╗░█████╗░███████╗███╗░░░███╗░█████╗░
████╗░████║██╔══██╗████╗░██║██╔══██╗╚════██║████╗░████║██╔══██╗
██╔████╔██║███████║██╔██╗██║███████║░░███╔═╝██╔████╔██║███████║
██║╚██╔╝██║██╔══██║██║╚████║██╔══██║██╔══╝░░██║╚██╔╝██║██╔══██║
██║░╚═╝░██║██║░░██║██║░╚███║██║░░██║███████╗██║░╚═╝░██║██║░░██║
╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝╚══════╝╚═╝░░░░░╚═╝╚═╝░░╚═╝  

🚀 Script by: @MEIMEIZK 🚀
"""

print(WATERMARK)

# Load environment variables dari .env
load_dotenv()

# Konfigurasi RPC Monad Testnet
RPC_URL = "https://testnet-rpc.monad.xyz/"
web3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={'timeout': 60}))

if web3.is_connected():
    logging.info("Berhasil terhubung ke RPC Monad Testnet!")
else:
    logging.error("Gagal terhubung ke RPC Monad Testnet!")
    exit()

# Ambil private key dari .env
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
if not PRIVATE_KEY:
    logging.error("PRIVATE_KEY tidak ditemukan di .env!")
    exit()

WALLET_ADDRESS = web3.eth.account.from_key(PRIVATE_KEY).address
logging.info(f"Wallet Address: {WALLET_ADDRESS}")

# Konversi alamat ke checksum
MAGMA_STAKING_CONTRACT = Web3.to_checksum_address("0x2c9C959516e9AAEdB2C748224a41249202ca8BE7")
WMONAD_CONTRACT = Web3.to_checksum_address("0x760AfE86e5de5fa0Ee542fc7B7B713e1c5425701")
USDC_CONTRACT = Web3.to_checksum_address("0xf817257fed379853cDe0fa4F97AB987181B1E5Ea")
MONORAIL_CONTRACT = Web3.to_checksum_address("0xB91e5D9f7D6b5E1c8b3D0f6C6C4e36A52748C3fD")

# ABI untuk kontrak
MAGMA_STAKING_ABI = '[{"inputs":[],"name":"depositMon","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"withdrawMon","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
WMONAD_ABI = '[{"inputs":[],"name":"deposit","outputs":[],"stateMutability":"payable","type":"function"}]'
MONORAIL_ABI = '[{"inputs":[{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"minAmountOut","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[],"stateMutability":"payable","type":"function"}]'

# Inisialisasi kontrak
staking_contract = web3.eth.contract(address=MAGMA_STAKING_CONTRACT, abi=MAGMA_STAKING_ABI)
wmonad_contract = web3.eth.contract(address=WMONAD_CONTRACT, abi=WMONAD_ABI)
monorail_contract = web3.eth.contract(address=MONORAIL_CONTRACT, abi=MONORAIL_ABI)

def get_mon_balance():
    return web3.eth.get_balance(WALLET_ADDRESS) / 10**18

def human_like_delay():
    delay = random.uniform(30, 180)
    logging.info(f"Menunggu {delay:.2f} detik sebelum transaksi berikutnya...")
    time.sleep(delay)

def stake_mon():
    try:
        amount_wei = web3.to_wei(random.uniform(0.001, 0.01), 'ether')
        tx = staking_contract.functions.depositMon().build_transaction({
            'from': WALLET_ADDRESS,
            'value': amount_wei,
            'gas': random.randint(100000, 150000),
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(WALLET_ADDRESS)
        })
        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        logging.info(f"Staking berhasil! TX Hash: {web3.to_hex(tx_hash)}")
    except Exception as e:
        logging.error(f"Gagal staking: {str(e)}")
    human_like_delay()

def unstake_mon():
    try:
        amount_wei = web3.to_wei(random.uniform(0.001, 0.005), 'ether')
        tx = staking_contract.functions.withdrawMon(amount_wei).build_transaction({
            'from': WALLET_ADDRESS,
            'gas': random.randint(100000, 150000),
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(WALLET_ADDRESS)
        })
        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        logging.info(f"Unstake berhasil! TX Hash: {web3.to_hex(tx_hash)}")
    except Exception as e:
        logging.error(f"Gagal unstake: {str(e)}")
    human_like_delay()

def swap_mon():
    try:
        amount_wei = web3.to_wei(random.uniform(0.001, 0.005), 'ether')
        min_out = int(amount_wei * 0.9)
        tx = monorail_contract.functions.swapExactETHForTokens(USDC_CONTRACT, amount_wei, min_out).build_transaction({
            'from': WALLET_ADDRESS,
            'value': amount_wei,
            'gas': random.randint(200000, 300000),
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(WALLET_ADDRESS)
        })
        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        logging.info(f"Swap MON ke USDC berhasil! TX Hash: {web3.to_hex(tx_hash)}")
    except Exception as e:
        logging.error(f"Gagal swap: {str(e)}")
    human_like_delay()

tx_counter = 0
while True:
    if get_mon_balance() <= 0.2:
        logging.warning("Saldo MON kurang dari 0.2 MON, menghentikan semua transaksi!")
        break
    random.choice([stake_mon, unstake_mon, swap_mon])()
    tx_counter += 1
    if tx_counter >= random.randint(80, 100):
        sleep_time = random.randint(28800, 86400)
        logging.info(f"Jeda panjang selama {sleep_time / 3600:.2f} jam...")
        time.sleep(sleep_time)
        tx_counter = 0
