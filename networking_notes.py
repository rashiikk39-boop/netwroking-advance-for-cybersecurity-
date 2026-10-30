#!/usr/bin/env python3
"""
Computer Networking Notes
Beginner to Advanced (Cybersecurity Focus)

Created by Rashida Kathiriya

Every section of the notes is a function decorated with @section(...).
Timestamps in [brackets] show where each slide appears in the video.

Usage:
    python networking_notes.py                 # print every section
    python networking_notes.py --list          # list all sections
    python networking_notes.py 12              # print section 12
    python networking_notes.py 3 19 20         # print several sections
    python networking_notes.py --search tcp    # sections that mention "tcp"
    python networking_notes.py --out notes.txt # save everything to a text file
"""

import argparse
import contextlib
import io
import sys
import textwrap

WIDTH = 78

LOGO = r"""
 ____  _  __
|  _ \| |/ /
| |_) | ' /
|  _ <| . \
|_| \_\_|\_\
"""

SECTIONS = []  # filled by the @section decorator: (title, timestamp, function)


# ---------------------------------------------------------------------------
# Helpers used by the notes
# ---------------------------------------------------------------------------
def section(title, time=""):
    """Register a function as one section of the notes."""

    def decorator(fn):
        SECTIONS.append((title, time, fn))
        return fn

    return decorator


def para(text):
    print(textwrap.fill(text, WIDTH))
    print()


def note(text):
    """Instructor annotation or side note."""
    print(textwrap.fill("(" + text + ")", WIDTH))
    print()


def label(name, text):
    print(textwrap.fill(f"{name} {text}", WIDTH))
    print()


def subheading(text):
    print(text)
    print("~" * len(text))


def bullets(items):
    """Each item is plain text, or 'Label|text' to show a bold-style label."""
    for item in items:
        if "|" in item:
            head, body = item.split("|", 1)
            item = f"{head}: {body}"
        print(textwrap.fill(item, WIDTH, initial_indent="  - ", subsequent_indent="    "))
    print()


def numbered(items):
    for i, item in enumerate(items, 1):
        print(textwrap.fill(item, WIDTH, initial_indent=f"  {i}. ", subsequent_indent="     "))
    print()


def callout(name, text):
    print(textwrap.fill(f">> {name} {text}", WIDTH, subsequent_indent="   "))
    print()


def table(headers, rows):
    """Print a simple text table that wraps long cells to fit WIDTH."""
    ncols = len(headers)
    cols = [[str(h)] + [str(r[i]) for r in rows] for i, h in enumerate(headers)]
    widths = [max(len(c) for c in col) for col in cols]
    avail = WIDTH - (3 * ncols + 1)
    while sum(widths) > avail:
        widest = max(range(ncols), key=lambda k: widths[k])
        if widths[widest] <= 8:
            break
        widths[widest] -= 1

    def cell_lines(text, w):
        return textwrap.wrap(text, w) or [""]

    def divider(ch):
        return "+" + "+".join(ch * (w + 2) for w in widths) + "+"

    def row(cells):
        wrapped = [cell_lines(str(c), widths[i]) for i, c in enumerate(cells)]
        for k in range(max(len(w) for w in wrapped)):
            parts = [(w[k] if k < len(w) else "").ljust(widths[i]) for i, w in enumerate(wrapped)]
            print("| " + " | ".join(parts) + " |")

    print(divider("-"))
    row(headers)
    print(divider("="))
    for r in rows:
        row(r)
        print(divider("-"))
    print()


# ---------------------------------------------------------------------------
# The notes
# ---------------------------------------------------------------------------
@section("How Networking Was Born", "before 5:43")
def history():
    para("From military experiments to the internet we use every day.")
    table(
        ["Decade", "What happened"],
        [
            ["1960s", "ARPANET created by the US Defense Department. First network, connecting 4 universities."],
            ["1970s", "TCP/IP protocols invented. Email introduced for the first time."],
            ["1980s", "DNS system created. Internet opens up to more institutions."],
            ["1990s", "World Wide Web invented by Tim Berners-Lee. Internet goes public and commercial."],
            ["2000s", "Wi-Fi becomes mainstream. Broadband replaces dial-up globally."],
            ["2010s", "Cloud computing explodes. Mobile internet dominates traffic."],
            ["2020s", "5G rolls out globally. IoT connects billions of devices."],
        ],
    )
    subheading("Fun facts from the slide")
    bullets(
        [
            '1969|The first message ever sent over ARPANET was "LO". The system crashed after 2 letters.',
            "TCP/IP|The protocol suite invented in 1974 still powers the internet today.",
            "Hacking|The first computer hack was recorded in 1971, on phone networks.",
            "Instructor emphasis|Network = connect (computers connecting to each other).",
        ]
    )


