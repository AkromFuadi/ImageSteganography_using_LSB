import cv2
import numpy as np

def generate_playfair_matrix(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key = key.upper().replace("J", "I")
    key = "".join(sorted(set(key), key=key.index))
    combined_key = key + ''.join([char for char in alphabet if char not in key])
    return [combined_key[i:i + 5] for i in range(0, 25, 5)]

def find_char_position(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
    return None, None

def clean_text_for_playfair(text):
    text = text.upper().replace("J", "I")
    cleaned_text = "".join(char for char in text if char in "ABCDEFGHIKLMNOPQRSTUVWXYZ")
    cleaned_text += 'X' * (len(cleaned_text) % 2)
    return cleaned_text

def print_playfair_matrix(matrix):
    for row in matrix:
        print(row)

def playfair_encrypt(key, plaintext):
    matrix = generate_playfair_matrix(key)
    plaintext = clean_text_for_playfair(plaintext)
    ciphertext = []

    print_playfair_matrix(matrix)

    for i in range(0, len(plaintext), 2):
        char1, char2 = plaintext[i], plaintext[i + 1]
        print(f"Memproses karakter: {char1} dan {char2}")
    
    for i in range(0, len(plaintext), 2):
        char1, char2 = plaintext[i], plaintext[i + 1]
        
        position1 = find_char_position(matrix, char1)
        position2 = find_char_position(matrix, char2)
        
        if position1[0] is None or position1[1] is None or position2[0] is None or position2[1] is None:
            raise ValueError(f"Karakter {char1} atau {char2} tidak ditemukan dalam matriks!")
        
        row1, col1 = position1
        row2, col2 = position2
        
        if row1 == row2:
            ciphertext.extend([matrix[row1][(col1 + 1) % 5], matrix[row2][(col2 + 1) % 5]])
        elif col1 == col2:
            ciphertext.extend([matrix[(row1 + 1) % 5][col1], matrix[(row2 + 1) % 5][col2]])
        else:
            ciphertext.extend([matrix[row1][col2], matrix[row2][col1]])
    
    return ''.join(ciphertext)

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def main():
    key = input("Masukkan kunci untuk enkripsi: ")
    plaintext = input("Masukkan pesan yang ingin Anda enkripsi: ")
    ciphertext = playfair_encrypt(key, plaintext)
    
    input_image_path = "c:\\Users\\KURO\\Desktop\\apkri\\example.jpg"
    output_image_path = "c:\\Users\\KURO\\Desktop\\apkri\\example_with_message.jpg"
    
    lsb_embed(ciphertext, input_image_path, output_image_path)

def lsb_embed(ciphertext, input_image_path, output_image_path):
    image = cv2.imread(input_image_path)
    
    if image is None:
        raise ValueError(f"File gambar {input_image_path} tidak dapat dibaca.")
    
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
    
    cv2.imwrite(output_image_path, image)
    print(f"Pesan berhasil disisipkan dalam {output_image_path}")

if __name__ == "__main__":
    main()