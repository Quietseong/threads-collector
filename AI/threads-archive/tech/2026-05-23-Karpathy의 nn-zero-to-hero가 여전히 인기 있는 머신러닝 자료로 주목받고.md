---
title: "Karpathy의 nn-zero-to-hero가 여전히 인기 있는 머신러닝 자료로 주목받고 있다."
source: threads
author: "@devkhpark"
category: "개발/기술"
subcategory: "머신러닝 교육"
tags: ["Karpathy", "nn-zero-to-hero", "JupyterNotebook", "PyTorch", "micrograd"]
confidence: 0.9
original_url: "https://www.threads.com/@devkhpark/post/DYqTBgEE1fp"
collected_at: "2026-05-23T15:59:45.568116Z"
classified_at: "2026-05-23T15:59:49.895200Z"
---

# Karpathy의 nn-zero-to-hero가 여전히 인기 있는 머신러닝 자료로 주목받고 있다.

> **출처**: threads @devkhpark (Threads)
> **카테고리**: 개발/기술 > 머신러닝 교육

## 원문

devkhpark

Karpathy의 nn-zero-to-hero가 또 트렌딩에 올라왔다. 별 93개가 하루에 붙었다는 건, 새 코드 한 줄 없이도 이 리포가 여전히 사람들 손에 들리고 있다는 뜻이다.

흥미로운 건 포맷이다. 책도 아니고, 강의 사이트도 아니고, framework 코드도 아니다. 그냥 Jupyter Notebook 묶음과 YouTube 영상 링크가 전부다. micrograd부터 makemore, GPT를 처음부터 쌓아 올리는 과정을 노트북 셀 단위로 따라가게 만들어 두었다.

여기서 보통의 ML 교재와 갈라진다. PyTorch의 nn.Module을 먼저 가르치지 않는다. 스칼라 값 하나에 backward()를 붙이는 micrograd로 시작해서, autograd가 마법이 아니라 dict와 set으로 짠 DAG라는 걸 손으로 만지게 한다. 그 다음에 character-level bigram, MLP, WaveNet 스타일, 그리고 nanoGPT로 자연스럽게 옮겨간다.

---
[원본 보기](https://www.threads.com/@devkhpark/post/DYqTBgEE1fp)