@section("What is Networking & Why Hackers Must Understand It", "5:43")
def what_is_networking():
    label(
        "Definition:",
        "Networking enables computers to communicate and share resources through "
        "interconnected systems, using standardized protocols and addressing schemes.",
    )
    print("Why it matters for ethical hackers:\n")
    table(
        ["Skill area", "What it means"],
        [
            ["Packet Sniffing & Analysis", "Intercept and decode network traffic to find vulnerabilities and sensitive data being transmitted."],
            ["Protocol Exploitation", "Understand weaknesses in the TCP/IP stack to carry out attacks such as session hijacking or DNS poisoning."],
            ["Network Reconnaissance", "Map target infrastructure with tools like Nmap to discover hosts, open ports and running services."],
            ["Firewall Evasion", "Bypass security controls by manipulating packet headers and understanding filtering mechanisms."],
        ],
    )


@section("Types of Networks", "12:28")
def network_types():
    table(
        ["Type", "Full form", "Description"],
        [
            ["LAN", "Local Area Network", "Connects devices within a limited geographical area, such as an office building or campus."],
            ["MAN", "Metropolitan Area Network", "Covers a city or large town. Larger than a LAN but smaller than a WAN."],
            ["WAN", "Wide Area Network", "Spans large distances across cities, countries or continents, connecting multiple LANs."],
            ["PAN", "Personal Area Network", "Connects devices within a personal workspace, such as smartphone, laptop and peripherals."],
        ],
    )
    subheading("Fiber optic cables (undersea cables) [16:33]")
    bullets(
        [
            "WAN|Wide Area Network connects countries. Instructor note: countries.",
            "The slide shows a diver working on an undersea cable and a submarine-cable map around India, "
            "the Arabian Sea, the Bay of Bengal, Sri Lanka, the Maldives and Southeast Asia.",
            "Takeaway|Cables laid on the sea floor are what physically link countries and continents, "
            "so most international internet traffic travels under the ocean.",
        ]
    )


@section("Network Devices", "18:13")
def network_devices():
    table(
        ["Device", "Function"],
        [
            ["Router", "Forwards packets between different networks using IP addresses."],
            ["Switch", "Connects devices on the same network using MAC addresses."],
            ["Hub", "Broadcasts data to all connected devices (obsolete technology)."],
            ["Firewall", "Filters traffic based on security rules, blocking unauthorized access."],
            ["Modem", "Converts digital signals to analogue for internet connectivity."],
            ["Access Point", "Provides wireless network connectivity to devices."],
        ],
    )
    callout("Instructor marked:", "Router, Switch and Hub (tick marks on these three).")


@section("IP Address vs MAC Address", "24:47")
def ip_vs_mac():
    table(
        ["", "IP Address", "MAC Address"],
        [
            ["Definition", "Logical address assigned by the network.", "Physical address burned into the hardware."],
            ["Changes?", "Changes when the device moves networks.", "Permanent and unique to the device. Never changes."],
            ["Assigned by", "Network administrator or DHCP.", "Manufacturer (built into the hardware)."],
            ["Used for", "Routing across networks.", "Local network communication."],
        ],
    )
    note("Instructor sketch: a device uses its IP address to reach the Internet.")


@section("IPv4 vs IPv6 Comparison", "28:08")
def ipv4_vs_ipv6():
    table(
        ["", "IPv4", "IPv6"],
        [
            ["Format", "32-bit, dotted decimal notation", "128-bit, hexadecimal notation"],
            ["Example", "192.168.1.1", "2001:0db8::1"],
            ["Structure", "4 octets (8 bits each): 192 . 168 . 1 . 1",
             "8 groups (16 bits each): 2001 : 0db8 : 0000 : 0000 : 0000 : 0000 : 0000 : 0001"],
        ],
    )
    note("Instructor example: 192.168.10.1 is a 32-bit address.")


