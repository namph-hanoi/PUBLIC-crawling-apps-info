# A SIMPLE CRAWLER APP

## How to run
- Run 'cp .env.template .env' to create a proper environment file for Docker and the app itself.
- Run 'docker compose up'. Make sure you already installed the latest docker version with its compose plugin.
- To run the test: firstly run 'docker compose up', then 'docker compose exec backend pytest'. It will execute all the unit tests along with the e2e tests.
### To run manual test on the running app, please refer to the [postman guide here](documents/POSTMAN.md)

## Notice:
### There are some limitations of the app like: 
- The targeted site would have a thresthold on the number of requests made from our app.
- The e2e testing also relies on the real API calls to the targeted site.
- Any API call would spend a considerable amount of time depending on the internet speed at the host and the number of apps we want to crawl. So does the e2e testing.

### On-going improvement:
- The 'Todo' comments in the code.
- Slice apps into injectable services when the app grows up.
- To overcome the thresthold of the API calls to the targeted site, we can crawl from its google cached version. However, sometimes the cached is not up-to-date.
