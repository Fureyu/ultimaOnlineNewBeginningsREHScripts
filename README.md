# Original README by TheWarDoctor95:
```
# Razor Enhanced Scripts
These are the scripts that I have written for the [Razor Enhanced client launcher](https://www.razorenhanced.org/) for the [Ultima Online video game](https://uo.com/). Some of these scripts were inspired by code written by other authors for the [UOSteam client launcher](https://www.uosteam.com) (e.g. [train_AnimalTaming.py](./train_AnimalTaming.py)), while others originated from me (e.g. [pvm_pvp_provocation.py](./pvm_pvp_provocation.py), the first [Ultima Online tameable animal compendium in script format](glossary/tameables.py), and the first [Ultima Online spell compendium in script format](glossary/spells.py)). Any work from others is cited in the title block of the file.

### A bit about how this is organized ###
At the time of this writing, RE does not support the ability to add scripts to the client out of any directories except for \<RE Install Directory\>\Scripts. This means that we are unable to move the scripts that we want to run from the client into subdirectories within the Scripts directory. To help maintain an organized file structure, each file starts with what its primary function falls under, for example:
- pvm_pvp for Player vs. Monster and Player vs. Player
- resource for resource gathering
- train for training skills

While we are unable to directly run files in subdirectories, we can import files from subdirectories that have been made into submodules by adding the \_\_init\_\_.py file to them (e.g. [the glossary submodule](glossary)). This is handy for having a central location for code that is referrenced in multiple files.
```

# Original from Fureyu:

### Quick Note:
If any file does not follow the above mentioned naming standards that TheWarDoctor95 set, it is something I created from scratch and may or may not work. The exception being automine.py, which I implemented from the automine script found on the Razor Enhanced website examples.

### How to extract properly ###
When you extract these files, do so directly into the `Scripts` directory in your Razor Enhanced file system, not into the same named folder as the .zip that you download. All of the <scriptName>.py files need to be in the `Scripts` directory to run, and all of the assets that they import will need to be there as well.

### A bit about what I've done here ###
This repository is adaptations done to TheWarDoctor95's scripts in order to be used on Ultime Online New Beginnings free shard. I am making edits to them as I encounter issues while running them while playing on the server. 
If you would like to play on the server, it can be found here: https://uonewbeginnings.com/
