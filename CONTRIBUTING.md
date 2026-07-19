# Projeye Katkı Sağlama Rehberi

ApexRestpy'a katkıda bulunmak istediğiniz için teşekkür ederiz! Bu belge, süreci olabildiğince verimli ve tutarlı hale getirmek için izlemeniz gereken adımları açıklar.

## İçindekiler

- [Davranış Kuralları](#davranış-kuralları)
- [Nasıl Katkıda Bulunabilirim?](#nasıl-katkıda-bulunabilirim)
- [Geliştirme Ortamı Kurulumu](#geliştirme-ortamı-kurulumu)
- [Kod Standartları](#kod-standartları)
- [Test Yazma Kuralları](#test-yazma-kuralları)
- [Commit ve PR Kuralları](#commit-ve-pr-kuralları)
- [Release Süreci](#release-süreci)

---

## Davranış Kuralları

Bu projeye katkıda bulunan herkesin saygılı ve kapsayıcı bir ortam oluşturmasını bekliyoruz. Ayrımcı, taciz edici veya saldırgan davranışlar kabul edilmez.

---

## Nasıl Katkıda Bulunabilirim?

### 🐛 Hata Bildirimi

1. [GitHub Issues](https://github.com/AtaCanYmc/ApexRestpy/issues) sayfasını açın.
2. "Bug Report" şablonunu seçin.
3. Aşağıdakileri eksiksiz doldurun:
   - Python sürümü ve işletim sistemi
   - Hatayı tekrarlamak için minimal kod örneği
   - Beklenen davranış ve gözlenen davranış
   - Varsa tam hata mesajı / traceback

### 💡 Özellik Önerisi

1. [GitHub Issues](https://github.com/AtaCanYmc/ApexRestpy/issues) sayfasını açın.
2. "Feature Request" şablonunu seçin.
3. Özelliğin hangi sorunu çözdüğünü ve nasıl çalışması gerektiğini açıklayın.

### 🔧 Kod Katkısı (Pull Request)

Kod katkısı için aşağıdaki adımları takip edin.

---

## Geliştirme Ortamı Kurulumu

```bash
# 1. Repoyu fork'la, ardından klonla
git clone https://github.com/<your-username>/ApexRestpy.git
cd ApexRestpy

# 2. Sanal ortam oluştur
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\Activate.ps1    # Windows PowerShell

# 3. Geliştirme bağımlılıklarıyla paketi yükle
pip install -e ".[dev]"

# 4. Kurulumu doğrula
python -m pytest tests/ -v
ruff check .
mypy apex_restpy --ignore-missing-imports
```

---

## Kod Standartları

Bu proje kalite kontrolü için aşağıdaki araçları kullanır:

| Araç | Amaç | Komut |
|---|---|---|
| **Ruff** | Lint + format | `ruff check . && ruff format .` |
| **mypy** | Statik tip kontrolü | `mypy apex_restpy --ignore-missing-imports` |
| **pytest** | Unit testler | `python -m pytest tests/ -v` |

### Kurallar

- **Satır uzunluğu:** Maksimum 100 karakter (`ruff` otomatik uygular)
- **Import sırası:** `isort` uyumlu (ruff tarafından otomatik düzenlenir)
- **Tip İpuçları:** Tüm public fonksiyon imzaları tip annotasyonu içermelidir
- **Docstring:** Tüm public metodlar Google-style docstring içermelidir
- **snake_case:** Tüm fonksiyon ve değişken adları `snake_case` olmalıdır

### Kod kalitesini PR öncesi doğrulama

```bash
# Tüm kontrolleri sırayla çalıştır
ruff check . && ruff format --check . && mypy apex_restpy --ignore-missing-imports && python -m pytest tests/ -v
```

---

## Test Yazma Kuralları

Her yeni özellik veya hata düzeltmesi için unit test yazılması **zorunludur**.

### İlkeler

- **Mock kullan:** Tüm HTTP istekleri `unittest.mock.MagicMock` ile simüle edilmelidir. Gerçek ağ bağlantısına ihtiyaç duyan testler kabul edilmez.
- **Her senaryo için ayrı test metodu:** Bir test metodu yalnızca bir senaryoyu kapsamalıdır.
- **Anlamlı isimler:** `test_<metodAdı>_<senaryo>` formatı kullanılmalıdır. Örn: `test_send_request_returns_empty_dict_on_connection_failure`
- **Assertion açıklaması:** `assertEqual`, `assertIn`, `assertRaises` gibi spesifik assertion metodları kullanılmalıdır.

### Test Çalıştırma

```bash
# Temel çalıştırma
python -m pytest tests/ -v

# Coverage ile
python -m pytest tests/ -v --cov=apex_restpy --cov-report=term-missing

# Belirli bir test sınıfı
python -m pytest tests/test_apex_bridge.py::TestSendRequestGet -v

# Belirli bir test metodu
python -m pytest tests/test_apex_bridge.py::TestSendRequestGet::test_get_returns_parsed_json -v
```

---

## Commit ve PR Kuralları

### Commit Mesajı Formatı (Conventional Commits)

Bu proje [Conventional Commits](https://www.conventionalcommits.org/) standardını zorunlu kılar. Release Please bu mesajları analiz ederek otomatik CHANGELOG üretir ve sürüm numarasını belirler.

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### Tip Tablosu

| Tip | Versiyon Etkisi | Kullanım |
|---|---|---|
| `feat:` | **minor** (`1.x.0`) | Yeni özellik |
| `fix:` | **patch** (`1.0.x`) | Hata düzeltme |
| `docs:` | Yok | Yalnızca dokümantasyon |
| `test:` | Yok | Test ekleme veya düzeltme |
| `refactor:` | Yok | Yeniden yapılandırma (davranış değişmez) |
| `perf:` | **patch** | Performans iyileştirme |
| `chore:` | Yok | Bağımlılık güncellemeleri, CI |
| `BREAKING CHANGE:` | **major** (`x.0.0`) | Geriye dönük uyumsuz değişiklik |

#### Örnekler

```bash
# Yeni özellik
git commit -m "feat: add retry mechanism for transient connection failures"

# Hata düzeltme
git commit -m "fix: correctly append ampersand when URL already has query params"

# Breaking change
git commit -m "feat!: rename send_request payload parameter to body

BREAKING CHANGE: The `payload` parameter has been renamed to `body` for clarity."
```

### Pull Request Kontrol Listesi

PR açmadan önce aşağıdakileri kontrol edin:

- [ ] `ruff check .` — sıfır hata
- [ ] `ruff format --check .` — sıfır değişiklik
- [ ] `mypy apex_restpy` — sıfır hata
- [ ] `python -m pytest tests/ -v` — tüm testler geçiyor
- [ ] Yeni özellik/düzeltme için test yazıldı
- [ ] Genel API değişikliklerinde `README.md` güncellendi
- [ ] Commit mesajları Conventional Commits formatında

---

## Release Süreci

Release'ler tamamen otomatiktir ve manuel müdahale gerektirmez:

1. `main` branch'e `feat:` veya `fix:` commit'i push edilir.
2. **Release Please** GitHub Action çalışır, CHANGELOG ve versiyon değişikliklerini içeren bir PR açar.
3. Maintainer bu PR'ı inceler ve merge eder.
4. Merge sonrasında:
   - GitHub Release otomatik oluşturulur.
   - Paket PyPI'ya otomatik yayınlanır (OIDC Trusted Publishing).
   - Dist dosyaları GitHub Release'e eklenir.

---

Sorularınız için [Discussions](https://github.com/AtaCanYmc/ApexRestpy/discussions) bölümünü veya doğrudan [atacanymc@gmail.com](mailto:atacanymc@gmail.com) adresini kullanabilirsiniz.
