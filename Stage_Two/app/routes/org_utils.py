from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import UserUtils, OrganizationUtils
from app.models import User, Organization
from app import db

org_bp = Blueprint('org_bp', __name__, url_prefix='/api/organizations')
user_utils = UserUtils()
org_utils = OrganizationUtils()

@org_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_organizations():
    try:
        current_user_id = get_jwt_identity()
        
        current_user = User.query.filter_by(id=current_user_id).first()

        user_orgs = user_utils.get_user_organizations(current_user)

        if not user_orgs:
            return jsonify({"status": "error", "message": "Unauthorized access"}), 403

        return jsonify({
            "status": "success",
		    "message": "User organizations retrieved successfully",
            "data": {
                "organisations": user_orgs
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)})


@org_bp.route('/<string:orgId>', methods=['GET'])
@jwt_required()
def get_organization(orgId):
    try:
        current_user_id = get_jwt_identity()
        
        current_user = User.query.filter_by(id=current_user_id).first()

        user_orgs = user_utils.get_user_organizations(current_user)

        if not user_orgs:
            return jsonify({"status": "error", "message": "Unauthorized access"}), 403
        
        for org in user_orgs:
            if org.get('orgId') == orgId:
                return jsonify({
                    "status": "success",
                    "message": "Organization retrieved successfully",
                    "data": org
                }), 200
            
        return jsonify({
                    "status": "error",
                    "message": "Organization not found",
                }), 404

    except Exception as e:
        return jsonify({"error": str(e)})



@org_bp.route('/', methods=['POST'])
@jwt_required()
def create_organization():
    try:
        current_user_id = get_jwt_identity()

        data = request.get_json()

        if not data.get('name'):
            return jsonify({
                "status": "Bad Request",
                "message": "Client error",
                "statusCode": 422,
                "errors": {"message": "name is required", "field": "name"}
            }), 422
        
        current_user = User.query.filter_by(id=current_user_id).first()

        new_organization = org_utils.create_organization(data)

        db.session.add(new_organization)
        current_user.organizations.append(new_organization)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Organisation created successfully",
            "data": new_organization.to_dict()
        }), 201


    except Exception as e:
        return jsonify({
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400
        }), 400


@org_bp.route('/<string:orgId>/users', methods=['POST'])
@jwt_required()
def add_user_to_organization(orgId):
    try:
        current_user_id = get_jwt_identity()

        data = request.get_json()
        current_user = User.query.filter_by(id=current_user_id).first()

        user_to_add = User.query.filter_by(id=data.get('userId')).first()

        if not user_to_add:
            return jsonify({"status": "error", "message": "User not found"}), 404

        user_organizations = user_utils.get_user_organizations(user=current_user)

        for organization in user_organizations:
            if organization.get('orgId') == orgId:
                org = Organization.query.filter_by(id=orgId).first()

                org.users.append(user_to_add)
                return jsonify({
                    "status": "success",
                    "message": "User added to organisation successfully",
                }), 200
            
        return jsonify({ 
            "status": "error",
            "message": "Organization not found",
        }), 404
                        

    except Exception as e:
        return jsonify({
             "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400,
            "errors": [str(e)]

        }), 400
    
