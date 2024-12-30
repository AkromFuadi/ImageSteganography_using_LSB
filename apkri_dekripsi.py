import cv2
import numpy as np
import re

def validate_key(key):
    # Memastikan kunci hanya berisi alfabet kapital
    if not re.match("^[A-Z]+$", key):
        raise ValueError("Kunci harus berisi hanya alfabet kapital!")

def lsb_extract(image_path):
    image = cv2.imread(image_path)
    
    if image is None:
        raise ValueError(f"File gambar {image_path} tidak dapat dibaca. Periksa path dan format file Anda.")
    
    extracted_binary = ""
    
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for k in range(3):  # Loop melalui channel warna (B, G, R)
                # Ambil bit paling tidak signifikan dari setiap piksel
                extracted_binary += str(image[i, j, k] & 1)
    
    # Memeriksa bahwa setiap karakter dalam extracted_binary adalah '0' atau '1'
    if not all(bit in '01' for bit in extracted_binary):
        raise ValueError("String biner yang diekstrak tidak valid!")
    
    # Memastikan panjang string biner adalah kelipatan 8
    padding_length = 8 - (len(extracted_binary) % 8)
    extracted_binary += '0' * padding_length
    
    extracted_text = "".join([chr(int(extracted_binary[i:i+8], 2)) for i in range(0, len(extracted_binary), 8)])
    
    return extracted_text

def generate_playfair_matrix(key):
    # Inisialisasi alfabet
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    # Konversi kunci ke huruf kapital dan hilangkan duplikasi
    key = key.upper().replace("J", "I")
    key = "".join(sorted(set(key), key=key.index))

    # Gabungkan kunci dengan alfabet tanpa duplikasi
    combined_key = key + ''.join([char for char in alphabet if char not in key])

    # Buat matriks 5x5 untuk Playfair Cipher
    matrix = [combined_key[i:i + 5] for i in range(0, 25, 5)]

    return matrix

def find_position(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
    # Jika karakter tidak ditemukan, kembalikan None
    return None

def is_valid_playfair_char(char):
    # Fungsi ini memeriksa apakah karakter adalah karakter valid untuk Playfair Cipher.
    valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return char in valid_chars

def playfair_decrypt(key, ciphertext):
    matrix = generate_playfair_matrix(key)
    
    if len(ciphertext) % 2 != 0:
        ciphertext += 'X'
    
    plaintext = ""
    
    pairs = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]
    
    for pair in pairs:
        char1, char2 = pair[0], pair[1]
        
        # Mengganti 'J' dengan 'I' saat mendekripsi
        if char1 == 'J':
            char1 = 'I'
        if char2 == 'J':
            char2 = 'I'
        
        # Periksa apakah kedua karakter valid
        if not (is_valid_playfair_char(char1) and is_valid_playfair_char(char2)):
            continue  # Abaikan pasangan ini jika salah satu karakter tidak valid
        
        position1 = find_position(matrix, char1)
        position2 = find_position(matrix, char2)
        
        if position1 is None or position2 is None:
            raise ValueError(f"Karakter {char1} atau {char2} tidak ditemukan dalam matriks!")
        
        row1, col1 = position1
        row2, col2 = position2
        
        if col1 == col2:
            plaintext += matrix[(row1 - 1) % 5][col1]
            plaintext += matrix[(row2 - 1) % 5][col2]
        else:
            plaintext += matrix[row1][col2]
            plaintext += matrix[row2][col1]
    
    return plaintext

def main():
    key = input("Masukkan kunci untuk dekripsi: ").upper()
    
    try:
        # Validasi kunci sebelum digunakan
        validate_key(key)
    except ValueError as e:
        print(e)
        return  # Keluar dari program jika kunci tidak valid
    
    stego_image_path = "c:\\Users\\KURO\\Desktop\\apkri\\example_with_message.jpg"
    
    try:
        extracted_message = lsb_extract(stego_image_path)
        
        if not extracted_message:
            print("Tidak ada pesan yang diekstrak dari gambar.")
            return  # Keluar dari program jika tidak ada pesan yang diekstrak
        
        plaintext = playfair_decrypt(key, extracted_message)
        print(f"Pesan yang diekstrak dari citra adalah: {plaintext}")
        
    except ValueError as e:
        print(f"Kesalahan dalam proses dekripsi: {e}")
        return  # Keluar dari program jika ada kesalahan

if __name__ == "__main__":
    main()