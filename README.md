# Extracting-products-data-from-Walmart-web-page

Hi!

In this case we are going to web scrape the Walmart online marketplace. Usually this kind of pages have strong security systems like:

 - Rendered Javascript code that hides html code
 - Captcha
 - Robots.txt file that denies requests to the user if the find something suspicious in your actions
 - Suspicious headers and many request from the same IP adress

We gotta be prepared!

In this case this page has all the preveious mentioned points so we gotta be very carefull about our actions. The most recommended action you could take in these cases are extract the data and save it as txt file so you can check the request response and see what kind of security has.

We use Beautifullsoup to turn it into and xml file but turns out that only loads some data and not all the data.

Analysing deeper we see in the console where all code is loaded once we do the http request only part of the data is loaded:

![image](https://github.com/user-attachments/assets/762e3bb8-fd14-4a84-843f-d06770a50cd8)

We have two options:

- Use Playwright or Selenium to wait for the data being loaded(slower)
- Use patters and algorithms to extract non-structured data from the request(faster)

We choose the **second option**:

You can see how we don't use Selenium or Playwright to extract the data:



https://github.com/user-attachments/assets/dc82e703-179a-42db-a5d5-b2fd45afa821



https://github.com/user-attachments/assets/8cd55b25-2480-43f2-8872-614d5e0b3d89




https://github.com/user-attachments/assets/816a605b-26e1-492f-aa46-82c646403314







