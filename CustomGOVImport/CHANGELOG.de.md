# CustomGOVImport – Änderungen

## Version 1.2.2 – 30. Oktober 2026

- Bereinigt doppelte alternative Namen, wenn Name, Sprache und normalisiertes
  Datum durch die aktuellen GOV-Daten bestätigt werden. Alte „ab/bis“-Angaben
  werden mit „nach/vor“ abgeglichen; Zeitspannen mit identischen Grenzen mit
  einfachen Datumsangaben. Unterschiedliche Sprachen und historische Zeiträume
  bleiben erhalten. Nicht bestätigte Namen bleiben unverändert.
- Vergleicht tatsächlich leere Datumsfelder einheitlich – sowohl bei Namen als
  auch bei Ortszugehörigkeiten. Damit entstehen nach manuellem Leeren, Speichern
  und erneutem Laden keine Dubletten durch unterschiedliche interne Leerwerte.
- Die vorhandene Datumssortieroption sortiert jetzt auch alternative Namen,
  aufsteigend nach Datum bzw. Zeitspannenbeginn, undatierte zuletzt. Bei gleichen
  Datumswerten bleibt die Reihenfolge stabil; der Hauptname wird nicht sortiert.
- Gilt auch für erfolgreich abgerufene übergeordnete Orte.

## Version 1.2.1

- Korrigiert doppelte Ortszugehörigkeiten nach der Umstellung von Zeitspannen
  mit identischem Beginn und Ende auf einfache Datumsangaben.
- Bestehende Zeitspannen mit gleichen Grenzen werden nur dann in ein einfaches
  Datum umgewandelt, wenn Zielort und Datum durch die aktuellen GOV-Daten
  bestätigt werden. Passende Dubletten werden auch ohne Aktualisierungsoption
  entfernt. Dies gilt für Jahres-, Monats- und Tagesangaben.
- Zeitspannen mit unterschiedlichen Grenzen bleiben unverändert.

## Version 1.2.0

- Optionale Sortierung aller Ortszugehörigkeiten nach Bezugsdatum beziehungsweise
  Beginn der Zeitspanne. Bei gleichem Datum: vor, genaues Datum oder Zeitraum,
  danach nach. Undatierte Einträge stehen zuletzt; Grenzwerte werden nicht benutzt.
- Optionale Aktualisierung vorhandener Orte mit GOV-Daten: Hauptname, gelieferte
  Ortsart und Koordinaten, Internetadressen sowie fehlende alternative Namen.
- Nicht mehr gelieferte Zugehörigkeiten werden nur im Aktualisierungsmodus
  entfernt, wenn die Gramps-ID des übergeordneten Zielortes durch GOV bestätigt
  ist. Andere und nicht bestätigte Zuordnungen bleiben erhalten. Fehlgeschlagene
  GOV-Abfragen lösen keine Löschung aus.
- Einseitige Datumsangaben werden mit unveränderten Datumswerten als „vor“ oder
  „nach“ importiert. Geschlossene Zeitspannen bleiben „von … bis …“. Die
  GOV-Ungenauigkeit innerhalb eines Jahres oder Monats wird durch die
  Gramps-Grenzberechnung nicht vollständig abgebildet; dies ist bewusst akzeptiert.
- Vorhandene „bis/ab“-Angaben werden nur korrigiert, wenn Zielort und Zeitraum in
  der aktuellen GOV-Antwort vorkommen. Unterschiedliche Schreibweisen erzeugen
  keine Doppelungen mehr. Nicht passende Zugehörigkeiten bleiben unverändert.
- Tooltips für alle drei Checkboxen und aktualisierte Übersetzungen auf Deutsch,
  Kroatisch, Niederländisch, europäischem Portugiesisch und Slowakisch. Beide
  neuen Optionen sind standardmäßig ausgeschaltet.

## Version 1.1.0

- Sortiert ausgeschlossene Ortsarten beim Laden und Speichern alphabetisch.
- Liest die Sprache direkt aus dem ausgewählten Gramps-Ortsformat; der alte
  Zugriff auf `preferences.place-lang` entfällt.
- Wählt Ortsartenbezeichnungen in der Ortsformatsprache, ersatzweise auf Deutsch
  und danach auf Englisch, unabhängig von der Sprache des importierten Ortsnamens.
- Protokolliert die Ortsformatsprache, fehlende oder ungültige Spracheinstellungen
  und verwendete Fallback-Sprachen. Die neuen Meldungen sind auf Deutsch,
  Kroatisch, Niederländisch, europäischem Portugiesisch und Slowakisch verfügbar.
