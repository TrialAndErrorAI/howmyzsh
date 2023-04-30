#!/bin/sh
set -e

# # create virtual environment if not exists
# if [ ! -d ".venv" ]; then
#     echo "Creating virtual environment..."
#     python3 -m venv .venv
# fi
# . ./.venv/bin/activate

pip install --no-cache-dir -r requirements.txt
export GIT_PYTHON_GIT_EXECUTABLE=/usr/bin/git
streamlit run app.py --server.port=8080
