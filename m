#!/bin/bash
# ------------------------------------------------------------
# InvoiceText local launcher (v1.0)
# (c) 2025 Carsten Hilbert - MIT License
# ------------------------------------------------------------
# This tiny wrapper runs the main Python script (make1.0.py)
# so you can call:
#     ./m i1
# or, after installation to ~/.local/bin:
#     m i1
# ------------------------------------------------------------

python3 "$(dirname "$0")/make1.0.py" "$@"
