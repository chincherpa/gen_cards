import csv
import math
import os
from PIL import Image, ImageDraw, ImageFont
import random

def create_card_background():
  """Erstellt einen Pokemon-ähnlichen Kartenhintergrund"""
  # Kartengröße (Standard Pokemon-Karte Verhältnis)
  global width, height
  # Breite und Höhe der Karte
  width, height = 400, 560

  # Erstelle ein neues Bild mit Farbverlauf
  card = Image.new('RGB', (width, height), '#f0f0f0')
  draw = ImageDraw.Draw(card)

  # Rahmen zeichnen
  border_color = '#1e3a8a'  # Dunkelblau
  draw.rectangle([0, 0, width-1, height-1], outline=border_color, width=8)
  draw.rectangle([8, 8, width-9, height-9], outline='#3b82f6', width=2)

  # Oberer Bereich (Titel-Bereich)
  draw.rectangle([15, 15, width-15, 80], fill='#fff', outline='#3b82f6', width=2)

  # Bild-Bereich (neue Sektion für das Bild)
  draw.rectangle([15, 90, width-15, 320], fill='#ffffff', outline='#3b82f6', width=2)

  # Text-Bereich (verschoben nach unten)
  draw.rectangle([15, 330, width-15, height-80], fill='#ffffff', outline='#3b82f6', width=2)

  # Unterer Bereich (Dekoration)
  draw.rectangle([15, height-75, width-15, height-15], fill='#f3f4f6', outline='#3b82f6', width=2)

  return card

