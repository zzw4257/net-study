# Project Nexus: A Hands-On Guide to Network Connectivity

Welcome to Project Nexus! This project is a practical, hands-on lab designed to teach you core networking concepts by doing. You will expose a web server running on your local machine to the public internet using two different methods, highlighting the roles of IPv6, IPv4, DNS, DDNS, and reverse proxying with tunneling.

## The Goal

To make a simple web page, running on your **[Local Device]**, accessible from the public internet via a domain name you own.

## Core Concepts You Will Learn

*   **IPv4 vs. IPv6:** Understand the practical differences in a real-world home network setup.
*   **DNS & DDNS:** See how domain names map to IP addresses and how to keep them updated automatically.
*   **NAT & Private Networks:** Experience why you can't directly access a device behind a typical IPv4 home router and how to overcome it.
*   **Reverse Proxies & Tunneling:** Learn how to use a public server to "punch a hole" through your private network to expose a service securely.

---

## 0. Environment & Prerequisite Setup

Before starting, ensure you have the following:

1.  **[Local Device]:** Your computer, connected to a home network. We assume it has a public IPv6 address but a private (NAT-ed) IPv4 address.
2.  **[Public Server]:** A cloud server (like an Aliyun ECS, AWS EC2, or DigitalOcean Droplet) with a public IPv4 and IPv6 address.
3.  **[Domain Name]:** A registered domain (e.g., `mydomain.com`) managed through a provider with an API, like Alibaba Cloud.
4.  **Tools:**
    *   On **[Public Server]**: `nginx` should be installed (`sudo apt update && sudo apt install nginx`).
    *   On **[Local Device] & [Public Server]**: `frp` (Fast Reverse Proxy). Download it from the official releases page on GitHub.

### Initial Step: Start Your Local Web Server

On your **[Local Device]**, navigate to the directory containing this `README.md` and the `index.html` file and run:

```sh
# This command serves the 'index.html' file on port 8080.
python -m http.server 8080
```

You should see a "Serving HTTP on 0.0.0.0 port 8080" message. Keep this running.

---

## Path A: The "Modern" Way (IPv6 + DDNS Direct Access)

This path uses your device's public IPv6 address to make it directly accessible on the internet.

### Step A1: Configure DNS

1.  Go to your DNS provider's control panel (e.g., Alibaba Cloud).
2.  Create a new **AAAA** record for your domain.
    *   **Host:** `ipv6` (this will create the address `ipv6.mydomain.com`)
    *   **Type:** `AAAA`
    *   **Value:** You can put a temporary placeholder IPv6 address for now, like `::1`.
    *   **TTL:** Set it to something low, like `600` seconds, for faster updates.

### Step A2: Set Up and Run the DDNS Script

The script `scripts/ddns_update.py` will automatically update the DNS record you just created with your local device's real public IPv6 address.

1.  **Edit the Script:** Open `scripts/ddns_update.py` and fill in your details:
    *   `ACCESS_KEY_ID` & `ACCESS_KEY_SECRET`: Your cloud provider's API keys. It's highly recommended to set these as environment variables for security.
    *   `DOMAIN_NAME`: Your domain, e.g., "mydomain.com".
    *   `SUBDOMAIN`: The host you created, e.g., "ipv6".
2.  **Run the Script:** On your **[Local Device]**, execute the script:
    ```sh
    python scripts/ddns_update.py
    ```
    The script will fetch your public IPv6 and simulate an API call to update your DNS record.

### Step A3: Verify and Access

1.  **Verify DNS:** Open a terminal and use `dig` to check if the DNS record is updated.
    ```sh
    dig AAAA ipv6.mydomain.com
    # Look for your device's IPv6 address in the "ANSWER SECTION".
    ```
2.  **Access:** Once updated, you can access your local server from any IPv6-enabled network!
    ```sh
    # Use curl (the -g and -6 flags are important for IPv6 addresses)
    curl -g -6 "http://[ipv6.mydomain.com]:8080"

    # Or open this URL in your browser.
    ```
    You should see the "Welcome to Project Nexus!" message from `index.html`.

---

## Path B: The "Compatibility" Way (IPv4 + Tunneling)

This path is necessary because your local device's IPv4 address is not public (it's behind NAT). We will use `frp` to tunnel traffic through your **[Public Server]**.

### Step B1: Configure and Run `frps` on the Public Server

1.  **Configuration:** The configuration is in `scripts/frps.ini`. It's very simple; by default, it just tells `frp` to listen on port `7000`.
2.  **Run `frps`:** On your **[Public Server]**, run the following command from the directory where you downloaded `frp`:
    ```sh
    ./frps -c /path/to/scripts/frps.ini
    ```
    Keep this running. It is now waiting for a client to connect.

### Step B2: Configure and Run `frpc` on the Local Device

1.  **Configuration:** Open `scripts/frpc.ini` and set `server_addr` to your **[Public Server]**'s public IPv4 address. The other values are pre-configured to:
    *   Connect to the server on port `7000`.
    *   Forward traffic from the server's port `7080` to your local port `8080`.
2.  **Run `frpc`:** On your **[Local Device]**, run the following command:
    ```sh
    ./frpc -c /path/to/scripts/frpc.ini
    ```
    You should see a message indicating a successful connection to the server. Your tunnel is now active!

### Step B3: Configure DNS and Nginx on the Public Server

1.  **Configure DNS:** Go to your DNS provider and create an **A** record.
    *   **Host:** `proxy` (this will create `proxy.mydomain.com`)
    *   **Type:** `A`
    *   **Value:** Your **[Public Server]**'s public IPv4 address.
2.  **Configure Nginx:**
    *   Copy the configuration file `scripts/nginx_proxy.conf` into your Nginx configuration directory (e.g., `/etc/nginx/sites-available/proxy.conf`).
    *   Update the `server_name` directive to match your domain (`proxy.mydomain.com`).
    *   Enable the site (e.g., `sudo ln -s /etc/nginx/sites-available/proxy.conf /etc/nginx/sites-enabled/`).
    *   Test and reload Nginx: `sudo nginx -t && sudo systemctl reload nginx`.

### Step B4: Verify and Access

You can now access your **[Local Device]**'s web server through your **[Public Server]**!

*   **Access:** Open `http://proxy.mydomain.com` in your browser.

**How does it work?**
Browser -> DNS resolves `proxy.mydomain.com` to your Public Server -> Nginx (port 80) -> Forwards to `127.0.0.1:7080` -> `frps` -> Tunnel -> `frpc` on Local Device -> Your Python server on port `8080`.

Congratulations! You have successfully configured and tested two major ways of connecting to services in a home network.
