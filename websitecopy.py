import requests
import os
import re

def copy_website(url):
    # Make a GET request to the specified URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Get the HTML source code from the response
        html_source = response.text
        
        # Create a directory to store the website files
        website_dir = "website"
        os.makedirs(website_dir, exist_ok=True)
        
        # Write the HTML source code to a file
        with open(f"{website_dir}/index.html", "w") as file:
            file.write(html_source)
        
        # Find all the URLs for resources (e.g., images, stylesheets, scripts)
        resource_urls = re.findall(r'(?:src|href)="([^"]+)"', html_source)
        
        # Download each resource and save it to the website directory
        for resource_url in resource_urls:
            # Make sure the resource URL is absolute
            if not resource_url.startswith("http"):
                resource_url = url + resource_url
                
            resource_response = requests.get(resource_url)
            
            if resource_response.status_code == 200:
                filename = resource_url.split("/")[-1]
                with open(f"{website_dir}/{filename}", "wb") as file:
                    file.write(resource_response.content)
            
        print("Website copied successfully")
    else:
        print("Failed to copy website")

# Example usage
copy_website("https://www.hackittech.com/")

