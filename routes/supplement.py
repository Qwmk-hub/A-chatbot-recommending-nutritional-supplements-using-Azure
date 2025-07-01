from flask import Blueprint, jsonify, request
from src.models.supplement import Supplement, db

supplement_bp = Blueprint('supplement', __name__)

@supplement_bp.route('/trending', methods=['GET'])
def get_trending_supplements():
    """요즘 떠오르는 영양제 추천"""
    try:
        supplements = Supplement.query.filter_by(is_trending=True).all()
        return jsonify([supplement.to_dict() for supplement in supplements]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@supplement_bp.route('/by-demographics', methods=['GET'])
def get_supplements_by_demographics():
    """성별/나이대별 영양제 추천"""
    try:
        gender = request.args.get('gender')  # 'male' or 'female'
        age_group = request.args.get('age_group')  # '20s', '30s', '40s', '50s+'
        
        query = Supplement.query
        
        if gender:
            query = query.filter_by(category=gender)
        
        if age_group:
            query = query.filter_by(age_group=age_group)
        
        supplements = query.all()
        return jsonify([supplement.to_dict() for supplement in supplements]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@supplement_bp.route('/search', methods=['GET'])
def search_supplements():
    """영양제 검색"""
    try:
        keyword = request.args.get('keyword', '')
        
        if not keyword:
            return jsonify([]), 200
        
        supplements = Supplement.query.filter(
            Supplement.name.contains(keyword) | 
            Supplement.description.contains(keyword)
        ).all()
        
        return jsonify([supplement.to_dict() for supplement in supplements]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@supplement_bp.route('/recommendations', methods=['GET'])
def get_personalized_recommendations():
    """개인화된 영양제 추천 (로그인 사용자 기준)"""
    try:
        from flask import session
        from src.models.user import User
        import json
        
        if 'user_id' not in session:
            return jsonify({'error': 'Login required'}), 401
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # 사용자의 성별과 나이대에 맞는 영양제 추천
        age_group = f"{user.age // 10 * 10}s"  # 20s, 30s, 40s, 50s+
        if user.age >= 50:
            age_group = "50s+"
        
        supplements = Supplement.query.filter(
            (Supplement.category == user.gender) | 
            (Supplement.age_group == age_group) |
            (Supplement.is_trending == True)
        ).limit(10).all()
        
        return jsonify([supplement.to_dict() for supplement in supplements]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@supplement_bp.route('/add', methods=['POST'])
def add_supplement():
    """영양제 추가 (관리자용)"""
    try:
        data = request.json
        
        supplement = Supplement(
            name=data['name'],
            description=data.get('description'),
            category=data['category'],
            age_group=data.get('age_group'),
            benefits=data.get('benefits'),
            price_range=data.get('price_range'),
            brand=data.get('brand'),
            image_url=data.get('image_url'),
            is_trending=data.get('is_trending', False)
        )
        
        db.session.add(supplement)
        db.session.commit()
        
        return jsonify({
            'message': 'Supplement added successfully',
            'supplement': supplement.to_dict()
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

