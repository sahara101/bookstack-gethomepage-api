# bookstack-gethomepage-api
Combine bookstack books and pages into one API call.

This is a docker container which will enable you to create a widget for [Bookstack](https://www.bookstackapp.com) in [Homepage](https://gethomepage.dev/main/).

<img width="379" alt="image" src="https://github.com/user-attachments/assets/8829fd3a-5c27-4f4b-98c1-475480196a7a">

# Docker-compose
```
bookstack-gethomepage-api:
    image: ghcr.io/sahara101/bookstack-gethomepage-api:latest
    container_name: bookstack-gethomepage-api
    ports:
      - "4001:4001"
    environment:
      BOOKSTACK_URL: https://bookstack.domain.tld
      AUTH_TOKEN: TOKEN-ID:TOKEN-SECRET #Bookstack API Token
      UPDATE_INTERVAL: 300
```
## How to get Bookstack API 
User > My Account > Access & Security > Create Token

# Homepage

Edit services.yml and add the following to your Bookstack service.
```
widget:
  type: customapi
  url: http://{dockerhost}:4001
  mappings:
    - field: total_books
      label: Total Books
    - field: total_pages
      label: total Pages
```
