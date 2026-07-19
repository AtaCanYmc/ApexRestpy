<div align="center">

# 🌉 ApexRestpy

### Oracle APEX RESTful API İstemcisi — Python

*[ApexBridge C++ Arduino Kütüphanesinin](https://github.com/AtaCanYmc/ApexBridge) Python Uyarlaması*

---

[![CI](https://github.com/AtaCanYmc/ApexRestpy/actions/workflows/ci.yml/badge.svg)](https://github.com/AtaCanYmc/ApexRestpy/actions/workflows/ci.yml)
[![Release](https://github.com/AtaCanYmc/ApexRestpy/actions/workflows/release-please.yml/badge.svg)](https://github.com/AtaCanYmc/ApexRestpy/actions/workflows/release-please.yml)
[![PyPI version](https://img.shields.io/pypi/v/apex-restpy.svg?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/apex-restpy/)
[![Python Versions](https://img.shields.io/pypi/pyversions/apex-restpy.svg?logo=python&logoColor=white)](https://pypi.org/project/apex-restpy/)
[![codecov](https://codecov.io/gh/AtaCanYmc/ApexRestpy/branch/main/graph/badge.svg)](https://codecov.io/gh/AtaCanYmc/ApexRestpy)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://img.shields.io/pypi/dm/apex-restpy.svg?color=green)](https://pypi.org/project/apex-restpy/)

</div>

---

## 📋 İçindekiler

- [Yönetici Özeti](#-yönetici-özeti)
- [Temel Özellikler](#-temel-özellikler)
- [Mimari ve Akış](#-mimari-ve-akış)
- [Teknoloji Yığını](#-teknoloji-yığını)
- [Ön Koşullar](#-ön-koşullar)
- [Kurulum](#-kurulum)
- [Hızlı Başlangıç](#-hızlı-başlangıç)
- [Kullanım ve API Referansı](#-kullanım-ve-api-referansı)
- [Çevre Değişkenleri](#-çevre-değişkenleri)
- [Test Süreçleri](#-test-süreçleri)
- [Projeye Katkı Sağlama](#-projeye-katkı-sağlama)
- [Güvenlik Politikası](#-güvenlik-politikası)
- [Lisans ve İletişim](#-lisans-ve-iletişim)

---

## 🎯 Yönetici Özeti

**ApexRestpy**, Oracle APEX RESTful servisleriyle Python uygulamalarından hızla iletişim kurmanızı sağlayan hafif, sıfır-bağımlılıklı (yalnızca `requests`) bir istemci kütüphanesidir. Mikrodenetleyiciler (ESP32/ESP8266) için C++ ile yazılmış [ApexBridge](https://github.com/AtaCanYmc/ApexBridge) kütüphanesinin birebir Python uyarlamasıdır; aynı mantıksal API'yi sunucu, Raspberry Pi, otomasyon scripti ve CI/CD pipeline'larında kullanabilirsiniz.

Oracle APEX'in standart `/<base_path>/<schema>/<module>/<resource>` URL yapısını soyutlayan kütüphane, Bearer token kimlik doğrulamasını, query parametre yönetimini ve tüm HTTP metodlarını (GET/POST/PUT/PATCH/DELETE) birleşik ve test edilmesi kolay bir arayüzde sunar. Sıfır konfigürasyonla HTTPS bağlantısı kurulur; SSL sertifika yönetimi tamamen `requests + certifi` tarafından otomatik sağlanır.

**Hedef kitle:** Oracle APEX backend'ini kullanan Python geliştiricileri, IoT entegrasyon mühendisleri ve Arduino ekosisteminden Python'a geçiş yapan gömülü sistem geliştiricileri.

---

## ✨ Temel Özellikler

| Özellik | Açıklama |
|---|---|
| 🔗 **Sorunsuz APEX İletişimi** | `schema/module/resource` URL kalıbıyla otomatik endpoint inşası |
| 🔒 **Otomatik HTTPS** | `requests + certifi` ile sıfır konfigürasyonlu SSL — manuel sertifika yok |
| 🔑 **Bearer Token Kimlik Doğrulama** | `set_token()` ile tek satırda OAuth/JWT entegrasyonu |
| 🛠️ **Tam HTTP Desteği** | GET · POST · PUT · PATCH · DELETE |
| 🧩 **Akıcı URL Yönetimi** | `prepare_url()` + `add_parameter()` + `add_path()` zincirleme API |
| 🐍 **Pythonic Tasarım** | `snake_case`, `@dataclass`, type hints, `logging` modülü |
| ⚡ **Hafif** | Tek harici bağımlılık: `requests>=2.28` |
| 🧪 **Yüksek Test Kapsamı** | 38 unit test, mock HTTP — gerçek ağ gerekmez |
| 🔄 **Oturum Yönetimi** | `requests.Session` ile bağlantı yeniden kullanımı |
| 📦 **Paketlenebilir** | `pip install apex-restpy` ile standart PyPI kurulumu |

---

## 🏗️ Mimari ve Akış

ApexRestpy, uygulamanız ile Oracle APEX sunucusu arasında ince bir soyutlama katmanı görevi görür:

```mermaid
flowchart LR
    subgraph Uygulama["Uygulamanız"]
        direction TB
        A["bridge = ApexBridge(schema)"]
        B["bridge.set_token(token)"]
        C["bridge.prepare_url(module, resource)"]
        D["bridge.add_parameter(k, v)"]
        E["bridge.send_request('GET')"]
    end

    subgraph ApexRestpy["apex_restpy Katmanı"]
        direction TB
        AB["ApexBridge"]
        APP["ApexApp @dataclass"]
        EXC["ApexConnectionError\nApexResponseError"]
        AB --> APP
        AB --> EXC
    end

    subgraph HTTP["HTTP Katmanı"]
        REQ["requests.Session\n(HTTPS + certifi)"]
    end

    subgraph APEX["Oracle APEX"]
        ORDS["APEX REST Services\nhttps://apex.oracle.com/pls/apex/\n{schema}/{module}/{resource}"]
    end

    Uygulama --> ApexRestpy
    ApexRestpy --> HTTP
    HTTP -->|"HTTPS GET/POST/PUT/PATCH/DELETE"| APEX
    APEX -->|"JSON Response"| HTTP
    HTTP -->|"dict"| ApexRestpy
    ApexRestpy -->|"dict"| Uygulama
```

### URL İnşa Süreci

```
ApexApp.base_path  +  schema  +  module  +  resource  [?param=val&...]  [/path]
    /pls/apex      /  myschema /  sensor  /   data     ?id=42&type=temp  /details

→ https://apex.oracle.com/pls/apex/myschema/sensor/data/details?id=42&type=temp
```

### Paket Yapısı

```
apex_restpy/
├── __init__.py          # Public API: ApexBridge, ApexApp, hatalar
├── apex_bridge.py       # Ana istemci sınıfı
├── apex_app.py          # Konfigürasyon dataclass'ı
└── exceptions.py        # ApexConnectionError, ApexResponseError

tests/
└── test_apex_bridge.py  # 38 unit test (mock HTTP)

examples/
├── basic_get.py         # GET örneği
└── basic_post.py        # POST örneği
```

---

## 🛠️ Teknoloji Yığını

| Katman | Teknoloji | Versiyon |
|---|---|---|
| **Dil** | Python | ≥ 3.9 |
| **HTTP İstemci** | requests | ≥ 2.28.0 |
| **SSL** | certifi (requests bağımlılığı) | Otomatik |
| **Paketleme** | setuptools + pyproject.toml | PEP 517/518 |
| **Lint** | Ruff | ≥ 0.4.0 |
| **Tip Kontrolü** | mypy | ≥ 1.8.0 |
| **Test** | pytest + pytest-cov | ≥ 7.0 / ≥ 4.0 |
| **CI/CD** | GitHub Actions | — |
| **Sürüm Yönetimi** | Release Please | v4 |
| **Bağımlılık Güncellemeleri** | Dependabot | — |

---

## ✅ Ön Koşullar

Geliştirme ortamınızda aşağıdakilerin kurulu olması gerekir:

| Araç | Minimum Versiyon | Kontrol |
|---|---|---|
| Python | 3.9 | `python --version` |
| pip | 21.0 | `pip --version` |
| Git | 2.30 | `git --version` |

> [!NOTE]
> Kütüphane olarak yalnızca `requests` bağımlılığı vardır. Docker veya başka altyapı aracına gerek yoktur.

---

## 🚀 Kurulum

### PyPI'dan (Önerilen)

```bash
pip install apex-restpy
```

### Geliştirme Ortamı

```bash
# 1. Repoyu klonla
git clone https://github.com/AtaCanYmc/ApexRestpy.git
cd ApexRestpy

# 2. Sanal ortam oluştur ve aktifleştir
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate.bat     # Windows CMD
# .venv\Scripts\Activate.ps1     # Windows PowerShell

# 3. Geliştirme bağımlılıklarıyla birlikte paketi yükle
pip install -e ".[dev]"
```

### Kurulumu Doğrula

```bash
python -c "from apex_restpy import ApexBridge; print('✅ apex-restpy hazır!')"
```

---

## ⚡ Hızlı Başlangıç

```python
from apex_restpy import ApexBridge

# 1. Bridge'i başlat
bridge = ApexBridge(schema="myschema")

# 2. (İsteğe bağlı) Kimlik doğrulama token'ı ayarla
bridge.set_token("your-jwt-bearer-token")

# 3. Endpoint hazırla ve istek gönder
bridge.prepare_url("time", "now")
response = bridge.send_request()   # varsayılan: GET

# 4. Yanıtı kullan
print(response["full_timestamp"])  # → "2025-03-02T14:30:00"
print(response["year"])            # → 2025
```

---

## 📖 Kullanım ve API Referansı

### `ApexBridge(schema, base_path, host, timeout, debug, session)`

Ana istemci sınıfı. Tüm APEX iletişimi bu nesne üzerinden yürütülür.

```python
bridge = ApexBridge(
    schema="myschema",          # APEX workspace schema adı (zorunlu)
    base_path="/pls/apex",      # URL ön eki (varsayılan: "/pls/apex")
    host="apex.oracle.com",     # APEX sunucu adresi (varsayılan)
    timeout=10.0,               # İstek zaman aşımı saniye (varsayılan: 10)
    debug=False,                # True ise DEBUG log seviyesi etkin
)
```

---

### `set_token(token: str)`

Bearer token kimlik doğrulamasını etkinleştirir. Sonraki tüm isteklerde `Authorization: Bearer <token>` başlığı otomatik eklenir.

```python
bridge.set_token("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...")
```

> [!NOTE]
> Token uzunluğu 1 karakterden fazla olmalıdır (C++ orijinali ile birebir uyumluluk). Boş string verilirse başlık eklenmez.

---

### `prepare_url(module, resource, schema=None) → str`

APEX REST endpoint yolunu inşa eder ve dahili `_last_endpoint`'e kaydeder.

```python
url = bridge.prepare_url("sensor", "data")
# → "/pls/apex/myschema/sensor/data"

# Farklı schema ile
url = bridge.prepare_url("time", "now", schema="otherschema")
# → "/pls/apex/otherschema/time/now"
```

---

### `add_parameter(param, value, url=None) → str`

Aktif endpoint'e (veya verilen URL'ye) query parametresi ekler.

```python
bridge.prepare_url("sensor", "data")
bridge.add_parameter("id", "42")       # → ...?id=42
bridge.add_parameter("type", "temp")   # → ...?id=42&type=temp

# Özel URL üzerinde (son endpoint değişmez)
result = bridge.add_parameter("limit", "10", url="/pls/apex/myschema/items/list")
# → "/pls/apex/myschema/items/list?limit=10"
```

---

### `add_path(path, url=None) → str`

Aktif endpoint'e ek bir yol segmenti ekler.

```python
bridge.prepare_url("items", "list")
bridge.add_path("active")
# _last_endpoint → "/pls/apex/myschema/items/list/active"
```

---

### `send_request(method="GET", payload=None, url=None) → dict`

HTTP isteği gönderir ve JSON yanıtını `dict` olarak döner.

```python
# GET
response = bridge.send_request()

# POST — JSON gövdesiyle
response = bridge.send_request(
    method="POST",
    payload={"sensor_id": "42", "value": 23.5},
)

# PUT, PATCH, DELETE
bridge.send_request("PUT",   payload={"name": "updated"})
bridge.send_request("PATCH", payload={"status": "active"})
bridge.send_request("DELETE")

# Farklı URL'ye istek (son endpoint değişmez)
response = bridge.send_request("GET", url="/pls/apex/myschema/custom/path")
```

**Desteklenen metodlar:** `GET` · `POST` · `PUT` · `PATCH` · `DELETE`

---

### İstisnalar

| İstisna | Ne zaman fırlatılır |
|---|---|
| `ApexConnectionError` | Ağ bağlantısı kurulamazsa veya zaman aşımı |
| `ApexResponseError` | Yanıt geçerli JSON değilse |
| `ValueError` | Desteklenmeyen HTTP metodu girilirse |

```python
from apex_restpy import ApexBridge, ApexConnectionError, ApexResponseError

try:
    response = bridge.send_request()
except ApexConnectionError as e:
    print(f"Bağlantı hatası: {e}")
except ApexResponseError as e:
    print(f"Geçersiz yanıt: {e}")
```

---

### Tam Senaryo Örneği

```python
from apex_restpy import ApexBridge

bridge = ApexBridge(schema="iot_prod", timeout=15.0, debug=True)
bridge.set_token("your-jwt-token")

# Sayfalama ve filtreleme ile veri çekme
bridge.prepare_url("sensors", "readings")
bridge.add_parameter("device_id", "esp32-01")
bridge.add_parameter("limit", "100")
bridge.add_path("latest")
# → /pls/apex/iot_prod/sensors/readings/latest?device_id=esp32-01&limit=100

response = bridge.send_request("GET")

for reading in response.get("items", []):
    print(f"{reading['ts']} → {reading['value']} {reading['unit']}")
```

---

## 🔐 Çevre Değişkenleri

ApexRestpy bir CLI aracı veya servis değil, bir kütüphanedir; dolayısıyla kendi `.env` dosyası yoktur. Kimlik bilgilerini kullanan uygulamalarda aşağıdaki örüntüyü kullanmanızı tavsiye ederiz:

**`.env.example`** — Projenizde bu dosyayı referans alın:

```env
# Oracle APEX Konfigürasyonu
APEX_SCHEMA=your_schema_name
APEX_BASE_PATH=/pls/apex
APEX_HOST=apex.oracle.com
APEX_TIMEOUT=10

# Kimlik Doğrulama
APEX_BEARER_TOKEN=your_jwt_or_oauth_token
```

**Kullanım:**

```python
import os
from dotenv import load_dotenv
from apex_restpy import ApexBridge

load_dotenv()

bridge = ApexBridge(
    schema=os.environ["APEX_SCHEMA"],
    host=os.environ.get("APEX_HOST", "apex.oracle.com"),
    timeout=float(os.environ.get("APEX_TIMEOUT", "10")),
)
bridge.set_token(os.environ["APEX_BEARER_TOKEN"])
```

> [!CAUTION]
> `.env` dosyasını asla Git'e eklemeyin. `.gitignore` dosyamız bu dosyayı zaten dışlar.

---

## 🧪 Test Süreçleri

### Test Çalıştırma

```bash
# Tüm testleri çalıştır
pytest tests/ -v

# Coverage raporu ile
pytest tests/ -v --cov=apex_restpy --cov-report=term-missing

# HTML coverage raporu
pytest tests/ --cov=apex_restpy --cov-report=html
open htmlcov/index.html
```

### Test Matrisi

```
tests/
└── test_apex_bridge.py          38 test
    ├── TestPrepareUrl             4 test  — URL inşa mantığı
    ├── TestAddParameter           5 test  — Query string yönetimi
    ├── TestAddPath                3 test  — Path ekleme
    ├── TestSetToken               4 test  — Token ve başlık yönetimi
    ├── TestSendRequestGet         5 test  — GET istekleri
    ├── TestSendRequestPost        3 test  — POST istekleri ve payload
    ├── TestSendRequestOtherMethods 4 test — PUT / PATCH / DELETE
    ├── TestErrorHandling          3 test  — Hata yönetimi
    ├── TestBuildFullUrl           3 test  — URL normalleştirme
    └── TestProperties             4 test  — Read-only properties
```

> [!TIP]
> Tüm testler `unittest.mock.MagicMock` ile HTTP'yi simüle eder. Gerçek bir APEX sunucusuna veya ağ bağlantısına gerek yoktur.

### Lint ve Tip Kontrolü

```bash
# Lint
ruff check .

# Format kontrolü
ruff format --check .

# Otomatik format düzeltme
ruff format .

# Tip kontrolü
mypy apex_restpy --ignore-missing-imports
```

---

## 🤝 Projeye Katkı Sağlama

Katkılarınızı memnuniyetle karşılıyoruz! Detaylı rehber için [CONTRIBUTING.md](CONTRIBUTING.md) dosyasına bakın.

### Hızlı Başlangıç

```bash
# 1. Fork'la ve klonla
git clone https://github.com/<your-username>/ApexRestpy.git
cd ApexRestpy

# 2. Geliştirme ortamını kur
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# 3. Feature branch oluştur
git checkout -b feat/my-feature

# 4. Değişikliklerini yap, testleri çalıştır
pytest tests/ -v

# 5. Lint ve format kontrolü
ruff check . && ruff format --check . && mypy apex_restpy

# 6. Commit mesajını Conventional Commits formatında yaz
git commit -m "feat: add retry mechanism for connection failures"

# 7. PR aç
git push origin feat/my-feature
```

### Commit Mesajı Kuralları

Bu proje [Conventional Commits](https://www.conventionalcommits.org/) standardını kullanır:

| Prefix | Kullanım |
|---|---|
| `feat:` | Yeni özellik |
| `fix:` | Hata düzeltme |
| `docs:` | Yalnızca dokümantasyon |
| `test:` | Test ekleme veya düzeltme |
| `refactor:` | Kod yeniden yapılandırma |
| `chore:` | Bağımlılık güncellemeleri, CI |
| `BREAKING CHANGE:` | Geriye dönük uyumsuz değişiklik |

> Release Please bu mesajları analiz ederek otomatik CHANGELOG ve versiyon ataması yapar.

### Kod Standartları

- **Formatter:** Ruff (`line-length = 100`)
- **Linter:** Ruff (`E, W, F, I, B, UP` kuralları)
- **Tip kontrolü:** mypy (`warn_return_any = true`)
- **Test kapsamı:** Yeni özellikler için unit test zorunludur
- **Docstring:** Tüm public metotlara Google-style docstring

---

## 🔒 Güvenlik Politikası

Güvenlik açığı bildirimleri için lütfen [SECURITY.md](SECURITY.md) dosyasını okuyun.

**Özetle:** Açıkları GitHub Issues'a değil, doğrudan `atacanymc@gmail.com` adresine bildirin. 90 gün içinde düzeltme taahhüt edilir.

---

## 📜 Lisans ve İletişim

Bu proje **MIT Lisansı** altında dağıtılmaktadır. Ayrıntılar için [LICENSE](LICENSE) dosyasına bakın.

---

<div align="center">

**Ata Can Yaymacı**

[![Medium](https://img.shields.io/badge/Medium-%40atacanymc-black?logo=medium)](https://medium.com/@atacanymc)
[![GitHub](https://img.shields.io/badge/GitHub-AtaCanYmc-181717?logo=github)](https://github.com/AtaCanYmc)
[![Email](https://img.shields.io/badge/Email-atacanymc%40gmail.com-D14836?logo=gmail&logoColor=white)](mailto:atacanymc@gmail.com)

---

*C++ orijinali: [ApexBridge](https://github.com/AtaCanYmc/ApexBridge) — ESP32/ESP8266 için Arduino kütüphanesi*

⭐ Faydalı bulduysan GitHub'da yıldız vermeyi unutma!

</div>
