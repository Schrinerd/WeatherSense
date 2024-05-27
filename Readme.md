# WeatherSense
This is a hobby project to play with inside and outside temperatures and a Raspberry Pi:
Inside temperatures are logged from a temperature sensor connected to the GPIO pins.
Outside temperatures are retrieved from OpenWeatherMap.org's API.
Temperatures are then graphed with Matplotlib and saved as an image.
The image is viewed using the RPi as a local webserver.

-DJS, 2022

### Prerequisites:
-Rpi w/ lighttpd (as in, one running Pi-Hole)

#### Add another folder to /var/www/html and set its permissions
from https://medium.com/@haquangvu/how-do-i-give-myself-access-to-var-www-to-create-and-edit-files-and-folders-in-it-without-sudo-ac93ca943a26
sudo mkdir /var/www/html/pitemp
sudo chown $USER:www-data /var/www/html/pitemp
sudo chmod g+s /var/www/html/pitemp
sudo chmod o-rwx /var/www/html/pitemp

Put an "index.html" file in /var/www/pitemp
