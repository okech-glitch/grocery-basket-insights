import requests

url = "http://localhost:5000/submit"
file_path = "data/baseline_submission.csv"
user_id = "test_user"

with open(file_path, 'rb') as file:
    files = {'file': file}
    data = {'user_id': user_id}
    response = requests.post(url, files=files, data=data)

print(response.json()) 
