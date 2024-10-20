from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from .serializer import ScrapeSerializer

@api_view(['POST'])
def scrape_site(request):
    # Deserialize incoming data
    serializer = ScrapeSerializer(data=request.data)
    
    if serializer.is_valid():
        # Extract the validated URL
        url = serializer.validated_data['url']

        # Setup Edge WebDriver
        edge_driver_path = r'D:\selenium\msedgedriver.exe'
        options = Options()
        options.use_chromium = True
        options.add_argument("--headless")  # Run browser in the background
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")

        service = Service(edge_driver_path)
        driver = webdriver.Edge(service=service, options=options)

        try:
            driver.get(url)

            # Wait until the body element is present (indicating the page has loaded)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Extract the entire text from the <body> of the page
            body = driver.find_element(By.TAG_NAME, "body")
            whole_text = body.text
            
            return Response({"text": whole_text}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        finally:
            driver.quit()  # Ensure the driver is closed

    # Return validation errors if any
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
