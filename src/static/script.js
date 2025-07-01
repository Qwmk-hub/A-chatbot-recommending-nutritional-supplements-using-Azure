// 전역 변수
let currentUser = null;

// DOM 로드 완료 시 실행
document.addEventListener('DOMContentLoaded', function () {
    initializeApp();
});

// 앱 초기화
function initializeApp() {
    setupEventListeners();
    checkAuthStatus();
    loadTrendingSupplements();
}

// 이벤트 리스너 설정
function setupEventListeners() {
    // 네비게이션 링크
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const targetSection = this.getAttribute('href').substring(1);
            showSection(targetSection);
        });
    });

    // 모달 관련
    document.getElementById('loginBtn').addEventListener('click', () => showModal('loginModal'));
    document.getElementById('registerBtn').addEventListener('click', () => showModal('registerModal'));
    document.getElementById('logoutBtn').addEventListener('click', logout);

    // 모달 닫기
    document.querySelectorAll('.close').forEach(closeBtn => {
        closeBtn.addEventListener('click', function () {
            this.closest('.modal').style.display = 'none';
        });
    });

    // 모달 외부 클릭 시 닫기
    window.addEventListener('click', function (e) {
        if (e.target.classList.contains('modal')) {
            e.target.style.display = 'none';
        }
    });

    // 폼 제출
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    document.getElementById('registerForm').addEventListener('submit', handleRegister);

    // 필터 검색
    document.getElementById('filterBtn').addEventListener('click', filterSupplements);

    // 챗봇
    document.getElementById('sendBtn').addEventListener('click', sendChatMessage);
    document.getElementById('chatInput').addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendChatMessage();
        }
    });
}

