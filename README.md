## Automated setup
Open in vscode

## Manual setup

```sh
# Setup
pip3 install -r requirements.txt

# Run
python3 -m flask run --host 0.0.0.0 --port 9000 --no-debugger --no-reload

# Usage (open in browser or use curl)
curl -F 'file=@image.png' http://localhost:9000
```