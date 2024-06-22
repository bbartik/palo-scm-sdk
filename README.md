# Palo Alto Networks Strata Coud Manager SDK and CSV Import Application

## Overview

This repository contains two primary components:
1. **Strata Cloud Manager SDK**: A Python SDK for interacting with the Palto Alto's Strata Cloud Manager (SCM) API.
2. **CSV Import Application**: A Python application that uses the SDK to import address and tag data from CSV files into SCM.

## Repository Structure

```
palo-scm-sdk/
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py
├── scm/
│   ├── __init__.py
│   ├── auth.py
│   ├── client.py
│   ├── config.py
│   ├── scm.py
├── sdk_tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_client.py
│   ├── test_config.py
│   ├── test_scm.py
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── csv/
├── .venv/
```

## Getting Started

### Prerequisites

- Python 3.7+
- [pip](https://pip.pypa.io/en/stable/)

### Installation

1. **Clone the Repository**
    ```bash
    git clone <your-repo-url>
    cd palo-scm-sdk
    ```

2. **Create and Activate Virtual Environment**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    pip install -e .
    ```

### Configuration

Create a `.env` file in the root directory with the following content:

SCM_DEBUG=True # Set to False to disable detailed error messages
CLIENT_ID=<palo-service-account-id> # Service account in Palo IAM
CLIENT_SECRET=<palo-svc-acct-secret> # From service account in Palo IAM
BASE_URL=https://api.sase.paloaltonetworks.com/sse/config/v1
TOKEN_URL=https://auth.apps.paloaltonetworks.com/oauth2/access_token
TSG_ID=<palo-tenant-id>


### Running the Application

To run the application and import data from the CSV files that have you download from Panorama or a Palo FW:
(Currently on Addresses and Tags are supported)

```bash
run-app
```

Alternatively, you can run the application directly:

```bash
python app/main.py
```

## SDK Usage

You can use the SDK independently to interact with the Prisma SASE API. Here's a brief example:

\```python
from scm import AddressEndpoint

address_endpoint = AddressEndpoint()
folder_name = "your_folder_name"

# Create an address
address_data = {
    "name": "Test Address",
    "ip_netmask": "192.168.1.0/24",
    "tag": ["tag1", "tag2"]
}

created_address = address_endpoint.create(folder_name, address_data)
if created_address:
    print("Address created successfully")
else:
    print("Failed to create address")
```

## Testing

To run tests for the SDK:

```bash
pytest sdk_tests/
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [httpx](https://github.com/encode/httpx)
- [pandas](https://pandas.pydata.org/)


