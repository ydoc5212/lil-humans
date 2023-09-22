# lil-humans
Watch your lil humans grow! This is an open-source simulation project based on [this Scratch project](https://scratch.mit.edu/projects/25031437/) from 2014.

## Features
Currently a PyWebIO-based browser sim!
## Installation & Usage
* [Install Git](https://git-scm.com/downloads) and [Python](https://www.python.org/downloads/)
* Click the bright green 'Code' button and copy the URL. We will paste this later.
* Open Command Prompt (Windows) or Terminal (Mac)
* Now run the following commands into your terminal window:
* type `pip install pipenv`
* type `git clone [paste url here]`
* type `cd lil-humans`
* type `pipenv install`
* type `pipenv run simulation.py`

Your browser should open "PyWebIO" in a new tab. That's it!
## Screenshots


# For open-source contributors
It's important to set up some ground rules for contributions to the project. Here are some of our values:
### Modularity
* Code Style: Make it easy to revamp your systems in the future, or remove them if they're breaking things. 
* Temporal Modularity: (for functions that take ticks as input) I want this sim to be as temporarlly-scalable as possible. That is to say, implementations should be easily changeable if '1 tick' were to change from years to days. The ticks are currently years, but perhaps could be made into smaller units of time in the future for more granular simulations. Adding in behaviors on those smaller levels with introduce the variation necessary to make an interesting grand-scale sim.
### First-principles
The idealistic goal is for this sim to zoom as for in and out as we can; it should be persistently entertaining to watch our lil humans interact and figure things out for themselves. Encoding as basic of principles as is necessary to give rise to emergent patterns, but make simplifying assumptions as necessary to create scaffolding that fleshes out the project.
