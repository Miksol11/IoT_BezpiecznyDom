# Przewodnik Home Assistant dla Projektu IoT - Od Podstaw

## 📚 Część 1: Dla Kompletnych Laików - Co to jest Home Assistant?

### Wyobraź sobie...

Masz w domu różne urządzenia: czujnik temperatury, inteligentne żarówki, kamery, sensory ruchu, itp. Każde z tych urządzeń ma swoją własną aplikację na telefonie. Home Assistant to **jedno miejsce**, gdzie możesz zobaczyć i kontrolować wszystko na raz.

**Prosta analogia:** 
- Bez Home Assistant = 10 różnych aplikacji do 10 różnych urządzeń
- Z Home Assistant = 1 aplikacja/strona internetowa do wszystkich urządzeń

### Co dokładnie robi Home Assistant?

1. **Zbiera dane** z twoich urządzeń (np. czujnik mówi "temperatura to 23°C")
2. **Pokazuje dane** na ładnym dashboardzie (tablicy rozdzielczej)
3. **Automatyzuje działania** (np. "jeśli temperatura > 30°C, wyślij mi powiadomienie")
4. **Działa lokalnie** - wszystko na twoim urządzeniu, bez wysyłania danych do chmury

### Jak to działa w kontekście waszego projektu?

W laboratorium robicie projekt **"Bezpieczny Dom"** z Raspberry Pi, prawda? Prawdopodobnie macie:
- 🌡️ Czujnik temperatury (BME280/DHT22)
- 💳 Czytnik RFID (do sejfu)
- 📊 Możliwe inne sensory

**Bez Home Assistant:**
- Musielibyście pisać własny kod do wyświetlania danych
- Trudno zrobić ładny interfejs graficzny
- Ciężko zobaczyć wykresy historyczne
- Brak łatwych automatyzacji

**Z Home Assistant:**
- ✅ Gotowy, piękny interfejs webowy
- ✅ Automatyczne wykresy i historia danych
- ✅ Łatwe tworzenie automatyzacji (klik-klik)
- ✅ Dostęp z telefonu, tabletu, komputera
- ✅ Darmowe i open-source

---

## 🖱️ Jak wygląda i jak się używa Home Assistant?

### Interfejs - Co zobaczysz po zalogowaniu?

Po pierwszym uruchomieniu Home Assistant otwiera się w przeglądarce (jak normalna strona internetowa). Główne elementy:

```
┌─────────────────────────────────────────────────────┐
│  🏠 Home Assistant         👤 Admin    ⚙️ Settings  │  <- Górny pasek
├─────────────────────────────────────────────────────┤
│  📊 Overview (Przegląd)                              │  <- Główna zakładka
│                                                      │
│  ┌──────────────┐  ┌──────────────┐                │
│  │ Temperatura  │  │  Wilgotność  │                │  <- Karty (Cards)
│  │    23.5°C    │  │     45%      │                │
│  └──────────────┘  └──────────────┘                │
│                                                      │
│  ┌────────────────────────────────┐                │
│  │   📈 Wykres temperatury        │                │  <- Wykres historii
│  │   (ostatnie 24h)               │                │
│  └────────────────────────────────┘                │
└─────────────────────────────────────────────────────┘
```

### Podstawowe zakładki (lewy pasek boczny):

1. **📊 Overview** - Twój dashboard, tu widzisz wszystkie dane
2. **🔧 Settings** - Ustawienia (tu dodajesz urządzenia, konfiguracja)
3. **🔌 Devices & Services** - Lista urządzeń i integracji (MQTT, itp.)
4. **🤖 Automations** - Automatyzacje (np. alarm przy wysokiej temp.)
5. **👨‍💻 Developer Tools** - Narzędzia do testowania (przydatne!)

---

## 🎯 Podstawowe Pojęcia - Co Musisz Wiedzieć

### 1. **Entity (Encja)** = "Rzecz" w Home Assistant