// 섹션 표시
function showSection(sectionId) {
    // 모든 섹션 숨기기
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });

    // 선택된 섹션 표시
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
    }

    // 네비게이션 활성화 상태 업데이트
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${sectionId}`) {
            link.classList.add('active');
        }
    });
}

// 모달 표시
function showModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

// 로그인 상태 확인
async function checkAuthStatus() {
    try {
        const response = await fetch('/api/check-auth');
        const data = await response.json();

        if (data.authenticated) {
            currentUser = data.user;
            updateUIForLoggedInUser();
        } else {
            updateUIForLoggedOutUser();
        }
    } catch (error) {
        console.error('Auth check failed:', error);
        updateUIForLoggedOutUser();
    }
}

// 로그인된 사용자 UI 업데이트
function updateUIForLoggedInUser() {
    document.getElementById('loginBtn').style.display = 'none';
    document.getElementById('registerBtn').style.display = 'none';
    document.getElementById('userInfo').style.display = 'flex';
    document.getElementById('userEmail').textContent = currentUser.email;
}

// 로그아웃된 사용자 UI 업데이트
function updateUIForLoggedOutUser() {
    document.getElementById('loginBtn').style.display = 'inline-block';
    document.getElementById('registerBtn').style.display = 'inline-block';
    document.getElementById('userInfo').style.display = 'none';
    currentUser = null;
}

// 로그인 처리
async function handleLogin(e) {
    e.preventDefault();

    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            currentUser = data.user;
            updateUIForLoggedInUser();
            document.getElementById('loginModal').style.display = 'none';
            document.getElementById('loginForm').reset();
            showNotification('로그인 성공!', 'success');
        } else {
            showNotification(data.error || '로그인 실패', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showNotification('로그인 중 오류가 발생했습니다.', 'error');
    }
}

// 회원가입 처리
async function handleRegister(e) {
    e.preventDefault();

    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const gender = document.getElementById('registerGender').value;
    const age = document.getElementById('registerAge').value;
    const supplements = document.getElementById('registerSupplements').value;

    const interested_supplements = supplements ? supplements.split(',').map(s => s.trim()) : [];

    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email,
                password,
                gender,
                age: parseInt(age),
                interested_supplements
            })
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('registerModal').style.display = 'none';
            document.getElementById('registerForm').reset();
            showNotification('회원가입 성공! 로그인해주세요.', 'success');
        } else {
            showNotification(data.error || '회원가입 실패', 'error');
        }
    } catch (error) {
        console.error('Register error:', error);
        showNotification('회원가입 중 오류가 발생했습니다.', 'error');
    }
}

// 로그아웃
async function logout() {
    try {
        const response = await fetch('/api/logout', {
            method: 'POST'
        });

        if (response.ok) {
            updateUIForLoggedOutUser();
            showNotification('로그아웃되었습니다.', 'success');
            showSection('home');
        }
    } catch (error) {
        console.error('Logout error:', error);
        showNotification('로그아웃 중 오류가 발생했습니다.', 'error');
    }
}

// 트렌딩 영양제 로드
async function loadTrendingSupplements() {
    try {
        const response = await fetch('/api/supplements/trending');
        const supplements = await response.json();

        const container = document.getElementById('trendingSupplements');
        container.innerHTML = '';

        if (supplements.length === 0) {
            container.innerHTML = '<p>현재 등록된 트렌딩 영양제가 없습니다.</p>';
            return;
        }

        supplements.forEach(supplement => {
            const card = createSupplementCard(supplement);
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Failed to load trending supplements:', error);
        document.getElementById('trendingSupplements').innerHTML = '<p>영양제 정보를 불러오는데 실패했습니다.</p>';
    }
}

// 영양제 필터링
async function filterSupplements() {
    const gender = document.getElementById('genderFilter').value;
    const ageGroup = document.getElementById('ageFilter').value;

    try {
        const params = new URLSearchParams();
        if (gender) params.append('gender', gender);
        if (ageGroup) params.append('age_group', ageGroup);

        const response = await fetch(`/api/supplements/by-demographics?${params}`);
        const supplements = await response.json();

        const container = document.getElementById('demographicSupplements');
        container.innerHTML = '';

        if (supplements.length === 0) {
            container.innerHTML = '<p>해당 조건에 맞는 영양제가 없습니다.</p>';
            return;
        }

        supplements.forEach(supplement => {
            const card = createSupplementCard(supplement);
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Failed to filter supplements:', error);
        document.getElementById('demographicSupplements').innerHTML = '<p>영양제 정보를 불러오는데 실패했습니다.</p>';
    }
}

// 영양제 카드 생성
function createSupplementCard(supplement) {
    const card = document.createElement('div');
    card.className = 'supplement-card';

    card.innerHTML = `
        <h3>${supplement.name}</h3>
        <p>${supplement.description || '설명이 없습니다.'}</p>
        <div class="supplement-meta">
            <span>카테고리: ${supplement.category}</span>
            <span>나이대: ${supplement.age_group || '전체'}</span>
        </div>
        ${supplement.price_range ? `<div class="supplement-meta"><span>가격대: ${supplement.price_range}</span></div>` : ''}
        ${supplement.brand ? `<div class="supplement-meta"><span>브랜드: ${supplement.brand}</span></div>` : ''}
    `;

    return card;
}

// 챗봇 메시지 전송
async function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();

    if (!message) return;

    // 사용자 메시지 추가
    addChatMessage(message, 'user');
    input.value = '';

    // GPT 연동: Flask 서버에 POST 요청
    try {
        const response = await fetch('/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                height: currentUser?.height || 170, // 기본값 지정
                weight: currentUser?.weight || 60,
                age: currentUser?.age || 30,
                gender: currentUser?.gender || '남성',
                message: message
            })
        });

        const data = await response.json();

        if (response.ok) {
            addChatMessage(data.response, 'bot');
        } else {
            addChatMessage('챗봇 응답 중 오류가 발생했어요.', 'bot');
        }
    } catch (error) {
        console.error('Chatbot error:', error);
        addChatMessage('서버 연결에 실패했어요.', 'bot');
    }
}

// 챗 메시지 추가
function addChatMessage(message, sender) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.innerHTML = `<p>${message}</p>`;

    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// 봇 응답 생성 (임시)
function generateBotResponse(userMessage) {
    const responses = {
        '안녕': '안녕하세요! 영양제 관련 궁금한 점이 있으시면 언제든 물어보세요.',
        '비타민': '비타민은 우리 몸에 필수적인 영양소입니다. 어떤 비타민에 대해 궁금하신가요?',
        '오메가3': '오메가3는 심혈관 건강과 뇌 건강에 도움이 되는 필수 지방산입니다.',
        '추천': '개인 맞춤 추천을 위해서는 성별/나이별 추천 메뉴를 이용해보세요!',
        '가격': '영양제 가격은 브랜드와 성분에 따라 다양합니다. 구체적인 제품명을 알려주시면 더 자세한 정보를 드릴 수 있어요.',
        '부작용': '영양제도 과다 복용 시 부작용이 있을 수 있습니다. 권장량을 지켜서 복용하시고, 기존 복용 약물이 있다면 의사와 상담하세요.'
    };

    for (const keyword in responses) {
        if (userMessage.includes(keyword)) {
            return responses[keyword];
        }
    }

    return '죄송합니다. 좀 더 구체적인 질문을 해주시면 더 정확한 답변을 드릴 수 있어요. 영양제 이름이나 관심 있는 효능을 말씀해주세요.';
}

// 알림 표시
function showNotification(message, type = 'info') {
    // 기존 알림 제거
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }

    // 새 알림 생성
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    // 스타일 적용
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 5px;
        color: white;
        font-weight: 500;
        z-index: 3000;
        animation: slideIn 0.3s ease;
    `;

    // 타입별 색상
    const colors = {
        success: '#4caf50',
        error: '#f44336',
        info: '#2196f3',
        warning: '#ff9800'
    };

    notification.style.backgroundColor = colors[type] || colors.info;

    document.body.appendChild(notification);

    // 3초 후 자동 제거
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// CSS 애니메이션 추가
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

