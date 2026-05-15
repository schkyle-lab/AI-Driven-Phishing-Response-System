import urequests
import time
from machine import Pin
import json
from config import API_KEY

# --- SOAR CONFIGURATION ---
RED_LED = Pin(13, Pin.OUT)   # Alert Indicator
GREEN_LED = Pin(12, Pin.OUT) # Safe Indicator
RELAY = Pin(14, Pin.OUT)     # "Kill Switch" for network

# Mock input: In a real system, this comes from a server or email monitor
suspicious_urls = [
    "http://google.com",             # Safe
    "http://secure-login-bank.xyz"   # Phishing
]

def ai_analyze_url(url):
    """
    Queries an AI API to detect phishing.
    Replace URL with your actual LLM endpoint (e.g., OpenAI/Gemini).
    """
    print(f"Orchestrating analysis for: {url}")
    
    # SIMULATED AI RESPONSE for demonstration
    # In production, use urequests.post(API_URL, json=payload, headers=header)
    if "xyz" in url or "login" in url:
        return {"verdict": "MALICIOUS", "confidence": 0.98}
    else:
        return {"verdict": "SAFE", "confidence": 0.99}

def execute_playbook(threat_level):
    """
    The 'Response' part of SOAR.
    """
    if threat_level == "MALICIOUS":
        print(">>> THREAT DETECTED! Executing Containment Playbook...")
        GREEN_LED.off()
        RED_LED.on()
        RELAY.on() # Activate relay to cut connection
        print(">>> Response: Device Isolated. Admin Notified.")
    else:
        print(">>> Target Safe. No action taken.")
        RED_LED.off()
        GREEN_LED.on()
        RELAY.off()

def main():
    GREEN_LED.on()
    while True:
        # Simulate polling an inbox or SIEM
        for url in suspicious_urls:
            result = ai_analyze_url(url)
            print(f"AI Verdict: {result['verdict']} ({result['confidence']*100}%)")
            
            execute_playbook(result['verdict'])
            
            time.sleep(5) # Wait before next scan

if __name__ == "__main__":
    main()
