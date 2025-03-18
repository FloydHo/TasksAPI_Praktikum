# TasksAPI Praktikum

Dieses Projekt ist eine einfache ToDo-API, die mit FastAPI erstellt wurde. Es ermöglicht das Erstellen, Lesen, Aktualisieren und Löschen von Aufgaben (Tasks) in einer SQLite-Datenbank. Die API ist in Docker-Containern verpackt, um die Bereitstellung und Entwicklung zu vereinfachen.

## Verwendete Technologien

- **FastAPI**: Ein modernes, schnelles (hochperformantes) Web-Framework für die Erstellung von APIs mit Python.
- **SQLite**: Eine leichte, serverlose Datenbank, die für die Speicherung von Aufgaben verwendet wird.
- **Docker**: Eine Plattform zur Containerisierung von Anwendungen, die die Bereitstellung und Entwicklung vereinfacht.
- **Pydantic**: Eine Bibliothek zur Datenvalidierung und Einstellungsverwaltung mittels Python-Typannotationen.
- **SQLAlchemy**: Ein ORM (Object-Relational Mapping) für Python, das die Interaktion mit der Datenbank vereinfacht.

## Verwendung

### Installation und Ausführung

#### Repository klonen

Das GitHub-Repository klonen und in das Verzeichnis wechseln:

```bash
git clone https://github.com/FloydHo/TasksAPI_Praktikum
cd TasksAPI_Praktikum
```

### Docker-Setup

- Docker muss auf Ihrem System installiert sein.  
  [Download Docker](https://www.docker.com/)

Docker-Container bauen und starten:

```bash
docker-compose up -d --build
```

Nun sollte die API laufen und unter `localhost:8000` verfügbar sein!  
Unter `localhost:8000/docs` finden Sie die Swagger-Dokumentation der API-Endpunkte.

Docker-Container beenden:

```bash
docker-compose down
```

---

### Setup ohne Docker

- Python muss auf Ihrem System installiert sein.  
  [Download Python](https://www.python.org/downloads/)

Virtuelle Umgebung einrichten:

```bash
python -m venv .venv
```

Virtuelle Umgebung aktivieren:

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```

API starten:

```bash
fastapi run app/main.py
```

Nun sollte die API laufen und unter `localhost:8000` verfügbar sein!  
Unter `localhost:8000/docs` finden Sie die Swagger-Dokumentation der API-Endpunkte.

Zum Beenden:  
Strg + C drücken und anschließend die virtuelle Umgebung deaktivieren:

```bash
deactivate
```

---

## Tests

Um die Unit-Tests auszuführen, folgen Sie den Schritten im Abschnitt **"Setup ohne Docker"** bis einschließlich der Aktivierung der virtuellen Umgebung.  
Dann in den `tests`-Ordner wechseln:

```bash
cd tests
```

Tests mit `pytest` ausführen:

```bash
pytest -v
```

