# project

### wondoofin.csv : wondoodoo2.csv에서 '컵 노트' value들을 전처리
1. 오타 및 같은 종류 다른 이름으로 적혀 있는 같은 통일성 있게 처리.
2. 가격 정보 추가.

### category.csv : wondoofin.csv에서 '컵 노트'열
: (해당 원두의 컵노트들이 리스트로 저장)의 요소들에 따라 7개의 카테고리에 해당되는 값들이 있으면 카테고리명의 열에 1로 입력, 없으면 0.

### features.csv : 원두들의 특징들을 one-hot encoding 및 카테고리화.
: ['바디감', '신맛', '단맛', '쓴맛', '타입'(디카페인, 블렌드, 싱글오리진), '지속가능성'(0, 공정무역, 유기농, 직접무역), '로스팅 포인트'(다크, 라이트, 라이트미디엄, 미디엄, 미디엄다크), '꽃', '과일', '허브', '달콤함', '고소함', '향료_풍미', '초콜릿']

