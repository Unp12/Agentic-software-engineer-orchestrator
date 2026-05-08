import requests

print("🚀 Sending request to the AI Squad...")
response = requests.post(
    "http://127.0.0.1:8000/api/generate",
    json={"prompt": "Write a Python script using pandas that reads a CSV file called 'patients.csv' and calculates the average age of the patients."}
)

# Check if the server actually succeeded (Status 200)
if response.status_code == 200:
    data = response.json()
    print("\n" + "="*60)
    print("🧠 THE PRODUCT MANAGER'S PLAN")
    print("="*60)
    print(data["pm_plan"]) 
    print("\n" + "="*60)
    print("💻 THE CODER'S OUTPUT")
    print("="*60)
    print(data["generated_code"])
else:
    # If the server crashed, print the exact reason!
    print(f"\n❌ SERVER CRASHED (Status {response.status_code})")
    print(f"Raw Error: {response.text}")