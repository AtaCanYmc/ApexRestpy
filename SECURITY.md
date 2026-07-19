# Güvenlik Politikası

## Desteklenen Sürümler

Güvenlik yamaları yalnızca en son kararlı sürüm için yayınlanır.

| Sürüm | Destek Durumu |
|---|---|
| `1.x` (en güncel) | ✅ Aktif destek |
| `< 1.0` | ❌ Destek yok |

---

## Güvenlik Açığı Bildirimi

> [!CAUTION]
> Güvenlik açıklarını **asla** GitHub Issues olarak bildirmeyin. Issues herkese açıktır; bu durum açığın kamuya yayılmasına neden olabilir.

### Bildirme Kanalı

Tespit ettiğiniz güvenlik açığını doğrudan e-posta ile bildirin:

📧 **[atacanymc@gmail.com](mailto:atacanymc@gmail.com)**

**E-posta konusu:** `[SECURITY] ApexRestpy - <Kısa açıklama>`

### E-postanıza Dahil Edin

- **Açıklama:** Güvenlik açığının ne olduğu ve nerede bulunduğu
- **Etki analizi:** Hangi kullanıcılar veya sistemler etkilenebilir?
- **Tekrarlama adımları:** Açığı yeniden oluşturmak için minimal örnek
- **Çözüm önerisi:** Varsa önerilen düzeltme veya geçici çözüm
- **Keşif tarihi:** Açığı ne zaman fark ettiğiniz

---

## Yanıt Süreci

| Aşama | Süre |
|---|---|
| Bildirim alındığının onaylanması | **48 saat** içinde |
| İlk değerlendirme ve ciddiyet tespiti | **7 gün** içinde |
| Düzeltme yayınlanması (patch release) | **90 gün** içinde |
| Kamuoyu bildirimi (CVE veya Release Notes) | Düzeltme yayınından sonra |

---

## Kapsam

Aşağıdaki kategoriler bu güvenlik politikası kapsamındadır:

- **Kimlik bilgisi sızıntısı:** Bearer token veya konfigürasyonun kasıtsız olarak açığa çıkması
- **HTTPS bypass:** SSL doğrulamasının atlatılabilmesi
- **Bağımlılık güvenlik açıkları:** `requests` kütüphanesindeki kritik CVE'ler
- **Injection saldırıları:** URL veya başlıklarda kontrol edilmemiş kullanıcı girdisi

Aşağıdakiler kapsam **dışındadır:**

- Kullanıcının kendi geliştirme ortamındaki konfigürasyon hataları
- APEX sunucusunun kendisindeki güvenlik sorunları
- Test ortamına veya CI'a özgü sorunlar

---

## Sorumlu Açıklama (Responsible Disclosure)

Bu proje [Coordinated Vulnerability Disclosure](https://cheatsheetseries.owasp.org/cheatsheets/Vulnerability_Disclosure_Cheat_Sheet.html) ilkesini benimser. Bildirimin ardından:

1. Sorunu birlikte değerlendiririz.
2. Düzeltme hazırlanır ve test edilir.
3. Yeni sürüm yayınlanır.
4. Kamuoyu bildirimi yapılır; katkınız için teşekkür edilir (isterseniz isminiz belirtilir).

Güvenlik araştırmacılarının katkılarına değer veriyor ve bu süreci mümkün olduğunca şeffaf yürütmeye çalışıyoruz.

---

## İletişim

- **E-posta:** [atacanymc@gmail.com](mailto:atacanymc@gmail.com)
- **GitHub:** [AtaCanYmc](https://github.com/AtaCanYmc)
