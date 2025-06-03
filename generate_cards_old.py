import csv
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_card_background(width, height):
  '''Erstellt einen Pokemon-ähnlichen Kartenhintergrund'''

  # Erstelle ein neues Bild mit Farbverlauf
  card = Image.new('RGB', (width, height), '#f0f0f0')
  draw = ImageDraw.Draw(card)

  # Rahmen zeichnen
  border_color = '#1e3a8a'  # Dunkelblau
  draw.rectangle([0, 0, width-1, height-1], outline=border_color, width=8)
  draw.rectangle([8, 8, width-9, height-9], outline='#ff0000', width=2)#3b82f6

  # Oberer Bereich (Titel-Bereich)
  draw.rectangle([15, 15, width-15, 80], fill='#dbeafe', outline='#00ff00', width=2)

  # Hauptbereich (Text-Bereich)
  draw.rectangle([15, 90, width-15, height-80], fill='#ffffff', outline='#0000ff', width=2)

  # Unterer Bereich (Dekoration)
  draw.rectangle([15, height-75, width-15, height-15], fill='#f3f4f6', outline='#ffff00', width=2)

  return card

def wrap_text(text, font, max_width):
  '''Bricht Text in mehrere Zeilen um'''
  lines = []
  words = text.split()
  current_line = []

  for word in words:
    test_line = ' '.join(current_line + [word])
    bbox = font.getbbox(test_line)
    if bbox[2] - bbox[0] <= max_width:
      current_line.append(word)
    else:
      if current_line:
        lines.append(' '.join(current_line))
        current_line = [word]
      else:
        lines.append(word)

  if current_line:
    lines.append(' '.join(current_line))

  return lines

def create_card(name, text):
  '''Erstellt eine einzelne Spielkarte'''

  # Kartengröße (Standard Pokemon-Karte Verhältnis)
  width, height = 400, 560

  # Grundkarte erstellen
  card = create_card_background(width, height)
  draw = ImageDraw.Draw(card)

  try:
    # Schriftarten laden (falls verfügbar)
    title_font = ImageFont.truetype('arial.ttf', 24)
    text_font = ImageFont.truetype('arial.ttf', 14)
    small_font = ImageFont.truetype('arial.ttf', 12)
  except:
    # Fallback auf Standard-Schrift
    title_font = ImageFont.load_default()
    text_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

  # Titel zeichnen
  title_bbox = draw.textbbox((0, 0), name, font=title_font)
  title_width = title_bbox[2] - title_bbox[0]
  title_x = (400 - title_width) // 2
  draw.text((title_x, 35), name, fill='#1e3a8a', font=title_font)

  # Text umbrechen und zeichnen
  wrapped_text = wrap_text(text, text_font, 350)

  y_position = 110
  line_height = 20

  for line in wrapped_text:
    draw.text((25, y_position), line, fill='#374151', font=text_font)
    y_position += line_height

  # Dekorative Elemente hinzufügen
  # Kleine Punkte in den Ecken
  draw.ellipse([25, height-60, 35, height-50], fill='#3b82f6')
  draw.ellipse([width-35, height-60, width-25, height-50], fill='#3b82f6')

  # Typ-Bezeichnung
  draw.text((30, height-45), 'AKTIONSKARTE', fill='#6b7280', font=small_font)

  return card

def generate_cards_from_csv(csv_file, output_dir):
  '''Liest CSV-Datei und generiert Karten'''

  # Output-Verzeichnis erstellen falls nicht vorhanden
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  # CSV-Datei lesen
  with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')

    card_count = 0
    for row in reader:
      print(f'{row = }')
      name = row[0].strip()  # Name aus der ersten Spalte
      text = row[1].strip()  # Name aus der ersten Spalte
      print(f'{name = }')
      print(f'{text = }')

      # Karte erstellen
      card = create_card(name, text)

      # Dateiname erstellen (Sonderzeichen entfernen)
      safe_name = ''.join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
      filename = f'{card_count+1:03d}_{safe_name}.jpg'
      filepath = os.path.join(output_dir, filename)

      # Karte speichern
      card.save(filepath, 'JPEG', quality=95)
      card_count += 1
      if card_count == 8:
        break

    print(f"\n{card_count} Karten erfolgreich erstellt in '{output_dir}'")

def main():
  '''Hauptfunktion'''
  # Konfiguration
  csv_file = 'spielkarten.csv'  # Name der CSV-Datei
  output_dir = 'spielkarten_output'  # Ausgabe-Verzeichnis

  print('Spielkarten-Generator gestartet...')
  print(f'Lese CSV-Datei: {csv_file}')
  print(f'Ausgabe-Verzeichnis: {output_dir}')
  print('-' * 50)

  # Karten generieren
  generate_cards_from_csv(csv_file, output_dir)

  print('-' * 50)
  print('Fertig!')

if __name__ == '__main__':
  main()
