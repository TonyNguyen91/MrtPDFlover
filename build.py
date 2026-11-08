# Build the offline app: wrap src/app.src.html in a full HTML shell with a Content-Security-Policy
# that blocks every network connection. The page may only load local files (file:) and in-memory data (data:, blob:).
#
#   python build.py          -> writes app/index.html
#   python build.py --zip    -> also writes dist/MrT-PDFlover-offline.zip (app/ folder, ready to copy to another PC)
import os, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'src', 'app.src.html')
APP = os.path.join(HERE, 'app')

CSP = ("default-src 'none'; "
       "script-src 'self' file: blob: 'unsafe-inline' 'unsafe-eval' 'wasm-unsafe-eval'; "
       "worker-src 'self' file: blob:; "
       "style-src 'self' file: 'unsafe-inline'; "
       "font-src data: blob:; "
       "img-src 'self' file: data: blob:; "
       "media-src data: blob:; "
       "connect-src data: blob:; "
       "frame-src 'self' about: blob: data:; "
       "child-src 'self' about: blob: data:; "
       "object-src 'none'; base-uri 'none'; form-action 'none'")
HEAD = ('<!doctype html><html lang="vi"><head><meta charset="utf-8">'
        '<meta http-equiv="Content-Security-Policy" content="' + CSP + '">'
        '<meta name="referrer" content="no-referrer">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<style>:root{color-scheme:light}body{margin:0;font:14px system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>'
        '</head><body>\n')

def build():
    src = open(SRC, encoding='utf-8').read()
    os.makedirs(APP, exist_ok=True)
    out = os.path.join(APP, 'index.html')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(HEAD + src + '\n</body></html>\n')
    print('built', out)

def make_zip():
    dist = os.path.join(HERE, 'dist'); os.makedirs(dist, exist_ok=True)
    out = os.path.join(dist, 'MrT-PDFlover-offline.zip')
    extra = [('CHANGELOG.md', 'CHANGELOG.md'), ('THIRD_PARTY_NOTICES.md', 'THIRD_PARTY_NOTICES.md')]
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(APP):
            for name in sorted(files):
                p = os.path.join(root, name)
                z.write(p, os.path.join('MrT-PDFlover', os.path.relpath(p, APP)))
        for rel, arc in extra:
            p = os.path.join(HERE, rel)
            if os.path.exists(p): z.write(p, os.path.join('MrT-PDFlover', arc))
        lic = os.path.join(HERE, 'licenses')
        for name in sorted(os.listdir(lic)) if os.path.isdir(lic) else []:
            z.write(os.path.join(lic, name), os.path.join('MrT-PDFlover', 'licenses', name))
    print('zipped', out)

if __name__ == '__main__':
    build()
    if '--zip' in sys.argv:
        make_zip()
