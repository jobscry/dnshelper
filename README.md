# DNS Helper

Finds all IPs that can send/recieve email from a FQDN via the DNS records.  Will continue to resolve hostnames until an IP is found.

## Installation

```python
pip install -r /path/to/requirements.txt
```

## Commands

### MX Lookup

```python
python dnshelper.py [OPTIONS] [DOMAIN] mx_lookup
```

* **geo_lookup** - Perform geo lookups on found IPs
* **domain** - FQDN to lookup


### SPF Lookup

```python
python dnshelper.py [OPTIONS] [DOMAIN] SPF_lookup
```

* **geo_lookup** - Perform geo lookups on found IPs
* **domain** - FQDN to lookup
