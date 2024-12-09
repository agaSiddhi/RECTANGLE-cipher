# generate_qr.py
import qrcode
# from encryptor import encrypt

def generate_qr(message: str, output_file: str):
    # Encrypt the payment details
    encrypted_data = encryption(message)
    print("ENCRYPTED_DATA", encrypted_data)
    img = qrcode.make(encrypted_data)
    img.save(output_file)
    print(f"QR code saved as {output_file}")

if __name__ == "__main__":
    message = "SIDDHI"
    message_hex = ''.join(format(ord(char), '02X') for char in message)
    print(message_hex, len(message_hex))
    generate_qr(message_hex, "message.png")
    
    message = "1703MAR"
    message_hex = ''.join(format(ord(char), '02X') for char in message)
    print(message_hex, len(message_hex))
    generate_qr(message_hex, "birth.png")