@section("Public vs Private IP Addresses", "36:26")
def public_vs_private():
    table(
        ["", "Public IP", "Private IP"],
        [
            ["Definition", "Globally unique address, routable on the internet.", "Non-routable address used within private networks."],
            ["Example", "8.8.8.8 (Google DNS)", "192.168.1.100"],
            ["Use case", "Servers, websites, devices accessible from the internet.", "Home networks, corporate LANs, internal devices."],
        ],
    )
    print("Private IP ranges:\n")
    table(
        ["Class", "Range"],
        [
            ["Class A", "10.0.0.0 to 10.255.255.255"],
            ["Class B", "172.16.0.0 to 172.31.255.255"],
            ["Class C", "192.168.0.0 to 192.168.255.255"],
        ],
    )
    callout("Important:", "Private IPs are not routable on the internet.")


@section("Static vs Dynamic IP Assignment", "39:52")
def static_vs_dynamic():
    table(
        ["", "Static IP", "Dynamic IP"],
        [
            ["Definition", "Manually assigned, fixed address.", "Automatically assigned by a DHCP server."],
            ["Behaviour", "Does not change.", "Changes periodically or when reconnecting."],
            ["Assigned by", "Administrator.", "DHCP protocol."],
            ["Used for", "Servers, printers, network devices.", "Home networks, mobile devices."],
        ],
    )
    print("DHCP flow:\n")
    numbered(
        [
            "Device connects to the network.",
            "DHCP assigns an IP address.",
            "Device uses that IP.",
            "Lease expires, so the device renews the same IP or gets a new one.",
        ]
    )


@section("IP Address Classes (Classful Addressing)", "42:46 and 49:15")
def ip_classes():
    label("Definition:", "The original method of dividing IPv4 addresses into classes based on the first octet.")
    table(
        ["Class", "First octet", "Network bits", "Host bits", "Example"],
        [
            ["A", "1 to 126", "8 bits", "24 bits", "10.0.0.0 (16 million hosts)"],
            ["B", "128 to 191", "16 bits", "16 bits", "172.16.0.0 (65,000 hosts)"],
            ["C", "192 to 223", "24 bits", "8 bits", "192.168.0.0 (254 hosts)"],
            ["D", "224 to 239", "Reserved", "Multicast", "224.0.0.0 (group communication)"],
            ["E", "240 to 255", "Reserved", "Experimental", "240.0.0.0 (research only)"],
        ],
    )
    print("Key points:\n")
    bullets(
        [
            "Class A|Large networks (few networks, many hosts).",
            "Class B|Medium networks (balanced).",
            "Class C|Small networks (many networks, few hosts).",
            "Classes D & E|Special use, not for standard addressing.",
            "Instructor underlined|Class A, B, C and their host counts: 16 million, 65,000, 254.",
        ]
    )
    callout(
        "Extra note:",
        "The slide shows Class A as 1 to 126 and Class B starting at 128. The 127.x.x.x block is skipped "
        'because it is reserved for loopback (127.0.0.1, "localhost").',
    )


@section("CIDR Notation", "48:40 and 49:45")
def cidr():
    label("Definition:", "A way to express an IP address and its network size in one line.")
    print("Example: 192.168.1.0/24\n")
    bullets(
        [
            "Network portion|First 24 bits identify the network (e.g. 192.168.1).",
            "Host portion|Last 8 bits identify the device (.0 to .255).",
        ]
    )
    table(
        ["CIDR", "Subnet mask", "Usable hosts"],
        [
            ["/8", "255.0.0.0", "16,777,214"],
            ["/16", "255.255.0.0", "65,534"],
            ["/24", "255.255.255.0", "254"],
            ["/26", "255.255.255.192", "62"],
            ["/30", "255.255.255.252", "2"],
        ],
    )


