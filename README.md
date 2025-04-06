# Naive SQL Injection Demo

This repository contains a **naive SQL Injection** demonstration script. The primary goal is to show how unsanitized input fields can be exploited by malicious actors.  
**The code is educational and should only be run on systems for which you have explicit permission.**

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Usage](#usage)
- [Disclaimer](#disclaimer)
- [License](#license)

---

## Overview

**Naive SQL Injection** refers to basic injection payloads inserted into form fields to manipulate or break underlying SQL queries. Although modern websites often use parameterized queries and other mitigations, these attacks can still succeed on improperly secured systems.

This project is composed of:

- **`sql_injector_demo.py`** – A Python script that:
  1. Retrieves all `<input>` fields from a target webpage.
  2. (Optionally) attempts multiple common SQL injection payloads.
  3. Compares the “normal” response to an “injection” response to gauge potential vulnerability.
  4. Uses DNS lookups for demonstration purposes (e.g., retrieving CNAME records).

## Features

1. **Extract HTML Inputs**  
   Automatically detects `<input>` elements on a target page using **BeautifulSoup**.

2. **Multiple SQL Injection Payloads**  
   Demonstrates naive injections (e.g., `' OR 1=1 --`, `'; DROP TABLE users; --`).

3. **Safe by Default**  
   Injection attempts are **commented out** to avoid accidental misuse. You must **uncomment** to run them.

4. **DNS Lookup**  
   Shows how to query CNAME records for a given domain using `dns.resolver`.

## Usage

1. **Install Dependencies**
   ```bash
   pip install requests beautifulsoup4 dnspython
   ```

2. **Run the Script**
   ```bash
   python sql_injector_demo.py
   ```

3. **Modify as Needed**
   - Edit the `TARGET_URL` variable in the script to point to the web page you want to test.
   - Uncomment any injection payloads you wish to test.
   - Follow the on-screen instructions and review console output for signs of vulnerability.

> ⚠️ WARNING: Only use this tool on systems you **own** or have **explicit written permission** to test.

## Disclaimer

This project is provided for **educational purposes only**.  
Do **not** use this code on any production, public-facing, or unauthorized system.  
The author assumes **no responsibility** for misuse of this code or any consequences resulting from its execution.
