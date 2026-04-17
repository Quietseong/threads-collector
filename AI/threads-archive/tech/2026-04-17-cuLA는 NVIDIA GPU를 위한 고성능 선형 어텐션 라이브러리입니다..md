---
title: "cuLA는 NVIDIA GPU를 위한 고성능 선형 어텐션 라이브러리입니다."
source: discuss
author: ""
category: "개발/기술"
subcategory: "GPU 최적화"
tags: ["cuLA", "CUDA", "선형어텐션", "NVIDIA", "GPU최적화"]
confidence: 0.9
original_url: "https://discuss.pytorch.kr/t/cula-cuda-linear-attention-nvidia-blackwell-hopper-gpu-cuda/9658?u=j808esc"
collected_at: "2026-04-17T02:08:07.312304Z"
classified_at: "2026-04-17T02:08:11.335697Z"
---

# cuLA는 NVIDIA GPU를 위한 고성능 선형 어텐션 라이브러리입니다.

> **출처**: discuss (PyTorchKR)
> **카테고리**: 개발/기술 > GPU 최적화

## 원문

cuLA(CUDA Linear Attention): NVIDIA Blackwell, Hopper GPU를 위한 선형 어텐션 고성능 CUDA 커널 라이브러리

cuLA 소개 트랜스포머(Transformer) 기반 언어 모델이 점점 더 긴 컨텍스트를 다루게 되면서, 기존의 소프트맥스 어텐션(Softmax Attention)이 가진 O(n^2) 계산 복잡도 문제는 핵심적인 병목이 되었습니다. 이를 해결하기 위해 등장한 선형 어텐션(Linear Attention)은 상태 업데이트를 선형 시간으로 수행함으로써 긴 컨텍스트 처리에 훨씬 유리한 구조를 제공합니다. 그러나 이론적인 효율성을 실제 하드웨어 성능으로 연결하려면, GPU의 특성에 맞게 세심하게 최적화된 커널 구현이 반드시 필요합니다.  cuLA는 선형 어텐션 변형들을 위한 고성능 CUDA 커널 라이브러리입니다. inclusionAI가 개발한 이 프로젝트는 CuTe DSL과 CUTLASS C++를 활용하여 NVIDIA Blackwell(SM10X) 및 Hopper(SM90) GPU 아키텍처에 특화된 핸드튜닝(hand-tuned) 구현을 제공합니다. cuLA는 flash-linear-at...

---
[원본 보기](https://discuss.pytorch.kr/t/cula-cuda-linear-attention-nvidia-blackwell-hopper-gpu-cuda/9658?u=j808esc)
