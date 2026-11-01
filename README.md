# Sokratischer Vorlesungs- und Klausur-Tutor

Ein eigenständiges Lernprojekt nach der [Trinity-Architekturreferenz](https://profengel.github.io/KI-Literacy/trinity-agenten.html): Rollenregeln, Projektkonventionen, Ablauf, Ausgabeschema, deterministische Werkzeuge und lokales SQLite-Gedächtnis sind getrennt. Der Tutor hilft mit Fragen und Hinweisen statt sofortiger Musterlösungen.

## Was macht der Tutor?

Der Tutor unterstützt beim Verstehen von Vorlesungsstoff und bei der Klausurvorbereitung. Du kannst für jedes Fach einen eigenen Lernbereich anlegen, ein Skript hochladen und anschließend eine Frage stellen. Statt bei einer Übungsaufgabe sofort eine vollständige Musterlösung zu verraten, erklärt der Tutor die Grundlagen und begleitet dich mit Hinweisen und Rückfragen zum eigenen Ergebnis.

**Ein typischer Ablauf:**

1. Ein Fach auswählen, zum Beispiel „Marketing“ oder „Controlling“.
2. Optional ein Skript als `.txt`, `.md` oder `.json` hochladen.
3. Eine Frage eingeben, zum Beispiel: „Was bedeutet Deckungsbeitrag?“
4. Eine Erklärung in der gewünschten Stufe erhalten: **Einfach**, **Normal** oder **Fachlich**.
5. Mit „Noch nicht verstanden“ nachfragen oder nach „Verstanden“ eine Reflexionsaufgabe erstellen lassen.
6. Themen als „In Arbeit“, „Gemeistert“ oder „Noch unsicher“ festhalten und den Fortschritt im jeweiligen Fach ansehen.

Der Tutor kann auch ohne eigenes Skript verwendet werden. Dann sind seine Aussagen nicht durch deine Vorlesungsunterlagen belegt. Bei einem hochgeladenen Skript werden passende Textabschnitte ausgewählt und ein angegebenes Zitat auf Übereinstimmung geprüft.

## Funktionen im Überblick

| Bereich | Funktion |
| --- | --- |
| **Lernbereiche** | Fächer getrennt anlegen und ihren jeweiligen Lernstand verwalten. |
| **Unterlagen** | Textdateien, Markdown und JSON als Lernmaterial hochladen. |
| **Erklärungen** | Zwischen einfacher, normaler und fachlicher Erklärung wechseln und vertiefend nachfragen. |
| **Üben** | Nach der Erklärung eine Reflexionsaufgabe anfordern. |
| **Fortschritt** | Themen und Einschätzungen lokal speichern; den Lernstand grafisch darstellen. |
| **Modelle** | Codex, Ollama, LM Studio, OpenAI API oder Google Gemini auswählen. Ein vorbereiteter Übungsmodus steht ohne Modell zur Verfügung. |
| **Einstellungen** | Modellwahl, Dark Mode, Memory-Ansicht und Trinity-Dateien über das Zahnrad öffnen. |

## So sieht der Tutor aus

Die Lernansicht verbindet optionale Unterlagen, Fragen in drei Erklärstufen und einen fachbezogenen Lernstand:

![Lernansicht mit Fragen und Fortschritt](./screenshots/lernansicht.jpg)

Modellauswahl, Dark Mode, Memory-Grafik und die Trinity-Dateien sind über die Einstellungen erreichbar:

![Einstellungen mit Modellauswahl und Dark Mode](./screenshots/einstellungen.jpg)

## Start auf dem eigenen Computer

Python 3.9 oder neuer genügt; zusätzliche Pakete sind nicht erforderlich.

Das Repository zuerst herunterladen oder klonen und im Terminal in den Projektordner wechseln:

```sh
git clone https://github.com/LeonieTroblGomez/sokratischer-tutor-agent.git
cd sokratischer-tutor-agent
```

Danach den Tutor starten:

```sh
python3 server.py
```

Öffne anschließend **http://127.0.0.1:8001/**. Beenden mit `Strg+C`. Die Bridge hört ausschließlich auf diesem Computer; `--port 8002` ändert bei Bedarf den Port. Die App ist nicht für öffentliche Server oder gleichzeitige fremde Nutzer ausgelegt.

1. Ein Fach bzw. Projekt auswählen oder neu anlegen, dann eine Frage stellen. Optional `.txt`, `.md` oder `.json` (UTF-8) als Skript auswählen. Ohne Skript sind Hinweise allgemein und als nicht skriptbelegt gekennzeichnet. Skripte werden nicht dauerhaft gespeichert und beim Fachwechsel aus dem Formular entfernt.
2. Wähle eine Erklärstufe: einfach, normal (Standard) oder fachlich. Nach der Antwort kannst du die Stufe wechseln oder eine vertiefende Frage stellen. Nach „Verstanden“ kannst du eine Reflexionsaufgabe anfordern; diese Aktionen erzeugen jeweils eine neue Modellanfrage.
3. Codex wird bei verbundener Bridge vorausgewählt. Der Modellkatalog wird automatisch aus der lokalen Codex-Installation geladen; das konfigurierte Standardmodell wird vorausgewählt, sofern es im Katalog steht. Eine erfolgreiche Anfrage setzt eine gültige Anmeldung und Modellzugriff voraus.
4. Für Ollama (Port 11434) oder LM Studio (Port 1234) den lokalen Dienst starten und ein Modell laden. Beim Auswählen des Dienstes wird die Modellliste abgefragt.
5. Für OpenAI oder Gemini Modellnamen und Schlüssel für die Anfrage eingeben. Alternativ `OPENAI_API_KEY` bzw. `GEMINI_API_KEY` vor dem Start in der lokalen Umgebung setzen. Der eingegebene Schlüssel wird nach der Anfrage aus dem Formular entfernt und weder in Dateien noch in SQLite gespeichert. Konsolenausgaben protokollieren keine Anfragen.

**Cloud:** Bei Auswahl von Codex, OpenAI oder Gemini werden die Frage und ausgewählte Skriptauszüge an den jeweiligen Anbieter übertragen. Der Übungsmodus führt keine Modellanfrage aus. Für einen rein lokalen Betrieb nur ein tatsächlich lokal laufendes Modell verwenden.

## Codex und Antigravity

Im Cockpit ruft die lokale Bridge Codex direkt über die Codex-CLI auf. Alternativ kannst du den Projektordner im jeweiligen Harness öffnen und ihm `role.yaml`, `AGENTS.md`, `workflow.json`, `output.schema.json` und den relevanten Skriptauszug mit deiner Frage übergeben. Oder ein Prompt-Paket im Terminal ausgeben:

```sh
python3 cli.py --script /pfad/zum/skript.txt --question "Was ist der Deckungsbeitrag?"
```

Das Paket kann in Codex oder Antigravity eingefügt werden. Die CLI startet kein Harness automatisch und speichert das Skript nicht. Der Konsolentext kann sensible Skriptauszüge enthalten.

## Quellen, Grenzen und Speicher

Die lokale Bridge wählt anhand gemeinsamer Wörter Skriptabschnitte aus; sie ist keine semantische Suche. Ohne Treffer gibt sie eine Rückfrage statt einer erfundenen Quelle zurück. Das Modell muss ein JSON mit Verständnischeck, Hinweis, Rückfrage und Quellenstatus liefern. Ein angebliches Zitat wird deterministisch auf exakte Übereinstimmung mit den übermittelten Auszügen geprüft. Dies garantiert weder die sachliche Richtigkeit der gesamten Antwort noch die Befolgung der sokratischen Regel: LLMs können irren, Inhalte falsch deuten oder trotz Vorgaben eine Lösung verraten. Prüfe Antworten am Originalskript.

Beim Start über die Bridge werden explizit gespeicherte Lernstände und Bewertungen nach Projekt getrennt in `memory/memory.db` abgelegt – auch wenn der vorbereitete Übungsdialog ausgewählt ist. Die Memory-Grafik gruppiert deine gespeicherten Themen nach Status; sie behauptet keine Beziehungen zwischen Themen. Die Datei wird bei Bedarf automatisch erzeugt und ist durch `.gitignore` vom Repository ausgeschlossen. Skripte, Chatverlauf und Schlüssel werden dort nicht gespeichert. Im statischen Modus ohne Bridge liegt der Lernstand separat im Browser; eine automatische Synchronisierung findet nicht statt. Browserdaten und lokale Datenbank können verloren gehen: selbst sichern, wenn benötigt.

Das Zahnrad oben rechts öffnet die Einstellungen mit Modellauswahl, Dark Mode, Memory-Grafik und Trinity-Dateien. Der Entwicklungsverlauf erfasst Lernstandsänderungen ab Einführung dieser Funktion; ältere Änderungen lassen sich nicht rückwirkend rekonstruieren.

## Wie ist das Projekt aufgebaut?

Der Tutor folgt einem mehrteiligen Aufbau: Die Steuerdateien beschreiben, was er tun soll, während das Python-Programm die lokale Verarbeitung und Speicherung übernimmt.

| Datei oder Ordner | Aufgabe |
| --- | --- |
| `index.html`, `enhancements.js` | Oberfläche und interaktive Bedienung. |
| `manifest.json` | Name, Version und Metadaten des Tutors. |
| `role.yaml`, `AGENTS.md` | Rolle, Grenzen und Arbeitsregeln des Lernbegleiters. |
| `workflow.json` | Beschreibt den Ablauf von der Skriptsuche bis zur Rückmeldung. |
| `output.schema.json` | Legt die Struktur einer Tutor-Antwort fest. |
| `server.py`, `tutor_tools.py`, `cli.py` | Lokale Bridge, Skriptsuche, Quellenprüfung, Speicher und CLI-Hilfe. |
| `memory/migrations/` | Datenbankschema für den lokalen Lernfortschritt. |
| `tests/` | Tests für zentrale Funktionen. |

Die README erklärt das Projekt und zeigt seine Oberfläche. **Der Tutor selbst läuft nach dem lokalen Start im Browser**; eine GitHub-README kann die App nicht direkt interaktiv ausführen.

## GitHub Pages / Demonstration

`index.html` und `enhancements.js` können auch statisch auf GitHub Pages liegen: Dort funktionieren der vorbereitete Übungsdialog und Lernstand im Browser. Hochgeladene Unterlagen werden im Übungsmodus nicht analysiert. Modellanfragen, Datei-Inspektor, SQLite und Feedback benötigen die lokale Bridge; GitHub Pages führt kein Python aus. Keine Zugangsschlüssel im Repository hinterlegen.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

Die Tests prüfen deterministische Skriptsuche, Zitatprüfung und lokale Fortschrittsdaten; sie ersetzen keine Prüfung einzelner Modellanbieter oder der Modellqualität.
