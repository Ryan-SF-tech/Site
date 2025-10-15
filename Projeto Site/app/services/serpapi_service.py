

#from flask import Blueprint, jsonify, request
#import requests

#serpapi_bp = Blueprint("serpapi", __name__)

#@serpapi_bp.route('/api/search-centers', methods=['GET'])
#def search_centers():
    
        
   # try:
        #lat = request.args.get('lat')
       # lng = request.args.get('lng')
        
        #if not lat or not lng:
            #return jsonify({"error": "Coordenadas faltando"}), 400
        
       # params = {
        #  "engine": "google_maps",
        #  "q": "centro de adoção de animais", 
        #  "ll": f"@{lat},{lng},15z",
        #  "type": "search",
        #  "hl": "pt-BR",  
        #  "gl": "br",      
       #   "api_key": "04fa7ea9827380a90f7412fe2d4ebb09f8820c096cc3d1a2ece1c935bcff80fb"
       # }
        
       # response = requests.get('https://serpapi.com/search.json', params=params)
       # response.raise_for_status()
        
       # data = response.json()
        #return jsonify(data.get('local_results', []))
        
    #except Exception as e:
        #print(f"Erro na API: {str(e)}")
        #return jsonify({"error": "Erro ao buscar centros de adoção"}), 500
           