To każdy sensor, przełącznik, czy urządzenie. Każda encja ma:
- **Nazwę**: np. "Dom - Temperatura"
- **ID**: np. `sensor.dom_temperatura` (używane w kodzie)
- **Stan**: aktualna wartość (np. "23.5")
- **Atrybuty**: dodatkowe info (np. jednostka "°C")

**Przykład:** Twój czujnik temperatury = 1 encja typu `sensor`

### 2. **Integration (Integracja)** = sposób podłączenia urządzeń

To "wtyczka" która pozwala Home Assistant rozmawiać z urządzeniami.

Dla waszego projektu najważniejsza to **MQTT Integration**:
- MQTT = protokół komunikacji (jak język)
- Raspberry Pi publikuje dane przez MQTT
- Home Assistant odbiera te dane przez MQTT

### 3. **Dashboard (Lovelace)** = Twoja tablica rozdzielcza

To strona którą widzisz - możesz ją edytować!
- Dodawać **karty** (cards): wykresy, liczby, przyciski
- Układać je jak chcesz
- Tworzyć kilka różnych dashboardów

### 4. **Automation (Automatyzacja)** = "Jeśli... to..."

Zasada: **TRIGGER → CONDITION → ACTION**

**Przykład:**
- **TRIGGER** (wyzwalacz): Temperatura > 30°C
- **CONDITION** (warunek): Jest między 8:00 a 22:00 (opcjonalne)
- **ACTION** (akcja): Wyślij powiadomienie na telefon

### 5. **MQTT Broker** = "pośrednik" w komunikacji

To serwer który przekazuje wiadomości:

```
Raspberry Pi → wysyła dane → MQTT Broker → przekazuje → Home Assistant
   (Publisher)                (Mosquitto)              (Subscriber)
```

**Topik** (topic) = "adres" wiadomości, np: `home/bezpieczny_dom/temperature`

---

## 🚀 Podstawowy Workflow - Jak to wszystko działa krok po kroku

### Typowy dzień z Home Assistant w waszym projekcie:

**1. Raspberry Pi czyta czujnik temperatury:**
```python
temperature = read_temperature()  # np. 23.5
```

**2. Raspberry Pi wysyła przez MQTT:**
```python
mqtt_client.publish("home/bezpieczny_dom/temperature", "23.5")
```

**3. MQTT Broker otrzymuje wiadomość i przekazuje subskrybentom**

**4. Home Assistant otrzymuje wiadomość:**
- Automatycznie aktualizuje sensor `sensor.dom_temperatura`
- Wartość zmienia się z poprzedniej na `23.5°C`

**5. Dashboard się odświeża:**
- Widzisz nową temperaturę
- Wykres dodaje nowy punkt

**6. Jeśli temperatura > 30°C:**
- Automatyzacja się uruchamia
- Wysyła powiadomienie: "⚠️ Alarm! Temperatura: 31.2°C"

---

## 🎮 Praktyczne Użycie - Pierwsze Kroki po Instalacji

### Krok 1: Pierwsze Logowanie

Po instalacji (szczegóły niżej) wchodzisz na: `http://homeassistant.local:8123`

1. **Utwórz konto administratora:**
   - Imię: Twoje imię
   - Username: np. `admin`
   - Hasło: coś bezpiecznego
   
2. **Nazwij swój dom:** np. "Bezpieczny Dom - Projekt IoT"

3. **Lokalizacja:** Wybierz Polskę (wpływa na pogodę, strefy czasowe)

4. **Pomijaj** wszelkie "Share analytics" - nie musisz

### Krok 2: Zainstaluj Integrację MQTT

**Najprostszy sposób:**

1. Kliknij **Settings** (⚙️) → **Devices & Services**
2. Kliknij niebieski przycisk **+ ADD INTEGRATION** (prawy dolny róg)
3. Wpisz w wyszukiwarce: **MQTT**
4. Wybierz **MQTT**
5. Pojawi się formularz:
   - **Broker:** `localhost` (jeśli Mosquitto na tym samym urządzeniu co HA)
   - **Port:** `1883` (domyślny port MQTT)
   - **Username:** zostaw puste (na razie)
   - **Password:** zostaw puste (na razie)