@section("What is Subnetting?", "53:33")
def subnetting():
    label("Definition:", "Dividing one large network into smaller, manageable pieces.")
    para("Example: one big network 192.168.1.0/24 is split into four /26 subnets, each with 62 usable hosts.")
    table(
        ["Subnet", "Network", "Hosts"],
        [
            ["Subnet A", "192.168.1.0/26", "62"],
            ["Subnet B", "192.168.1.64/26", "62"],
            ["Subnet C", "192.168.1.128/26", "62"],
            ["Subnet D", "192.168.1.192/26", "62"],
        ],
    )


@section("NAT: Network Address Translation", "56:33")
def nat():
    label(
        "Definition:",
        "NAT allows private IP addresses to communicate with the internet by translating them to public IP addresses.",
    )
    print("Path of a request:\n")
    para("Private device (192.168.1.100) -> Router (NAT translation) -> Public IP (203.0.113.45) -> Internet -> Google")
    print("Translation step (at the router):\n")
    bullets(
        [
            "Private IP is replaced with the public IP for outbound traffic.",
            "Response traffic is translated back to the private IP for the device.",
        ]
    )
    print("Why NAT exists:\n")
    bullets(
        [
            "IP address conservation|Reduces the need for public IPs (billions of devices, limited IPv4 addresses).",
            "Security|Hides the internal network structure from the internet.",
            "Network flexibility|Lets private networks operate independently.",
        ]
    )


@section("What is a Protocol and Port?", "1:02:28")
def protocol_and_port():
    bullets(
        [
            "Protocol|Rules and standards for communication between devices. Examples: HTTP, HTTPS, FTP, DNS, SSH, SMTP.",
            'Port|A logical endpoint, or "door", on a device for network communication. '
            "Range 0 to 65535 (65,536 ports in total).",
        ]
    )
    print("Common ports:\n")
    table(
        ["Protocol", "Port"],
        [["HTTP", "80"], ["HTTPS", "443"], ["FTP", "21"], ["SSH", "22"], ["DNS", "53"]],
    )
    table(
        ["Port range", "Category"],
        [
            ["0 to 1023", "Well-known ports"],
            ["1024 to 49151", "Registered ports"],
            ["49152 to 65535", "Dynamic / private ports"],
        ],
    )


@section("OSI Model: All 7 Layers", "1:08:00")
def osi_model():
    table(
        ["Layer", "Name", "Role"],
        [
            ["7", "Application", "User interface and network services."],
            ["6", "Presentation", "Data translation, encryption, compression."],
            ["5", "Session", "Establishes and manages connections."],
            ["4", "Transport", "TCP/UDP, error recovery, flow control."],
            ["3", "Network", "IP addressing and routing packets."],
            ["2", "Data Link", "MAC addressing and framing."],
            ["1", "Physical", "Physical transmission of bits."],
        ],
    )
    note("Instructor note: OSI has 7 layers.")


@section("TCP/IP Model Explained", "1:14:06")
def tcpip_model():
    table(
        ["Layer", "Protocols / role"],
        [
            ["Application Layer", "HTTP, FTP, DNS, SMTP protocols."],
            ["Transport Layer", "TCP, UDP for reliable data delivery."],
            ["Internet Layer", "IP, ICMP, ARP for addressing and routing."],
            ["Network Access Layer", "Physical hardware and data link protocols."],
        ],
    )


@section("OSI vs TCP/IP Comparison", "1:15:20")
def osi_vs_tcpip():
    table(
        ["OSI model", "TCP/IP model", "Examples"],
        [
            ["7 Application, 6 Presentation, 5 Session", "Application", "HTTP, DNS, FTP, SMTP"],
            ["4 Transport", "Transport", "TCP, UDP"],
            ["3 Network", "Internet", "IP, ICMP"],
            ["2 Data Link, 1 Physical", "Network Access", "Ethernet, ARP, MAC"],
        ],
    )
    callout(
        "Key idea:",
        "The TCP/IP model consolidates OSI's top three layers into a single Application layer "
        "and combines the bottom two into the Network Access layer.",
    )


@section("Data Encapsulation & Decapsulation", "1:16:00")
def encapsulation():
    table(
        ["Step", "Data unit", "What happens"],
        [
            ["1", "Data", "Created at the Application layer."],
            ["2", "Segment", "Transport layer adds a TCP/UDP header."],
            ["3", "Packet", "Network layer adds an IP header."],
            ["4", "Frame", "Data Link layer adds MAC addresses."],
            ["5", "Bits", "Physical layer transmits signals."],
        ],
    )
    callout(
        "Summary:",
        "Encapsulation wraps data with headers at each layer as it goes down. "
        "Decapsulation reverses the process when receiving.",
    )


