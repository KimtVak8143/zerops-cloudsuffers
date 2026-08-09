"""Run wrapper for development.

Allows starting the FastAPI app with a short command:

    python run.py

This uses PORT if provided, otherwise falls back to 8000.
"""
import os
import uvicorn


def main() -> None:
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)


if __name__ == "__main__":
    main()
