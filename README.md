# <img src= "https://user-images.githubusercontent.com/51865580/179876417-d2feba7c-43e9-40fb-997c-fbb16f98d14b.png" data-canonical-src= "https://user-images.githubusercontent.com/51865580/179876417-d2feba7c-43e9-40fb-997c-fbb16f98d14b.png" width = "50" height = "50" /> TeamRandomizerBot 

> *If you wish to use this bot in your discord server simply clone the repository and run the trbot.py file.*

<p align="center">
<img src= "https://user-images.githubusercontent.com/51865580/179876418-0e8028b6-602c-4c2a-88d2-3326604889bd.png" data-canonical-src= "https://user-images.githubusercontent.com/51865580/179876418-0e8028b6-602c-4c2a-88d2-3326604889bd.png" />
</p>

<br />
Project Goals:
- .....

Future Goals:
- Host discord bot online so users can simply invite the TR bot into their discord server and use it freely.
  - *Currently trying to find a free hosting service with persistance. Since TR bot utilizes SQLite3 for its database
  the hosting service has to consistantly update the database so that adding, removing, and editing players is instant
  for the user.*
<br />
<br />

Documentation:
> *Here i will go over how to use the bot and its functionality.*
``` 
To view all the possible commands for the bot type "/tr".
TRbot utilizes group commands with the prefix /tr to make it easier for the user.
```
<img src= "https://user-images.githubusercontent.com/51865580/179876423-5d95d078-16e5-4789-a226-f7ce7aa10102.png" data-canonical-src= "https://user-images.githubusercontent.com/51865580/179876423-5d95d078-16e5-4789-a226-f7ce7aa10102.png" />

```
To get help on how to use the commands and there limitations use "/tr help".
This command provides the necessary documentation for all the commands.
```
<img src= "https://user-images.githubusercontent.com/51865580/179876419-0fa63fa7-310d-4ccf-8ecf-cd6782ff4999.png" data-canonical-src= "https://user-images.githubusercontent.com/51865580/179876419-0fa63fa7-310d-4ccf-8ecf-cd6782ff4999.png" />

```
To add a player to the database use "/tr add-player".
The names in the database are all unique and do not account for capitals or any special characters.

On success the bot will return the success embed as shown below:
```
<img src= "https://user-images.githubusercontent.com/51865580/179876414-5a62205f-0f1f-409a-b4df-e9f8046d7435.png" data-canonical-src= "https://user-images.githubusercontent.com/51865580/179876414-5a62205f-0f1f-409a-b4df-e9f8046d7435.png" />

```
On failure the bot will return the failed embed as shown below:

The same principle applies for removing players, editing players, adding maps, and removing maps.
The bot will always return the appropraite embed with comments.
```
<img src= "https://user-images.githubusercontent.com/51865580/179876415-d61b7d85-4c83-4073-934a-fbc88546109d.png" data-canonical-src= "https://user-images.githubusercontent.com/51865580/179876415-d61b7d85-4c83-4073-934a-fbc88546109d.png" />

```
To check all the players in the database currently use "/tr players".
```
<img src= "https://user-images.githubusercontent.com/51865580/179876421-66d6174e-638b-476e-bb56-ae6b6dd59eee.png" data-canonical-src= "https://user-images.githubusercontent.com/51865580/179876421-66d6174e-638b-476e-bb56-ae6b6dd59eee.png" />

```
Similarly, the same can be done for "/tr maps".
```
<img src= "https://user-images.githubusercontent.com/51865580/179876420-668175dc-8adc-488e-80cd-e105b8655836.png" data-canonical-src= "https://user-images.githubusercontent.com/51865580/179876420-668175dc-8adc-488e-80cd-e105b8655836.png" />