6. Kliknij **SUBMIT**

✅ Gotowe! MQTT działa.

### Krok 3: Dodaj Swój Pierwszy Sensor

**Opcja A: Przez interfejs (prostsze dla początkujących)**

1. **Settings** → **Devices & Services** → znajdź **MQTT** → kliknij **CONFIGURE**
2. Niestety, sensory MQTT najłatwiej dodać przez YAML...

**Opcja B: Przez edycję pliku `configuration.yaml`** (ZALECANE)

1. Zainstaluj File Editor:
   - **Settings** → **Add-ons** → **Add-on Store**
   - Wyszukaj **File Editor** → **Install** → **Start**
   - Włącz **Show in sidebar**

2. Otwórz **File Editor** (pojawi się w lewym pasku)

3. Otwórz plik **`configuration.yaml`**

4. **Przewiń na sam dół** i dodaj:

```yaml
mqtt:
  sensor:
    - name: "Testowa Temperatura"
      state_topic: "home/test/temperature"
      unit_of_measurement: "°C"
```

5. **Zapisz** plik (Ctrl+S lub ikona dyskietki)

6. **Sprawdź konfigurację:**
   - **Developer Tools** (🔧 w lewym menu)
   - Zakładka **YAML**
   - Kliknij **CHECK CONFIGURATION**
   - Jeśli OK zobaczysz: ✅ "Configuration valid"

7. **Zrestartuj Home Assistant:**
   - W tym samym miejscu kliknij **RESTART**
   - Poczekaj ~30 sekund

8. Wróć do **Overview** - powinieneś zobaczyć nowy sensor (może być bez wartości, to OK)

### Krok 4: Wyślij Testowe Dane przez MQTT

**Z komputera (jeśli masz zainstalowane `mosquitto_pub`):**

```bash
mosquitto_pub -h localhost -t "home/test/temperature" -m "25.5"
```

**Lub z Pythona (na Raspberry Pi):**

```python
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost", 1883)  # Lub IP Home Assistant
client.publish("home/test/temperature", "25.5")
client.disconnect()
```

**Sprawdź w Home Assistant:**
- Developer Tools → **STATES** → Znajdź `sensor.testowa_temperatura`
- Powinno pokazać: `25.5`

✅ Działa! Twój pierwszy sensor MQTT!

### Krok 5: Stwórz Dashboard

1. Idź do **Overview**
2. Kliknij **3 kropki** (góra-prawo) → **Edit Dashboard**
3. Kliknij niebieski **+ ADD CARD**
4. Wybierz **Gauge** (wskaźnik)
5. W polu **Entity** wybierz `sensor.testowa_temperatura`
6. **Needle**: włącz (będzie ruchoma wskazówka)
7. **Min**: 0
8. **Max**: 50
9. Kliknij **SAVE**
10. Kliknij **DONE** (na górze)

🎉 Masz swój pierwszy dashboard z dynamicznym wskaźnikiem temperatury!

---

## 🧩 Jak to łączy się z Waszym Projektem IoT?

### Schemat całego systemu:

```
┌─────────────────────┐
│   Raspberry Pi      │
│  ┌──────────────┐   │
│  │ Czujniki:    │   │
│  │ - BME280     │   │  1. Czyta dane z czujników
│  │ - RFID       │   │  
│  │ - inne...    │   │
│  └──────────────┘   │
│         ↓           │
│  ┌──────────────┐   │
│  │ Kod Python   │   │  2. Przetwarza i publikuje przez MQTT
│  │ (paho-mqtt)  │   │     Topic: "home/bezpieczny_dom/temperature"
│  └──────────────┘   │     Payload: "23.5"
└─────────────────────┘
          ↓
          ↓ MQTT
          ↓
┌─────────────────────┐
│  MQTT Broker        │  3. Przekazuje wiadomości
│  (Mosquitto)        │
└─────────────────────┘
          ↓
          ↓
┌─────────────────────┐
│  Home Assistant     │  4. Odbiera dane
│  ┌──────────────┐   │     - Aktualizuje sensory
│  │ MQTT Integ.  │   │     - Aktualizuje dashboard
│  └──────────────┘   │     - Uruchamia automatyzacje
│         ↓           │
│  ┌──────────────┐   │
│  │ Dashboard    │   │  5. Pokazuje na stronie webowej
│  │ Wykresy      │   │
│  │ Alarmy       │   │
│  └──────────────┘   │
└─────────────────────┘
          ↓
   ┌─────────────┐
   │  Przeglądarka│     6. TY widzisz dane
   │  (Chrome)    │
   └─────────────┘
```

