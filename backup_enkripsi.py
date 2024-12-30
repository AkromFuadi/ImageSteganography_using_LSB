import cv2
import numpy as np

# Fungsi untuk mengenkripsi teks dengan Playfair Cipher
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

def clean_text_for_playfair(text):
    # Konversi teks menjadi huruf besar dan ganti 'J' dengan 'I'
    text = text.upper().replace("J", "I")

    # Hapus karakter non-alfabet
    cleaned_text = ""
    for char in text:
        if char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
            cleaned_text += char

    # Tambahkan 'X' jika ada dua karakter yang sama atau panjangnya ganjil
    i = 0
    while i < len(cleaned_text):
        if i == len(cleaned_text) - 1:
            cleaned_text += 'X'
        elif cleaned_text[i] == cleaned_text[i + 1]:
            cleaned_text = cleaned_text[:i + 1] + 'X' + cleaned_text[i + 1:]
        i += 2

    # Cetak teks yang telah dibersihkan untuk pemeriksaan
    print(cleaned_text)

    return cleaned_text


def print_playfair_matrix(matrix):
    for row in matrix:
        print(row)

def playfair_encrypt(key, plaintext):
    matrix = generate_playfair_matrix(key)
    
    # Tampilkan matriks untuk pemeriksaan
    print_playfair_matrix(matrix)
    
    # Membersihkan teks sebelum enkripsi
    plaintext = clean_text_for_playfair(plaintext)
    
    ciphertext = []
    for i in range(0, len(plaintext), 2):
        char1, char2 = plaintext[i], plaintext[i + 1]
        
        # Debug: Tambahkan print untuk karakter
        print(f"Memproses karakter: {char1} dan {char2}")
        
    ciphertext = []
    for i in range(0, len(plaintext), 2):
        char1, char2 = plaintext[i], plaintext[i + 1]
        
        # Jika kedua karakter sama, tambahkan 'X' dan lanjutkan
        if char1 == char2:
            char2 = 'X'
        
        row1, col1 = find_char_position(matrix, char1)
        row2, col2 = find_char_position(matrix, char2)
        
        if row1 is None or col1 is None or row2 is None or col2 is None:
            raise ValueError(f"Karakter {char1} atau {char2} tidak ditemukan dalam matriks!")
        
        # Proses enkripsi menggunakan logika Playfair
        # Jika kedua karakter berada dalam baris yang sama
        if row1 == row2:
            ciphertext.append(matrix[row1][(col1 + 1) % 5])
            ciphertext.append(matrix[row2][(col2 + 1) % 5])
        # Jika kedua karakter berada dalam kolom yang sama
        elif col1 == col2:
            ciphertext.append(matrix[(row1 + 1) % 5][col1])
            ciphertext.append(matrix[(row2 + 1) % 5][col2])
        # Jika kedua karakter berada di baris dan kolom yang berbeda
        else:
            ciphertext.append(matrix[row1][col2])
            ciphertext.append(matrix[row2][col1])
        
    return ''.join(ciphertext)

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)


def find_char_position(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
    return None, None

def main():
    key = "KUNCI"
    plaintext = "HALOINIPESANRAHASIA"
    ciphertext = playfair_encrypt(key, plaintext)
    
    # Gantilah path berikut dengan path absolut ke file gambar Anda
    input_image_path = "c:\\Users\\KURO\\Desktop\\apkri\\insideout.jpg"  
    output_image_path = "c:\\Users\\KURO\\Desktop\\apkri\\insideout_with_message2.jpg"  

    lsb_embed(ciphertext, input_image_path, output_image_path)

def lsb_embed(ciphertext, input_image_path, output_image_path):
    # Membaca gambar dari path yang diberikan
    image = cv2.imread(input_image_path)

    # Memeriksa apakah gambar berhasil dibaca
    if image is None:
        raise ValueError(f"File gambar {input_image_path} tidak dapat dibaca. Periksa path dan format file Anda.")

    max_message_length = image.shape[0] * image.shape[1] * 3 // 8
    if len(ciphertext) > max_message_length:
        raise ValueError("Pesan terlalu panjang untuk disisipkan dalam citra ini.")

    binary_message = text_to_binary(ciphertext)

    message_index = 0
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for k in range(3):
                if message_index < len(binary_message):
                    pixel_value = image[i, j, k]
                    image[i, j, k] = pixel_value & 0xFE | int(binary_message[message_index])
                    message_index += 1
                else:
                    break

    output_path = "c:\\Users\\KURO\\Desktop\\apkri\\insideout_with_message.jpg"
    cv2.imwrite(output_path, image)
    print(f"Pesan berhasil disisipkan dalam {output_path}")

if __name__ == "__main__":
    main()