# RetinaNet Deployment using React and Flask

## 개요

Object Detection 모델의 훈련부터 배포까지의 전체 워크플로우를 구현한다. RetinaNet을 이용한 object detection 모델을 훈련하고 테스트한다. 배포를 위해서 Streamlit을 사용하여 간단한 웹앱을 구성해보고, 나아가 React와 Flask를 활용해 프론트엔드와 백엔드를 구현한다.



## RetinaNet

논문) [Focal Loss for Dense Object Detection](https://arxiv.org/abs/1708.02002)

2017년 FAIR에서 발표한 RetinaNet은 성능 향상을 가로막는 클래스 분균형 문제를 해결하기 위해 focal loss를 도입하였다. 이를 통해서 one-stage detector만큼 빠른 속도를 가지면서 two-stage detector를 능가하는 성능을 얻을 수 있었다. PyTorch 1.7 버전부터는 RetinaNet pre-trained 모델을 제공하기 때문에, 이를 활용한 응용을 더욱 손쉽게 구현할 수 있다. 그러나 여기에서는 새로운 데이터셋으로부터 직접 훈련시키고, 훈련된 모델을 활용한 응용을 목표로 한다. 따라서 pre-trained 모델 대신 [pytorch-retinanet](https://github.com/yhenon/pytorch-retinanet) 의 코드를 참고/변형하여 진행한다.



### Dataset

 여기서는 roboflow가 제공하는 Public Dataset 중에서 [Hard Hat Workers Dataset](https://public.roboflow.com/object-detection/hard-hat-workers)을 사용하였다. RetinaNet은 COCO 데이터셋과 같은 json 포맷의 annotation 데이터를 사용한다. roboflow는 train 과 test 폴더 안에 _annotations.coco.json이라는 파일명으로 각각의 annotation 정보를 제공한다. 앞으로의 학습과정의 통일성을 위하여 각각의 파일을 train.json과 test.json으로 바꾸고, 상위 폴더로 이동시켜서 사용한다.



### 모델 학습

 학습에 필요한 하이퍼 파라미터 등은 configuration.yml을 통해 지정한다. 다음은 configuration.yml에 지정된 파라미터에 대한 설명이다.

[train] 

- image_dir : 훈련 데이터의 디렉토리 경로
- annotation : 훈련 데이터의 annotation 정보를 담은 json 파일 경로
- model : RetinaNet에서 사용할 backbone 모델의 지정. 참고한 repository에서는 ResNet-18/34/50/101/152 모델이 구현되어 있는데, 추후의 확장을 고려하여 모델은 모델명소문자+depth (e.g.  resnet18)로 호출하도록 한다.