Refer to the proj2.pdf for the assignment instructions

Major changes:
1. Arranging global variables and comments. The previous version (project 1) looked too messy. So I redesigned the python file
2. Reading the following sensor data: Cliffs, Bumpers and wheel drops
3. Uploading and playing a song. (Song choice: Imperial March)

Thought process:
Ideally I would have liked to use the Stream function (Refer to Roomba open interface spec)
Stream would have allowed me to read all the necessary sensor data from the Roomba with one write instruction
However I could not decipher the values stream gave me. I tried using struct to unpack and tried using the raw return values. 
The Roomba interface spec was too vague in their in explanation and I had to give up on that method due to time constraints. 

Instead I implemented sempahores. There is a constant need to read sensor data. So if you send multiple threads to write and read 
from the serial port, you get a resource busy error. It makes sense as when one thread is trying to read data from the serial port
another thread is simultaneously trying to write to the serial port. Hence by implementing semaphores for each method, it let me avoid the 
synchronisation problem altogether. 

Due to a lack of time, I did not implement data logging. (It was extra credit)

Pitfalls:
You need to press and hold the clean button for 1-2 seconds and let go immediately after. After a short delay, the Roomba will start moving.
The reason being -> semaphores. Pressing the clean button while another method is in the crtical section yields no result. By pressing and
holding the clean button for 1-2 seconds you would be at the exact time that the clean button method would read the state of the button.
Holding it for longer means the method reads the button press twice, resulting in a negation of the intial button press. 
