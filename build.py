#!/usr/bin/env python3
"""master-blog: skill dosyalarindan ve terim verisinden tek dosyalik siteyi uretir."""
import json, subprocess, pathlib, sys

ROOT   = pathlib.Path(__file__).parent
SKILL  = ROOT / "skill" / "master-blog"
SITE   = ROOT / "site"
DIST   = ROOT / "docs"   # GitHub Pages kaynağı (main dalı /docs)
TERMSJS = SITE / "data" / "terms.js"

# 1) terms.js -> JSON
terms = json.loads(subprocess.run(
    ["node", "-e", f"const t=eval(require('fs').readFileSync({json.dumps(str(TERMSJS))},'utf8')+'; TERMS');process.stdout.write(JSON.stringify(t))"],
    capture_output=True, text=True, check=True).stdout)

# 2) terim sozlugunu skill referansi olarak uret
LEVELS = {"Başlangıç": 1, "Orta": 2, "İleri": 3, "Uzman": 4}
lines = ["# Terimler Sözlüğü",
         "",
         f"Bu dosya `site/data/terms.js` dosyasından üretilir; elle düzenlenmez. {len(terms)} terim.",
         "",
         "Kullanıcıya bir terimi açıklarken buradaki yapıyı kullan: tanım → basit anlatım →",
         "teknik anlatım → neden önemli → örnek → yaygın yanılgı.",
         ""]
for cat in ["Claude", "SEO", "İçerik", "Teknik"]:
    grup = sorted([t for t in terms if t["cat"] == cat], key=lambda t: (LEVELS.get(t["level"], 9), t["name"]))
    if not grup:
        continue
    lines += [f"## {cat}", ""]
    for t in grup:
        lines += [f"### {t['name']} ({t['en']})", "",
                  f"`{t['cat']}` · `{t['level']}` · skill'de: {t['usedIn']}", "",
                  f"**Tanım.** {t['short']}", "",
                  "**Basitçe.**", "", t["simple"], "",
                  "**Teknik olarak.**", "", t["technical"], "",
                  "**Neden önemli.**", "", t["why"], "",
                  "**Örnek.**", "", t["example"], "",
                  "**Yaygın yanılgı.**", "", t["myth"], "",
                  "**İlgili terimler:** " + ", ".join(
                      next(x["name"] for x in terms if x["slug"] == r) for r in t["related"]), "",
                  "---", ""]
(SKILL / "references" / "terimler-sozlugu.md").write_text("\n".join(lines), encoding="utf-8")

# 3) skill dosyalari
ORDER = ["SKILL.md",
         "references/yayin-oncesi-kontrol.md",
         "references/terimler-sozlugu.md",
         "references/schema-ve-geo.md",
         "references/kaynaklar.md",
         "scripts/kontrol.py"]
files = []
for rel in ORDER:
    p = SKILL / rel
    files.append({"name": p.name, "path": f"master-blog/{rel}", "text": p.read_text(encoding="utf-8")})

# 4) tek komutluk kurulum betigi
HEREDOC = "MASTERBLOG_EOF"
cmd = ["mkdir -p ~/.claude/skills/master-blog/references ~/.claude/skills/master-blog/scripts"]
for rel, f in zip(ORDER, files):
    assert HEREDOC not in f["text"], f"heredoc sinirlayicisi dosyada geciyor: {rel}"
    cmd.append(f"cat > ~/.claude/skills/master-blog/{rel} <<'{HEREDOC}'\n{f['text'].rstrip()}\n{HEREDOC}")
cmd.append("chmod +x ~/.claude/skills/master-blog/scripts/kontrol.py")
cmd.append('echo "master-blog kuruldu -> ~/.claude/skills/master-blog (yeni bir Claude oturumu baslat)"')
install_cmd = "\n".join(cmd) + "\n"

# 5) siteyi uret
tpl = (SITE / "template.html").read_text(encoding="utf-8")
terms_src = TERMSJS.read_text(encoding="utf-8")
data = (terms_src.rstrip().rstrip(";") + ";\n"
        + "const FILES = " + json.dumps(files, ensure_ascii=False) + ";\n"
        + "const INSTALL_CMD = " + json.dumps(install_cmd, ensure_ascii=False) + ";\n")
data = data.replace("</script>", "<\\/script>")
out = tpl.replace("/*__DATA__*/", data)
DIST.mkdir(exist_ok=True)
(DIST / "index.html").write_text(out, encoding="utf-8")

kb = len(out.encode("utf-8")) / 1024
print(f"docs/index.html · {kb:.0f} KB · {len(terms)} terim · {len(files)} dosya · "
      f"{sum(len(f['text'].splitlines()) for f in files)} satir skill")
