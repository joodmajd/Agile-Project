"""Development entry point for the Practice Quiz Bank."""

from app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4173, debug=False)
