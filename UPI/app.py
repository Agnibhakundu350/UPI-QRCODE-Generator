from flask import Flask, render_template, request
import qrcode
import io
import base64
from urllib.parse import quote_plus

app = Flask(__name__)


def build_upi_uri(pa: str, pn: str | None = None, am: str | None = None, tn: str | None = None, cu: str = "INR") -> str:
    params = []
    params.append(("pa", pa))
    if pn:
        params.append(("pn", pn))
    if am:
        params.append(("am", am))
    if tn:
        params.append(("tn", tn))
    if cu:
        params.append(("cu", cu))
    query = "&".join(f"{k}={quote_plus(v)}" for k, v in params)
    return f"upi://pay?{query}"


def qr_image_base64(data: str) -> str:
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode("utf-8")
    return img_b64


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    pa = request.form.get("pa", "").strip()
    if not pa:
        return render_template("index.html", error="UPI ID (pa) is required")
    pn = request.form.get("pn") or None
    am = request.form.get("am") or None
    tn = request.form.get("tn") or None

    uri = build_upi_uri(pa, pn, am, tn)
    qr_b64 = qr_image_base64(uri)

    return render_template("result.html", uri=uri, qr_b64=qr_b64, pa=pa)


if __name__ == "__main__":
    app.run(debug=True)
