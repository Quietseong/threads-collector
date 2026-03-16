---
type: dashboard
---

# Threads 수집 대시보드

## 최근 수집 (7일)

```dataview
TABLE author AS "작성자", category AS "카테고리", subcategory AS "소분류", confidence AS "확신도"
FROM "AI/threads-archive"
WHERE source = "threads"
AND date(classified_at) >= date(today) - dur(7 days)
SORT classified_at DESC
LIMIT 30
```

## 카테고리별 통계

```dataview
TABLE length(rows) AS "게시글 수"
FROM "AI/threads-archive"
WHERE source = "threads"
GROUP BY category
SORT length(rows) DESC
```

## 태그 클라우드

```dataview
FLATTEN tags AS tag
WHERE source = "threads"
GROUP BY tag
SORT length(rows) DESC
LIMIT 20
TABLE length(rows) AS "횟수"
```