@section("TCP vs UDP Comparison", "1:17:30")
def tcp_vs_udp():
    table(
        ["Feature", "TCP", "UDP"],
        [
            ["Connection", "Connection-oriented", "Connectionless"],
            ["Speed", "Slower (reliable)", "Faster (no overhead)"],
            ["Reliability", "Guaranteed delivery", "No guarantee"],
            ["Error checking", "Yes, extensive", "Minimal"],
            ["Ordering", "Maintains packet order", "No ordering"],
            ["Use case", "Web, Email, File Transfer", "Gaming, Streaming, DNS"],
        ],
    )
    print("Key differences:\n")
    bullets(
        [
            "TCP|Reliable, ordered, connection-based.",
            "UDP|Fast, connectionless, best-effort.",
        ]
    )
    callout("Remember:", "TCP = Web / File Transfer  |  UDP = Gaming / Streaming / DNS")


@section("TCP 3-Way Handshake (Connection Establishment)", "1:21:41")
def three_way_handshake():
    label("Definition:", "Establishes a reliable TCP connection between two devices.")
    table(
        ["Step", "Direction", "Message"],
        [
            ["1", "Client -> SYN -> Server", '"I want to connect" (SYN packet sent).'],
            ["2", "Server -> SYN-ACK -> Client", '"Acknowledged, you may connect" (server responds with SYN-ACK).'],
            ["3", "Client -> ACK -> Server", '"Connected" (client sends the final ACK).'],
        ],
    )
    callout("Final status:", '"Connection Established"')


@section("TCP 4-Way Handshake (Connection Termination)", "1:25:27")
def four_way_handshake():
    label("Definition:", "Gracefully terminates a TCP connection between two devices.")
    table(
        ["Step", "Direction", "Message"],
        [
            ["1", "Client -> FIN -> Server", '"I\'m done sending data" (FIN packet sent).'],
            ["2", "Server -> ACK -> Client", '"Got it, I acknowledge" (server sends ACK).'],
            ["3", "Server -> FIN -> Client", '"I\'m done too" (server sends its own FIN).'],
            ["4", "Client -> ACK -> Server", '"Confirmed, connection closed" (client sends the final ACK).'],
        ],
    )
    callout("Final status:", '"Connection Closed"')


@section("Real-World Example: Opening Google.com", "1:27:38")
def opening_google():
    para("Flow: Browser (google.com) -> DNS -> TCP 3-way handshake -> HTTP GET -> google.com")
    table(
        ["Stage", "What happens"],
        [
            ["1. DNS query sent", "Browser requests the IP address for google.com."],
            ["2. DNS response received", "IP address is returned to the browser."],
            ["3. TCP handshake", "SYN, SYN-ACK and ACK packets establish the connection."],
            ["4. HTTP request sent", "GET request for the webpage content."],
            ["5. Server processes request", "Web server handles the request and retrieves the data."],
        ],
    )


@section("Common TCP Flags", "1:27:43")
def tcp_flags():
    para("TCP flags control the state and behavior of communication.")
    table(
        ["Flag", "Meaning"],
        [
            ["SYN", "Initiates a new connection (synchronization)."],
            ["ACK", "Acknowledges receipt of data or packets."],
            ["FIN", "Gracefully closes a connection."],
            ["RST", "Forces an immediate connection reset."],
            ["PSH", "Pushes data immediately without buffering."],
            ["URG", "Marks data as urgent and high priority."],
        ],
    )
    callout("Note:", "TCP flags are used in Nmap scans, port scanning, firewall evasion and TCP manipulation attacks.")


