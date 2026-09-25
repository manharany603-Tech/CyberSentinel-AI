# ============================================================
# 🛡️ CYBERSENTINEL AI — MK
# All-in-One Cyber Security Toolkit
# Single File GUI Version
# ============================================================

import re
import os
import socket
import hashlib
import threading
import ssl
import datetime as dt
import urllib.request
import urllib.error
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox


# ============================================================
# CONFIGURATION
# ============================================================

APP_NAME = "CYBERSENTINEL AI — MK"

BG = "#0b1220"
FG = "#e5e7eb"
ACCENT = "#00e5ff"
GREEN = "#00ff88"
RED = "#ff4d4d"
YELLOW = "#ffd166"
CARD = "#111827"

VT_API_KEY = ""


# ============================================================
# SECURITY DATA
# ============================================================

SUSPICIOUS_KEYWORDS = [
    "login",
    "verify",
    "verification",
    "account",
    "secure",
    "update",
    "confirm",
    "password",
    "bank",
    "wallet",
    "payment",
    "signin",
    "security"
]

URL_SHORTENERS = [
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "is.gd",
    "ow.ly",
    "buff.ly"
]

KNOWN_BRANDS = [
    "paypal",
    "google",
    "microsoft",
    "apple",
    "amazon",
    "facebook",
    "instagram",
    "netflix",
    "bank"
]

KNOWN_BAD_MD5 = {
    "d41d8cd98f00b204e9800998ecf8427e",
    "098f6bcd4621d373cade4e832627b4f6"
}

COMMON_PORTS = [
    21, 22, 23, 25, 53,
    80, 110, 135, 139, 143,
    443, 445, 3389, 8080
]


# ============================================================
# MAIN APPLICATION
# ============================================================

