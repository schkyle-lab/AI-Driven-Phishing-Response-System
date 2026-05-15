import urequests  # MicroPython library for handling HTTP network requests
import time       # Library for introducing delays and timing functions
from machine import Pin  # Hardware library to directly control ESP32/Raspberry Pi Pico GPIO pins
import json       # Library to parse and format JSON data payloads
from config import API_KEY  # Security best practice: Imports secrets from an external configuration file

# --- HARDWARE & SOAR CONFIGURATION ---
# Initialize GPIO pins. Pin.OUT configures them to send voltage signals to peripherals.
RED_LED = Pin(13, Pin.OUT)    # Visual Alert Indicator: Lights up when a threat is active
GREEN_LED = Pin(12, Pin.OUT)  # Visual Safe Indicator: Lights up when the system is secure
RELAY = Pin(14, Pin.OUT)      # Physical "Kill Switch": Controls a physical relay to sever network connections

# Mock telemetry input queue: Simulates incoming data streams harvested from a SIEM or email monitor
suspicious_urls = [
    "http://google.com",            # Legitimate domain (Safe baseline)
    "http://secure-login-bank.xyz"  # Lookalike domain pattern (Phishing indicator)
]

def ai_analyze_url(url):
    """
    Orchestration Layer: Queries a remote AI/LLM deployment to parse and classify threat data.
    
    Args:
        url (str): The suspicious endpoint harvested from telemetry.
    Returns:
        dict: A structured response containing the security classification and accuracy confidence.
    """
    print(f"Orchestrating analysis for: {url}")
    
    # --- PRODUCTION IMPLEMENTATION TEMPLATE ---
    # api_url = "https://openai.com"
    # headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    # payload = {"model": "gpt-4", "messages": [{"role": "user", "content": f"Is this phishing? {url}"}]}
    # response = urequests.post(api_url, json=payload, headers=headers)
    # data = response.json()
    
    # --- SIMULATED AI CORE (Edge Rule-Engine) ---
    # Simulates AI classification heuristic by catching standard malicious top-level domains (.xyz) or keywords
    if "xyz" in url or "login" in url:
        return {"verdict": "MALICIOUS", "confidence": 0.98}
    else:
        return {"verdict": "SAFE", "confidence": 0.99}

def execute_playbook(threat_level):
    """
    Automation & Response Layer: Executes programmatic containment protocols based on threat severity.
    
    Args:
        threat_level (str): The threat verdict ('MALICIOUS' or 'SAFE') handed down by the AI layer.
    """
    if threat_level == "MALICIOUS":
        print(">>> THREAT DETECTED! Executing Containment Playbook...")
        
        # Containment Protocol: Change physical device state to signal breach
        GREEN_LED.off()  # Turn off the safety beacon
        RED_LED.on()     # Illuminate the warning beacon
        RELAY.on()       # Trip the physical relay mechanism to drop network line power and isolate the asset
        
        print(">>> Response: Device Isolated. Admin Notified.")
        
    else:
        # Maintenance Protocol: Revert hardware to secure default running operations
        print(">>> Target Safe. No action taken.")
        RED_LED.off()    # Deactivate warning beacon
        GREEN_LED.on()   # Re-engage safety status light
        RELAY.off()      # Keep network path closed/connected

def main():
    """
    Main Execution Loop: Emulates a continuous security automation engine monitoring remote pipelines.
    """
    # System Initialization: Flash safe light to signal code is actively running
    GREEN_LED.on()
    
    while True:
        # Sequentially process each item sitting inside the incoming telemetry queue
        for url in suspicious_urls:
            # Step 1: Send telemetry out to the intelligence tier
            result = ai_analyze_url(url)
            print(f"AI Verdict: {result['verdict']} ({result['confidence']*100}%)")
            
            # Step 2: Feed intelligence into the automation engine to take immediate physical action
            execute_playbook(result['verdict'])
            
            # Step 3: Throttling delay to respect external API rate-limits and prevent resource exhaustion
            time.sleep(5) 

# Conditional guard preventing script execution if imported as a module elsewhere
if __name__ == "__main__":
    main()
