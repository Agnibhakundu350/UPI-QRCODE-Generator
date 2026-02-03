"""
Simple UPI helper
- Generates a UPI payment URI
- Produces a QR code (PNG) for the UPI URI using the `qrcode` package
- Prints official links for Google Pay, Paytm and PhonePe
"""

import qrcode
import webbrowser
from urllib.parse import quote_plus
import argparse
import os


def build_upi_uri(pa: str, pn: str | None = None, am: str | None = None, tn: str | None = None, cu: str = "INR") -> str:
    """Build a standard UPI payment URI. Only includes provided params."""
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


def save_qr(data: str, filename: str) -> None:
    """Create and save a QR code image for the given data."""
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="pink", back_color="white")
    img.save(filename)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate UPI payment URI and QR code")
    parser.add_argument("--pa", help="UPI ID (pa)")
    parser.add_argument("--pn", help="Payee name (pn)")
    parser.add_argument("--am", help="Amount (am)")
    parser.add_argument("--tn", help="Transaction note (tn)")
    parser.add_argument("--open", action="store_true", help="Open the generated QR image after creating")
    args = parser.parse_args()

    if args.pa:
        pa = args.pa
        pn = args.pn
        am = args.am
        tn = args.tn
    else:
        pa = input("Enter UPI ID (pa): ").strip()
        if not pa:
            print("UPI ID is required. Exiting.")
            return
        pn = input("Payee name (optional): ").strip() or None
        am = input("Amount (optional): ").strip() or None
        tn = input("Transaction note (optional): ").strip() or None

    uri = build_upi_uri(pa, pn, am, tn)
    print("\nGenerated UPI URI:")
    print(uri)

    filename = f"{pa.replace('@', '_')}_upi_qr.png"
    save_qr(uri, filename)
    print(f"Saved QR code to {filename}")

    # Try to open the UPI URI (if the system has a handler, it will open the app)
    try:
        open_uri = input("Open UPI URI now (this may open a UPI app on your device)? [y/N]: ").strip().lower()
        if open_uri == "y":
            webbrowser.open(uri)
    except Exception:
        pass

    if args.open:
        try:
            webbrowser.open(filename)
        except Exception as e:
            print("Could not open image:", e)

    print("\nOfficial app/web links:")
    print("- Google Pay: https://pay.google.com")
    print("- Paytm: https://paytm.com")
    print("- PhonePe: https://www.phonepe.com")

    print("\nNotes: ")
    print("- The generated UPI URI uses the standard 'upi://pay' scheme and should be accepted by most UPI apps.")
    print("- You can scan the saved QR code with any UPI app to pay.")


if __name__ == "__main__":
    main()
