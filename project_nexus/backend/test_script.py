import sys
import requests

def main():
    # 1. Print to stdout
    print("Hello from the sandbox!")

    # 2. Check Python version
    print(f"Running on Python version: {sys.version.split()[0]}")

    # 3. Test network connectivity and the 'requests' library
    try:
        response = requests.get("http://httpbin.org/get", timeout=5)
        response.raise_for_status()
        print("Network test successful: Able to reach httpbin.org.")
        # print(f"Response from httpbin: {response.json().get('headers', {}).get('User-Agent')}")
    except requests.RequestException as e:
        print(f"Network test failed: {e}", file=sys.stderr)

    # 4. Print a message to stderr
    print("This is a test message to stderr.", file=sys.stderr)

    print("\nScript finished.")

if __name__ == "__main__":
    main()
