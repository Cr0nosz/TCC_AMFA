#!/usr/bin/env python3
"""
Script para iniciar o servidor Flask
"""
from app import app

if __name__ == '__main__':
    print('=' * 50)
    print('AMFA - Cyber Security Platform')
    print('Backend Python/Flask')
    print('=' * 50)
    print('\nServidor iniciando em http://localhost:5000')
    print('Pressione CTRL+C para parar\n')
    
    app.run(host='0.0.0.0', port=5000, debug=True)
