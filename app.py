from flask import Flask, render_template_string, send_file, request, jsonify
from PIL import Image
import colorsys
import io
import random

app = Flask(__name__)

DIACRITICS = [chr(i) for i in range(0x0300, 0x036F + 1)]
BASE_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

def generate_rainbow_gif(w, h, n):
    frames = [Image.new("RGB", (w, h), tuple(int(c * 255) for c in colorsys.hsv_to_rgb(i/n, 1, 1))) for i in range(n)]
    out = io.BytesIO()
    frames[0].save(out, format="GIF", save_all=True, append_images=frames[1:], duration=50, loop=0)
    out.seek(0)
    return out

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Toolbox</title>
    <style>
        :root { --primary: #000; --bg: #ffffff; --border: #e0e0e0; }
        body { font-family: -apple-system, sans-serif; background: var(--bg); color: #333; max-width: 400px; margin: auto; padding: 40px 20px; }
        h1 { font-size: 1.2rem; font-weight: 600; margin-bottom: 30px; text-align: center; }
        section { margin-bottom: 40px; border-bottom: 1px solid var(--border); padding-bottom: 20px; }
        h2 { font-size: 0.9rem; text-transform: uppercase; color: #888; margin-bottom: 15px; }
        .field { margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; }
        label { font-size: 0.85rem; }
        input { width: 60px; border: 1px solid var(--border); border-radius: 4px; padding: 4px; text-align: right; }
        button { width: 100%; padding: 10px; background: var(--primary); color: white; border: none; border-radius: 6px; cursor: pointer; }
        #preview { margin-top: 15px; word-break: break-all; font-size: 0.9rem; background: #f9f9f9; padding: 10px; }
    </style>
</head>
<body>
    <h1>Web Toolbox</h1>
    <section>
        <h2>Rainbow GIF</h2>
        <form action="/download-gif" method="get">
            <div class="field"><label>Size (px)</label> <div><input type="number" name="w" value="200"> × <input type="number" name="h" value="200"></div></div>
            <div class="field"><label>Frames</label> <input type="number" name="n" value="30"></div>
            <button type="submit">Download GIF</button>
        </form>
    </section>
    <section>
        <h2>Zalgo Generator</h2>
        <div class="field"><label>Length (m)</label> <input type="number" id="m" value="5"></div>
        <div class="field"><label>Level (n)</label> <input type="number" id="zn" value="10"></div>
        <button onclick="generateZalgo()">Generate & Copy</button>
        <div id="preview">Results will appear here...</div>
    </section>
    <script>
        async function generateZalgo() {
            const m = document.getElementById('m').value;
            const n = document.getElementById('zn').value;
            const res = await fetch(`/api/zalgo?m=${m}&n=${n}`).then(r => r.json());
            document.getElementById('preview').innerText = res.result;
            navigator.clipboard.writeText(res.result);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download-gif')
def download_gif():
    w = int(request.args.get('w', 200))
    h = int(request.args.get('h', 200))
    n = int(request.args.get('n', 30))
    gif_io = generate_rainbow_gif(w, h, n)
    return send_file(gif_io, mimetype='image/gif', as_attachment=True, download_name='rainbow.gif')

@app.route('/api/zalgo')
def api_zalgo():
    m = int(request.args.get('m', 5))
    n = int(request.args.get('n', 10))
    res = "".join(random.choice(BASE_CHARS) + "".join(random.choice(DIACRITICS) for _ in range(n)) for _ in range(m))
    return jsonify({"result": res})

@app.errorhandler(404)
def page_not_found(e):
    return "404 Not Found", 404

if __name__ == '__main__':
    app.run()