### Co musicie zrobić w projekcie?

1. **Na Raspberry Pi:**
   - Zainstalować bibliotekę `paho-mqtt`
   - W kodzie Pythona dodać publikację danych MQTT
   
2. **Zainstalować Home Assistant** (jedna z metod z tego przewodnika)

3. **Zainstalować MQTT Broker** (Mosquitto)

4. **Połączyć** Home Assistant z MQTT

5. **Skonfigurować sensory** w `configuration.yaml`

6. **Stworzyć dashboard** z wykresami

7. **Dodać automatyzacje** (np. alarm temperatury)

---

## ❓ FAQ dla Laików

### Q: Czy Home Assistant to aplikacja na telefon?
**A:** Nie i tak. To głównie serwer webowy (strona internetowa), ale możesz ją otworzyć na telefonie w przeglądarce. Jest też oficjalna aplikacja mobilna.

### Q: Czy muszę płacić?
**A:** Nie! Home Assistant jest całkowicie darmowy i open-source. Opcjonalnie możesz wykupić "Home Assistant Cloud" ($6.50/mc) dla łatwego dostępu zdalnego.

### Q: Na czym to działa?
**A:** 
- Raspberry Pi (zalecane)
- Komputer z Windows/Mac/Linux
- NAS (Synology, itp.)
- Wirtualna maszyna

### Q: Czy mogę to uruchomić na tym samym Raspberry Pi co mój projekt?
**A:** Tak! Możesz użyć Docker lub zainstalować Mosquitto systemowo razem z Home Assistant.

### Q: Co jeśli coś popsuję?
**A:** Home Assistant ma wbudowane backupy. Możesz zawsze wrócić do poprzedniej wersji. Plus, wszystko jest w plikach tekstowych (YAML) które możesz edytować.

### Q: Czy to trudne?
**A:** Pierwsze 30 minut może być przytłaczające, ale potem jest bardzo intuicyjne. Interfejs jest naprawdę przyjazny.

### Q: Czy muszę znać programowanie?
**A:** Nie do podstawowych rzeczy! Większość możesz klikać. Do zaawansowanych automatyzacji przydaje się YAML (prosty format plików).

### Q: Jak długo trwa instalacja?
**A:** 
- Nagranie obrazu na kartę SD: 5-10 min
- Pierwsze uruchomienie: 5-20 min
- Podstawowa konfiguracja: 15-30 min
- **Razem: ~1 godzina do działającego systemu**

---

## ✅ Przed Przejściem Dalej - Checklist

Upewnij się że rozumiesz:
- [ ] Co to jest Home Assistant (platforma automatyzacji domu)
- [ ] Że działa jako strona webowa dostępna przez przeglądarkę
- [ ] Co to jest MQTT i że to protokół komunikacji
- [ ] Że Raspberry Pi będzie wysyłać dane, a HA odbierać
- [ ] Podstawowe elementy interfejsu (Dashboard, Settings, Devices)
- [ ] Co to są Entities (sensory, przełączniki, itp.)

Jeśli wszystko jasne - **czas przejść do instalacji!** ⬇️

---

## 🔧 Część 2: Instalacja i Konfiguracja

## Czym jest Home Assistant?

