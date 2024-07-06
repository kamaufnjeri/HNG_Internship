from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import UserUtils
from app.models import User

user_bp = Blueprint('user_bp', __name__, url_prefix='/api/users')
user_utils = UserUtils()

@user_bp.route('/<string:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    try:
        current_user_id = get_jwt_identity()

        user = User.query.filter_by(id=id).first()
        if not user:
            return jsonify({"status": "error", "message": "User not found"}), 404
        

        user_info = user_utils.check_users_share_same_organizations(current_user_id, id)

        if not user_info:
            return jsonify({"status": "error", "message": "Unauthorized access"}), 403


        response_data = {
            "status": "success",
            "message": "User record retrieved successfully",
            "data": user_info
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