@section("Common Protocols Quick Reference", "1:29:39")
def protocols_quick_reference():
    table(
        ["Protocol", "Port", "Purpose"],
        [
            ["HTTP", "80", "Unencrypted web traffic"],
            ["HTTPS", "443", "Encrypted web traffic (SSL/TLS)"],
            ["FTP", "21", "File transfer (unencrypted)"],
            ["SFTP", "22", "Secure file transfer (SSH)"],
            ["SSH", "22", "Secure shell, remote access"],
            ["Telnet", "23", "Remote access (unencrypted, deprecated)"],
            ["DNS", "53", "Domain name resolution"],
            ["DHCP", "67-68", "Dynamic IP assignment"],
            ["SMTP", "25", "Send email"],
            ["POP3", "110", "Receive email (older)"],
            ["IMAP", "143", "Receive email (modern)"],
            ["RDP", "3389", "Remote desktop (Windows)"],
        ],
    )
    callout("Important:", "Memorizing ports is essential for CTFs, pentesting and network security assessments.")


@section("Encryption & Decryption Process", "1:37:30")
def encryption():
    label("Definition:", "Converting plaintext into ciphertext (encryption) and back (decryption) using cryptographic keys.")
    table(
        ["", "Encryption", "Decryption"],
        [
            ["Step 1", "Plaintext (readable data) + encryption key.", "Ciphertext (encrypted data) + decryption key."],
            ["Step 2", "Encryption algorithm (AES, RSA, DES).", "Decryption algorithm (reverse of encryption)."],
            ["Step 3", "Ciphertext (unreadable, scrambled data).", "Plaintext (original readable data)."],
            ["Result", "Data is now secure and unreadable without the key.", "Data is recovered and readable again."],
        ],
    )
    note('Instructor sketch: a sender types "Hi" (plain), it is encrypted into cipher text, '
         "travels across the network, and is decrypted at the receiver.")
    print("Key encryption types:\n")
    table(
        ["", "Symmetric", "Asymmetric"],
        [
            ["Keys", "Same key for encryption and decryption (AES, DES).", "Different keys, public and private (RSA, ECC)."],
            ["Speed / security", "Fast and efficient.", "Slower but more secure."],
            ["Key handling", "Key must be shared securely.", "Public key encrypts, private key decrypts."],
            ["Used for", "Bulk data.", "Key exchange and digital signatures."],
        ],
    )


@section("DNS: How Domain Resolution Works", "1:42:15")
def dns():
    label("Definition:", "Translates human-readable domain names into IP addresses.")
    numbered(
        [
            "User types google.com in the browser.",
            "Query is sent to the Recursive Resolver (ISP DNS).",
            "Resolver queries the Root Nameserver.",
            "Root directs it to the TLD server (.com).",
            "TLD server directs it to the Authoritative Nameserver.",
            "Authoritative server returns the IP address (142.250.185.46).",
            "Browser connects to the IP and loads the website.",
        ]
    )


@section("ARP: Address Resolution Protocol", "1:46:09 to 1:48:31")
def arp():
    label("Definition:", "Maps IP addresses to MAC addresses on a local network.")
    table(
        ["Step", "What happens"],
        [
            ["1", "Device A wants to reach 192.168.1.5. It has the IP but needs the MAC address."],
            ["2", 'Broadcasts an ARP request: "Who has 192.168.1.5?" Sent to all devices on the local network (broadcast).'],
            ["3", 'Device B replies: "I do. MAC: XX:XX:XX:XX:XX:XX". Device B sends an ARP reply with its MAC address.'],
            ["4", "Device A stores the result in its ARP cache (caches the IP-to-MAC mapping for future use)."],
            ["5", "Communication begins using the MAC address. Devices can now communicate on the local network."],
        ],
    )
    callout("Instructor summary:", "ARP works inside a LAN and converts IP -> MAC.")


@section("ICMP: Ping & Traceroute", "1:48:42")
def icmp():
    label("Full form:", "Internet Control Message Protocol.")
    para("ICMP handles diagnostics, error reporting and network troubleshooting. Typical messages:")
    bullets(
        [
            "Address not found.",
            "Packet expired in transit.",
            "Are you there? (Ping)",
            "Yes, I'm here! (ICMP echo reply)",
        ]
    )
    para("Ping flow: Echo Request -> Target -> Echo Reply")
    bullets(
        [
            "Measures|Round-Trip Time (RTT) in milliseconds.",
            "Use|Check if a host is reachable, measure latency.",
            "Example|ping google.com -> 25ms response.",
        ]
    )


