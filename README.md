## Как запустить проект
1. Установить пакеты
```bash
pip install fastapi uvicorn
```
2. Запустить main.py
```bash
python main.py
```
3. Перейти к документации по ссылке [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
## Примеры curl
1. Получить все отзывы
```bash
curl --location 'http://127.0.0.1:8000/api/reviews'
```
Результат
```json
[
    {
        "id": 1,
        "text": "люблю",
        "sentiment": "positive",
        "created_at": "2025-07-08T15:49:06.946321"
    },
    {
        "id": 2,
        "text": "плохо",
        "sentiment": "negative",
        "created_at": "2025-07-08T15:57:48.557009"
    }
]
```
2. Получить все отрицательные отзывы
```bash
curl --location 'http://127.0.0.1:8000/api/reviews?sentiment=negative'
```
Результат
```json
[
    {
        "id": 2,
        "text": "плохо",
        "sentiment": "negative",
        "created_at": "2025-07-08T15:57:48.557009"
    }
]
```
3. Создать новый отзыв
```bash
curl --location 'http://127.0.0.1:8000/api/reviews' \
--header 'Content-Type: application/json' \
--data '{
    "text": "плохо"
}'
```
Результат
```json
{
    "id": 4,
    "text": "плохо",
    "sentiment": "negative",
    "created_at": "2025-07-08T18:57:11.397092"
}
```
