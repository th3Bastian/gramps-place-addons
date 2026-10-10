# CustomDetails — Version 1.3.0

Gramplet für Gramps 6.0, erstellt auf Grundlage von `persondetails.py` aus
Gramps 6.0.8. Die ursprünglichen Urheber- und GPL-Hinweise bleiben erhalten.
Lizenz: GPL Version 2 oder neuer.

## Aktivieren

Gramps neu starten. In der Personenansicht das Menü der unteren Leiste oder
Seitenleiste öffnen und unter „Gramplet hinzufügen“ **CustomDetails** wählen.
Das bisherige Details-Gramplet kann anschließend aus dieser Leiste entfernt werden.

## Bezugsperson und Nummern

Die in Gramps festgelegte Hauptperson ist die Bezugsperson mit Nummer 1.
„Als Hauptperson festlegen“ in Gramps ändert die Bezugsperson. Ihr Name und ihre
Gramps-ID werden angezeigt. Ohne Hauptperson erscheint ein entsprechender Hinweis.
Vater = 2n, Mutter = 2n+1. Alle Nummern einer mehrfach vorkommenden Person werden
angezeigt. Nicht-Vorfahren erhalten einen entsprechenden Text.

Die Berechnung folgt der **Hauptelternfamilie**, genau wie die Elternanzeige des
Original-Gramplets. Sie folgt deshalb auch Adoptiv- oder Pflegeeltern, wenn diese
Familie als Hauptelternfamilie gesetzt ist. Das kann vom Ahnenlistenbericht abweichen,
der nach Geburtsbeziehungen sucht.

Die Anzeige aktualisiert sich beim Personenwechsel, Hauptpersonenwechsel und bei
Änderungen an Personen und Familien; Ereignisse, Orte und Medien aktualisieren die
übernommenen Detailangaben ebenfalls. Ein Nummern-Cache wird bei Änderungen an
Personen, Familien oder der Hauptperson verworfen. Es werden keine genealogischen
Daten oder Personenattribute geschrieben.

Zyklische Beziehungen werden erkannt. Die Berechnung ist auf 100 Elternschritte
und 100.000 Pfadpositionen begrenzt. Bei fehlenden Datensätzen, Zyklen oder einer
erreichten Grenze wird die möglicherweise unvollständige Anzeige gekennzeichnet.

Alle Anzeige- und Konfigurationstexte verwenden die Spracheinstellung von Gramps;
Deutsch und Englisch sind vollständig hinterlegt.

Die Kekulé-Nummer und Bezugsperson stehen unter den ursprünglichen Detailangaben.

Alle Personenattribute werden mit Typ und Wert in gespeicherter Reihenfolge vor den Kekulé-Angaben angezeigt. Mehrfach vorkommende Attribute erhalten eigene Zeilen.

Zwischen Bezugsperson und Kekulé-Nummer wird die Verwandtschaft der ausgewählten Person zur Hauptperson angezeigt. Verwendet werden Gramps’ lokalisierte Verwandtschaftsberechnung und eingestellte Generationen-Suchtiefe. Bei mehreren Beziehungen erscheint die von Gramps als relevanteste ausgewählte Beziehung; die Kekulé-Anzeige enthält weiterhin alle berechneten Nummern.


## Konfiguration

Die Gramplet-Konfiguration öffnen, wie bei CustomGOVImport. Die drei Checkboxen
„Bezugsperson anzeigen“, „Verwandtschaft anzeigen“ und „Kekulé-Nummer anzeigen“
sind unabhängig voneinander und anfangs aktiviert.

Unter „Folgende Attribute anzeigen“ einen Attributtyp pro Zeile eintragen, so wie
er in Gramps angezeigt wird. Groß-/Kleinschreibung und äußere Leerzeichen werden
ignoriert. Nur aufgeführte Typen werden angezeigt; eine leere Liste blendet alle
Attribute aus. Mehrfache Werte bleiben eigene Zeilen. Anfangs ist die Liste mit
Standardtypen und den bekannten eigenen Attributtypen des geöffneten Stammbaums
vorbelegt. Nach dem ersten Speichern wird ausschließlich die gespeicherte Liste
verwendet; neue Attributtypen müssen dann ausdrücklich ergänzt werden.

Erst „Speichern“ übernimmt Änderungen. Einstellungen werden wie bei CustomGOVImport
über einen eigenen Gramps-Konfigurationsmanager gespeichert und zwischen geöffneten
CustomDetails-Instanzen geteilt. Ausgeblendete Verwandtschafts- und Kekulé-Angaben
werden nicht berechnet.

Die Attributliste wird beim Laden und Speichern alphabetisch nach der aktuellen Sprachumgebung sortiert, ohne Unterscheidung der Groß-/Kleinschreibung. Nach „Speichern“ zeigt das Textfeld unmittelbar die sortierte, bereinigte Liste.

Die Checkboxen stehen ohne zusätzliche Beschriftungen davor über die volle Breite. Ihre eigenen Texte bleiben erhalten.


## d’Aboville-Nummerierung

Unter der Kekulé-Nummer wird die d’Aboville-Nummer angezeigt. Die Gramps-Hauptperson
ist Ausgangsperson 1. Ihre Kinder erhalten 1.1, 1.2 usw.; deren Kinder beispielsweise
1.2.1. Gezählt wird nach der gespeicherten Reihenfolge der Familien und ihrer Kinder
über alle Familien eines Elternteils hinweg, wie im ausführlichen Nachkommenbericht
von Gramps. Geburtsdaten werden nicht zum Sortieren verwendet. Alle eingetragenen
Kindbeziehungen werden berücksichtigt, auch Adoptiv- und Pflegekinder. Partner
bekommen allein durch ihre Partnerschaft keine Nachkommennummer.

Bei mehreren Abstammungswegen erscheinen alle gültigen Nummern, numerisch nach
Pfad sortiert. Wer kein Nachkomme der Hauptperson ist, erhält einen entsprechenden
Hinweis. Änderungen an Personen, Familien oder Hauptperson leeren den Nummern-Cache.
Zyklen und fehlende Datensätze führen zu einem Berechnungshinweis. Dieselben Grenzen
wie bei Kekulé gelten: 100 Kindschritte und 100.000 Pfadpositionen.

Die vierte Checkbox „d’Aboville-Nummer anzeigen“ ist anfangs aktiviert. Sie ist
unabhängig von der Kekulé-Anzeige; bei ausgeschalteter Checkbox wird die
Nachkommennummerierung nicht berechnet. Bereits gespeicherte Anzeige- und
Attributeinstellungen bleiben erhalten.

Das Foto ist am oberen Rand seines linken Bildbereichs ausgerichtet.

Der Bildbereich hat oben und unten jeweils 5 Pixel Abstand.


## Sprache

CustomDetails verwendet die in Gramps gewählte Sprache. Englische Ausgangstexte und deutsche sowie englische Übersetzungskataloge liegen im Plugin. `po/` enthält die bearbeitbaren Sprachdateien und `locale/` die kompilierten Laufzeitdateien. Die Konfiguration verwendet weiterhin dieselben Schlüssel. Namen und Attributwerte aus dem Stammbaum werden nicht übersetzt.
