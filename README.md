# ArcBot v1.0

If you're like me, you love the gym. UC Davis recently opened up their worldclass gym to the school and public, but they only are running at 10% capacity and as you can imagine, it's created a botteneck. 

Here's a little from their site: 

>There is a max of one reservation per person per day. Reservations are for 1 hour and 30 minutes, followed by a 30 minute sterolization period. Facility access will closed during the final 20 minutes of each time slot, and no additional patrons can enter at that time.

Typically you need to book 3 days in advance if you want a chance at a workout so I wanted to automate reserving timeslots for my university's gym. 


### First Install some basic dependencies.

First you want to fork the source code in this project. This means you make a copy of my project into your github account. Then you want to create a local copy of that repository as follows:

```bash

git clone https://github.com/YOUR-USERNAME/Spoon-Knife

```


We will create a conda virtual environment to encapsulate our project.


```bash
conda create -n arcbot python=3.8
conda activate arcbot
```


Framework that allows us to interact with HTML elements.
```bash
pip install selenium
```

### [Download latest GeckoDriver](https://github.com/mozilla/geckodriver/releases).
This is the same piece of software which Firefox uses to handle things like implementing the DOM, navigation through hyperlinks, data submission through forms and enforcing security policy between documents. 


In Linux:
```bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-linux32.tar.gz

tar -xzf geckodriver-v0.28.0-linux32.tar.gz
sudo mv -f geckodriver /usr/local/bin/geckodriver
```

In Windows:

Download [Here](https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-win64.zip)
and unzip in the same directory your code is in.

Now you want to make sure that you have Firefox installed into your computer. 


Simply change the kerebos credentials in `main.py` to your account info and then run:

```python 

python main.py

```