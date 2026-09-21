# CustomGOVImport

**[English instructions](README.md)**

CustomGOVImport ist ein Gramplet für Gramps 6.0 zum Importieren von Orten aus dem
[Geschichtlichen Ortsverzeichnis (GOV)](https://gov.genealogy.net/). Es ist eine
unabhängige Abspaltung des GetGOV-Gramplets und verwendet eine eigene Plugin-ID
und eigene Einstellungen.

## Funktionen

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

## Verwendung

Füge das Gramplet **CustomGOVImport** einer Gramps-Ansicht hinzu, gib eine
GOV-Objekt-ID wie `object_12345` ein und wähle **Ort holen**.

Aktiviere **Keine übergeordneten Orte importieren**, um nur das angeforderte
Objekt zu importieren. Seine direkten Referenzen auf übergeordnete Orte werden
weiterhin geprüft. Ist der referenzierte Ort bereits in Gramps vorhanden,
wird eine Beziehung angelegt; andernfalls wird die fehlende Referenz im
Live-Log gemeldet.

## Konfiguration

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

## Kompatibilität

Die Erweiterung ist für Gramps 6.0 vorgesehen und benötigt Netzwerkzugriff auf
`gov.genealogy.net`.

## Herkunft und Lizenz

CustomGOVImport basiert auf GetGOV 1.0.25 von Nick Hall und Gary Griffin aus dem
[Gramps-Addons-Projekt](https://github.com/gramps-project/addons-source/tree/maintenance/gramps60/GetGOV).

Copyright © 2015 Nick Hall

Copyright © 2024 Gary Griffin

Copyright © 2026 Sebastian Klossek

Lizenziert unter der GNU General Public License, Version 2 oder höher.
