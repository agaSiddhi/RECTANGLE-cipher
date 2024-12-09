import cv2

def hex_to_alphabets(hex_string):
    # Ensure the hex string has an even length, else pad with a leading zero
    if len(hex_string) % 2 != 0:
        hex_string = '0' + hex_string

    # Convert hex to bytes
    byte_data = bytes.fromhex(hex_string)

    # Convert bytes to string using ASCII encoding
    decoded_string = byte_data.decode('ascii', errors='ignore')

    return decoded_string
    
def scan_and_decrypt_qr(image_path: str):
    
    d = cv2.QRCodeDetector()
    val, points, straight_code = d.detectAndDecode(cv2.imread(image_path))
    print(val)
    decrypted_data = decryption(val)
    print(f"Decrypted Data: {decrypted_data}")
    print("Original Message", hex_to_alphabets(decrypted_data))
scan_and_decrypt_qr("/content/message.png")
