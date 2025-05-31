# AO Build Checker
Purpose: Identify a build given stat points and show a list of skills one can learn given said stat points.

I'm not doing a proper database nor an online database for this, so I'm putting the data CSV here. In real practice, for anyone interested in coding, **you do NOT upload the data into your Github.**

## How to run
This project makes use of python and uv to run. Check how to install uv on your computer [here](https://docs.astral.sh/uv/#installation), and how it can install python for you [here](https://docs.astral.sh/uv/guides/install-python/).

Once you have uv, you'll have to sync the libraries used with
```
uv sync
```

And then, you'll be able to run the code by doing 
```
uv run buildcheck.py
```

## About the code

The code will show you both the build name and the percentages alloted to each stat. It will also show the different skills you can learn. Magic and Strength skill options have NOT been taken into account. Weapon levels are shown for the maximum weapon level the build would be able to use for each different skill, and takes into account the uniqueness and exclusiveness of a skill.

The code offers stat input given a file, and result output onto a file. This can be achieved using the command line arguments ``-i`` and ``-o`` respectively.

Here's an example on how to use both:
```
uv run buildcheck.py -i my_build.txt -o result.txt
```

This will read the file named ``my_build.txt`` and write the results into the file named ``result.txt``.