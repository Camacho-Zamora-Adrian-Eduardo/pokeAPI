from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests

API="https://pokeapi.co/api/v2/pokemon"
app = Flask(__name__)
app.secret_key = "20cosas_que_no_sabias_de_las_empanadas"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['post'])
def search_pokemon():
    pokemon_name = request.form.get('pokemon_name','').strip().lower()
    
    if not pokemon_name:
        flash('Por favor, ingrese un nombre de pokemon','error')
        return redirect(url_for('index'))
    
    try:
        resp = requests.get(f"{API}{pokemon_name}")
        if resp.status_code == 200:
            pokemon_data = resp.json()
    
            pokemon_info = {
                'name': pokemon_data['name'].title(),
                'id': pokemon_data['id'],
                'height':pokemon_data['height']/10,
                'weight': pokemon_data['weight']/10,
                'image': pokemon_data['sprites']['front_defaul'],
                'types': [t['type']['name'].title() for t in pokemon_data['types']],
                'abilities': [a['ability']['name'].title() for a in pokemon_data['abilities']]
                }
            return render_template('pokemon2.html' , pokemon=pokemon_info)
        else:   
            flash(f'Pokemon "{pokemon_name} "no encontrado', 'error')
            return redirect(url_for('index'))
    except requests.exceptions.requestsException as e:
        flash('Error al buscar el pokemon','error')
        return redirect(url_for('index'))
    


if __name__ == '__main__':
    app.run(debug=True)