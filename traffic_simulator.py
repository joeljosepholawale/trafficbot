#!/usr/bin/env python3
"""
Web Traffic Simulator

This script generates realistic web traffic from various sources including search engines
and social media platforms. It properly simulates referrers, user agents, and other
HTTP headers to appear as genuine traffic to analytics tools. Enhanced with SEO-boosting
features like organic search behavior, dwell time simulation, and social signals.
"""

import requests
import random
import time
import argparse
import logging
import json
import datetime
from typing import Dict, List, Any, Optional, Tuple
from urllib.parse import urlencode, urlparse, parse_qs
from bs4 import BeautifulSoup

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
    """Simulates web traffic from various sources with SEO-enhancing features."""
    
    def __init__(self, config_file: str = "traffic_config.json"):
        """
        Initialize the traffic simulator.
        
        Args:
            config_file: Path to the configuration file
        """
        self.config = self._load_config(config_file)
        self.session = requests.Session()
        self.config_file = config_file
        
        # Initialize keyword list if specified
        if self.config.get("seo_settings", {}).get("keyword_file"):
            self.add_keyword_focused_traffic(self.config["seo_settings"]["keyword_file"])
        
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file {config_file} not found.")
            # Create enhanced default configuration
            default_config = {
                "target_urls": ["https://example.com"],
                "request_interval": {
                    "min": 1,
                    "max": 5
                },
                "seo_settings": {
                    "simulate_organic_behavior": True,
                    "min_dwell_time": 30,
                    "max_dwell_time": 180,
                    "internal_navigation_probability": 0.6,
                    "bounce_rate_target": 40,
                    "mobile_percentage": 65,
                    "keyword_file": "keywords.txt",
                    "geo_targeting": {
                        "enabled": False,
                        "countries": ["US", "UK", "CA", "AU", "DE", "FR", "IN"]
                    },
                    "time_based_patterns": True
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
                        },
                        "duckduckgo": {
                            "weight": 10,
                            "domains": ["duckduckgo.com"],
                            "referrer_templates": [
                                "https://duckduckgo.com/?q={query}"
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
                        },
                        "pinterest": {
                            "weight": 10,
                            "domains": ["pinterest.com", "www.pinterest.com"],
                            "referrer_templates": [
                                "https://www.pinterest.com/search/pins/?q={query}"
                            ],
                            "queries": ["product inspiration", "design ideas"]
                        },
                        "reddit": {
                            "weight": 10,
                            "domains": ["reddit.com", "www.reddit.com"],
                            "referrer_templates": [
                                "https://www.reddit.com/r/web_design/",
                                "https://www.reddit.com/search/?q={query}"
                            ],
                            "queries": ["website recommendations", "web design"]
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
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55",
                            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
                        ]
                    },
                    "mobile": {
                        "weight": 40,
                        "agents": [
                            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
                            "Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0",
                            "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
                            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.80 Mobile/15E148 Safari/604.1",
                            "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36"
                        ]
                    }
                },
                "proxies": []
            }
            
            # Save default configuration
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
            
            logger.info(f"Created enhanced default configuration file: {config_file}")
            
            # Create sample keywords file
            sample_keywords = [
                "best product in category",
                "how to use product",
                "product vs competitor",
                "product reviews",
                "buy product online"
            ]
            with open("keywords.txt", 'w') as f:
                f.write('\n'.join(sample_keywords))
                
            logger.info("Created sample keywords file: keywords.txt")
            
            return default_config
    
    def _save_config(self) -> None:
        """Save the current configuration back to the file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
        logger.debug(f"Configuration saved to {self.config_file}")
    
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
        
        # Extract weights, ensuring each source has a weight
        weights = []
        for s in source_types:
            if isinstance(sources[s], dict) and "weight" in sources[s]:
                weights.append(sources[s]["weight"])
            else:
                # Default weight if not specified
                weights.append(10)
        
        # Choose source type (search_engines, social_media, direct)
        source_type = random.choices(source_types, weights=weights)[0]
        
        if source_type == "direct":
            return {"type": "direct"}
        
        # Choose specific source within the type
        specific_sources = list(sources[source_type].keys())
        specific_weights = []
        
        for s in specific_sources:
            if isinstance(sources[source_type][s], dict) and "weight" in sources[source_type][s]:
                specific_weights.append(sources[source_type][s]["weight"])
            else:
                # Default weight if not specified
                specific_weights.append(10)
        
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
            
            if source["type"] == "search_engines" or (source["type"] == "social_media" and "queries" in config):
                query = random.choice(config["queries"])
                referrer = referrer_template.format(query=urlencode({"q": query})[2:])
            else:
                referrer = referrer_template
                
            headers["Referer"] = referrer
            
        return headers
    
    def send_request(self, target_url: str) -> None:
        """Send a simulated request to the target URL."""
        source = self._get_traffic_source()
        
        # Apply time-based traffic patterns if enabled
        if self.config.get("seo_settings", {}).get("time_based_patterns", False):
            multiplier = self.apply_traffic_patterns()
            if random.random() > multiplier:
                logger.debug(f"Skipping request due to time-based pattern (multiplier: {multiplier:.2f})")
                return
        
        # Use geo-diverse proxies if enabled and available
        if self.config.get("seo_settings", {}).get("geo_targeting", {}).get("enabled", False):
            self.use_geo_diverse_proxies()
        
        # Determine if we should simulate organic search behavior
        if (source["type"] == "search_engines" and 
            self.config.get("seo_settings", {}).get("simulate_organic_behavior", False)):
            self.simulate_organic_search_behavior(target_url, source)
        else:
            # Regular request
            headers = self._build_headers(source, target_url)
            
            source_type = source["type"]
            source_name = source.get("source", "direct")
            
            try:
                logger.info(f"Sending request to {target_url} from {source_type}/{source_name}")
                response = self.session.get(target_url, headers=headers, timeout=10)
                logger.info(f"Response status: {response.status_code}")
                
                # Simulate dwell time and page interaction
                if response.status_code == 200:
                    self.simulate_page_interaction(target_url)
                    
                    # Possibly simulate social sharing
                    if random.random() < 0.1:  # 10% chance
                        self.simulate_social_sharing(target_url)
                    
                                        # Possibly navigate to another page on the site
                    if random.random() < self.config.get("seo_settings", {}).get("internal_navigation_probability", 0.3):
                        self._navigate_to_internal_page(target_url, response)
                
            except Exception as e:
                logger.error(f"Request failed: {str(e)}")
    
    def _navigate_to_internal_page(self, base_url: str, response: requests.Response) -> None:
        """Navigate to an internal page on the site to simulate deeper engagement."""
        try:
            # Parse the HTML to find internal links
            soup = BeautifulSoup(response.text, 'html.parser')
            internal_links = []
            
            base_domain = urlparse(base_url).netloc
            
            # Find all links
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Handle relative URLs
                if href.startswith('/'):
                    href = f"{urlparse(base_url).scheme}://{base_domain}{href}"
                elif not href.startswith(('http://', 'https://')):
                    href = f"{base_url.rstrip('/')}/{href.lstrip('/')}"
                
                # Check if it's an internal link
                if urlparse(href).netloc == base_domain:
                    internal_links.append(href)
            
            if internal_links:
                next_url = random.choice(internal_links)
                logger.info(f"Navigating to internal page: {next_url}")
                
                # Use the same session to maintain cookies
                headers = {
                    "User-Agent": self._get_random_user_agent(),
                    "Referer": base_url
                }
                
                next_response = self.session.get(next_url, headers=headers, timeout=10)
                logger.info(f"Internal navigation response: {next_response.status_code}")
                
                # Simulate interaction with this page too
                if next_response.status_code == 200:
                    self.simulate_page_interaction(next_url, is_internal=True)
            else:
                logger.debug(f"No internal links found on {base_url}")
        
        except Exception as e:
            logger.error(f"Internal navigation failed: {str(e)}")
    
    def simulate_organic_search_behavior(self, target_url: str, source: Dict[str, Any]) -> None:
        """Simulate realistic organic search behavior including click-through and dwell time."""
        # Only proceed if this is a search engine source
        if source["type"] != "search_engines":
            return
            
        search_engine = source["source"]
        config = source["config"]
        
        # 1. First visit the search engine
        query = random.choice(config["queries"])
        search_url = random.choice(config["referrer_templates"]).format(
            query=urlencode({"q": query})[2:]
        )
        search_headers = {
            "User-Agent": self._get_random_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
        
        logger.info(f"Simulating organic search: Visiting {search_engine} with query '{query}'")
        try:
            # Visit the search engine
            self.session.get(search_url, headers=search_headers, timeout=10)
            
            # 2. Wait as if user is reviewing search results (3-10 seconds)
            search_review_time = random.uniform(3, 10)
            logger.debug(f"Reviewing search results for {search_review_time:.1f} seconds")
            time.sleep(search_review_time)
            
            # 3. Now click through to the target site
            headers = self._build_headers(source, target_url)
            logger.info(f"Clicking through to: {target_url}")
            response = self.session.get(target_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # 4. Simulate page interaction and dwell time
                self.simulate_page_interaction(target_url)
                
                # 5. Possibly navigate to another page on the same site
                if random.random() < self.config.get("seo_settings", {}).get("internal_navigation_probability", 0.6):
                    self._navigate_to_internal_page(target_url, response)
                    
                # 6. Possibly go back to search results and visit another site (to signal quality)
                if random.random() < 0.3:  # 30% chance
                    logger.info("Returning to search results")
                    self.session.get(search_url, headers={
                        "User-Agent": headers["User-Agent"],
                        "Referer": target_url
                    }, timeout=10)
                    
        except Exception as e:
            logger.error(f"Organic search simulation failed: {str(e)}")
    
    def simulate_page_interaction(self, target_url: str, is_internal: bool = False) -> None:
        """Simulate user interactions with the page like scrolling and dwelling."""
        # Determine dwell time based on configuration
        seo_settings = self.config.get("seo_settings", {})
        min_dwell = seo_settings.get("min_dwell_time", 30)
        max_dwell = seo_settings.get("max_dwell_time", 180)
        
        # Internal pages might have shorter dwell times
        if is_internal:
            min_dwell = max(5, min_dwell // 2)
            max_dwell = max(20, max_dwell // 2)
        
        dwell_time = random.uniform(min_dwell, max_dwell)
        
        # Simulate initial page load time
        initial_load = random.uniform(0.5, 3)
        time.sleep(initial_load)
        
        # Simulate scrolling behavior
        scroll_depth = random.uniform(0.3, 1.0)  # How far down the page
        scroll_time = scroll_depth * random.uniform(5, 15)  # Time spent scrolling
        
        logger.info(f"Simulating user interaction: scroll to {scroll_depth*100:.0f}% over {scroll_time:.1f}s, dwell for {dwell_time:.1f}s")
        
        # Simulate scrolling
        time.sleep(scroll_time)
        
        # Simulate possible click on page element (without actually clicking)
        if random.random() < 0.4:  # 40% chance to "click" something
            logger.debug("Simulating click on page element")
            time.sleep(random.uniform(0.5, 2))
        
        # Remaining dwell time
        remaining_dwell = max(0, dwell_time - scroll_time - initial_load)
        if remaining_dwell > 0:
            time.sleep(remaining_dwell)
    
    def simulate_social_sharing(self, target_url: str) -> None:
        """Simulate social sharing behavior."""
        social_platforms = ["facebook", "twitter", "linkedin", "pinterest"]
        platform = random.choice(social_platforms)
        
        logger.info(f"Simulating share to {platform}")
        
        # Create sharing URL (these would be actual sharing endpoints in production)
        if platform == "facebook":
            share_url = f"https://www.facebook.com/sharer/sharer.php?u={target_url}"
        elif platform == "twitter":
            share_url = f"https://twitter.com/intent/tweet?url={target_url}"
        elif platform == "linkedin":
            share_url = f"https://www.linkedin.com/sharing/share-offsite/?url={target_url}"
        elif platform == "pinterest":
            share_url = f"https://pinterest.com/pin/create/button/?url={target_url}"
        
        # Simulate visiting the share URL
        headers = {
            "User-Agent": self._get_random_user_agent(),
            "Referer": target_url
        }
        
        try:
            self.session.get(share_url, headers=headers, timeout=10)
            logger.info(f"Shared {target_url} to {platform}")
        except Exception as e:
            logger.error(f"Social sharing simulation failed: {str(e)}")
    
    def add_keyword_focused_traffic(self, keywords_file: str = "keywords.txt") -> None:
        """Add keyword-focused traffic based on a list of target keywords."""
        try:
            with open(keywords_file, 'r') as f:
                keywords = [line.strip() for line in f if line.strip()]
            
            # Add these keywords to all search engines
            for engine in self.config["sources"]["search_engines"]:
                current_queries = self.config["sources"]["search_engines"][engine].get("queries", [])
                # Add new keywords while avoiding duplicates
                self.config["sources"]["search_engines"][engine]["queries"] = list(set(current_queries + keywords))
                
            # Also add to social platforms that support queries
            for platform in self.config["sources"]["social_media"]:
                if "queries" in self.config["sources"]["social_media"][platform]:
                    current_queries = self.config["sources"]["social_media"][platform].get("queries", [])
                    self.config["sources"]["social_media"][platform]["queries"] = list(set(current_queries + keywords))
            
            # Save the updated configuration
            self._save_config()
            
            logger.info(f"Added {len(keywords)} keywords from {keywords_file}")
        except FileNotFoundError:
            logger.warning(f"Keywords file {keywords_file} not found. Creating sample file.")
            sample_keywords = [
                "best product in category",
                "how to use product",
                "product vs competitor",
                "product reviews",
                "buy product online"
            ]
            with open(keywords_file, 'w') as f:
                f.write('\n'.join(sample_keywords))
            
            # Recursively call this function now that the file exists
            self.add_keyword_focused_traffic(keywords_file)
    
    def use_geo_diverse_proxies(self) -> None:
        """Use geographically diverse proxies to simulate traffic from different locations."""
        proxy_list = self.config.get("proxies", [])
        if not proxy_list:
            logger.debug("No proxies configured. Using direct connection.")
            return
            
        proxy = random.choice(proxy_list)
        self.session.proxies = {
            "http": proxy,
            "https": proxy
        }
        logger.info(f"Using proxy: {proxy}")
    
    def adjust_device_balance(self, mobile_percentage: float = 60.0) -> None:
        """Adjust the balance between mobile and desktop traffic."""
        if 0 <= mobile_percentage <= 100:
            self.config["user_agents"]["mobile"]["weight"] = mobile_percentage
            self.config["user_agents"]["desktop"]["weight"] = 100 - mobile_percentage
            
            # Save the updated configuration
            self._save_config()
            
            logger.info(f"Adjusted device balance: {mobile_percentage}% mobile, {100-mobile_percentage}% desktop")
        else:
            logger.error("Mobile percentage must be between 0 and 100")
    
    def apply_traffic_patterns(self) -> float:
        """Apply realistic traffic patterns based on time of day and day of week."""
        # Get current time
        now = datetime.datetime.now()
        hour = now.hour
        day_of_week = now.weekday()  # 0-6 (Monday to Sunday)
        
        # Base multiplier
        multiplier = 1.0
        
        # Time of day adjustment (busier during business hours)
        if 9 <= hour <= 17:  # 9 AM to 5 PM
            multiplier *= random.uniform(1.2, 1.5)
        elif 18 <= hour <= 22:  # 6 PM to 10 PM
            multiplier *= random.uniform(1.1, 1.3)
        else:  # Late night/early morning
            multiplier *= random.uniform(0.5, 0.8)
        
        # Day of week adjustment (weekdays busier for B2B, weekends for B2C)
        if day_of_week < 5:  # Weekday
            multiplier *= random.uniform(1.1, 1.3)
        else:  # Weekend
            multiplier *= random.uniform(0.8, 1.0)
        
        logger.debug(f"Traffic pattern multiplier: {multiplier:.2f} (Hour: {hour}, Day: {day_of_week})")
        return multiplier
    
    def run(self, num_requests: int = None) -> None:
        """
        Run the traffic simulator.
        
        Args:
            num_requests: Number of requests to send. If None, run indefinitely.
        """
        count = 0
        
        # Apply mobile/desktop balance from config if specified
        if "mobile_percentage" in self.config.get("seo_settings", {}):
            self.adjust_device_balance(self.config["seo_settings"]["mobile_percentage"])
        
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
    parser = argparse.ArgumentParser(description="Simulate web traffic from various sources with SEO-enhancing features")
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
    parser.add_argument(
        "-t", "--target", 
        help="Override target URL(s) in config (comma-separated for multiple)"
    )
    parser.add_argument(
        "-k", "--keywords",
        help="Path to keywords file"
    )
    parser.add_argument(
        "-m", "--mobile",
        type=float,
        help="Set mobile traffic percentage (0-100)"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    simulator = TrafficSimulator(args.config)
    
    # Apply command line overrides
    if args.target:
        simulator.config["target_urls"] = args.target.split(',')
        logger.info(f"Target URL(s) set to: {simulator.config['target_urls']}")
    
    if args.keywords:
        simulator.add_keyword_focused_traffic(args.keywords)
    
    if args.mobile is not None:
        simulator.adjust_device_balance(args.mobile)
    
    simulator.run(args.num_requests)

if __name__ == "__main__":
    main()