@section("HTTP Request & Response Cycle", "1:49:56")
def http_cycle():
    label("Definition:", "HTTP is the protocol used to transfer data between browser and server.")
    numbered(
        [
            "User enters a URL in the browser.",
            "Browser sends an HTTP request to the server.",
            "Server processes the request.",
            "Server sends back an HTTP response.",
            "Browser renders the page.",
        ]
    )
    table(
        ["HTTP request contains", "HTTP response contains"],
        [
            ["Method (GET, POST, etc.)", "Status code (200, 404, 500, etc.)"],
            ["URL / Path", "Headers (Set-Cookie, Content-Type)"],
            ["Headers (Host, User-Agent, Cookie)", "Body (HTML, JSON, etc.)"],
            ["Body (optional, for POST/PUT)", ""],
        ],
    )


@section("HTTP Methods & Headers", "1:52:17")
def http_methods():
    table(
        ["Method", "Purpose", "Hacker relevance"],
        [
            ["GET", "Fetch data from server", "Parameter tampering, URL manipulation"],
            ["POST", "Send data to server", "SQLi, login brute force, form injection"],
            ["PUT", "Update existing resource", "Unauthorized file upload, resource overwrite"],
            ["DELETE", "Remove resource", "Unauthorized deletion, data destruction"],
            ["PATCH", "Partial update to resource", "Privilege escalation, partial data modification"],
            ["OPTIONS", "Check allowed methods", "Recon, discover available endpoints"],
        ],
    )
    table(
        ["Request headers", "Response headers"],
        [
            ["Host", "Set-Cookie"],
            ["User-Agent", "Server"],
            ["Cookie", "Content-Type"],
            ["Authorization", "X-Frame-Options"],
            ["Content-Type", "Access-Control-Allow-Origin (CORS)"],
            ["Referer", "Cache-Control"],
        ],
    )


@section("HTTP Status Codes", "1:54:48")
def http_status_codes():
    para("Status codes tell you what happened with your request.")
    table(
        ["Range", "Meaning", "Examples"],
        [
            ["1xx", "Informational", "100 Continue, 101 Switching Protocols"],
            ["2xx", "Success", "200 OK, 201 Created, 204 No Content"],
            ["3xx", "Redirection", "301 Moved Permanently, 302 Found, 304 Not Modified"],
            ["4xx", "Client error", "400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found"],
            ["5xx", "Server error", "500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable"],
        ],
    )
    print("Key status codes breakdown:\n")
    table(
        ["Code", "Meaning"],
        [
            ["200 OK", "Request succeeded."],
            ["201 Created", "Resource created successfully."],
            ["301 / 302", "Redirect to a new location."],
            ["400 Bad Request", "Malformed request."],
            ["401 Unauthorized", "Authentication required."],
            ["403 Forbidden", "Access denied (found but blocked)."],
            ["404 Not Found", "Resource doesn't exist."],
            ["500 Internal Server Error", "Server misconfiguration or crash."],
            ["503 Service Unavailable", "Server overloaded."],
        ],
    )


@section("HTTPS & TLS Handshake", "1:56:30")
def https_tls():
    label("Definition:", "HTTPS = HTTP + TLS encryption layer for secure communication. (Instructor note: HTTP + SSL / TLS.)")
    print("TLS handshake steps:\n")
    numbered(
        [
            'Client sends "Hello" with its supported TLS versions and ciphers.',
            'Server replies "Hello" with the chosen cipher and its SSL certificate.',
            "Client verifies the certificate (checks the CA trust chain).",
            "Client generates a session key and encrypts it with the server's public key.",
            "Server decrypts the session key with its private key.",
            "Both sides confirm, and the encrypted tunnel is established.",
            "HTTP data flows securely inside the encrypted tunnel.",
        ]
    )
    table(
        ["HTTP (unencrypted)", "HTTPS (encrypted)"],
        [
            ["Plain text communication", "TLS/SSL encryption"],
            ["Easily interceptable", "Requires a certificate"],
            ["No authentication", "Mutual authentication"],
            ["Vulnerable to MITM attacks", "Protected from MITM (if properly implemented)"],
        ],
    )