class CyberSentinel(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.geometry("780x600")
        self.minsize(780, 600)
        self.configure(bg=BG)

        self.setup_style()
        self.build_header()
        self.build_notebook()

        # Existing tabs
        self.tab_url()
        self.tab_password()
        self.tab_ports()
        self.tab_file()
        self.tab_logs()

        # Added tabs
        self.tab_ssl()
        self.tab_headers()
        self.tab_email()
        self.tab_breach()


    # ========================================================
    # STYLE
    # ========================================================

    def setup_style(self):

        style = ttk.Style(self)

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "TNotebook",
            background=BG,
            borderwidth=0
        )

        style.configure(
            "TNotebook.Tab",
            background="#172033",
            foreground=FG,
            padding=[12, 8],
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "TNotebook.Tab",
            background=[
                ("selected", "#123044")
            ],
            foreground=[
                ("selected", ACCENT)
            ]
        )

        style.configure(
            "TButton",
            background="#172033",
            foreground=FG,
            padding=7,
            font=("Segoe UI", 9, "bold")
        )

        style.map(
            "TButton",
            background=[
                ("active", "#1e4054")
            ],
            foreground=[
                ("active", ACCENT)
            ]
        )


    # ========================================================
    # HEADER
    # ========================================================

    def build_header(self):

        header = tk.Frame(
            self,
            bg=BG,
            height=75
        )

        header.pack(
            fill="x",
            padx=15,
            pady=(10, 0)
        )

        title = tk.Label(
            header,
            text="🛡️ CYBERSENTINEL AI — MK",
            bg=BG,
            fg=ACCENT,
            font=("Segoe UI", 22, "bold")
        )

        title.pack(anchor="w")

        subtitle = tk.Label(
            header,
            text="All-in-One Cyber Security Toolkit",
            bg=BG,
            fg=FG,
            font=("Segoe UI", 10)
        )

        subtitle.pack(anchor="w", pady=(2, 0))


    # ========================================================
    # NOTEBOOK
    # ========================================================

    def build_notebook(self):

        self.notebook = ttk.Notebook(self)

        self.notebook.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=10
        )


    # ========================================================
    # COMMON TAB FUNCTIONS
    # ========================================================

    def create_tab(self, name):

        frame = tk.Frame(
            self.notebook,
            bg=BG
        )

        self.notebook.add(
            frame,
            text=name
        )

        return frame


    def output_box(self, parent):

        box = scrolledtext.ScrolledText(
            parent,
            height=18,
            bg="#050b14",
            fg=FG,
            insertbackground=ACCENT,
            font=("Consolas", 10),
            relief="flat",
            borderwidth=1
        )

        box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        return box


    def log(self, box, text):

        def update():
            box.insert(
                tk.END,
                text + "\n"
            )
            box.see(tk.END)

        self.after(0, update)


    def run_bg(self, func):

        thread = threading.Thread(
            target=func,
            daemon=True
        )

        thread.start()


    # ========================================================
    # TAB 1 — URL PHISHING
    # ========================================================

    def tab_url(self):

        tab = self.create_tab("URL Phishing")

        tk.Label(
            tab,
            text="🔎 URL Phishing Detector",
            bg=BG,
            fg=ACCENT,
            font=("Segoe UI", 15, "bold")
        ).pack(
            pady=(12, 5)
        )

        tk.Label(
            tab,
            text="Enter a URL to perform a basic phishing-risk analysis.",
            bg=BG,
            fg=FG
        ).pack()

        entry = tk.Entry(
            tab,
            bg="#111827",
            fg=FG,
            insertbackground=ACCENT,
            font=("Segoe UI", 11)
        )

        entry.pack(
            fill="x",
            padx=15,
            pady=10
        )

        output = self.output_box(tab)

        def check_url():

            url = entry.get().strip()

            if not url:
                messagebox.showwarning(
                    "Input Required",
                    "Please enter a URL."
                )
                return

            def worker():

                score = 0
                reasons = []

                low = url.lower()

                if not low.startswith(("http://", "https://")):
                    score += 2
                    reasons.append(
                        "URL does not start with HTTP/HTTPS."
                    )

                for keyword in SUSPICIOUS_KEYWORDS:

                    if keyword in low:
                        score += 1
                        reasons.append(
                            f"Suspicious keyword found: {keyword}"
                        )

                for shortener in URL_SHORTENERS:

                    if shortener in low:
                        score += 3
                        reasons.append(
                            f"URL shortener detected: {shortener}"
                        )

                for brand in KNOWN_BRANDS:

                    if brand in low:
                        score += 1
                        reasons.append(
                            f"Brand-related keyword found: {brand}"
                        )

                if "@" in url:
                    score += 3
                    reasons.append(
                        "URL contains @ character."
                    )

                if len(url) > 100:
                    score += 2
                    reasons.append(
                        "Unusually long URL."
                    )

                self.log(
                    output,
                    "\n========== URL ANALYSIS =========="
                )

                self.log(
                    output,
                    f"URL: {url}"
                )

                self.log(
                    output,
                    f"Risk Score: {score}"
                )

                if score >= 7:

                    self.log(
                        output,
                        "⚠ HIGH RISK / SUSPICIOUS"
                    )

                elif score >= 3:

                    self.log(
                        output,
                        "⚠ MEDIUM RISK"

                    )

                else:

                    self.log(
                        output,
                        "✓ LOW RISK"
                    )

                if reasons:

                    self.log(
                        output,
                        "\nReasons:"
                    )

                    for reason in reasons:

                        self.log(
                            output,
                            "• " + reason
                        )

                else:

                    self.log(
                        output,
                        "No obvious heuristic indicators found."
                    )

            self.run_bg(worker)


        tk.Button(
            tab,
            text="Analyze URL",
            command=check_url,
            bg="#172033",
            fg=ACCENT,
            activebackground="#1e4054",
            activeforeground=ACCENT
        ).pack(
            pady=5
        )


    # ========================================================
    # TAB 2 — PASSWORD SECURITY
    # ========================================================

    def tab_password(self):

        tab = self.create_tab("Password Security")

        tk.Label(
            tab,
            text="🔐 Password Strength Checker",
            bg=BG,
            fg=ACCENT,
            font=("Segoe UI", 15, "bold")
        ).pack(
            pady=(12, 8)
        )

        entry = tk.Entry(
            tab,
            show="*",
            bg="#111827",
            fg=FG,
            insertbackground=ACCENT,
            font=("Segoe UI", 11)
        )

        entry.pack(
            fill="x",
            padx=15,
            pady=10
        )

        output = self.output_box(tab)

        def check_password():

            password = entry.get()

            if not password:

                messagebox.showwarning(
                    "Input Required",
                    "Enter a password."
                )

                return

            score = 0
            reasons = []

            if len(password) >= 8:
                score += 2
            else:
                reasons.append(
                    "Use at least 8 characters."
                )

            if len(password) >= 12:
                score += 1

            if re.search(r"[A-Z]", password):
                score += 1
            else:
                reasons.append(
                    "Add uppercase letters."
                )

            if re.search(r"[a-z]", password):
                score += 1
            else:
                reasons.append(
                    "Add lowercase letters."
                )

            if re.search(r"\d", password):
                score += 1
            else:
                reasons.append(
                    "Add numbers."
                )

            if re.search(r"[^A-Za-z0-9]", password):
                score += 1
            else:
                reasons.append(
                    "Add special characters."
                )

            output.delete(
                "1.0",
                tk.END
            )

            output.insert(
                tk.END,
                "========== PASSWORD SECURITY ==========\n\n"
            )

            output.insert(
                tk.END,
                f"Score: {score}/7\n"
            )

            if score >= 6:

                output.insert(
                    tk.END,
                    "✓ Strong Password\n"
                )

            elif score >= 4:

                output.insert(
                    tk.END,
                    "⚠ Medium Password\n"
                )

            else:

                output.insert(
                    tk.END,
                    "⚠ Weak Password\n"
                )

            if reasons:

                output.insert(
                    tk.END,
                    "\nRecommendations:\n"
                )

                for r in reasons:

                    output.insert(
                        tk.END,
                        "• " + r + "\n"
                    )

        tk.Button(
            tab,
            text="Check Password",
            command=check_password,
            bg="#172033",
            fg=ACCENT
        ).pack(
            pady=5
        )


    # ========================================================
    # TAB 3 — PORT SCANNER
    # ========================================================

    def tab_ports(self):

        tab = self.create_tab("Port Scanner")

        tk.Label(
            tab,
            text="🌐 Port Scanner",
            bg=BG,
            fg=ACCENT,
            font=("Segoe UI", 15, "bold")
        ).pack(
            pady=(12, 5)
        )

        tk.Label(
            tab,
            text="Use only on systems you own or are authorized to test.",
            bg=BG,
            fg=YELLOW
        ).pack()

        entry = tk.Entry(
            tab,
            bg="#111827",
            fg=FG,
            insertbackground=ACCENT
        )

        entry.pack(
            fill="x",
            padx=15,
            pady=10
        )

        output = self.output_box(tab)

        def scan():

            host = entry.get().strip()

            if not host:

                messagebox.showwarning(
                    "Input Required",
                    "Enter a hostname or IP address."
                )

                return

            def worker():

                output_text = f"""
========== PORT SCAN ==========
Target: {host}

"""

                self.log(
                    output,
                    output_text
                )

                try:

                    ip = socket.gethostbyname(host)

                    self.log(
                        output,
                        f"Resolved IP: {ip}\n"
                    )

                except Exception as e:

                    self.log(
                        output,
                        f"DNS Error: {e}"
                    )

                    return

                for port in COMMON_PORTS:

                    try:

                        sock = socket.socket(
                            socket.AF_INET,
                            socket.SOCK_STREAM
                        )

                        sock.settimeout(0.5)

                        result = sock.connect_ex(
                            (host, port)
                        )

                        sock.close()

                        if result == 0:

                            self.log(
                                output,
                                f"[OPEN] Port {port}"
                            )

                        else:

                            self.log(
                                output,
                                f"[CLOSED] Port {port}"
                            )

                    except Exception as e:

                        self.log(
                            output,
                            f"Port {port}: {e}"
                        )

            self.run_bg(worker)


        tk.Button(
            tab,
            text="Start Scan",
            command=scan,
            bg="#172033",
            fg=ACCENT
        ).pack(
            pady=5
        )


    # ========================================================
    # TAB 4 — FILE SCANNER
    # ========================================================

    def tab_file(self):

        tab = self.create_tab("File Scanner")

        tk.Label(
            tab,
            text="📁 File Malware Hash Scanner",
            bg=BG,
            fg=ACCENT,
            font=("Segoe UI", 15, "bold")
        ).pack(
            pady=(12, 10)
        )

        output = self.output_box(tab)

        def scan_file():

            path = filedialog.askopenfilename()

            if not path:
                return

            try:

                md5 = hashlib.md5()

                with open(
                    path,
                    "rb"
                ) as f:

                    for chunk in iter(
                        lambda: f.read(4096),
                        b""
                    ):

                        md5.update(chunk)

                file_hash = md5.hexdigest()

                output.delete(
                    "1.0",
                    tk.END
                )

                output.insert(
                    tk.END,
                    "========== FILE SCAN ==========\n\n"
                )

                output.insert(
                    tk.END,
                    f"File: {path}\n\n"
                )

                output.insert(
                    tk.END,
                    f"MD5: {file_hash}\n\n"
                )

                if file_hash in KNOWN_BAD_MD5:

                    output.insert(
                        tk.END,
                        "⚠ Known suspicious hash detected.\n"
                    )

                else:

                    output.insert(
                        tk.END,
                        "✓ Hash not found in local test database.\n"
                    )

            except Exception as e:

                messagebox.showerror(
                    "File Error",
                    str(e)
                )


        tk.Button(
            tab,
            text="Select & Scan File",
            command=scan_file,
            bg="#172033",
            fg=ACCENT
        ).pack(
            pady=10
        )


    # ========================================================
    # TAB 5 — LOG ANALYZER
    # ========================================================

    def tab_logs(self):

        tab = self.create_tab("Log Analyzer")

        tk.Label(
            tab,
            text="📊 Security Log Analyzer",
            bg=BG,
            fg=ACCENT,
            font=("Segoe UI", 15, "bold")
        ).pack(
            pady=(12, 8)
        )

        text = scrolledtext.ScrolledText(
            tab,
            height=12,
            bg="#111827",
            fg=FG,
            insertbackground=ACCENT
        )

        text.pack(
            fill="both",
            expand=False,
            padx=10,
            pady=10
        )

        output = self.output_box(tab)

        def analyze():

            logs = text.get(
                "1.0",
                tk.END
            )

            output.delete(
                "1.0",
                tk.END
            )

            patterns = {

                "Failed Login":
                    r"failed login|authentication failed|login failed",

                "SQL Injection":
                    r"union select|or 1=1|sql injection",

                "XSS":
                    r"<script|javascript:|xss",

                "Brute Force":
                    r"brute force|too many attempts"

            }

            output.insert(
                tk.END,
                "========== LOG ANALYSIS ==========\n\n"
            )

            found = False

            for name, pattern in patterns.items():

                matches = re.findall(
                    pattern,
                    logs,
                    re.I
                )

                if matches:

                    found = True

                    output.insert(
                        tk.END,
                        f"⚠ {name}: {len(matches)} indicator(s)\n"
                    )

            if not found:

                output.insert(
                    tk.END,
                    "✓ No matching indicators found.\n"
                )


        tk.Button(
            tab,
            text="Analyze Logs",
            command=analyze,
            bg="#172033",
            fg=ACCENT
        ).pack(
            pady=5
        )


    # ========================================================
    # TAB 6 — SSL CHECKER
    # ========================================================

    def tab_ssl(self):

        tab = self.create_tab("SSL Checker")

        tk.Label(
            tab,
            text="🔒 SSL Certificate Checker",
            bg=BG,
            fg=ACCENT,
            font=("Segoe UI", 15, "bold")
        ).pack(
            pady=(12, 5)
        )

        tk.Label(
            tab,
            text="Check HTTPS certificate information and expiry.",
            bg=BG,
            fg=FG
        ).pack()

        entry = tk.Entry(
            tab,
            bg="#111827",
            fg=FG,
            insertbackground=ACCENT
        )

        entry.pack(
            fill="x",
            padx=15,
            pady=10
        )

        output = self.output_box(tab)

        def check_ssl():

            domain = entry.get().strip()

            domain = re.sub(
                r"^https?://",
                "",
                domain,
                flags=re.I
            )

            domain = domain.split("/")[0]

            if not domain:

                messagebox.showwarning(
                    "Input Required",
                    "Enter a domain."
                )

                return

            def worker():

                self.log(
                    output,
                    "\n========== SSL CHECK =========="
                )

                self.log(
                    output,
                    f"Domain: {domain}"
                )

                try:

                    context = ssl.create_default_context()

                    with socket.create_connection(
                        (domain, 443),
                        timeout=8
                    ) as sock:

                        with context.wrap_socket(
                            sock,
                            server_hostname=domain
                        ) as secure_sock:

                            cert = secure_sock.getpeercert()

                    subject = dict(
                        x[0] for x in cert.get(
                            "subject",
                            []
                        )
                    )

                    issuer = dict(
                        x[0] for x in cert.get(
                            "issuer",
                            []
                        )
                    )

                    self.log(
                        output,
                        f"Subject: {subject.get('commonName', 'N/A')}"
                    )

                    self.log(
                        output,
                        f"Issuer: {issuer.get('commonName', 'N/A')}"
                    )

                    expiry = cert.get(
                        "notAfter",
                        "N/A"
                    )

                    self.log(
                        output,
                        f"Expiry: {expiry}"
                    )

                    if expiry != "N/A":

                        expiry_date = dt.datetime.strptime(
                            expiry,
                            "%b %d %H:%M:%S %Y %Z"
                        )

                        days = (
                            expiry_date -
                            dt.datetime.utcnow()
                        ).days

                        self.log(
                            output,
                            f"Days Remaining: {days}"
                        )

                        if days < 0:

                            self.log(
                                output,
                                "⚠ CERTIFICATE EXPIRED"
                            )

                        elif days < 30:

                            self.log(
                                output,
                                "⚠ Certificate expires soon."
                            )

                        else:

                            self.log(
                                output,
                                "✓ Certificate appears valid."
                            )

                except Exception as e:

                    self.log(
                        output,
                        f"SSL Error: {e}"
                    )

            self.run_bg(worker)


        tk.Button(
            tab,
            text="Check SSL",
            command=check_ssl,
            bg="#172033",
            fg=ACCENT
        ).pack(
            pady=5
        )


    # ========================================================
    # TAB 7 — WEB SECURITY HEADERS
    # ========================================================

    def tab_headers(self):

        tab = self.create_tab(
            "Web Security Headers"
        )

        tk.Label(
            tab,
            text="🛡️ Web Security Headers Checker",
            bg=BG,
            fg=ACCENT,
            font=("Segoe UI", 15, "bold")
        ).pack(
            pady=(12, 5)
        )

        tk.Label(
            tab,
            text="Check common defensive HTTP security headers.",
            bg=BG,
            fg=FG
        ).pack()

        entry = tk.Entry(
            tab,
            bg="#111827",
            fg=FG,
            insertbackground=ACCENT
        )

        entry.pack(
            fill="x",
            padx=15,
            pady=10
        )

        output = self.output_box(tab)

        required_headers = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Referrer-Policy"
        ]

        def check_headers():

            url = entry.get().strip()

            if not url:

                messagebox.showwarning(
                    "Input Required",
                    "Enter a website URL."
                )

                return

            if not url.startswith(
                ("http://", "https://")
            ):

                url = "https://" + url

            def worker():

                self.log(
                    output,
                    "\n========== WEB SECURITY HEADERS =========="
                )

                self.log(
                    output,
                    f"URL: {url}\n"
                )

                try:

                    request = urllib.request.Request(
                        url,
                        headers={
                            "User-Agent":
                            "CyberSentinelAI-MK-Security-Checker"
                        }
                    )

                    with urllib.request.urlopen(
                        request,
                        timeout=10
                    ) as response:

                        headers = {
                            k.lower(): v
                            for k, v in response.headers.items()
                        }

                    score = 0

                    for header in required_headers:

                        if header.lower() in headers:

                            score += 20

                            self.log(
                                output,
                                f"✓ {header}: PRESENT"
                            )

                        else:

                            self.log(
                                output,
                                f"⚠ {header}: MISSING"
                            )

                    self.log(
                        output,
                        f"\nSecurity Header Score: {score}/100"
                    )

                except Exception as e:

                    self.log(
                        output,
                        f"Header Check Error: {e}"
                    )

            self.run_bg(worker)


        tk.Button(
            tab,
            text="Check Headers",
            command=check_headers,
            bg="#172033",
            fg=ACCENT
        ).pack(
            pady=5
        )


    # ========================================================
    # TAB 8 — EMAIL HEADER ANALYZER
    # ========================================================

    def tab_email(self):

        tab = self.create_tab(
            "Email Header Analyzer"
        )

        tk.Label(
            tab,
            text="📧 Email Header Analyzer",
            bg=BG,
            fg=ACCENT,
            font=("Segoe UI", 15, "bold")
        ).pack(
            pady=(12, 5)
        )

        tk.Label(
            tab,
            text="Paste raw email headers for defensive analysis.",
            bg=BG,
            fg=FG
        ).pack()

        text = scrolledtext.ScrolledText(
            tab,
            height=10,
            bg="#111827",
            fg=FG,
            insertbackground=ACCENT
        )

        text.pack(
            fill="both",
            expand=False,
            padx=10,
            pady=10
        )

        output = self.output_box(tab)

        def analyze_email():

            raw = text.get(
                "1.0",
                tk.END
            )

            if not raw.strip():

                messagebox.showwarning(
                    "Input Required",
                    "Paste email headers."
                )

                return

            output.delete(
                "1.0",
                tk.END
            )

            output.insert(
                tk.END,
                "========== EMAIL HEADER ANALYSIS ==========\n\n"
            )

            checks = {
                "SPF": r"spf\s*[:=]\s*(pass|fail|softfail|neutral)",
                "DKIM": r"dkim\s*[:=]\s*(pass|fail|neutral)",
                "DMARC": r"dmarc\s*[:=]\s*(pass|fail|quarantine|none)"
            }

            for name, pattern in checks.items():

                match = re.search(
                    pattern,
                    raw,
                    re.I
                )

                if match:

                    output.insert(
                        tk.END,
                        f"{name}: {match.group(1).upper()}\n"
                    )

                else:

                    output.insert(
                        tk.END,
                        f"{name}: Not found\n"
                    )

            from_match = re.search(
                r"^From:\s*(.+)$",
                raw,
                re.I | re.M
            )

            reply_match = re.search(
                r"^Reply-To:\s*(.+)$",
                raw,
                re.I | re.M
            )

            output.insert(
                tk.END,
                "\n"
            )

            if from_match:

                output.insert(
                    tk.END,
                    f"From: {from_match.group(1).strip()}\n"
                )

            if reply_match:

                output.insert(
                    tk.END,
                    f"Reply-To: {reply_match.group(1).strip()}\n"
                )

                if from_match:

                    from_email = re.findall(
                        r"[\w.+-]+@[\w.-]+\.\w+",
                        from_match.group(1)
                    )

                    reply_email = re.findall(
                        r"[\w.+-]+@[\w.-]+\.\w+",
                        reply_match.group(1)
                    )

                    if (
                        from_email and
                        reply_email and
                        from_email[0].lower()
                        != reply_email[0].lower()
                    ):

                        output.insert(
                            tk.END,
                            "\n⚠ From and Reply-To addresses differ.\n"
                        )


    # ========================================================
    # TAB 9 — PASSWORD BREACH CHECKER
    # ========================================================

    def tab_breach(self):

        tab = self.create_tab(
            "Password Breach Checker"
        )

        tk.Label(
            tab,
            text="🔐 Password Breach Checker",
            bg=BG,
            fg=ACCENT,
            font=("Segoe UI", 15, "bold")
        ).pack(
            pady=(12, 5)
        )

        tk.Label(
            tab,
            text="Checks a password using SHA-1 k-anonymity.",
            bg=BG,
            fg=FG
        ).pack()

        entry = tk.Entry(
            tab,
            show="*",
            bg="#111827",
            fg=FG,
            insertbackground=ACCENT
        )

        entry.pack(
            fill="x",
            padx=15,
            pady=10
        )

        output = self.output_box(tab)

        def breach_check():

            password = entry.get()

            if not password:

                messagebox.showwarning(
                    "Input Required",
                    "Enter a password."
                )

                return

            def worker():

                self.log(
                    output,
                    "\n========== PASSWORD BREACH CHECK =========="
                )

                try:

                    sha1 = hashlib.sha1(
                        password.encode("utf-8")
                    ).hexdigest().upper()

                    prefix = sha1[:5]
                    suffix = sha1[5:]

                    url = (
                        "https://api.pwnedpasswords.com/range/"
                        + prefix
                    )

                    request = urllib.request.Request(
                        url,
                        headers={
                            "User-Agent":
                            "CyberSentinelAI-MK"
                        }
                    )

                    with urllib.request.urlopen(
                        request,
                        timeout=10
                    ) as response:

                        data = response.read().decode(
                            "utf-8"
                        )

                    found = False

                    for line in data.splitlines():

                        parts = line.split(":")

                        if len(parts) == 2:

                            if parts[0].strip().upper() == suffix:

                                count = parts[1].strip()

                                self.log(
                                    output,
                                    f"⚠ Password found in breach database."
                                )

                                self.log(
                                    output,
                                    f"Known occurrences: {count}"
                                )

                                found = True

                                break

                    if not found:

                        self.log(
                            output,
                            "✓ No match found in the queried breach database."
                        )

                    self.log(
                        output,
                        "\nOnly the first 5 characters of the SHA-1 hash"
                    )

                    self.log(
                        output,
                        "are sent to the service."
                    )

                except Exception as e:

                    self.log(
                        output,
                        f"Breach Check Error: {e}"
                    )

            self.run_bg(worker)


        tk.Button(
            tab,
            text="Check Password Breach",
            command=breach_check,
            bg="#172033",
            fg=ACCENT
        ).pack(
            pady=5
        )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    app = CyberSentinel()

    app.mainloop()