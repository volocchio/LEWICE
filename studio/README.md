# LEWICE Studio

Modern UI for NASA LEWICE aircraft icing simulation. No PhD in ice required.

## What It Does

- **Airfoil Selection** — pick from NACA library or upload custom .xyd
- **Flight Condition Builder** — enter speed/altitude/temp in engineering units
- **FAA Envelope Automation** — pre-loaded Appendix C and O condition matrices
- **Batch Runner** — run full certification envelope in one click
- **Ice Shape Visualization** — interactive Plotly overlay of ice on clean airfoil
- **Risk Assessment** — auto green/yellow/red based on ice type and severity
- **Report Generator** — auto-generate PowerPoint or PDF certification reports

## Quick Start

```
cd studio
pip install -r requirements.txt
streamlit run app.py
```

## Architecture

```
studio/
  app.py                    # Streamlit main app
  lewice_engine/
    input_builder.py        # Generate LEWICE input files
    runner.py               # Execute LEWICE, manage batch runs
    output_parser.py        # Parse LEWICE results
  envelopes/
    appendix_c.json         # FAA Appendix C conditions
  airfoils/
    naca_library.py         # NACA 4-digit generator
  reports/
    (PowerPoint template and generator — coming soon)
```

## Requirements

- Python 3.9+
- LEWICE 3.2 executable (lewice.exe in repo root)
- Streamlit, Plotly, python-pptx
