# Prozeda Solar Controller Integration for Home Assistant

[🇩🇪 Deutsche Version](#deutsche-version) | [🇺🇸 English Version](#english-version)

---

## English Version

This integration allows you to integrate data from Prozeda solar controllers into Home Assistant.

### Supported Devices

- **Primos 600SR** - Full feature set with all sensors
- **Primos 250SR** - Compact version with reduced sensors
- **Grandis 650HK** - (In preparation)
- **Grandis 600SR** - (In preparation)

### Installation

#### Option 1: HACS (Recommended)

1. **Install HACS** (if not already installed):
   - Follow the [official HACS guide](https://hacs.xyz/docs/setup/download)

2. **Add Repository**:
   - Open HACS in Home Assistant
   - Go to "Integrations"
   - Click the three dots (⋮) in the top right
   - Select "Custom repositories"
   - Add this URL: `https://github.com/YOUR-USERNAME/prozeda-homeassistant`
   - Category: "Integration"
   - Click "Add"

3. **Install Integration**:
   - Search for "Prozeda Solar Controllers"
   - Click "Download"
   - Restart Home Assistant

#### Option 2: Manual Installation

1. **Download Files**:
   - Download all files from this repository

2. **Create Folder**:
   - Create folder `config/custom_components/prozeda/` in your Home Assistant

3. **Copy Files**:
   - Copy all `.py` files to the `prozeda` folder
   - Copy the `manifest.json` file

4. **Restart Home Assistant**

### Configuration

Add the following to your `configuration.yaml`:

```yaml
sensor:
  - platform: prozeda
    host: "192.168.64.131"  # IP address of your Prozeda controller
    name: "Prozeda Primos"  # Name of the Integration/Controller, e.g. Primos 250SR
    device_type: auto       # Optional: auto, primos_600sr, primos_250sr
    scan_interval: 30       # Optional: Update interval in seconds
```

**Parameters:**
- `host`: IP address of the Prozeda controller (required)
- `name`: Name of the integration (optional, default: "Prozeda Solar Controller")
- `device_type`: Device type (optional, default: "auto" for automatic detection)
- `scan_interval`: Update interval in seconds (optional, default: 30)

### Available Sensors

#### Primos 600SR (Full feature set)

**Temperature Sensors (°C)**
- `sensor.prozeda_primos_600sr_s1` - Sensor 1
- `sensor.prozeda_primos_600sr_s2` - Sensor 2
- `sensor.prozeda_primos_600sr_s3` - Sensor 3
- `sensor.prozeda_primos_600sr_s4` - Sensor 4
- `sensor.prozeda_primos_600sr_s5` - Sensor 5
- `sensor.prozeda_primos_600sr_s6` - Sensor 6

**Output Sensors (%)**
- `sensor.prozeda_primos_600sr_r1` - Output 1
- `sensor.prozeda_primos_600sr_r2` - Output 2
- `sensor.prozeda_primos_600sr_r3` - Output 3
- `sensor.prozeda_primos_600sr_r0` - Output 0

**PWM Sensors (%)**
- `sensor.prozeda_primos_600sr_he1` - Heating Element 1
- `sensor.prozeda_primos_600sr_he2` - Heating Element 2

**Energy Sensors (kWh)**
- `sensor.prozeda_primos_600sr_energieertrag` - Energy Yield
- `sensor.prozeda_primos_600sr_energieertrag2` - Energy Yield 2

**Operating Hours (h)**
- `sensor.prozeda_primos_600sr_betriebsstunden` - Operating Hours
- `sensor.prozeda_primos_600sr_betriebsstunden2` - Operating Hours 2

#### Primos 250SR (Compact version)

**Temperature Sensors (°C)**
- `sensor.prozeda_primos_250sr_s1` - Sensor 1
- `sensor.prozeda_primos_250sr_s2` - Sensor 2
- `sensor.prozeda_primos_250sr_s3` - Sensor 3
- `sensor.prozeda_primos_250sr_s4` - Sensor 4

**Output Sensors (%)**
- `sensor.prozeda_primos_250sr_r1` - Output 1
- `sensor.prozeda_primos_250sr_r0` - Output 0

**PWM Sensors (%)**
- `sensor.prozeda_primos_250sr_he1` - Heating Element 1

**Energy Sensors (kWh)**
- `sensor.prozeda_primos_250sr_energieertrag` - Energy Yield

**Operating Hours (h)**
- `sensor.prozeda_primos_250sr_betriebsstunden` - Operating Hours

### Automatic Device Detection

The integration automatically detects the device type based on the data structure:
- Position 41-42 = "3B" → Primos 600SR
- Position 41-42 = "33" → Primos 250SR

### Example Dashboard

```yaml
type: entities
title: Prozeda Solar Controller
entities:
  - sensor.prozeda_primos_600sr_s1
  - sensor.prozeda_primos_600sr_s2
  - sensor.prozeda_primos_600sr_s3
  - sensor.prozeda_primos_600sr_r1
  - sensor.prozeda_primos_600sr_r2
  - sensor.prozeda_primos_600sr_energieertrag
  - sensor.prozeda_primos_600sr_betriebsstunden
```

### Troubleshooting

#### Sensors show "unavailable"
- Check the IP address in the configuration
- Ensure the Prozeda controller is reachable: `http://IP-ADDRESS/primos_val.xml`
- Check the logs: Settings → System → Logs

#### Integration not found
- Ensure all files are in the correct folder: `config/custom_components/prozeda/`
- Restart Home Assistant after installation

#### Wrong sensors displayed
- Check automatic device detection in the logs
- Manually set `device_type` to the correct value

#### Values are incorrect
- The integration parses XML data automatically
- For issues, check logs for error messages
- Compare raw XML values with Home Assistant values

### Support

For issues, create an issue on GitHub or post in the Home Assistant Community.

### License

MIT License

---

## Deutsche Version

Diese Integration ermöglicht es, Daten von Prozeda Solarreglern in Home Assistant zu integrieren.

### Unterstützte Geräte

- **Primos 600SR** - Vollausstattung mit allen Sensoren
- **Primos 250SR** - Kompakte Version mit reduzierten Sensoren
- **Grandis 650HK** - (In Vorbereitung)
- **Grandis 600SR** - (In Vorbereitung)

### Installation

#### Option 1: HACS (Empfohlen)

1. **HACS installieren** (falls noch nicht vorhanden):
   - Folge der [offiziellen HACS Anleitung](https://hacs.xyz/docs/setup/download)

2. **Repository hinzufügen**:
   - Öffne HACS in Home Assistant
   - Gehe zu "Integrations"
   - Klicke auf die drei Punkte (⋮) oben rechts
   - Wähle "Custom repositories"
   - Füge diese URL hinzu: `https://github.com/DEIN-USERNAME/prozeda-homeassistant`
   - Kategorie: "Integration"
   - Klicke "Add"

3. **Integration installieren**:
   - Suche nach "Prozeda Solar Controllers"
   - Klicke "Download"
   - Starte Home Assistant neu

#### Option 2: Manuelle Installation

1. **Dateien herunterladen**:
   - Lade alle Dateien aus diesem Repository herunter

2. **Ordner erstellen**:
   - Erstelle den Ordner `config/custom_components/prozeda/` in deinem Home Assistant

3. **Dateien kopieren**:
   - Kopiere alle `.py` Dateien in den `prozeda` Ordner
   - Kopiere die `manifest.json` Datei

4. **Home Assistant neu starten**

### Konfiguration

Füge folgendes zu deiner `configuration.yaml` hinzu:

```yaml
sensor:
  - platform: prozeda
    host: "192.168.64.131"  # IP-Adresse deines Prozeda Controllers
    name: "Prozeda Primos"  # Optional: Name der Integration
    device_type: auto       # Optional: auto, primos_600sr, primos_250sr
    scan_interval: 30       # Optional: Aktualisierungsintervall in Sekunden
```

**Parameter:**
- `host`: IP-Adresse des Prozeda Controllers (erforderlich)
- `name`: Name der Integration (optional, Standard: "Prozeda Solar Controller")
- `device_type`: Gerätetyp (optional, Standard: "auto" für automatische Erkennung)
- `scan_interval`: Aktualisierungsintervall in Sekunden (optional, Standard: 30)

### Verfügbare Sensoren

#### Primos 600SR (Vollausstattung)

**Temperatursensoren (°C)**
- `sensor.prozeda_primos_600sr_s1` - Sensor 1
- `sensor.prozeda_primos_600sr_s2` - Sensor 2
- `sensor.prozeda_primos_600sr_s3` - Sensor 3
- `sensor.prozeda_primos_600sr_s4` - Sensor 4
- `sensor.prozeda_primos_600sr_s5` - Sensor 5
- `sensor.prozeda_primos_600sr_s6` - Sensor 6

**Ausgangssensoren (%)**
- `sensor.prozeda_primos_600sr_r1` - Ausgang 1
- `sensor.prozeda_primos_600sr_r2` - Ausgang 2
- `sensor.prozeda_primos_600sr_r3` - Ausgang 3
- `sensor.prozeda_primos_600sr_r0` - Ausgang 0

**PWM-Sensoren (%)**
- `sensor.prozeda_primos_600sr_he1` - Heizstab 1
- `sensor.prozeda_primos_600sr_he2` - Heizstab 2

**Energiesensoren (kWh)**
- `sensor.prozeda_primos_600sr_energieertrag` - Energieertrag
- `sensor.prozeda_primos_600sr_energieertrag2` - Energieertrag 2

**Betriebsstunden (h)**
- `sensor.prozeda_primos_600sr_betriebsstunden` - Betriebsstunden
- `sensor.prozeda_primos_600sr_betriebsstunden2` - Betriebsstunden 2

#### Primos 250SR (Kompaktversion)

**Temperatursensoren (°C)**
- `sensor.prozeda_primos_250sr_s1` - Sensor 1
- `sensor.prozeda_primos_250sr_s2` - Sensor 2
- `sensor.prozeda_primos_250sr_s3` - Sensor 3
- `sensor.prozeda_primos_250sr_s4` - Sensor 4

**Ausgangssensoren (%)**
- `sensor.prozeda_primos_250sr_r1` - Ausgang 1
- `sensor.prozeda_primos_250sr_r0` - Ausgang 0

**PWM-Sensoren (%)**
- `sensor.prozeda_primos_250sr_he1` - Heizstab 1

**Energiesensoren (kWh)**
- `sensor.prozeda_primos_250sr_energieertrag` - Energieertrag

**Betriebsstunden (h)**
- `sensor.prozeda_primos_250sr_betriebsstunden` - Betriebsstunden

### Automatische Geräteerkennung

Die Integration erkennt automatisch den Gerätetyp basierend auf der Datenstruktur:
- Position 41-42 = "3B" → Primos 600SR
- Position 41-42 = "33" → Primos 250SR

### Beispiel Dashboard

```yaml
type: entities
title: Prozeda Solar Controller
entities:
  - sensor.prozeda_primos_600sr_s1
  - sensor.prozeda_primos_600sr_s2
  - sensor.prozeda_primos_600sr_s3
  - sensor.prozeda_primos_600sr_r1
  - sensor.prozeda_primos_600sr_r2
  - sensor.prozeda_primos_600sr_energieertrag
  - sensor.prozeda_primos_600sr_betriebsstunden
```

### Fehlerbehebung

#### Sensoren zeigen "unavailable"
- Überprüfe die IP-Adresse in der Konfiguration
- Stelle sicher, dass der Prozeda Controller erreichbar ist: `http://IP-ADRESSE/primos_val.xml`
- Überprüfe die Logs: Einstellungen → System → Logs

#### Integration wird nicht gefunden
- Stelle sicher, dass alle Dateien im richtigen Ordner sind: `config/custom_components/prozeda/`
- Starte Home Assistant neu nach der Installation

#### Falsche Sensoren werden angezeigt
- Überprüfe die automatische Geräteerkennung in den Logs
- Setze `device_type` manuell auf den richtigen Wert

#### Werte sind falsch
- Die Integration parst die XML-Daten automatisch
- Bei Problemen überprüfe die Logs für Fehlermeldungen
- Vergleiche die Rohwerte im XML mit den Home Assistant Werten

### Support

Bei Problemen erstelle ein Issue auf GitHub oder poste in der Home Assistant Community.

### Lizenz

MIT License