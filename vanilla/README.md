# EC2 Instance Setup

Once you've created an EC2 instance, these files will turn it into an automated Minecraft server upon startup.

## systemd service

The minecraft.service file will allow the minecraft server to start automatically when your EC2 instance is started.
Before using it, you must ensure you have java installed, and update these values for your server:

 - WorkingDirectory must be set to the ABSOLUTE path from which you wish to run the server.
 - ExecStart must be updated with the path to the server.jar file, and the min and max memory allocation updated for your requirements.

To use the minecraft.service file, place it into /etc/systemd/system/

Then, run the following commands (may not have to run with sudo):

```
sudo systemctl daemon-reload
sudo systemctl start minecraft
sudo systemctl enable minecraft
```

These three commands will refresh the daemon configs, start the minecraft server, and enable it, meaning the server will run when the EC2 instance is started.