from web3 import Web3
import json
import os
from dotenv import load_dotenv

# โหลด ENV
load_dotenv()

RPC_URL = os.getenv("ALCHEMY_API_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = "0xBE237d64F7fa5456d52F74710D97B0c1606eA8C6"

# โหลด ABI ของ Smart Contract
ABI_PATH = os.path.join(os.path.dirname(__file__), "../contracts/MorphixDAO_abi.json")

try:
    with open(ABI_PATH, "r") as file:
        ABI = json.load(file)
except FileNotFoundError:
    print(f"❌ Error: ABI file not found: {ABI_PATH}")
    exit()

# เชื่อมต่อ Web3
web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)

# โหลด Smart Contract
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

# ตรวจสอบยอดคงเหลือ
balance = web3.eth.get_balance(account.address)
eth_balance = web3.from_wei(balance, "ether")
print(f"🔹 Current Balance: {eth_balance} ETH")

def create_proposal(description):
    nonce = web3.eth.get_transaction_count(account.address)
    
    tx = contract.functions.createProposal(description).build_transaction({
        "from": account.address,
        "nonce": nonce,
        "gas": 2000000,
        "gasPrice": web3.to_wei("10", "gwei")
    })
    
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    print(f"✅ Proposal Created! Tx Hash: {web3.to_hex(tx_hash)}")

# สร้าง Proposal อัตโนมัติ
create_proposal("Increase Token Burn Rate")