**Home Assistant** (HA) to open-source platforma automatyzacji domu, która:
- Integruje różne urządzenia IoT w jednym miejscu
- Umożliwia tworzenie dashboardów do wizualizacji danych
- Pozwala na automatyzacje (np. jeśli temperatura > 30°C → wyślij powiadomienie)
- Działa lokalnie (bez chmury) lub z dostępem zdalnym
- Ma interfejs webowy dostępny przez przeglądarkę

## Metody Instalacji

### Opcja 1: Home Assistant OS (ZALECANE dla Raspberry Pi)

**Najlepsza opcja jeśli masz dodatkową kartę SD lub Raspberry Pi tylko dla HA.**

1. **Pobierz obraz:**
   ```
   https://www.home-assistant.io/installation/raspberrypi
   ```
   Wybierz odpowiednią wersję dla swojego Raspberry Pi (3, 4, 5, itp.)

2. **Nagraj obraz na kartę SD:**
   - Użyj **Raspberry Pi Imager** lub **Balena Etcher**
   - Wybierz pobrany obraz Home Assistant OS
   - Wybierz kartę SD (min. 16GB, zalecane 32GB)
   - Nagraj obraz

3. **Pierwsze uruchomienie:**
   - Włóż kartę SD do Raspberry Pi
   - Podłącz Ethernet (WiFi można skonfigurować później)
   - Podłącz zasilanie
   - Poczekaj 5-20 minut na pierwszą instalację

4. **Dostęp do interfejsu:**
   - Otwórz przeglądarkę i wejdź na: `http://homeassistant.local:8123`
   - Lub użyj IP Raspberry Pi: `http://192.168.x.x:8123`
   - Stwórz konto administratora

**Zalety:**
- Najprostsza instalacja
- Automatyczne aktualizacje
- Wbudowany Add-on Store (łatwa instalacja Mosquitto MQTT)
- Najlepsze wsparcie

**Wady:**
- Potrzebna dedykowana karta SD / Raspberry Pi
- Nie można używać Pi do innych rzeczy jednocześnie

---

### Opcja 2: Home Assistant Container (Docker)

**Dobra opcja jeśli masz Raspberry Pi z już zainstalowanym systemem.**

1. **Instalacja Docker:**
   ```bash
   curl -sSL https://get.docker.com | sh
   sudo usermod -aG docker $USER
   # Wyloguj się i zaloguj ponownie
   ```

2. **Uruchomienie Home Assistant:**
   ```bash
   docker run -d \
     --name homeassistant \
     --privileged \
     --restart=unless-stopped \
     -e TZ=Europe/Warsaw \
     -v /home/pi/homeassistant:/config \
     --network=host \
     ghcr.io/home-assistant/home-assistant:stable
   ```

3. **Dostęp:**
   - `http://localhost:8123` (z Raspberry Pi)
   - `http://192.168.x.x:8123` (z innego komputera w sieci)

**Zalety:**
- Można używać Raspberry Pi do innych projektów
- Łatwa aktualizacja (docker pull + restart)

**Wady:**
- Brak Add-on Store (trzeba instalować dodatki ręcznie)
- Bardziej skomplikowana konfiguracja

---

### Opcja 3: Home Assistant na PC (do testów)

**Najlepsza opcja jeśli NIE masz jeszcze Raspberry Pi i chcesz się nauczyć HA.**

**Windows (Docker Desktop):**
```powershell
# 1. Zainstaluj Docker Desktop ze strony docker.com
# 2. Uruchom PowerShell i wykonaj:

docker run -d `
  --name homeassistant `
  --restart=unless-stopped `
  -e TZ=Europe/Warsaw `
  -v C:\homeassistant:/config `
  -p 8123:8123 `
  ghcr.io/home-assistant/home-assistant:stable
```

**Linux/Mac:**
```bash
docker run -d \
  --name homeassistant \
  --restart=unless-stopped \
  -e TZ=Europe/Warsaw \
  -v ~/homeassistant:/config \
  -p 8123:8123 \
  ghcr.io/home-assistant/home-assistant:stable
```

Dostęp: `http://localhost:8123`

---

## Konfiguracja MQTT (Mosquitto Broker)

