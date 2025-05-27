from flask import request, jsonify
from app.database import get_db
from datetime import datetime
import requests


def init_routes(app):
    
    # Busca player
    @app.route("/player", methods=["GET"])
    def get_player():
        print('funçao')
        conn = get_db()
        '''
        # # Remove todos os player com senha igual a 0
        conn.execute("DELETE FROM player WHERE senha = 0")
        conn.commit()
        '''
        
        # Busca todos os player restantes
        player = conn.execute("SELECT * FROM player").fetchall()
        return jsonify([dict(row) for row in player])

    # Cria/Registra o material
    @app.route("/player_create", methods=["POST"])
    def create_material():
        data = request.get_json()
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not data:
            return jsonify({"error": "Nenhum dado enviado"}), 400

        # Verifica se todos os campos necessários estão presentes
        required_fields = ["nome", "email", "senha"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo obrigatório ausente: {field}"}), 400

        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO player (nome, email, senha, time_play) VALUES (?, ?, ?, ?)",
                (data["nome"], data["email"], data["senha"], now_str)
            )
            conn.commit()
            return jsonify({"message": "Player inserido com sucesso!"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400


    # Deleta o material
    @app.route("/player/<nome>", methods=["DELETE"])
    def delete_material(nome):
        conn = get_db()
        cursor = conn.execute("DELETE FROM player WHERE nome = ?", (nome,))
        conn.commit()
        
        # Verifica se alguma linha foi afetada
        if cursor.rowcount == 0:
            return jsonify({"error": "Material não encontrado"}), 404
        
        return jsonify({"message": "Material deletado com sucesso!"}), 200
    
    # Atualiza o material
    @app.route("/player/<nome>", methods=["PUT"])
    def update_material(nome):
        
        print('funçao')
        data = request.get_json()
        conn = get_db()
        now_str_for_put = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Verifica se existe
        cursor = conn.execute(
            "SELECT 1 FROM player WHERE nome = ?",
            (nome,)
        )
        if cursor.fetchone() is None:
            return jsonify({"error": "Material não encontrado"}), 404

        # Atualiza somente a linha cujo nome bate
        conn.execute(
            """
            UPDATE player
            SET email     = ?,
                senha          = ?,
                time_play            = ?
            WHERE nome        = ?
            """,
            (
                data["email"],
                data["senha"],
                now_str_for_put,
                nome
            )
        )
        conn.commit()

        return jsonify({"message": "Material atualizado com sucesso!"}), 200

    # Busca o material específico
    @app.route("/player/<nome>", methods=["GET"])
    def searchGet(nome):
        conn = get_db()
        
        cursor = conn.execute("SELECT * FROM player WHERE nome = ?", (nome,))
        material = cursor.fetchone()
        
        if not material:
            return jsonify({"error": "Material não encontrado"}), 404
        '''
        # mock de cursor.data e visualização dos dados
        for row in material:
            print(row)

        print(dict(material))
        
        
        data = {'nome': 1001,
                 'nome': 11146098, 
                 'email': '02-13-05', 
                 'senha': 10, 
                 'description_material': 'Z', 
                 'last_mod': '2025-05-16 08:17:00'}
        
        print(material["senha"])
        '''
        
        if material["senha"] == 0:
            conn.execute("DELETE FROM player WHERE senha = 0")
            conn.commit()

            return jsonify({"error": "Material indisponível no Estoque"}), 404
        
        return jsonify([dict(material)])
