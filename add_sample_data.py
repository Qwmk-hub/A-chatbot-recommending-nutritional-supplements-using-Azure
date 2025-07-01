#!/usr/bin/env python3
"""
영양제 샘플 데이터 추가 스크립트
"""
import os
import sys
import json

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db
from src.models.supplement import Supplement
from src.main import app

def add_sample_supplements():
    """샘플 영양제 데이터 추가"""
    
    sample_supplements = [
        # 트렌딩 영양제
        {
            "name": "비타민 D3",
            "description": "면역력 강화와 뼈 건강에 도움을 주는 필수 비타민입니다.",
            "category": "trending",
            "age_group": None,
            "benefits": json.dumps(["면역력 강화", "뼈 건강", "칼슘 흡수 촉진"]),
            "price_range": "10,000-20,000원",
            "brand": "종근당",
            "is_trending": True
        },
        {
            "name": "오메가-3",
            "description": "심혈관 건강과 뇌 기능 개선에 도움을 주는 필수 지방산입니다.",
            "category": "trending",
            "age_group": None,
            "benefits": json.dumps(["심혈관 건강", "뇌 기능 개선", "염증 완화"]),
            "price_range": "15,000-30,000원",
            "brand": "솔가",
            "is_trending": True
        },
        {
            "name": "멀티비타민",
            "description": "일일 필요 비타민과 미네랄을 한 번에 섭취할 수 있는 종합 영양제입니다.",
            "category": "trending",
            "age_group": None,
            "benefits": json.dumps(["종합 영양 보충", "피로 회복", "신진대사 촉진"]),
            "price_range": "20,000-40,000원",
            "brand": "센트룸",
            "is_trending": True
        },
        
        # 남성용 영양제
        {
            "name": "아연",
            "description": "남성 건강과 면역력 강화에 도움을 주는 필수 미네랄입니다.",
            "category": "male",
            "age_group": "20s",
            "benefits": json.dumps(["남성 건강", "면역력 강화", "상처 치유"]),
            "price_range": "8,000-15,000원",
            "brand": "나우푸드",
            "is_trending": False
        },
        {
            "name": "마그네슘",
            "description": "근육 기능과 에너지 대사에 도움을 주는 필수 미네랄입니다.",
            "category": "male",
            "age_group": "30s",
            "benefits": json.dumps(["근육 기능", "에너지 대사", "스트레스 완화"]),
            "price_range": "12,000-25,000원",
            "brand": "라이프익스텐션",
            "is_trending": False
        },
        {
            "name": "코엔자임 Q10",
            "description": "심장 건강과 에너지 생성에 도움을 주는 항산화 성분입니다.",
            "category": "male",
            "age_group": "40s",
            "benefits": json.dumps(["심장 건강", "에너지 생성", "항산화 작용"]),
            "price_range": "25,000-50,000원",
            "brand": "닥터스베스트",
            "is_trending": False
        },
        
        # 여성용 영양제
        {
            "name": "철분",
            "description": "여성의 빈혈 예방과 에너지 생성에 도움을 주는 필수 미네랄입니다.",
            "category": "female",
            "age_group": "20s",
            "benefits": json.dumps(["빈혈 예방", "에너지 생성", "산소 운반"]),
            "price_range": "10,000-20,000원",
            "brand": "페로그라드C",
            "is_trending": False
        },
        {
            "name": "엽산",
            "description": "임신 준비 여성과 태아 건강에 필수적인 비타민 B군입니다.",
            "category": "female",
            "age_group": "30s",
            "benefits": json.dumps(["태아 건강", "세포 분열", "혈액 생성"]),
            "price_range": "8,000-15,000원",
            "brand": "일동제약",
            "is_trending": False
        },
        {
            "name": "칼슘 + 비타민 D",
            "description": "여성의 골다공증 예방과 뼈 건강에 도움을 주는 복합 영양제입니다.",
            "category": "female",
            "age_group": "40s",
            "benefits": json.dumps(["뼈 건강", "골다공증 예방", "칼슘 흡수"]),
            "price_range": "15,000-30,000원",
            "brand": "칼트레이트",
            "is_trending": False
        },
        {
            "name": "콜라겐",
            "description": "피부 탄력과 관절 건강에 도움을 주는 단백질 보충제입니다.",
            "category": "female",
            "age_group": "50s+",
            "benefits": json.dumps(["피부 탄력", "관절 건강", "노화 방지"]),
            "price_range": "20,000-40,000원",
            "brand": "바이탈뷰티",
            "is_trending": False
        },
        
        # 추가 트렌딩 영양제
        {
            "name": "프로바이오틱스",
            "description": "장 건강과 면역력 강화에 도움을 주는 유익균 보충제입니다.",
            "category": "trending",
            "age_group": None,
            "benefits": json.dumps(["장 건강", "면역력 강화", "소화 개선"]),
            "price_range": "20,000-35,000원",
            "brand": "컬처렐",
            "is_trending": True
        },
        {
            "name": "루테인",
            "description": "눈 건강과 시력 보호에 도움을 주는 카로티노이드 성분입니다.",
            "category": "trending",
            "age_group": None,
            "benefits": json.dumps(["눈 건강", "시력 보호", "황반 건강"]),
            "price_range": "15,000-25,000원",
            "brand": "아이케어",
            "is_trending": True
        }
    ]
    
    with app.app_context():
        # 기존 데이터 삭제 (개발 환경에서만)
        Supplement.query.delete()
        
        # 새 데이터 추가
        for supplement_data in sample_supplements:
            supplement = Supplement(**supplement_data)
            db.session.add(supplement)
        
        db.session.commit()
        print(f"Successfully added {len(sample_supplements)} supplements to the database!")

if __name__ == "__main__":
    add_sample_supplements()

