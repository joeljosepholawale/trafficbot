# Advanced Traffic Bot Simulator

A sophisticated web traffic simulator that generates realistic traffic patterns from various sources including search engines and social media platforms. This tool is designed to help website owners understand how their sites respond to different traffic patterns and can be used for testing and SEO analysis.

## Features

- **Realistic Traffic Sources**: Simulates traffic from search engines, social media, and direct visits
- **Organic Search Behavior**: Mimics real user search patterns including search engine visits, result evaluation, and click-through
- **User Interaction Simulation**: Simulates scrolling, clicking, and realistic dwell times
- **SEO-Enhancing Capabilities**:
  - Keyword-focused traffic generation
  - Geographic diversity with proxy support
  - Mobile vs. desktop traffic balance
  - Internal site navigation patterns
  - Social sharing signals
  - Time-based traffic patterns
- **Detailed Logging**: Comprehensive logging of all activities for analysis

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/joeljosepholawale/trafficbot.git
   cd trafficbot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Run the simulator with default settings:

```bash
python traffic_simulator.py
```

This will create a default configuration file (`traffic_config.json`) if one doesn't exist and start sending traffic to the configured target URLs.

### Command Line Options

```
python traffic_simulator.py [-h] [-c CONFIG] [-n NUM_REQUESTS] [-v] [-t TARGET] [-k KEYWORDS] [-m MOBILE]

options:
  -h, --help            Show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to configuration file
  -n NUM_REQUESTS, --num-requests NUM_REQUESTS
                        Number of requests to send (default: run indefinitely)
  -v, --verbose         Enable verbose logging
  -t TARGET, --target TARGET
                        Override target URL(s) in config (comma-separated for multiple)
  -k KEYWORDS, --keywords KEYWORDS
                        Path to keywords file
  -m MOBILE, --mobile MOBILE
                        Set mobile traffic percentage (0-100)
```

### Examples

1. Send 50 requests with verbose logging:
   ```
   python traffic_simulator.py --num-requests 50 --verbose
   ```

2. Target a specific URL:
   ```
   python traffic_simulator.py --target https://yourwebsite.com
   ```

3. Use custom keywords file:
   ```
   python traffic_simulator.py --keywords your_keywords.txt
   ```

4. Set mobile traffic to 70%:
   ```
   python traffic_simulator.py --mobile 70
   ```

## Configuration

The simulator uses a JSON configuration file (`traffic_config.json` by default) to control its behavior. The configuration includes:

- Target URLs
- Request intervals
- Traffic sources and their weights
- User agent configurations
- SEO-specific settings
- Proxy configurations

### Sample Configuration

```json
{
  "target_urls": ["https://example.com"],
  "request_interval": {
    "min": 1,
    "max": 5
  },
  "seo_settings": {
    "simulate_organic_behavior": true,
    "min_dwell_time": 30,
    "max_dwell_time": 180,
    "internal_navigation_probability": 0.6,
    "bounce_rate_target": 40,
    "mobile_percentage": 65,
    "keyword_file": "keywords.txt",
    "geo_targeting": {
      "enabled": false,
      "countries": ["US", "UK", "CA", "AU", "DE", "FR", "IN"]
    },
    "time_based_patterns": true
  },
  "sources": {
    "search_engines": {
      "google": {
        "weight": 40,
        "domains": ["www.google.com", "google.com"],
        "referrer_templates": [
          "https://www.google.com/search?q={query}"
        ],
        "queries": ["example website", "sample site"]
      },
      // Other search engines...
    },
    "social_media": {
      // Social media platforms...
    },
    "direct": {
      "weight": 20
    }
  }
}
```

## Keywords File

The keywords file is a simple text file with one keyword or phrase per line. These keywords will be used for search engine queries and social media searches.

## Disclaimer

This tool is intended for educational and testing purposes only. Use responsibly and in accordance with the terms of service of any websites you target. The authors are not responsible for any misuse of this software.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
```

Now let's create a simple keywords.txt file with some generic keywords:

```text:keywords.txt
best website design
how to improve website SEO
website performance optimization
responsive web design examples
website traffic analysis
website conversion rate optimization
best practices for website navigation
website loading speed improvement
website user experience design
website content strategy
website analytics tools
website mobile optimization
website security best practices
website accessibility standards
website design trends 2023