import csv

CSV_FILE = "bible_reading_plan.csv"
OUTPUT_FILE = "formatted_bible_messages.txt"

def reformat_questions_answers():
    with open(CSV_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
            for row in reader:
                # Split questions and answers by '||' for OT and NT
                questions_parts = row["Questions"].split("||")
                answers_parts = row["Answers"].split("||")

                # Prepare Questions section
                out.write(f"📅 {row['Date']} - Questions\n\n")
                num = 1
                for idx, chapter_q in enumerate(questions_parts):
                    # Split each chapter's questions by newline or semicolon
                    chapter_lines = [q.strip() for q in chapter_q.replace("\n", ";").split(";") if q.strip()]
                    # Get chapter name from first line (optional: you can store in CSV)
                    chapter_name = chapter_lines[0].split()[0]  # naive, first word as chapter
                    out.write(f"**{chapter_lines[0].split()[0]}**\n")
                    for q in chapter_lines:
                        out.write(f"{num}️⃣  {q}\n\n")
                        num += 1

                # Prepare Answers section
                out.write("\n📜 Answers\n\n")
                num = 1
                for idx, chapter_a in enumerate(answers_parts):
                    chapter_lines = [a.strip() for a in chapter_a.replace("\n", ";").split(";") if a.strip()]
                    out.write(f"**{questions_parts[idx].split()[0]}**\n")
                    for a in chapter_lines:
                        out.write(f"{num}️⃣  {a}\n\n")
                        num += 1

    print(f"✅ Reformatted messages saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    reformat_questions_answers()
