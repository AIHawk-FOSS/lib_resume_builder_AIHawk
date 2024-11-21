import platform
import os
import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager

def create_driver_selenium():
    options = get_chrome_browser_options()  # Use the method to get Chrome options

    chrome_install = ChromeDriverManager().install()
    folder = os.path.dirname(chrome_install)
    if platform.system() == "Windows":
        chromedriver_path = os.path.join(folder, "chromedriver.exe")
    else:
        chromedriver_path = os.path.join(folder, "chromedriver")
    service = ChromeService(executable_path=chromedriver_path)
    return webdriver.Chrome(service=service, options=options)

def HTML_to_PDF(FilePath):
    # Validating and preparing the file path
    if not os.path.isfile(FilePath):
        raise FileNotFoundError(f"The specified file does not exist: {FilePath}")
    FilePath = f"file:///{os.path.abspath(FilePath).replace(os.sep, '/')}"
    driver = create_driver_selenium()

    try:
        driver.get(FilePath)
        time.sleep(2)
        pdf_base64 = driver.execute_cdp_cmd("Page.printToPDF", {
            "printBackground": True,         # Includes background in print
            "landscape": False,              # Vertical printing (False for portrait)
            "paperWidth": 8.27,              # Paper width in inches (A4)
            "paperHeight": 11.69,            # Paper height in inches (A4)
            "marginTop": 0.8,                # Top margin in inches (approximately 2 cm)
            "marginBottom": 0.8,             # Bottom margin in inches (approximately 2 cm)
            "marginLeft": 0.5,               # Left margin in inches (approximately 2 cm)
            "marginRight": 0.5,              # Right margin in inches (approximately 2 cm)
            "displayHeaderFooter": False,    # Do not display headers and footers
            "preferCSSPageSize": True,       # Prefer CSS page size
            "generateDocumentOutline": False,# Do not generate a document summary
            "generateTaggedPDF": False,      # Do not generate tagged PDF
            "transferMode": "ReturnAsBase64" # Return the PDF as a base64 string
        })
        return pdf_base64['data']
    except WebDriverException as e:
        raise RuntimeError(f"WebDriver exception occurred: {e}")
    finally:
        driver.quit()

def get_chrome_browser_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Start the browser in full screen
    options.add_argument("--no-sandbox")  # Disable sandboxing to improve performance
    options.add_argument("--disable-dev-shm-usage")  # Use a temporary directory for shared memory
    options.add_argument("--ignore-certificate-errors")  # Ignore SSL certificate errors
    options.add_argument("--disable-extensions")  # Disable browser extensions
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("window-size=1200x800")  # Set the browser window size
    options.add_argument("--disable-background-timer-throttling")  # Disable background timer throttling
    options.add_argument("--disable-backgrounding-occluded-windows")  # Disable backgrounding of occluded windows
    options.add_argument("--disable-translate")  # Disable automatic translation
    options.add_argument("--disable-popup-blocking")  # Disable popup blocking
    #options.add_argument("--disable-features=VizDisplayCompositor")  # Disable the Viz display compositor
    options.add_argument("--no-first-run")  # Disable the initial browser setup
    options.add_argument("--no-default-browser-check")  # Disable the default browser check
    options.add_argument("--single-process")  # Run Chrome in a single process
    options.add_argument("--disable-logging")  # Disable logging
    options.add_argument("--disable-autofill")  # Disable form autofill
    #options.add_argument("--disable-software-rasterizer")  # Disable software rasterizer
    options.add_argument("--disable-plugins")  # Disable browser plugins
    options.add_argument("--disable-animations")  # Disable animations
    options.add_argument("--disable-cache")  # Disable cache
    #options.add_argument('--proxy-server=localhost:8081')
    #options.add_experimental_option("useAutomationExtension", False)  # Disable Chrome automation extension
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])  # Exclude automation and logging switches

    options.add_argument("--single-process")  # Run Chrome in a single process
    return options

def printred(text):
    RED = "\033[91m"
    RESET = "\033[0m"
    print(f"{RED}{text}{RESET}")

def printyellow(text):
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    print(f"{YELLOW}{text}{RESET}")
