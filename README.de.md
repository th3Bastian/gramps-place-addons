# Gramps Place Addons

Unabhängig gepflegte Gramps-Erweiterungen rund um Ortsdaten.

**[English instructions](README.md)**

## Verfügbare Erweiterungen

| Erweiterung | Status | Zweck |
| --- | --- | --- |
| [Doppelte Ortsnamen unterdrücken](HideDuplicatePlaceNames/) | Stabil für Gramps 6.0 | Fasst unmittelbar aufeinanderfolgende gleiche Ortsnamen für ausgewählte Ortsarten in der Anzeige zusammen. |
| [CustomGOVImport](CustomGOVImport/README.de.md) | Stabil für Gramps 6.0 | Importiert GOV-Orte mit konfigurierbaren ausgeschlossenen Ortsarten, optionalem Import übergeordneter Orte und Live-Log. |

## Installation über die Erweiterungsverwaltung

Die Erweiterungen werden über den Veröffentlichungszweig dieses Projekts
installiert. In Gramps 6.0:

1. Öffne **Bearbeiten → Erweiterungsverwaltung**.
2. Wähle den Tab **Projekte** und klicke auf **+**.
3. Vergib einen Namen, zum Beispiel `Bastian's Gramps Place Addons`.
4. Trage diese Adresse ein:

   ```text
   https://raw.githubusercontent.com/th3Bastian/gramps-place-addons/dist/gramps60
   ```

5. Wechsle zurück zum Tab **Erweiterungen** und aktualisiere die Liste.
6. Suche nach der Erweiterung, wähle **Installieren** und starte Gramps danach neu.

Die Projektadresse muss auf `gramps60` enden; sie ist ausdrücklich für Gramps
6.0 bestimmt.

## Doppelte Ortsnamen unterdrücken

Die Erweiterung verändert ausschließlich die Anzeige von Ortshierarchien in
Ereignis- und Textansichten. Sie ändert weder den Stammbaum noch Ortsdatensätze.

Öffne nach der Installation **Einstellungen → Ortsanzeige**. Trage eine Ortsart
pro Zeile ein. Ortsnamen werden nur dann zusammengefasst, wenn alle folgenden
Bedingungen zutreffen:

- zwei Einträge mit gleichem Namen stehen unmittelbar hintereinander;
- die Ortsart des späteren Eintrags steht in der konfigurierten Liste; und
- die Groß- und Kleinschreibung stimmt exakt mit der in Gramps gespeicherten
  Ortsart überein.

Leere und doppelte Einträge werden automatisch entfernt. Leerzeichen am Anfang
und Ende eines Eintrags werden entfernt; beim Verlassen des Felds wird die Liste
alphabetisch sortiert. Ein Wert wie `Stadt (Einheitsgemeinde)` wird unverändert
unterstützt.

