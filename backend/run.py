"""Run wrapper for development.

Allows starting the FastAPI app with a short command:

    python run.py

This runs the same uvicorn invocation used in the README.
"""
import uvicorn


def main() -> None:
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
