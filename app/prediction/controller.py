from flask import Blueprint, request, jsonify, g
from app.prediction.schema import HeartDiseaseInput, PredictionResponse
from app.prediction.service import PredictionService

prediction_bp = Blueprint('prediction', __name__)

@prediction_bp.route('/heart-disease', methods=['POST'])
def predict_heart_disease():
    try:
        data = HeartDiseaseInput.parse_obj(request.json)
        service = PredictionService(g.db)
        result, error = service.predict_heart_disease(data)
        
        if error:
            return jsonify(error), 400
            
        return jsonify(PredictionResponse.from_orm(result).dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@prediction_bp.route('/', methods=['GET'])
def list_predictions():
    service = PredictionService(g.db)
    predictions = service.get_all_predictions()
    return jsonify([PredictionResponse.from_orm(p).dict() for p in predictions]), 200

@prediction_bp.route('/<int:prediction_id>', methods=['GET'])
def get_prediction(prediction_id):
    service = PredictionService(g.db)
    prediction = service.get_prediction(prediction_id)
    if not prediction:
        return jsonify({"error": "Prediction not found"}), 404
    return jsonify(PredictionResponse.from_orm(prediction).dict()), 200

@prediction_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_predictions(user_id):
    service = PredictionService(g.db)
    predictions = service.get_user_predictions(user_id)
    return jsonify([PredictionResponse.from_orm(p).dict() for p in predictions]), 200

@prediction_bp.route('/<int:prediction_id>', methods=['DELETE'])
def delete_prediction(prediction_id):
    service = PredictionService(g.db)
    if not service.delete_prediction(prediction_id):
        return jsonify({"error": "Prediction not found"}), 404
    return jsonify({"message": "Prediction deleted"}), 200