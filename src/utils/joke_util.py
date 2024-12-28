import requests

def tell_joke():
    """Obtiene un chiste de JokeAPI y lo envía al usuario."""
    joke_api_url = "https://v2.jokeapi.dev/joke/Any"
    try:
        response = requests.get(joke_api_url)
        if response.status_code == 200:
            joke_data = response.json()
            if joke_data["type"] == "single":
                # Chiste de una sola línea
                joke = joke_data["joke"]
            elif joke_data["type"] == "twopart":
                # Chiste de dos partes
                joke = f'{joke_data["setup"]}\n{joke_data["delivery"]}'
            else:
                joke = "No pude encontrar un buen chiste esta vez."
        else:
            joke = f"Error al obtener el chiste: {response.status_code}"
    except Exception as e:
        joke = f"Error al conectar con JokeAPI: {str(e)}"
    
    print(joke)