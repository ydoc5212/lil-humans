# lil-humans
Watch your lil humans grow! This is an open-source simulation project based on [this Scratch project](https://scratch.mit.edu/projects/25031437/) from 2014.

## Features
*dust*
## Installation & Usage
Clone the GitHub repo and run `simulation.py` with the following command-line arguments as such:

`python --ticks [# ticks] --humans [# initial humans]`
## Screenshots
![image](https://user-images.githubusercontent.com/20691507/155107361-c6979692-0640-41d5-8f29-686a7a1456ad.png)

# For open-source contributors
It's important to set up some ground rules for contributions to the project. Here are some of our values:
### Modularity
* Code Style: Make it easy to revamp your systems in the future, or remove them if they're breaking things. 
* Temporal Modularity: (for functions that take ticks as input) I want this sim to be as temporarlly-scalable as possible. That is to say, implementations should be easily changeable if '1 tick' were to change from years to days. The ticks are currently years, but perhaps could be made into smaller units of time in the future for more granular simulations. Adding in behaviors on those smaller levels with introduce the variation necessary to make an interesting grand-scale sim.
### First-principles
The idealistic goal is for this sim to zoom as for in and out as we can; it should be persistently entertaining to watch our lil humans interact and figure things out for themselves. Encoding as basic of principles as is necessary to give rise to emergent patterns, but make simplifying assumptions as necessary to create scaffolding that fleshes out the project.
