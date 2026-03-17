import os
import sys
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

def main():
    # Configuration
    endpoint = "https://models.github.ai/inference"  # ✅ Correct for GitHub Actions
    model = "meta/llama-3.3-70b-instruct"  # Change if needed (see catalog)
    token = os.environ.get("GITHUB_TOKEN")
    
    if not token:
        print("❌ GITHUB_TOKEN environment variable not set.", file=sys.stderr)
        sys.exit(1)

    try:
        # Create client
        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
        )

        # Make request
        response = client.complete(
            messages=[
                SystemMessage("You are a helpful assistant."),
                UserMessage("What is the capital of France? Answer concisely."),
            ],
            temperature=0.7,
            top_p=1.0,
            model=model,
            max_tokens=100,
        )

        # Print result
        print("✅ AI Response:")
        print(response.choices[0].message.content)

    except HttpResponseError as e:
        print(f"❌ HTTP error: {e.status_code} - {e.message}", file=sys.stderr)
        # Suggest common fixes
        if e.status_code == 403:
            print("   → Check that the workflow has 'permissions: models: read'", file=sys.stderr)
            print("   → Also verify that the model name is correct and available.", file=sys.stderr)
        elif e.status_code == 401:
            print("   → Token may be invalid or expired.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
