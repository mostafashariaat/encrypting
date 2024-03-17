key = base64.b64decode(encrypted_data['key'])
ciphertext = base64.b64decode(encrypted_data['ciphertext'])

# Create cipher
cipher = AES.new(key, AES.MODE_ECB)

# Decrypt
decrypted_padded = cipher.decrypt(ciphertext)

# Remove padding
# decrypted_data = unpad(decrypted_padded, AES.block_size)

# Print decrypted data, handling non-ASCII characters
# try:
#     print(decrypted_data.decode('utf-8'))
# except UnicodeEncodeError:
#     print("Decrypted data contains non-ASCII characters.")