1. buat file .env isinya
```
PRIVATE_KEY=0x(private key lu)
INFURA_URL=rpc url lu
```
3. pip install web3
4. pip install python-dotenv
5. isi address sesuai di txtnya
6. ganti chain id di fungsi send_transaction jadi ngikutin rpcnya
 ```
    transaction = {
        'to': Web3.to_checksum_address(to_address),
        'value': web3.to_wei(value_ether, 'ether'),
        'gas': 21000,
        'gasPrice': gas_price,
        'nonce': nonce,
        'chainId': 2810  #<<Ubah
    }
    
```

8. py auto_tx.py
