"""Erzeugt index.html aus tracks.json (einmal ausführen nach Änderungen an der Kapitelliste)."""
import json, html

T = json.load(open("tracks.json", encoding="utf-8"))
total = sum(t["d"] for t in T)
h, m = int(total // 3600), round((total % 3600) / 60)

def mmss(s):
    s = int(round(s)); return f"{s // 60}:{s % 60:02d}"

rows = []
for i, t in enumerate(T):
    sub = f'<span class="sub">{html.escape(t["sub"])}</span>' if t["sub"] else ""
    rows.append(f'''      <li class="track" data-i="{i}">
        <button class="pick" type="button" aria-label="{html.escape((t["sub"] + ": " if t["sub"] else "") + t["title"])} abspielen">
          <span class="nr">{t["n"]}</span>
          <span class="name"><span class="title">{html.escape(t["title"])}</span>{sub}</span>
          <span class="dur">{mmss(t["d"])}</span>
        </button>
        <a class="dl" href="{t["f"]}" download aria-label="Teil {t["n"]} herunterladen" title="Herunterladen">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v11m0 0-4.5-4.5M12 15l4.5-4.5M5 19.5h14"/></svg>
        </a>
      </li>''')

page = open("page.tpl.html", encoding="utf-8").read()
page = (page.replace("{{ROWS}}", "\n".join(rows))
            .replace("{{TRACKS}}", json.dumps([{"t": t["title"], "s": t["sub"], "f": t["f"], "d": t["d"]} for t in T], ensure_ascii=False))
            .replace("{{MANN}}", open("img/mann.svg.html", encoding="utf-8").read())
            .replace("{{TOTAL}}", f"{h} Stunden {m} Minuten"))
open("index.html", "w", encoding="utf-8").write(page)
print("index.html geschrieben,", len(T), "Teile,", f"{h} h {m} min")
