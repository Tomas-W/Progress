import argparse
import os

from dataclasses import dataclass, field


@dataclass
class Directories:
    BASE: str = field(default_factory=lambda: os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
    WEIGHT: str = field(init=False)
    CALORIES: str = field(init=False)
    BOTH: str = field(init=False)
    INSTA: str = field(init=False)

    WEIGHT_REL: str = field(init=False)
    CALORIES_REL: str = field(init=False)
    BOTH_REL: str = field(init=False)
    INSTA_REL: str = field(init=False)

    def __post_init__(self):
        image_base = os.path.join(self.BASE, "static")
        self.WEIGHT = os.path.join(image_base, "images", "weight")
        self.CALORIES = os.path.join(image_base, "images", "calories")
        self.BOTH = os.path.join(image_base, "images", "both")
        self.INSTA = os.path.join(image_base, "images", "insta")

        self.WEIGHT_REL = "images/weight"
        self.CALORIES_REL = "images/calories"
        self.BOTH_REL = "images/both"
        self.INSTA_REL = "images/insta"


@dataclass
class Server:
    SECURITY_HEADERS: dict[str, str] = None

    def __post_init__(self):
        if self.SECURITY_HEADERS is None:
            self.SECURITY_HEADERS = {
        # Prevents MIME type sniffing
        "X-Content-Type-Options": "nosniff",
        # Controls how the site can be framed - protects against clickjacking
        "X-Frame-Options": "SAMEORIGIN",
        # Enforces HTTPS - 1 year duration with subdomains
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
        # Content Security Policy
        "Content-Security-Policy": (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: blob: *; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "media-src 'self'; "
            "object-src 'none'; "
            "frame-src 'self'; "
            "worker-src 'self'; "
            "form-action 'self'; "
            "base-uri 'self'; "
            "frame-ancestors 'self'; "
            "upgrade-insecure-requests; "
        ),
        # Controls how much referrer information is included with requests
        "Referrer-Policy": "strict-origin-when-cross-origin",
        # Prevents browsers from performing DNS prefetching
        "X-DNS-Prefetch-Control": "off",
        # Controls browser features - restricts potentially risky features
        "Permissions-Policy": (
            "accelerometer=(), "
            "camera=(), "
            "geolocation=(), "
            "gyroscope=(), "
            "magnetometer=(), "
            "microphone=(), "
            "payment=(), "
            "usb=()"
        ),
        # Enables cross-origin isolation capabilities
        "Cross-Origin-Opener-Policy": "same-origin",
        "Cross-Origin-Embedder-Policy": "require-corp",
        "Cross-Origin-Resource-Policy": "same-origin"
    }


@dataclass
class LocalServer:
    SECURITY_HEADERS: dict = None

    def __post_init__(self):
        if self.SECURITY_HEADERS is None:
            self.SECURITY_HEADERS = {}


@dataclass
class Routes:
    landing: str = "/"
    home: str = "/home"
    weight: str = "/weight"
    calories: str = "/calories"
    both: str = "/both"
    insta: str = "/insta"

    add_user: str = "/admin/add-user"
    add_weight: str = "/admin/add-weight"


@dataclass
class Templates:
    landing: str = "landing/landing.html"
    home: str = "home/home.html"
    graph: str = "home/graph.html"
    weight: str = "home/weight.html"
    calories: str = "home/calories.html"
    both: str = "home/both.html"
    insta: str = "home/insta.html"

    add_user: str = "admin/add_user.html"
    add_weight: str = "admin/add_weight.html"


@dataclass
class Redirects:
    landing: str = "landing.landing"
    home: str = "home.home"
    weight: str = "home.weight"
    calories: str = "home.calories"
    both: str = "home.both"
    insta: str = "home.insta"
    
    add_user: str = "admin.add_user"
    add_weight: str = "admin.add_weight"


@dataclass
class Config:
    server: Server | LocalServer = None
    route: Routes = field(default_factory=Routes)
    template: Templates = field(default_factory=Templates)
    redirect: Redirects = field(default_factory=Redirects)
    dir: Directories = field(default_factory=Directories)

    def __post_init__(self):
        if self.server is None:
            parser = argparse.ArgumentParser(description="Run the Flask application")
            parser.add_argument("--local", action="store_true", default=False, help="Run the application in debug mode")
            args = parser.parse_args()
            debug = args.local

            # Check if localhost
            is_local = os.environ.get("DEBUG") == "True" or debug
            self.server = LocalServer() if is_local else Server()


CFG = Config()
