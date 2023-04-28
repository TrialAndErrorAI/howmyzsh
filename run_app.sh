#!/bin/sh

source ./.venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.port=8080
