def ksa(iv, kunci):
# Key-Scheduling Algorithm (KSA)
# Mengacak array S (0-255) berdasarkan Kunci (Key) yang diberikan
    full_key_string = iv + kunci
    full_key = [ord(c) for c in full_key_string]
    key_length = len(full_key)
    
    # 1. Membuat S array (0-255)
    S = list(range(256)) 
    
    # 2. Membuat T array (Mengulang kunci sampai 256 elemen)
    T = [full_key[i % key_length] for i in range(256)]
    
    j = 0
    # Mengacak S array menggunakan T array
    for i in range(256):
        j = (j + S[i] + T[i]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def prga(S):
# Pseudo-Random Generation Algorithm (PRGA)
# Menghasilkan aliran kunci (keystream) terus-menerus
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        
        K = S[(S[i] + S[j]) % 256]   # Ambil nilai K dari array S yang sudah diacak
        yield K # yield digunakan agar fungsi ini menjadi generator aliran kunci

def rc4_encrypt_decrypt(iv,key_string, text_string):
# Fungsi utama untuk Enkripsi dan Dekripsi.
    key = [ord(c) for c in key_string] # Ord untuk string kunci menjadi bentuk angka (ASCII)
    
    # Inisialisasi KSA dan PRGA
    S = ksa(iv, key_string)
    keystream = prga(S)

    hasil = []
    
    for char in text_string:
        # Ubah karakter teks menjadi angka ASCII (jika dia string)
        if isinstance(char, str):
            char_val = ord(char)
        else:
            char_val = char # Jika sudah berupa angka (saat dekripsi)
            
        hasil_xor = char_val ^ next(keystream) # Next untuk mendapatkan nilai K berikutnya dari PRGA lalu dia tidur
        hasil.append(hasil_xor)
        
    return hasil

if __name__ == '__main__':   
    iv = "IV123"
    kunci = input("Masukkan Kunci (Password) : ")
    plaintext = input("Masukkan Teks (Plaintext) : ")
    
    print("-" * 50)
    buka_kunci = input("Masukkan Kunci untuk Membuka (Dekripsi) : ")
    print("-" * 50)
    
    # Proses Enkripsi
    ciphertext_nums = rc4_encrypt_decrypt(iv, kunci, plaintext)
    print(f"[ENKRIPSI] Ciphertext       : {ciphertext_nums}")
    
    # Proses Dekripsi
    decrypted_nums = rc4_encrypt_decrypt(iv, buka_kunci, ciphertext_nums)
    decrypted_text = ''.join([chr(num) for num in decrypted_nums]) # chr untuk ubah kembali angka hasil dekripsi menjadi karakter & join untuk gabungkan karakter menjadi string
    print(f"[DEKRIPSI] Teks Kembali     : {decrypted_text}")
    print("-" * 50)
    
    # Hasil
    if plaintext == decrypted_text:
        print("Sukses!")
    else:
        print("Gagal.")