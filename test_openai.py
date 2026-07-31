from backend.openai_helper import OpenAIHelper

try:
    helper = OpenAIHelper()
    response = helper.test_connection()

    print("=" * 60)
    print("OpenAI API Test Successful")
    print("=" * 60)
    print(response)

except Exception as e:
    print("Error testing OpenAI API:", e)
    