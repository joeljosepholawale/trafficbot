# Web Traffic Simulator

A professional Python script that simulates realistic web traffic from various sources including search engines and social media platforms. The traffic appears authentic to analytics tools by properly simulating referrers, user agents, and other HTTP headers.

## Features

- Simulates traffic from multiple search engines (Google, Bing, Yandex, etc.)
- Simulates traffic from social media platforms (Facebook, Twitter, Instagram, LinkedIn, etc.)
- Simulates direct traffic
- Configurable traffic distribution
- Realistic user agents for desktop and mobile devices
- Customizable request intervals
- Detailed logging

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/web-traffic-simulator.git
cd web-traffic-simulator
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the script with default settings:

```bash
python traffic_simulator.py
```

This will create a default configuration file (`traffic_config.json`) if one doesn't exist and start sending traffic to the default target URL.

### Command Line Options

- `-c, --config`: Path to configuration file (default: `traffic_config.json`)
- `-n, --num-requests`: Number of requests to send (default: run indefinitely)
- `-v, --verbose`: Enable verbose logging

Example:

```bash
python traffic_simulator.py --config my_config.json --num-requests 100 --verbose
```

### Configuration

The script uses a JSON configuration file. You can modify the default configuration or create your own:

```json
{
    "target_urls": ["https://yourdomain.com"],
    "request_interval": {
        "min": 1,
        "max": 5
    },
    "sources": {
        "search_engines": {
            "google": {
                "weight": 40,
                "domains": ["www.google.com", "google.com"],
                "referrer_templates": [
                    "https://www.google.com/search?q={query}"
                ],
                "queries": ["your keyword 1", "your keyword 2"]
            },
            // Add more search engines...
        },
        "social_media": {
            "facebook": {
                "weight": 30,
                "domains": ["www.facebook.com", "facebook.com", "m.facebook.com"],
                "referrer_templates": [
                    "https://www.facebook.com/",
                    "https://m.facebook.com/"
                ]
            },
            // Add more social media platforms...
        },
        "direct": {
            "weight": 20
        }
    },
    "user_agents": {
        "desktop": {
            "weight": 60,
            "agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                // Add more desktop user agents...
            ]
        },
        "mobile": {
            "weight": 40,
            "agents": [
                "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
                // Add more mobile user agents...
            ]
        }
    }
}
```

## Disclaimer

This tool is intended for testing and educational purposes only. Use responsibly and ethically. Do not use this tool to:

- Artificially inflate traffic metrics
- Manipulate analytics data
- Perform any actions that violate terms of service of websites
