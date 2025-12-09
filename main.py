"""
Stock Analyzer Application
Entry point for running the Streamlit stock analyzer app.
"""

import subprocess
import sys


def main():
    """Run the Streamlit stock analyzer application."""
    try:
        # Run the Streamlit app with explicit configuration
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port=8501",
            "--server.address=localhost",
            "--server.headless=false"
        ], check=True)
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
    except subprocess.CalledProcessError as e:
        print(f"Error running the application: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: Streamlit is not installed. Please install dependencies:")
        print("  pip install -r requirements.txt")
        print("  or")
        print("  pip install streamlit yfinance pandas")
        sys.exit(1)


if __name__ == "__main__":
    main()