MQTT to protokół komunikacji wykorzystywany w projekcie. Home Assistant będzie **subskrybentem** (odbiera dane z Raspberry Pi).

### Instalacja Mosquitto - Metoda 1: Add-on (tylko HA OS)

1. W Home Assistant → **Settings** → **Add-ons** → **Add-on Store**
2. Znajdź **Mosquitto broker** i kliknij **Install**
3. Po instalacji kliknij **Start**
4. W zakładce **Configuration** możesz ustawić:
   ```yaml
   logins:
     - username: pi
       password: raspberry
   ```
5. Kliknij **Save** i **Restart**

### Instalacja Mosquitto - Metoda 2: Docker (HA Container)

```bash
docker run -d \
  --name mosquitto \
  --restart=unless-stopped \
  -p 1883:1883 \
  -v /home/pi/mosquitto/config:/mosquitto/config \
  -v /home/pi/mosquitto/data:/mosquitto/data \
  eclipse-mosquitto
```

Utwórz plik konfiguracyjny:
```bash
mkdir -p /home/pi/mosquitto/config
nano /home/pi/mosquitto/config/mosquitto.conf
```

Zawartość:
```
listener 1883
allow_anonymous true
persistence true
persistence_location /mosquitto/data/
```

Restart:
```bash
docker restart mosquitto
```

### Instalacja Mosquitto - Metoda 3: Systemowa (Raspberry Pi)

```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients -y
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

Test:
```bash
# Terminal 1 - subskrybent
mosquitto_sub -h localhost -t "test/topic"

# Terminal 2 - publisher
mosquitto_pub -h localhost -t "test/topic" -m "Hello MQTT"
```

### Integracja MQTT w Home Assistant

1. **Settings** → **Devices & Services** → **Add Integration**
2. Szukaj **MQTT**
3. Wprowadź dane:
   - **Broker:** `localhost` (jeśli na tym samym urządzeniu) lub IP Raspberry Pi
   - **Port:** `1883`
   - **Username/Password:** jeśli ustawione (opcjonalnie)
4. Kliknij **Submit**

---

## Konfiguracja Sensorów dla Projektu "Bezpieczny Dom"

Edytuj plik `configuration.yaml` (w Home Assistant):

**Lokalizacja:**
- HA OS: Settings → Add-ons → File Editor (trzeba doinstalować addon)
- HA Container: `/home/pi/homeassistant/configuration.yaml`
- HA Docker (PC): `C:\homeassistant\configuration.yaml` lub `~/homeassistant/configuration.yaml`

### Dodaj sensory MQTT:

```yaml
mqtt:
  sensor:
    # Temperatura
    - name: "Dom - Temperatura"
      state_topic: "home/bezpieczny_dom/temperature"
      unit_of_measurement: "°C"
      device_class: temperature
      state_class: measurement
      
    # Wilgotność
    - name: "Dom - Wilgotność"
      state_topic: "home/bezpieczny_dom/humidity"
      unit_of_measurement: "%"
      device_class: humidity
      state_class: measurement
      
    # Ciśnienie
    - name: "Dom - Ciśnienie"
      state_topic: "home/bezpieczny_dom/pressure"
      unit_of_measurement: "hPa"
      device_class: pressure
      state_class: measurement
    
    # Ostatnio użyta karta RFID
    - name: "Sejf - Ostatnia Karta"
      state_topic: "home/bezpieczny_dom/rfid/last_card"
      icon: mdi:card-account-details
  
  binary_sensor:
    # Status dostępu do sejfu
    - name: "Sejf - Dostęp Przyznany"
      state_topic: "home/bezpieczny_dom/access/status"
      payload_on: "granted"
      payload_off: "denied"
      device_class: lock
      
    # Alarm temperatury
    - name: "Alarm - Temperatura"
      state_topic: "home/bezpieczny_dom/alarm/temperature"
      payload_on: "active"
      payload_off: "inactive"
      device_class: safety
      
    # Alarm - nieautoryzowany dostęp
    - name: "Alarm - Nieautoryzowany Dostęp"
      state_topic: "home/bezpieczny_dom/alarm/unauthorized"
      payload_on: "active"
      payload_off: "inactive"
      device_class: safety
