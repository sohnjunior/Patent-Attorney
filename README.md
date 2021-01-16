# Patent Attorney

# 💡 프로젝트 소개

2020 학년도 산학 연계 프로젝트 교과목에서 진행한 `AI 알고리즘을 활용한 이미지 유사도 측정` 프로젝트입니다.

구체적으로는 `특허 이미지(상표 및 디자인) 유사도 분석` 을 주제로 개발을 진행했습니다.

사용자가 자신이 등록하고자 하는 상표 혹은 디자인 이미지를 업로드하면

해당 웹 서비스에서 사전에 특허가 등록된 정보들 중 유사한 것이 있는지 쉽게 파악할 수 있도록 합니다.

이를 통해 특허 이미지 유사도 측정에 대한 객관성 지표를 얻고 유사도 판별에 소요되는 시간을 단축하여

불필요한 인력 낭비를 최소화하고자 해당 프로젝트를 진행하게 되었습니다.

# ⚙️ 개발 환경

![1](https://user-images.githubusercontent.com/37819666/104809757-c617f500-5832-11eb-8af3-926db5219e17.png)

# 🎯 주요 스펙 및 알고리즘

## Deep Ranking 알고리즘

### Deep Ranking 알고리즘 개요

`Deep-Ranking` 은 2014년 CVPR에서 "Learning Fine-grained Image Similarity with Deep Ranking" 논문에 기재된 `이미지 유사도` 문제를 해결하기 위한 알고리즘 입니다.

서로 다른 이미지간의 유사성을 비교하기 위해서 `triplet` 이라 불리는 이미지 집합을 사용합니다.

여기서 `triplet` 은 `query, positive, negative` 이미지로 구성되어 있는 쌍을 의미합니다.

![Untitled](https://user-images.githubusercontent.com/37819666/104809806-34f54e00-5833-11eb-9ec6-356aceb2a6d9.png)

`triplet` 의 각 이미지들은 유클리드 공간 상에 매핑 되어 `유클리드 제곱 거리` 를 통해 유사성을 비교합니다.

여기서 유클리드 공간 매핑 함수를 `임베딩 함수` 라고 하며 CNN 과 같은 모델을 사용할 수 있습니다.

일반 유클리드 거리가 아닌 제곱 거리를 사용해서 클러스터링을 고속화 할 수 있습니다.

우리가 사용하는 `유클리드 제곱 거리` 의 수식은 다음과 같습니다.

<img width="286" alt="_2021-01-16__2 47 10" src="https://user-images.githubusercontent.com/37819666/104809737-a1238200-5832-11eb-8b1a-850131a1d3eb.png">

이제 이 알고리즘이 사용하는 `손실 함수` 를 알아보겠습니다.

<img width="395" alt="_2021-01-16__2 48 16" src="https://user-images.githubusercontent.com/37819666/104809736-a08aeb80-5832-11eb-9bf7-f93e28b06174.png">

`Deep-Ranking` 알고리즘은 위와 같이 `triplet` 에 대한 `hinge loss` 를 사용하며

이를 통해 유사 이미지와는 더 가깝고 유사하지 않은 이미지와는 더 멀게 임베딩 되도록 학습됩니다.

실제 모델에서 학습에 사용되는 `목적 함수` 는 다음과 같습니다.

<img width="458" alt="_2021-01-16__2 48 47" src="https://user-images.githubusercontent.com/37819666/104809735-a08aeb80-5832-11eb-9220-9dabb0291dea.png">

여기서 람다는 정규화를 위한 매개변수이며 이를 통해 알고리즘을 일반화 할 수 있습니다.

해당 논문에서는 람다 값을 `0.001` 로 설정했습니다.

또한 `W` 는 임베딩 함수 `f` 에서 사용 되는 매개변수이고 이 값을 최적화 하는 것이 목표입니다.

**따라서, 위 목적 함수를 이용해서 임베딩 함수 `f` 에서 사용되는 `W` 의 최적의 값을 학습하기 위해**

**이후 설명하는 딥러닝 네트워크 구조가 활용되는 것입니다.**

### 네트워크 구조 살펴보기

<img width="400" alt="_2021-01-16__12 16 21" src="https://user-images.githubusercontent.com/37819666/104809733-9ff25500-5832-11eb-8fd3-e912e077e378.png">

`Deep-Ranking` 알고리즘은 전체적으로 봤을 때 학습을 위해 위 네트워크 구조를 사용합니다.

`Q, P, N` 은 각각 질의, 긍정, 부정 이미지를 임베딩하는 하위 네트워크를 의미합니다.

각각의 `Layer` 의 역할은 다음과 같습니다.

- **Triplet Sampling Layer**

  `Triplet Sampling Layer` 의 경우 이미지 샘플로부터 `Triplet` 을 생성하는 계층입니다.

  논문에 따르면 하나의 질의 이미지와 다른 이미지들 간의 `relevance score` 를 계산하여

  `긍정, 부정` 이미지를 정의하고 이를 통해 `triplet` 을 생성합니다.

- **Q, P, N Layer**

  해당 계층은 각각의 이미지 샘플을 유클리드 공간에 임베딩하는 역할을 합니다.

- **Ranking Layer**

  `Ranking Layer` 의 경우 임베딩된 값으로 `hinge loss` 를 계산하는 계층입니다.

<img width="400" alt="_2021-01-16__12 16 36" src="https://user-images.githubusercontent.com/37819666/104809732-9f59be80-5832-11eb-97ae-62e2231c97cb.png">

임베딩을 위한 하위 네트워크 구조(`Q, P, N Layer`) 는 위와 같은 세부 네트워크로 구성됩니다.

위와 같이 `ConvNet` 하나만 사용하는 것이 아니라 `multi-scale` 네트워크로 구성한 이유는

`fine-grained` 한 결과를 얻기 위함 입니다.

`ConvNet` 은 이미지 분류에 특화된 고성능 모델을 사용하고 그 외 두 개의 Convolution Layer는

입력 이미지의 고유한 `지역적 특성` 을 감지하기 위한 용도로 사용됩니다.

**Hyper Parameters (실제 학습 시 사용)**

- `Epoch` : 10
- `Batch size` : 20
- `optimizer` : Adam
- `Learning rate` : 0.001

### ⚠️ 실제 구현 시 기존 논문에서 변경한 부분

다음 세 가지 사항이 프로젝트 진행 시 실제 논문과 다르게 구현한 부분입니다.

1. `**ConvNet` 적용 모델\*\*

   `ConvNet` 은 논문과 같이 `AlexNet` 을 사용하지 않고 성능상의 이유로 `ResNet` 을 적용했습니다.

2. `**Q, P, N` 네트워크 구조\*\*

   논문에 따르면 `Q, P, N` 네트워크에서 사용 되는 임베딩 함수 `f` 는 동일한 파라미터 값 `W` 를 공유합니다.

   따라서 굳이 3 종류의 하위 네트워크를 구성하지 않고 하나의 네트워크로 통합하여 구현하였습니다.

   이는 프로젝트 규모와 훈련에 필요한 데이터의 양, 그리고 작업 시간 등을 고려한 것입니다.

3. `**Triplet` 샘플링 방식\*\*

   논문에는 `relevance score` 를 계산해서 온라인 버퍼 샘플링 알고리즘으로

   질의 이미지의 `긍정, 부정` 이미지 셋을 구성합니다.

   이를 위해선 방대한 이미지와 각 이미지에 특성 값을 직접 지정하는 작업이 필요한데

   (논문의 경우 27가지의 특성을 지정하여 `golden feature` 를 구성함)

   저희의 경우 특허청 오픈 API 를 통해 수집하는 이미지 데이터 양의 한계와 프로젝트 기간의 문제로

   빠르게 구현하고 테스트하기 위해 이 보다 단순한 방법이 필요했습니다.

   따라서 `triplet` 에 사용되는 긍정 및 부정 이미지는 각각 `in-class` 와 `out-class` 에서

   랜덤으로 생성하고 `triplet` 검증 과정을 거쳐 훈련에 사용될 이미지 셋을 걸러내기로 했습니다.

## Object Detection (YOLO v3)

### 도입한 계기

<img width="600" alt="_2021-01-16__1 13 00" src="https://user-images.githubusercontent.com/37819666/104809728-9c5ece00-5832-11eb-8cb5-bb79b9776b61.png">

상표 이미지는 사실 대부분 특정 객체(여기선 닭) 뿐만 아니라 상호명도 포함하는 경우가 많습니다.

이 경우 해당 이미지를 그대로 학습하면 상표 유사도 정확도가 크게 떨어지고 신뢰성을 잃게 됩니다.

따라서 상표의 유사성에 큰 영향을 주는 특정 객체만 추출해서 비교하고자 도입하게 되었습니다.

### 주요 특징

`YOLO` 알고리즘은 `단일 단계 방식` 의 객체 탐지 알고리즘입니다.

때문에 먼저 `영역 제안(Region Proposal)` 이 필요한 `이단계 방식` 의 알고리즘보다 속도 면에서 뛰어납니다.

이로 인해 실시간 탐지를 필요로 하는 애플리케이션에서 많이 활용됩니다.

### 활용 방식

실제 사용을 위해서 `OpenCV` 를 기반으로 구현된 오픈 소스를 활용 했으며

`YOLO` 의 백본 아키텍쳐인 `DarkNet` 을 학습하는 별도의 과정이 필요했습니다.

# 💪 개발 생산성

## Triplet Checker GUI 프로그램

`Deep-Ranking` 알고리즘은 정제된 `triplet` 이 필요합니다.

논문의 경우 온라인 샘플링 방식을 사용하고 있지만 저희는 `handcrafted` 방식을 사용하기로 했습니다.

이를 위해서 엑셀 파일로 질의, 긍정, 부정 이미지 셋을 생성하고 각각의 조합을 확인하며

모델 학습에 쓸 만한 데이터들을 걸러 내는 과정이 필요합니다.

모든 이미지를 직접 열어보며 비교하는 것은 많은 시간을 필요로 하기 때문에

`python tinker` 패키지를 활용하여 이 작업을 도와주는 GUI 프로그램을 제작해서 작업을 단순화했습니다.

## Google Image & API Crawler

`YOLO` 알고리즘 훈련을 위해서 많은 양의 학습 이미지가 필요했습니다.

학습에 사용한 카테고리는 총 5가지 (닭, 돼지, 사자, 소, 태양) 이며 데이터를 모으기 위해

구글 이미지 크롤러를 제작하여 진행했습니다.

또한 특허청 오픈 API 를 통해 특허 이미지와 정보를 수집했고, 이를 자동화하기 위해

마찬가지로 API 크롤러를 구현해서 사용했습니다.

# 🎥 데모 영상

[최종 발표영상 링크](https://www.youtube.com/watch?v=o7t08OFqWY0&feature=youtu.be)

# 📚 참고 자료

[Paper Review - Deep Ranking](https://you359.github.io/meta%20learning/DeepRanking/)

[Learning Fine-grained Image Similarity with Deep Ranking](https://arxiv.org/abs/1404.4661)

[Learning Fine-grained Image Similarity with Deep Ranking 정리](https://umbum.dev/262)

[Euclidean and Euclidean Squared](http://www.improvedoutcomes.com/docs/WebSiteDocs/Clustering/Clustering_Parameters/Euclidean_and_Euclidean_Squared_Distance_Metrics.htm)

[딥러닝을 활용한 객체 탐지 알고리즘 이해하기 - SAS Korea Blog](https://blogs.sas.com/content/saskorea/2018/12/21/%EB%94%A5%EB%9F%AC%EB%8B%9D%EC%9D%84-%ED%99%9C%EC%9A%A9%ED%95%9C-%EA%B0%9D%EC%B2%B4-%ED%83%90%EC%A7%80-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0/)
