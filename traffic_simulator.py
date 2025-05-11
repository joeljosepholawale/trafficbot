#!/usr/bin/env python3
"""
Web Traffic Simulator

This script generates realistic web traffic from various sources including search engines
and social media platforms. It properly simulates referrers, user agents, and other
HTTP headers to appear as genuine traffic to analytics tools.
"""

import requests
import random
import time
import argparse
import logging
import json
from typing import Dict, List, Any
from user_agents import parse
from urllib.parse import urlencode

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("traffic_simulator.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TrafficSimulator:
    """Simulates web traffic from various sources."""
    
    def __init__(self, config_file: str = "traffic_config.json"):
        """
        Initialize the traffic simulator.
        
        Args:
            config_file: Path to the configuration file
        """
        self.config = self._load_config(config_file)
        self.session = requests.Session()
        
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file {config_file} not found.")
            # Create default configuration
            default_config = {
                "target_urls": ["https://example.com"],
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
                            "queries": ["example website", "sample site"]
                        },
                        "bing": {
                            "weight": 20,
                            "domains": ["www.bing.com", "bing.com"],
                            "referrer_templates": [
                                "https://www.bing.com/search?q={query}"
                            ],
                            "queries": ["example website", "sample site"]
                        },
                        "yandex": {
                            "weight": 10,
                            "domains": ["yandex.com", "yandex.ru"],
                            "referrer_templates": [
                                "https://yandex.com/search/?text={query}"
                            ],
                            "queries": ["example website", "sample site"]
                        }
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
                        "twitter": {
                            "weight": 20,
                            "domains": ["twitter.com", "t.co"],
                            "referrer_templates": [
                                "https://twitter.com/",
                                "https://t.co/"
                            ]
                        },
                        "instagram": {
                            "weight": 15,
                            "domains": ["instagram.com", "www.instagram.com"],
                            "referrer_templates": [
                                "https://www.instagram.com/"
                            ]
                        },
                        "linkedin": {
                            "weight": 15,
                            "domains": ["linkedin.com", "www.linkedin.com"],
                            "referrer_templates": [
                                "https://www.linkedin.com/feed/"
                            ]
                        }
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
                            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
                        ]
                    },
                    "mobile": {
                        "weight": 40,
                        "agents": [
                            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
                            "Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0",
                            "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
                        ]
                    }
                }
            }
            
            # Save default configuration
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
            
            logger.info(f"Created default configuration file: {config_file}")
            return default_config
    
    def _get_random_user_agent(self) -> str:
        """Get a random user agent based on configured weights."""
        device_type = random.choices(
            list(self.config["user_agents"].keys()),
            weights=[self.config["user_agents"][k]["weight"] for k in self.config["user_agents"].keys()]
        )[0]
        
        return random.choice(self.config["user_agents"][device_type]["agents"])
    
    def _get_traffic_source(self) -> Dict[str, Any]:
        """Determine traffic source based on configured weights."""
        # Calculate total weight for all sources
        sources = self.config["sources"]
        source_types = list(sources.keys())
        weights = [sources[s]["weight"] for s in source_types]
        
        # Choose source type (search_engines, social_media, direct)
        source_type = random.choices(source_types, weights=weights)[0]
        
        if source_type == "direct":
            return {"type": "direct"}
        
        # Choose specific source within the type
        specific_sources = list(sources[source_type].keys())
        specific_weights = [sources[source_type][s]["weight"] for s in specific_sources]
        
        specific_source = random.choices(specific_sources, weights=specific_weights)[0]
        
        return {
            "type": source_type,
            "source": specific_source,
            "config": sources[source_type][specific_source]
        }
    
    def _build_headers(self, source: Dict[str, Any], target_url: str) -> Dict[str, str]:
        """Build realistic HTTP headers for the request."""
        user_agent = self._get_random_user_agent()
        headers = {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Cache-Control": "max-age=0",
        }
        
        # Add referrer for non-direct traffic
        if source["type"] != "direct":
            config = source["config"]
            referrer_template = random.choice(config["referrer_templates"])
            
            if source["type"] == "search_engines":
                query = random.choice(config["queries"])
                referrer = referrer_template.format(query=urlencode({"q": query})[2:])
            else:
                referrer = referrer_template
                
            headers["Referer"] = referrer
            
        return headers
    
    def send_request(self, target_url: str) -> None:
        """Send a simulated request to the target URL."""
        source = self._get_traffic_source()
        headers = self._build_headers(source, target_url)
        
        source_type = source["type"]
        source_name = source.get("source", "direct")
        
        try:
            logger.info(f"Sending request to {target_url} from {source_type}/{source_name}")
            response = self.session.get(target_url, headers=headers, timeout=10)
            logger.info(f"Response status: {response.status_code}")
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
    
    def run(self, num_requests: int = None) -> None:
        """
        Run the traffic simulator.
        
        Args:
            num_requests: Number of requests to send. If None, run indefinitely.
        """
        count = 0
        
        try:
            while num_requests is None or count < num_requests:
                target_url = random.choice(self.config["target_urls"])
                self.send_request(target_url)
                
                # Sleep for a random interval
                interval = random.uniform(
                    self.config["request_interval"]["min"],
                    self.config["request_interval"]["max"]
                )
                logger.debug(f"Sleeping for {interval:.2f} seconds")
                time.sleep(interval)
                
                count += 1
                if num_requests is not None:
                    logger.info(f"Completed {count}/{num_requests} requests")
                    
        except KeyboardInterrupt:
            logger.info("Traffic simulation stopped by user")
        
        logger.info(f"Traffic simulation completed. Sent {count} requests.")

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Simulate web traffic from various sources")
    parser.add_argument(
        "-c", "--config", 
        default="traffic_config.json",
        help="Path to configuration file"
    )
    parser.add_argument(
        "-n", "--num-requests", 
        type=int, 
        default=None,
        help="Number of requests to send (default: run indefinitely)"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    simulator = TrafficSimulator(args.config)
    simulator.run(args.num_requests)

if __name__ == "__main__":
    main()