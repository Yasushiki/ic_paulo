# IC PAULO

## What is
This is a website that I made for a friend's university project using Flask. Please see it not as the full project, but as a website template. Since I am NOT a designer nor a frontend dev, the CSS of this website is not mine, but from Claude.ia.

## Features and good points
### Multilingual
The website has support for multiple languages, being really easy to add new ones.  
The supported languages are listed in the ```SUPPORTED_LANGUAGES``` dictionary in ```app.py```, and unsupported languages will be redirected to the default language (in this case, English). Also, the code supports variations of the same language (pt-BR and pt-PT, en-US and en-GB, etc.).

### SSE
This is the main feature of the website, but unfortunately, you won’t be able to fully see it. This website will be running on a Raspberry Pi that has some sensors connected to it. It uses Server-Sent Events to send the sensor information to the local server so it can be shown on the website. You can test it by altering the subprocess in ```app.py``` from ```["python", "-u", "script.py"]``` to something like ```["ping", "example.com"]``` on Linux or ```["ping", "-t", "example.com"]``` on Windows, and by changing the ```comecaComNumero``` and ```updateValues``` functions inside ```index.html``` so it shows the ping output changing in real time.

### OOP without classes
This project has polymorphism: The website can have different information, layouts, formats, and so on, based on the current language.  
This project has inheritance: Almost all the HTML is inside ```base.html```, which is inherited by the other HTML files.  
This project has abstraction: The website doesn’t show the backend. :D  
This project has encapsulation: Each type of information is encapsulated inside a different file, and the title and content of each page are encapsulated inside a different ``block``.

---
Feel free to use this as a first template for your own website.
