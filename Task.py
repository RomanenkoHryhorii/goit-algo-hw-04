import random
import timeit
import statistics

def insertion_sort(arr):
    """Алгоритм сортування вставками"""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(arr):
    """Алгоритм сортування злиттям"""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    """Допоміжна функція для злиття підмасивів"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

def benchmark_sorting(algorithm, data):
    """Вимірювання часу виконання алгоритму сортування"""
    return timeit.timeit(lambda: algorithm(data.copy()), number=100)

def generate_test_data(size, distribution='random'):
    """Генерація тестових даних з різними характеристиками"""
    if distribution == 'random':
        return [random.randint(0, 10000) for _ in range(size)]
    elif distribution == 'sorted':
        return list(range(size))
    elif distribution == 'reverse_sorted':
        return list(range(size, 0, -1))
    elif distribution == 'mostly_sorted':
        data = list(range(size))
        # Внесемо невелику кількість випадкових змін
        for _ in range(size // 10):
            i, j = random.sample(range(size), 2)
            data[i], data[j] = data[j], data[i]
        return data

def run_benchmarks():
    """Запуск бенчмарків для різних розмірів і типів даних"""
    test_sizes = [100, 1000, 10000]
    distributions = ['random', 'sorted', 'reverse_sorted', 'mostly_sorted']
    
    results = {}
    
    for size in test_sizes:
        results[size] = {}
        for dist in distributions:
            data = generate_test_data(size, dist)
            
            results[size][dist] = {
                'insertion_sort': benchmark_sorting(insertion_sort, data),
                'merge_sort': benchmark_sorting(merge_sort, data),
                'timsort': benchmark_sorting(sorted, data)
            }
    
    return results

def format_results(results):
    """Форматування результатів для читабельного виводу"""
    output = "# Порівняння алгоритмів сортування\n\n"
    output += "## Методологія тестування\n"
    output += "- Використано модуль `timeit` для точного виміру часу\n"
    output += "- Кожен алгоритм запускався 100 разів для усереднення результатів\n"
    output += "- Тестування на різних розмірах масивів: 100, 1000, 10000 елементів\n"
    output += "- Типи розподілення даних: випадкове, відсортоване, обернено відсортоване, майже відсортоване\n\n"
    
    output += "## Результати тестування\n"
    for size, distributions in results.items():
        output += f"### Розмір масиву: {size} елементів\n\n"
        output += "| Розподілення | Insertion Sort | Merge Sort | Timsort |\n"
        output += "|--------------|----------------|------------|----------|\n"
        
        for dist, algorithms in distributions.items():
            output += f"| {dist} | {algorithms['insertion_sort']:.5f} | {algorithms['merge_sort']:.5f} | {algorithms['timsort']:.5f} |\n"
        
        output += "\n"
    
    output += "## Висновки\n"
    output += "1. **Timsort** демонструє найкращу продуктивність у всіх сценаріях\n"
    output += "2. Сортування вставками ефективне на малих масивах та майже відсортованих даних\n"
    output += "3. Сортування злиттям має стабільну продуктивність, але дещо гірше за Timsort\n"
    output += "4. Комбінування алгоритмів у Timsort (вставки + злиття) забезпечує оптимальну швидкодію\n"
    
    return output

def main():
    results = run_benchmarks()
    formatted_results = format_results(results)
    
    with open('readme.md', 'w', encoding='utf-8') as f:
        f.write(formatted_results)
    
    print("Результати збережено у readme.md")

if __name__ == "__main__":
    main()