```

**Zapisz i zrestartuj Home Assistant:**
- Developer Tools → YAML → **Restart** → **Check Configuration** → **Restart**

---

## Tworzenie Dashboard (Lovelace)

1. **Overview** (strona główna) → trzy kropki (góra-prawo) → **Edit Dashboard**
2. Kliknij **+ Add Card**

### Przykładowe karty dla projektu:

**1. Karta Gauge - Temperatura**
```yaml
type: gauge
entity: sensor.dom_temperatura
min: 0
max: 50
needle: true
severity:
  green: 0
  yellow: 25
  red: 30
```

**2. Karta History Graph - Historia temperatury**
```yaml
type: history-graph
entities:
  - sensor.dom_temperatura
  - sensor.dom_wilgotnosc
hours_to_show: 24
```

**3. Karta Entities - Wszystkie sensory**
```yaml
type: entities
title: Bezpieczny Dom
entities:
  - sensor.dom_temperatura
  - sensor.dom_wilgotnosc
  - sensor.dom_cisnienie
  - sensor.sejf_ostatnia_karta
  - binary_sensor.sejf_dostep_przyznany
  - binary_sensor.alarm_temperatura
  - binary_sensor.alarm_nieautoryzowany_dostep
```

**4. Karta Conditional - Alarm (pokazuje się tylko gdy alarm aktywny)**
```yaml
type: conditional
conditions:
  - entity: binary_sensor.alarm_temperatura
    state: 'on'
card:
  type: markdown
  content: |
    ## ⚠️ ALARM TEMPERATURY!
    Temperatura przekroczyła bezpieczny poziom.
```

---

## Automatyzacje

**Settings** → **Automations & Scenes** → **Create Automation**

### Przykład 1: Powiadomienie przy alarmie temperatury

**Przez YAML** (`automations.yaml`):
```yaml
- alias: "Powiadomienie - Alarm Temperatury"
  trigger:
    - platform: state
      entity_id: binary_sensor.alarm_temperatura
      to: 'on'
  action:
    - service: notify.notify
      data:
        title: "⚠️ Alarm Temperatury!"
        message: "Temperatura w domu przekroczyła bezpieczny poziom: {{ states('sensor.dom_temperatura') }}°C"
```

### Przykład 2: Logowanie dostępu do sejfu

```yaml
- alias: "Log - Dostęp do Sejfu"
  trigger:
    - platform: mqtt
      topic: home/bezpieczny_dom/access/status
  action:
    - service: logbook.log
      data:
        name: "Sejf"
        message: >
          Karta {{ states('sensor.sejf_ostatnia_karta') }}
          - Status: {{ trigger.payload }}
```

---

## Testowanie MQTT z Raspberry Pi

### Z kodu Python (Lab 11 - sender):

```python
import paho.mqtt.client as mqtt
import time

# Konfiguracja
broker = "192.168.x.x"  # IP Home Assistant
port = 1883
topic_temp = "home/bezpieczny_dom/temperature"

client = mqtt.Client("RaspberryPi_Test")
client.connect(broker, port)

# Publikuj testową temperaturę
client.publish(topic_temp, "22.5")
print("Wysłano temperaturę: 22.5°C")

client.disconnect()
```

### Ręczne testowanie przez terminal:

```bash
# Publikuj temperaturę
mosquitto_pub -h 192.168.x.x -t "home/bezpieczny_dom/temperature" -m "23.5"

