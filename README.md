# Überwachungssystem basierend auf der IMU des M5-Sticks

#### Erstellt am 21.04.2022
#### Zuletzt bearbeitet am 17.06.2022

## Table of Contents
1. [Autoren](#autoren)
2. [Projektbeschreibung](#projektbeschreibung)
3. [Verzeichnisstruktur](#verzeichnisstruktur)
4. [Kurzbeschreibung aller Dateien](#kurzbeschreibung-aller-dateien)

### Autoren
***
Lukas Ohdens, 7013982, 6. Semester Maschinenbau & Design <br>
Michel Grüther, 7013909, 6. Semester Maschinenbau & Design <br>
Luca Schulte, 7014030, 6. Semester Maschinenbau & Design <br>
Alexander Maul, 7014104, 6. Semester Maschinenbau & Design <br>
Hauke Helms, 7013828, 6. Semester Maschinenbau & Design <br>

### Projektbeschreibung
***
Die Aufgabe besteht darin, ein “Überwachungssystem basierend auf der IMU des M5-Sticks” zu erstellen. 
Das Überwachungssystem wird als Alarmanlage in einer “Internet of Things” (IoT) Anwendung in einem Smarthome eingebunden. 
Der M5StickC wird an Türen und Fenstern montiert und fungiert als Sensor, der mithilfe seiner IMU Bewegungen erkennt.
Ein Raspberry Pi 4B wird die Aufgabe der Alarmausgabe übernehmen und als Knotenpunkt für weitere M5StickC.

### Verzeichnisstruktur
***
In der .zip M5StickAlarmanlage sind alle nötigen Dateien für die Textdokumente enthalten. <br>
Im Unterordner Bilder sind die verwendeten Grafiken und Bilder zu finden. <br>
Im Unterordner CAD sind die 3D-gedruckten Bauteile im .stl Format abgelegt. <br>
Unter Quellen sind die Literaturen sowie die Internetquellen abgelegt. <br>
Das Verzeichnis Datenblaetter enthält die Datenblätter für unsere Hardwarekomponenten. <br>
Im Verzeichnis Entwicklerdokumentation finden sich die Unterkapitel für die Dokumentation, die package Datei und die Literatur.bib <br>
Im Verzeichnis Bedienungsanleitung finden sich die Unterkapitel für die Bedienungsanleitung <br>

### Kurzbeschreibung aller Dateien
***
**EntwicklerdokumentationM5StickAlarm.pdf:** In dieser Datei ist unsere Dokumentation zum Projekt zu finden. Darin enthalten sind die Bestellliste, die Beschreibung der Hardware, Herausforderungen und Lösungen. <br>
**EntwicklerdokumentationM5StickAlarm.tex:** Dies ist der TeX Quellcode für das oben aufgeführte .pdf Dokument mit gleichem Namen. Diese Datei ist die Root-Datei und fasst alle Unterkapitel zusammen. <br>
**Bedienungsanleitung.pdf:** In dieser Datei sind die Funktionen für den Nutzer erklärt. Sie beschreibt die Hardware und die vorgesehene Nutzung unseres Produkts. <br>
**Bedienungsanleitung.tex:** Dies ist der TeX Quellcode zur Bedienungsanleitung.pdf. Sie ist die Root-Datei für die Unterkapitel. <br>
**Schnelleinstieg.pdf** Ein einseitiger Schnelleinstieg für die Nutzung des Überwachungssystems. <br>
**Schnelleinstieg.tex** Dies ist der TeX Quellcode für das oben aufgeführte .pdf Dokument mit gleichem Namen. <br>
**Literatur.bib:** Dieses bibfile enthält alle Quellen und Literaturen, die wir für unsere Dokumentationen genutzt haben. <br>
**package.tex:** Dies ist eine Konfigurationsdatei, die in unseren .tex Files eingebunden wird. Sie enthält alle benötigten Pakete und Formatierungen.
**README.md:** Diese Datei, sie dient der Übersicht und Kurzbeschreibung unseres Projekts. <br>
**author.xlsx:** Enthält Informationen zu den Authoren. <br>
**Poster.pdf:** Ein Poster zur Präsentation des Ergebnisses <br>