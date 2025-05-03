from flask import Blueprint, request, jsonify, g
from app.predictions.schema import HeartDiseaseInput, PredictionResponse
from app.predictions.service import PredictionService

prediction_bp = Blueprint('predictions', __name__)

@prediction_bp.route('/heart-disease', methods=['POST'])
def predict_heart_disease():
    try:
        data = HeartDiseaseInput.parse_obj(request.json)
        service = PredictionService(g.db)
        prediction, error = service.predict_heart_disease(data)
        
        if error:
            return jsonify(error), 400
            
        # Create response from prediction entity
        response = PredictionResponse(
            id=prediction.id,
            user_id=prediction.user_id,
            age=prediction.age,
            sex=prediction.sex,
            cp=prediction.cp,
            trestbps=prediction.trestbps,
            chol=prediction.chol,
            fbs=prediction.fbs,
            restecg=prediction.restecg,
            thalach=prediction.thalach,
            exang=prediction.exang,
            oldpeak=prediction.oldpeak,
            slope=prediction.slope,
            probability=prediction.probability,
            prediction=prediction.prediction
        )
            
        return jsonify(response.dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@prediction_bp.route('/', methods=['GET'])
def list_predictions():
    service = PredictionService(g.db)
    predictions = service.get_all_predictions()
    result = []
    for p in predictions:
        response = PredictionResponse(
            id=p.id,
            user_id=p.user_id,
            age=p.age,
            sex=p.sex,
            cp=p.cp,
            trestbps=p.trestbps,
            chol=p.chol,
            fbs=p.fbs,
            restecg=p.restecg,
            thalach=p.thalach,
            exang=p.exang,
            oldpeak=p.oldpeak,
            slope=p.slope,
            probability=p.probability,
            prediction=p.prediction
        )
        result.append(response.dict())
    return jsonify(result), 200

@prediction_bp.route('/<int:prediction_id>', methods=['GET'])
def get_prediction(prediction_id):
    service = PredictionService(g.db)
    prediction = service.get_prediction(prediction_id)
    if not prediction:
        return jsonify({"error": "Prediction not found"}), 404
    
    response = PredictionResponse(
        id=prediction.id,
        user_id=prediction.user_id,
        age=prediction.age,
        sex=prediction.sex,
        cp=prediction.cp,
        trestbps=prediction.trestbps,
        chol=prediction.chol,
        fbs=prediction.fbs,
        restecg=prediction.restecg,
        thalach=prediction.thalach,
        exang=prediction.exang,
        oldpeak=prediction.oldpeak,
        slope=prediction.slope,
        probability=prediction.probability,
        prediction=prediction.prediction
    )
    return jsonify(response.dict()), 200

@prediction_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_predictions(user_id):
    service = PredictionService(g.db)
    predictions = service.get_user_predictions(user_id)
    result = []
    for p in predictions:
        response = PredictionResponse(
            id=p.id,
            user_id=p.user_id,
            probability=p.probability,
            prediction=p.prediction
        )
        result.append(response.dict())
    return jsonify(result), 200

@prediction_bp.route('/<int:prediction_id>', methods=['DELETE'])
def delete_prediction(prediction_id):
    service = PredictionService(g.db)
    if not service.delete_prediction(prediction_id):
        return jsonify({"error": "Prediction not found"}), 404
    return jsonify({"message": "Prediction deleted"}), 200