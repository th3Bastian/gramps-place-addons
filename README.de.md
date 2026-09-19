# Gramps Place Addons

Unabhängig gepflegte Gramps-Erweiterungen rund um Ortsdaten.

**[English instructions](README.md)**

## Verfügbare Erweiterungen

| Erweiterung | Status | Zweck |
| --- | --- | --- |
| [Doppelte Ortsnamen unterdrücken](HideDuplicatePlaceNames/) | Stabil für Gramps 6.0 | Fasst unmittelbar aufeinanderfolgende gleiche Ortsnamen für ausgewählte Ortsarten in der Anzeige zusammen. |

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

Jede Erweiterung dokumentiert ihr eigenes Urheberrecht und ihre Lizenz.
Doppelte Ortsnamen unterdrücken steht unter GPL-2.0-or-later.

## Hinweis zur Entstehung

Dieses Addon wurde mit Hilfe von ChatGPT erstellt.