def create_generic_image(width, height, card_number, name):
  """Erstellt ein generisches Bild mit geometrischen Mustern"""
  # Erstelle ein neues Bild
  img = Image.new('RGB', (width, height))
  draw = ImageDraw.Draw(img)

  # Farbpaletten für verschiedene Karten-Typen
  color_palettes = [
    ['#3b82f6', '#1e40af', '#60a5fa', '#93c5fd'],  # Blau-Töne
    ['#ef4444', '#dc2626', '#f87171', '#fca5a5'],  # Rot-Töne
    ['#10b981', '#059669', '#34d399', '#6ee7b7'],  # Grün-Töne
    ['#f59e0b', '#d97706', '#fbbf24', '#fcd34d'],  # Gelb-Töne
    ['#8b5cf6', '#7c3aed', '#a78bfa', '#c4b5fd'],  # Lila-Töne
    ['#ec4899', '#db2777', '#f472b6', '#f9a8d4'],  # Pink-Töne
  ]

  # Wähle Farbpalette basierend auf Kartennummer
  palette = color_palettes[int(card_number) % len(color_palettes)]

  # Hintergrund-Farbverlauf
  for y in range(height):
    ratio = y / height
    color_index = int(ratio * (len(palette) - 1))
    next_color_index = min(color_index + 1, len(palette) - 1)

    # Interpoliere zwischen zwei Farben
    color1 = palette[color_index]
    color2 = palette[next_color_index]

    # Einfacher Farbverlauf
    draw.line([(0, y), (width, y)], fill=color1)

  # Verschiedene Muster basierend auf Kartennummer
  pattern_type = int(card_number) % 5

  if pattern_type == 0:
    # Kreise
    for i in range(8):
      x = random.randint(10, width-50)
      y = random.randint(10, height-50)
      size = random.randint(20, 60)
      color = palette[random.randint(0, len(palette)-1)]
      # Transparenter Effekt durch hellere Farbe
      draw.ellipse([x, y, x+size, y+size], outline=color, width=3)

  elif pattern_type == 1:
    # Dreiecke
    for i in range(6):
      x1 = random.randint(20, width-40)
      y1 = random.randint(20, height-40)
      size = random.randint(30, 50)
      color = palette[random.randint(0, len(palette)-1)]

      # Dreieck zeichnen
      points = [
        (x1, y1),
        (x1 + size, y1),
        (x1 + size//2, y1 - size)
      ]
      draw.polygon(points, outline=color, width=2)

  elif pattern_type == 2:
    # Rechtecke
    for i in range(5):
      x = random.randint(10, width-80)
      y = random.randint(10, height-60)
      w = random.randint(40, 80)
      h = random.randint(30, 60)
      color = palette[random.randint(0, len(palette)-1)]
      draw.rectangle([x, y, x+w, y+h], outline=color, width=3)

  elif pattern_type == 3:
    # Sterne
    for i in range(4):
      center_x = random.randint(30, width-30)
      center_y = random.randint(30, height-30)
      radius = random.randint(20, 35)
      color = palette[random.randint(0, len(palette)-1)]

      # 5-zackiger Stern
      points = []
      for j in range(10):
        angle = j * math.pi / 5
        if j % 2 == 0:
          r = radius
        else:
          r = radius * 0.5
        x = center_x + r * math.cos(angle)
        y = center_y + r * math.sin(angle)
        points.append((x, y))

      draw.polygon(points, outline=color, width=2)

  else:
    # Wellenlinien
    for i in range(6):
      y_base = random.randint(30, height-30)
      color = palette[random.randint(0, len(palette)-1)]

      # Wellenlinie zeichnen
      points = []
      for x in range(0, width, 10):
        y = y_base + 20 * math.sin(x * 0.05 + i)
        points.append((x, y))

      # Linie durch Punkte zeichnen
      for j in range(len(points)-1):
        draw.line([points[j], points[j+1]], fill=color, width=3)

  # Kartenname als Wasserzeichen (optional)
  try:
    font = ImageFont.truetype('ITCKRIST.TTF', 20)
  except:
    font = ImageFont.load_default()

  # Halbtransparenter Text
  text_img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
  text_draw = ImageDraw.Draw(text_img)

  # Text in der Mitte
  bbox = text_draw.textbbox((0, 0), name, font=font)
  text_width = bbox[2] - bbox[0]
  text_height = bbox[3] - bbox[1]
  text_x = (width - text_width) // 2
  text_y = (height - text_height) // 2

  text_draw.text((text_x, text_y), name, fill=(255, 255, 255, 128), font=font)

  # Text-Layer auf Hauptbild anwenden
  img = Image.alpha_composite(img.convert('RGBA'), text_img).convert('RGB')

  return img

def load_and_resize_image(image_path, target_width, target_height):
  """Lädt und skaliert ein Bild auf die gewünschte Größe"""
  try:
    img = Image.open(image_path)

    # Bild proportional skalieren
    img_ratio = img.width / img.height
    target_ratio = target_width / target_height

    if img_ratio > target_ratio:
      # Bild ist breiter als das Zielformat
      new_width = target_width
      new_height = int(target_width / img_ratio)
    else:
      # Bild ist höher als das Zielformat
      new_height = target_height
      new_width = int(target_height * img_ratio)

    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return img_resized
  except Exception as e:
    print(f"Fehler beim Laden des Bildes {image_path}: {e}")
    return None

def wrap_text(text, font, max_width):
  """Bricht Text in mehrere Zeilen um"""
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

def create_card(name, text, card_number, jpgs_dir, output_dir):
  """Erstellt eine einzelne Spielkarte"""
  # Grundkarte erstellen
  card = create_card_background()
  draw = ImageDraw.Draw(card)

  try:
    # Schriftarten laden (falls verfügbar)
    title_font = ImageFont.truetype('verdana.ttf', 20)
    text_font = ImageFont.truetype('verdana.ttf', 18)
    small_font = ImageFont.truetype('verdana.ttf', 12)
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

  # Bild einfügen
  image_width = 400 - 30  # Breite minus Rahmen
  image_height = 320 - 90 - 10  # Höhe des Bildbereichs minus Padding

  # Versuche das entsprechende Bild zu laden
  possible_extensions = ['.jpg', '.jpeg', '.JPG', '.JPEG']
  image_loaded = False
  card_image = None

  for ext in possible_extensions:
    image_path = os.path.join(jpgs_dir, f"{card_number}{ext}")
    if os.path.exists(image_path):
      card_image = load_and_resize_image(image_path, image_width, image_height)
      if card_image:
        image_loaded = True
        print(f"  -> Bild eingefügt: {image_path}")
        break

  # Wenn kein Bild gefunden wurde, generiere ein generisches Bild
  if not image_loaded:
    print(f"  -> Generiere generisches Bild für Karte {card_number}")
    card_image = create_generic_image(image_width, image_height, card_number, name)

  # Bild zentriert einfügen
  if card_image:
    img_x = 15 + (image_width - card_image.width) // 2
    img_y = 95 + (image_height - card_image.height) // 2
    card.paste(card_image, (img_x, img_y))

  # Text umbrechen und zeichnen (jetzt in den unteren Bereich)
  wrapped_text = wrap_text(text, text_font, 350)

  y_position = 340
  line_height = 16
  max_lines = 8  # Begrenzte Anzahl von Zeilen im Textbereich

  for i, line in enumerate(wrapped_text[:max_lines]):
    if y_position > 460:  # Nicht über den unteren Rand hinaus
      break
    draw.text((25, y_position), line, fill='#374151', font=text_font)
    y_position += line_height

  # Warnung wenn Text zu lang ist
  if len(wrapped_text) > max_lines:
    draw.text((25, y_position), "...", fill='#ef4444', font=text_font)

  # Dekorative Elemente hinzufügen
  # Kleine Punkte in den Ecken
  draw.ellipse([25, height-60, 35, height-50], fill='#3b82f6')
  draw.ellipse([400-35, height-60, 400-25, height-50], fill='#3b82f6')

  # Typ-Bezeichnung und Kartennummer
  # draw.text((30, height-45), "AKTIONSKARTE", fill='#6b7280', font=small_font)
  draw.text((300, height-45), f"#{card_number}", fill='#6b7280', font=small_font)

  return card

def generate_cards_from_csv(csv_file, jpgs_dir, output_dir):
  """Liest CSV-Datei und generiert Karten"""

  # Output-Verzeichnis erstellen falls nicht vorhanden
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  # Prüfen ob jpgs-Verzeichnis existiert
  if not os.path.exists(jpgs_dir):
    print(f"Warnung: JPG-Verzeichnis '{jpgs_dir}' nicht gefunden!")
    print("Karten werden ohne Bilder erstellt.")

  # CSV-Datei lesen
  with open(csv_file, 'r', encoding='utf-8-sig') as file:
    reader = csv.reader(file, delimiter=';')

    card_count = 0
    for row_number, row in enumerate(reader, start=1):  # Start bei 1 für Kartennummerierung
      print(f'{row = }')
      name = row[0].strip()  # Name aus der ersten Spalte
      text = row[1].strip()  # Name aus der ersten Spalte
      row_number = f"{row_number:03d}"
      print(f"Erstelle Karte {row_number}: {name}")

      # Karte erstellen
      card = create_card(name, text, row_number, jpgs_dir, output_dir)

      # Dateiname erstellen (Sonderzeichen entfernen)
      safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
      filename = f"{row_number}_{safe_name}.jpg"
      filepath = os.path.join(output_dir, filename)

      # Karte speichern
      card.save(filepath, 'JPEG', quality=95)
      card_count += 1
      if card_count == 10:
        break

    print(f"\n{card_count} Karten erfolgreich erstellt in '{output_dir}'")

def main():
  """Hauptfunktion"""
  # Konfiguration
  csv_file = "spielkarten.csv"  # Name der CSV-Datei
  jpgs_dir = "jpgs"  # Verzeichnis mit den JPG-Bildern
  output_dir = "spielkarten_output"  # Ausgabe-Verzeichnis

  print("Spielkarten-Generator mit Bildern gestartet...")
  print(f"Lese CSV-Datei: {csv_file}")
  print(f"Bild-Verzeichnis: {jpgs_dir}")
  print(f"Ausgabe-Verzeichnis: {output_dir}")
  print("-" * 50)

  # Karten generieren
  generate_cards_from_csv(csv_file, jpgs_dir, output_dir)

  print("-" * 50)
  print("Fertig!")

if __name__ == "__main__":
  main()