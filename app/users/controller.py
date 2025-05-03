from flask import Blueprint, request, jsonify, g
from app.users.service import UserService
from app.users.schema import UserCreateSchema, UserOutSchema, UserUpdateSchema

user_bp = Blueprint("user", __name__, url_prefix="/users")

@user_bp.route("/", methods=["POST"])
def create_user():
    try:
        data = UserCreateSchema.parse_obj(request.json)
        service = UserService(g.db)
        user, error = service.create_user(data)
        
        if error:
            return jsonify(error), 400
            
        return jsonify(UserOutSchema.from_orm(user).dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@user_bp.route("/", methods=["GET"])
def list_users():
    service = UserService(g.db)
    users = service.list_users()
    return jsonify([UserOutSchema.from_orm(u).dict() for u in users]), 200

@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    service = UserService(g.db)
    user = service.get_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(UserOutSchema.from_orm(user).dict()), 200

@user_bp.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    try:
        data = UserUpdateSchema.parse_obj(request.json)
        service = UserService(g.db)
        user, error = service.update_user(user_id, data)
        
        if error:
            return jsonify(error), 400
            
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        return jsonify(UserOutSchema.from_orm(user).dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    service = UserService(g.db)
    if not service.delete_user(user_id):
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted"}), 200