# Subskrybuj wszystkie topiki projektu
mosquitto_sub -h 192.168.x.x -t "home/bezpieczny_dom/#" -v
```

W Home Assistant powinieneś zobaczyć zaktualizowaną wartość!

---

## Integracja z IFTTT

Home Assistant może wysyłać powiadomienia przez IFTTT jako alternatywę dla email.

### Setup IFTTT:

1. Załóż konto na `ifttt.com`
2. **Create** → **If This**
3. Wybierz **Webhooks**
4. **Receive a web request**
5. Event name: `temperature_alarm`
6. **Then That** → **Email** → **Send me an email**
7. Subject: `Alarm Temperatury - Bezpieczny Dom`
8. Body:
   ```
   Temperatura: {{Value1}}°C
   Próg: {{Value2}}°C
   Czas: {{OccurredAt}}
   ```

**Pobierz klucz Webhook:**
- `ifttt.com/maker_webhooks` → **Documentation**
- Skopiuj URL, który wygląda tak:
  ```
  https://maker.ifttt.com/trigger/{event}/with/key/{YOUR_KEY}
  ```

### Konfiguracja w Home Assistant:

`configuration.yaml`:
```yaml
ifttt:
  key: YOUR_IFTTT_KEY_HERE
```

**Automatyzacja z IFTTT:**
```yaml
- alias: "IFTTT - Alarm Temperatury"
  trigger:
    - platform: state
      entity_id: binary_sensor.alarm_temperatura
      to: 'on'
  action:
    - service: ifttt.trigger
      data:
        event: temperature_alarm
        value1: "{{ states('sensor.dom_temperatura') }}"
        value2: "30"  # Próg
```

---

## Dostęp Zdalny (Opcjonalnie)

Aby mieć dostęp do Home Assistant spoza sieci domowej:

### Opcja 1: Nabu Casa (płatne, $6.50/miesiąc)
- Najprostsze
- Settings → Home Assistant Cloud → Subscribe
- Automatyczne bezpieczne połączenie

### Opcja 2: DuckDNS + Let's Encrypt (darmowe)
- Wymaga przekierowania portów w routerze
- Tutorial: `https://www.home-assistant.io/docs/configuration/remote/`

---

## Przydatne Linki

- **Oficjalna dokumentacja:** `https://www.home-assistant.io/docs/`
- **Forum społeczności:** `https://community.home-assistant.io/`
- **MQTT Integration:** `https://www.home-assistant.io/integrations/mqtt/`
- **Video tutorial (PL):** Szukaj "Home Assistant po polsku" na YouTube

---

## Troubleshooting

### Problem: Nie mogę połączyć się z http://homeassistant.local:8123

**Rozwiązanie:**
1. Sprawdź IP Raspberry Pi: `hostname -I`
2. Użyj IP zamiast hostname: `http://192.168.x.x:8123`
3. Poczekaj 5-10 minut po pierwszym uruchomieniu

### Problem: Sensory MQTT nie pojawiają się w HA

**Rozwiązanie:**
1. Sprawdź czy broker działa: `sudo systemctl status mosquitto`
2. Sprawdź connection w HA: Settings → Integrations → MQTT → Configure
3. Test ręczny publikacji:
   ```bash
   mosquitto_pub -h localhost -t "home/bezpieczny_dom/temperature" -m "25.0"
   ```
4. Developer Tools → MQTT → Listen to topic: `home/bezpieczny_dom/#`

### Problem: Raspberry Pi nie może się połączyć z brokerem MQTT

**Rozwiązanie:**
1. Sprawdź firewall na Home Assistant
2. Sprawdź poprawność IP w `config.py`:
   ```python
   MQTT_BROKER = "192.168.1.100"  # IP Home Assistant
   MQTT_PORT = 1883
   ```
3. Test z Raspberry Pi:
   ```bash
   mosquitto_pub -h 192.168.1.100 -t "test" -m "hello"
   ```

---

## Następne Kroki dla Twojego Projektu

1. **Wybierz metodę instalacji** (zalecam HA OS jeśli masz dodatkowy Pi)
2. **Zainstaluj Home Assistant**
3. **Skonfiguruj broker MQTT** (Mosquitto)
4. **Dodaj sensory MQTT do `configuration.yaml`**
5. **Przetestuj połączenie** z Raspberry Pi
6. **Stwórz prosty dashboard** z kartą temperature gauge
7. **Dodaj automatyzację** na alarm temperatury

Powodzenia! 🏠🔐
