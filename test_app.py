import sys
from playwright.sync_api import sync_playwright
import time

def test_app(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            print(f"Navigating to {url}")
            page.goto(url)
            # Wait for the page to load
            page.wait_for_load_state("networkidle")
            
            print(f"Page title: {page.title()}")
            
            # Take a screenshot
            page.screenshot(path="screenshot.png")
            print("Screenshot saved to screenshot.png")
            
            # Check for some content
            content = page.content()
            if "RAG" in content or "Agent" in content:
                print("Found 'RAG' or 'Agent' in page content.")
            else:
                print("Did not find expected keywords in page content.")
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "http://localhost:8001" # Default Streamlit port
    test_app(url)
