import time
from atproto import Client

# --- GİRİŞ BİLGİLERİ ---
HANDLE = "becaecosystem.bsky.social"
APP_PASSWORD = "2222-1111-0000-1111"
TARGET_ACCOUNT = "indiegameswtf.bsky.social"

client = Client()

def seri_takip_baslat():
    try:
        client.login(HANDLE, APP_PASSWORD)
        print(f"--- İŞLEM BAŞLADI (1.5sn Hızında) ---")
        
        cursor = None  # Sayfaları birbirine bağlayan anahtar
        toplam_islem = 0

        while True:
            # Takipçileri 50'şerli paketler halinde çekiyoruz
            followers_response = client.get_followers(actor=TARGET_ACCOUNT, cursor=cursor)
            
            for follower in followers_response.followers:
                user_did = follower.did
                user_handle = follower.handle
                
                try:
                    # Takip etme komutu
                    client.follow(user_did)
                    toplam_islem += 1
                    print(f"[{toplam_islem}] Yeni takip edildi: {user_handle}")
                    
                    # İstediğin 1.5 saniyelik bekleme
                    time.sleep(1.5)

                except Exception as e:
                    # Zaten takip ediliyorsa veya başka bir durum varsa burada yakalıyoruz
                    if "already" in str(e).lower():
                        print(f"Atlandı (Zaten takip ediliyor): {user_handle}")
                    elif "rate limit" in str(e).lower():
                        print("!!! Bluesky geçici olarak durdurdu (Limit). Biraz beklemen gerek.")
                        return
                    else:
                        print(f"Hata ({user_handle}): {e}")

            # Sonraki sayfanın anahtarını (cursor) al
            cursor = followers_response.cursor
            if not cursor:
                print("Hedef hesaptaki herkes tarandı. İşlem bitti!")
                break
                
            print(f"--- Sıradaki 50 kişilik sayfaya geçiliyor... ---")

    except Exception as e:
        print(f"Sistem hatası: {e}")

if __name__ == "__main__":
    seri_takip_baslat()