@section("VPN: Virtual Private Network", "1:58:12")
def vpn():
    label("Definition:", "A VPN creates an encrypted tunnel between your device and the internet.")
    numbered(
        [
            "User connects to the VPN client.",
            "Traffic is encrypted on the device.",
            "Traffic is sent to the VPN server.",
            "VPN server decrypts it and forwards it to the internet.",
            "Response returns through the same encrypted tunnel.",
        ]
    )


@section("Proxy Servers", "2:00:30")
def proxy_servers():
    label("Definition:", "A proxy sits between your device and the internet, forwarding requests on your behalf.")
    table(
        ["", "Forward proxy", "Reverse proxy", "Transparent proxy"],
        [
            ["Side", "Client side proxy", "Server side proxy", "Intercepts without the user knowing"],
            ["Hides", "Hides the user from the internet", "Hides the server from the client", "Transparent to the user"],
            ["Used for", "Anonymity and filtering", "Load balancing and WAF", "Corporate networks"],
            ["Example", "Corporate proxy", "Cloudflare, Nginx", "ISP monitoring"],
        ],
    )
    print("Simple flow comparison:\n")
    bullets(
        [
            "With proxy|Device -> Proxy -> Internet",
            "Without proxy|Device -> Internet",
        ]
    )


@section("Tor: The Onion Router", "2:02:53")
def tor():
    label(
        "Definition:",
        "Tor anonymizes traffic by routing it through multiple encrypted relay nodes. "
        "(Instructor note: Tor Browser is used to reach the Dark Web, .onion sites.)",
    )
    numbered(
        [
            "User opens the Tor browser.",
            "Traffic is encrypted in 3 layers (like an onion).",
            "Sent to the Entry Node (knows your IP, not the destination).",
            "Passed to the Middle Node (knows nothing).",
            "Exit Node decrypts the final layer and connects to the destination.",
            "Destination sees the Exit Node IP, not your real IP.",
        ]
    )
    table(
        ["Tor characteristics", "Security risks"],
        [
            ["Highly anonymous", "Exit node traffic is unencrypted"],
            ["Slow due to multiple hops", "Exit node can be monitored"],
            ["Decentralized network", "Timing attacks possible"],
            ["Free to use", "Correlation attacks"],
        ],
    )


# ---------------------------------------------------------------------------
# Rendering and command line
# ---------------------------------------------------------------------------
def render(number):
    """Return the text of one section (1-based number)."""
    title, time, fn = SECTIONS[number - 1]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        stamp = f"  [{time}]" if time else ""
        heading = f"{number}. {title}{stamp}"
        print("=" * WIDTH)
        print(heading)
        print("=" * WIDTH)
        print()
        fn()
    return buf.getvalue()


def banner():
    return (
        "=" * WIDTH
        + LOGO
        + "\nComputer Networking Notes\n"
        + "Beginner to Advanced (Cybersecurity Focus)\n"
        + "Created by Rashida Kathiriya\n"
        + "=" * WIDTH
        + "\n"
    )


def list_sections():
    for i, (title, time, _) in enumerate(SECTIONS, 1):
        print(f"{i:>2}. {title}" + (f"  [{time}]" if time else ""))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Computer Networking Notes, created by Rashida Kathiriya.")
    parser.add_argument("numbers", nargs="*", type=int, help="section numbers to print (default: all)")
    parser.add_argument("--list", action="store_true", help="list all sections")
    parser.add_argument("--search", metavar="WORD", help="show sections that mention WORD")
    parser.add_argument("--out", metavar="FILE", help="write the output to a text file")
    args = parser.parse_args(argv)

    if args.list:
        list_sections()
        return 0

    if args.search:
        word = args.search.lower()
        wanted = [i for i in range(1, len(SECTIONS) + 1) if word in render(i).lower()]
        if not wanted:
            print(f'No section mentions "{args.search}".')
            return 1
    elif args.numbers:
        bad = [n for n in args.numbers if not 1 <= n <= len(SECTIONS)]
        if bad:
            print(f"Section numbers must be between 1 and {len(SECTIONS)}.", file=sys.stderr)
            return 2
        wanted = args.numbers
    else:
        wanted = list(range(1, len(SECTIONS) + 1))

    text = banner() + "\n" + "\n".join(render(i) for i in wanted)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved {len(wanted)} section(s) to {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
