from flask import Flask, render_template, redirect, Response, request
import subprocess
import threading
import queue
import time
import os

app = Flask(__name__)

SUPPORTED_LANGS = {
  "en": "English",
  "pt": "Português",
  "ja": "日本語"
}

def is_lang_valid(lang):
  return lang in SUPPORTED_LANGS.keys()

def return_correct_page(lang, page_name):
  if is_lang_valid(lang):
    return render_template(
      f'{page_name}.html',
      lang=lang,
      langs=SUPPORTED_LANGS
      )
  else:
    return redirect(f'/en/{page_name}')

output_queue = queue.Queue()


def run_sensor_script():
  try:
    process = subprocess.Popen(
      ["python", "-u", "script.py"],
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      universal_newlines=True,
      bufsize=1
    )

    if process.stdout is None:
      output_queue.put("Error: stdout is None")
      return

    for line in iter(process.stdout.readline, " "):
      if line:
        clean_line = line.strip()

        output_queue.put(clean_line)

    process.stdout.close()
    process.wait()

  except FileNotFoundError:
    output_queue.put("Error: 'script.py' not found")
  except Exception as e:
    output_queue.put(f"Error: {str(e)}")

def generate_sensor_data():
  while True:
    try:
      data = output_queue.get(timeout=2)
      yield f"data: {data}\n"
    except queue.Empty:
      yield "data: \n"
    except Exception as e:
      yield f"data: Erro na transmissão: {str(e)}\n"

##### INDEX/MAIN PAGE #####
@app.route('/')
@app.route('/<lang>/')
def index(lang="en"):
  return return_correct_page(lang, "index")

##### NEUTRINOS AND NOvA PAGE #####
@app.route('/<lang>/science')
@app.route('/<lang>/ciencia')
@app.route('/<lang>/kagaku')
def science(lang="en"):
  return return_correct_page(lang, "science")

##### ABOUT PAGE #####
@app.route('/<lang>/about')
@app.route('/<lang>/sobre')
@app.route('/<lang>/nitsuite')
def about(lang="en"):
  return return_correct_page(lang, "about")

@app.route('/sensor-stream')
def sensor_stream():
    return Response(
        generate_sensor_data(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*'
        }
    )

sensor_thread = threading.Thread(target=run_sensor_script, daemon=True)
sensor_thread.start()
