## Follow these steps for your manual tests:
1. Open the Postman app on your local machine or sign-in at https://identity.getpostman.com/login
2. Create a workspace or/and navigate to the relevant workspace.
3. Hit the "Import" button on the top left area of the browser's window.<br>
  ![Step 3](postman_img_1.png)<br>
4. Drag the [postman.json file](postman.json) into the import modal.<br> 
  ![Step 4](postman_img_2.png)<br>
5. Navigate to the 'Simple crawling app', click on the 'Variables' tab to change the 'host_and_port' to the relevant host and port of the application at your end. For e.g: http://localhost:3333<br>
  ![Step 5](postman_img_4.png)<br>
6. Navigate to the Body tab to modify your input and hit 'Send' to fire the request. Make sure the app is running on the 'host_and_port' above.<br>
  ![Step 6](postman_img_3.png)<br>