Wenn man die offizielle Ortsstruktur des
[Geschichtlichen Ortsverzeichnisses (GOV)](https://gov.genealogy.net/) abbildet,
ergibt sich oft derselbe Name für eine Stadt und den darunterliegenden Wohnplatz.
Das ist zwar korrekt, macht die Ortsdarstellung aber unübersichtlich. Diese
Erweiterung macht solche Hierarchien besser lesbar, ohne die zugrunde liegenden
Daten zu verändern.

## CustomGOVImport

CustomGOVImport importiert Orte aus dem Geschichtlichen Ortsverzeichnis (GOV)
und folgt ihren ausgehenden Beziehungen zu übergeordneten Orten. Eine
konfigurierbare Liste schließt ausgewählte Ortsarten vom Import aus, während
die Suche nach zulässigen übergeordneten Orten fortgesetzt wird. Optional wird
nur der angegebene Ort importiert und mit bereits in Gramps vorhandenen
übergeordneten Orten verbunden. Fortschritt, ausgelassene Orte und fehlende
Referenzen erscheinen im Live-Log des Gramplets.

CustomGOVImport ist eine unabhängige Abspaltung des GetGOV-Gramplets mit eigener
Plugin-ID und eigenen Einstellungen.

### Funktionen

- Importiert einen GOV-Ort und seine ausgehenden Beziehungen `isPartOf` und
  `isLocatedIn`.
- Verfolgt Beziehungen zu übergeordneten Orten auch dann weiter, wenn ein
  dazwischenliegender Ort bereits in der Gramps-Datenbank vorhanden ist.
- Kann nur den angeforderten Ort importieren und mit bereits vorhandenen
  übergeordneten Orten verbinden.
- Schließt konfigurierte Ortsarten vom Import aus und untersucht deren
  Beziehungen zu übergeordneten Orten trotzdem weiter.
- Zeigt den Importfortschritt und übersprungene Referenzen in einem Live-Log an.
- Übernimmt die bevorzugte Ortssprache aus Gramps und berücksichtigt diese
  Einstellung unabhängig von ihrer Groß- und Kleinschreibung.
- Bietet übersetzte Datumsausdrücke und Oberflächentexte für Deutsch,
  Kroatisch, Niederländisch, europäisches Portugiesisch und Slowakisch.

### Verwendung

Füge das Gramplet **CustomGOVImport** einer Gramps-Ansicht hinzu, gib eine
GOV-Objekt-ID wie `object_12345` ein und wähle **Ort holen**.

Aktiviere **Keine übergeordneten Orte importieren**, um nur das angeforderte
Objekt zu importieren. Seine direkten Referenzen auf übergeordnete Orte werden
weiterhin geprüft. Ist der referenzierte Ort bereits in Gramps vorhanden,
wird eine Beziehung angelegt; andernfalls wird die fehlende Referenz im
Live-Log gemeldet.

### Konfiguration

Öffne die Gramplet-Konfiguration und trage unter **Ortsarten, die nicht
importiert werden sollen** eine GOV-Ortsart pro Zeile ein. Die Einträge müssen
exakt mit der übersetzten GOV-Ortsart übereinstimmen; Groß- und Kleinschreibung
werden dabei unterschieden. Leere Zeilen und doppelte Einträge werden beim
Speichern der Einstellungen entfernt.

Ist das angeforderte Objekt selbst ausgeschlossen, wird es nicht zu Gramps
hinzugefügt. Bei einem normalen Import werden seine Beziehungen zu
übergeordneten Orten trotzdem weiterverfolgt, damit zulässige übergeordnete
Orte importiert werden können.

Die Ausschlussliste (Blacklist) gilt gemeinsam für alle Instanzen des
CustomGOVImport-Gramplets. Sie wird nur gespeichert, wenn in der Konfiguration
die Schaltfläche **Speichern** verwendet wird.

### Kompatibilität

Die Erweiterung ist für Gramps 6.0 vorgesehen und benötigt Netzwerkzugriff auf
`gov.genealogy.net`.

### Herkunft und Lizenz

CustomGOVImport basiert auf GetGOV 1.0.25 von Nick Hall und Gary Griffin aus dem
[Gramps-Addons-Projekt](https://github.com/gramps-project/addons-source/tree/maintenance/gramps60/GetGOV).

Copyright © 2015 Nick Hall

Copyright © 2024 Gary Griffin

Copyright © 2026 Sebastian Klossek

Lizenziert unter der GNU General Public License, Version 2 oder höher.

Die vollständige deutsche Plugin-Dokumentation steht in der
[deutschen README zu CustomGOVImport](CustomGOVImport/README.de.md).

## Aktualisieren und Fehler suchen

Wenn eine neue Version veröffentlicht wird, erkennt Gramps sie über dieselbe
Projektadresse in der Erweiterungsverwaltung. Installiere das Update und starte
Gramps neu.

Falls eine Erweiterung nicht erscheint:

- prüfe, ob die Projektadresse genau zur verwendeten Gramps-Hauptversion passt;
- aktualisiere die Erweiterungsliste; und
- prüfe den **Plugin-Manager** auf Ladefehler.

Während eines Tests über die Erweiterungsverwaltung sollte keine manuell
kopierte Version derselben Erweiterung im Benutzer-Plugin-Ordner liegen: Beide
Varianten verwenden dieselbe Plugin-ID.

## Entwicklung

Der Branch `main` enthält Quellcode, Tests und Übersetzungsquellen. Der Branch
`dist` enthält die installierbaren Pakete und Addon-Listen für die
Erweiterungsverwaltung. Erst getestete Versionen werden nach `dist`
übernommen.

## Rückmeldungen und Lizenz

Fehler und Vorschläge bitte über die
[Issues](https://github.com/th3Bastian/gramps-place-addons/issues) dieses
Repositorys melden.

Jede Erweiterung dokumentiert ihr eigenes Urheberrecht und ihre Lizenz. Beide
Erweiterungen stehen unter GPL-2.0-or-later.

## Hinweis zur Entstehung

Diese Addons wurden mit Hilfe von ChatGPT entwickelt.
