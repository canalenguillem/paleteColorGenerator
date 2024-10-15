from openai import OpenAI
import os
from flask import Flask,render_template,request
from dotenv import load_dotenv
import json

# Cargar las variables del archivo .env
load_dotenv()

# Obtener la clave de OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
# Verifica que la clave se ha cargado correctamente
if openai_api_key:
    print("La clave de OpenAI se ha cargado correctamente.")
else:
    print("Error al cargar la clave de OpenAI.")

client=OpenAI(api_key=openai_api_key)
MODEL='gpt-4-turbo'


def generate_colors(prompt):
    prompt_system = """
    Eres un asistente generador de paletas de colores que responde a indicaciones de texto para paletas de colores. 
    Debes generar paletas de colores que se ajusten al tema, estado de ánimo o instrucciones dadas en la indicación.
    Los colores deben estar ordenados en la paleta.
    Las paletas deben tener entre 2 y 8 colores.


    Formato deseado: un JSON Array con los códigos hexadecimales, solamente los codigos, nada más
    """

    #mejorado
    prompt_system="""
    Crea un arreglo JSON de códigos de colores hexadecimales que se alineen con el tema, estado de ánimo o instrucciones dadas. Los colores de la paleta deben estar ordenados según las indicaciones proporcionadas.

    # Pasos

    1. Analiza el prompt proporcionado para entender el tema, estado de ánimo o las instrucciones específicas.
    2. Selecciona colores que se alineen con el tema o estado de ánimo utilizando sus códigos hexadecimales.
    3. Asegúrate de que la paleta de colores se ajuste al rango especificado de 2 a 8 colores.

    # Formato de salida

    Devuelve solo un arreglo JSON que contenga los códigos de colores hexadecimales, por ejemplo, `["#FFFFFF", "#000000"]`.

    # Ejemplos

    **Ejemplo 1:**
    - **Entrada:** "Tema cálido y acogedor"
    - **Salida:** `["#FF5733", "#FFC300", "#DAF7A6"]`

    **Ejemplo 2:**
    - **Entrada:** "Paleta de noche estrellada"
    - **Salida:** `["#1a1a40", "#4a4a6a", "#f3e5ab"]`

    **Ejemplo 3:**
    - **Entrada:** "Colores de playa"
    - **Salida:** `["#00aaff", "#ffd700", "#ff7f50", "#fff485"]`

    # Notas

    - La selección de colores debe ser coherente con el contexto proporcionado.
    - Intenta lograr un equilibrio entre la diversidad de colores y la relevancia temática.
    - Evita añadir cualquier texto o metadatos; solo proporciona el arreglo de códigos de color.

    no uses ningu tipo de caracter en la salida da solo el json ya que lo tengo que usar en python y transformarlo con json.loads


    """
    

    messages=[
            {'role':'system','content':prompt_system},
            {'role':'user','content':prompt}
        ]

    response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=1,
            max_tokens=200,
            n=1
        )
    color_list = json.loads(response.choices[0].message.content)
    
    return color_list


app=Flask(__name__,
          template_folder='templates',
          static_url_path='',
          static_folder='static'  # folder for static files (css, js, images)
          )



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/paleta",methods=["POST"])
def prompt_to_palette():
    #open ai completion call
    prompt=request.form.get("prompt")
    print(f"PROMPT {prompt}")
    colors=generate_colors(prompt)
    print(f"colors {colors}")

    return {"colors":colors}



if __name__=="__main__":
    app.run(debug=True)
