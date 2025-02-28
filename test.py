# 원래 리스트
data = [10, 5, 8, 3, 7]

# (값, 원래 인덱스) 튜플 리스트 생성
indexed_data = [(value, index) for index, value in enumerate(data)]

# 값 기준으로 정렬
indexed_data.sort()

# 정렬된 리스트와 정렬 후 인덱스 변환
sorted_data = [value for value, _ in indexed_data]
sorted_indices = [index for _, index in indexed_data]

# 결과 출력
print("정렬된 리스트:", sorted_data)
print("정렬 후 원래 인덱스:", sorted_indices)