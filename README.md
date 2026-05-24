## 개발 및 작업 환경

###
* **IDE**: Visual Studio Code
* **Language**: Python 3.11.x (안정성 및 PyTorch 호환성을 위해 3.11 버전 사용)

### 핵심 라이브러리
이 프로젝트는 데이터 수집부터 딥러닝 모델링까지 다음과 같은 주요 패키지들을 활용했습니다.

| 분류 | 라이브러리 (버전) | 설명 및 용도 |
| **Deep Learning** | `torch`, `torchvision` | 1D CNN 감성 분류 모델 설계 및 텐서 연산 |
| **Data Processing** | `pandas` | 수집된 JSON 데이터의 데이터프레임 구조화 및 전처리 |
| **Data Collection** | `requests` | Steam Web API 통신 및 리뷰 데이터 크롤링 |
| **Machine Learning** | `scikit-learn` | Train / Test 데이터셋 분리 (train_test_split) |
| **Visualization** | `matplotlib`, `seaborn` | 장르별 긍부정 비율 파이 차트 등 데이터 시각화 |
| **Text Mining** | `wordcloud` | 긍정/부정 텍스트 코퍼스의 핵심 빈도 단어 시각화 |
| **Environment** | `ipykernel`, `ipython` | VS Code 내 Jupyter Notebook 실행 환경 구축 |
