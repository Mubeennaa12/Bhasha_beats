def create_story_tile(text, keywords, bg_image='assets/default_bg.jpg', output_dir='tiles'):
    os.makedirs(output_dir, exist_ok=True)
    img = Image.open(bg_image).convert("RGB")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", size=28)
    except:
        font = ImageFont.load_default()

    width, height = img.size
    margin = 50
    lines = []
    words = text.split(' ')
    line = ""

    for word in words:
        test_line = line + word + " "
        if draw.textlength(test_line, font=font) < (width - 2 * margin):
            line = test_line
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    y_text = margin
    for line in lines:
        draw.text((margin, y_text), line, font=font, fill="black")
        y_text += 35

    # Add keywords at the bottom
    kw_text = "Keywords: " + ", ".join(keywords)
    draw.text((margin, height - 50), kw_text, font=font, fill="gray")

    filename = f"{output_dir}/story_{uuid.uuid4().hex[:6]}.jpg"
    img.save(filename)
    return filename
