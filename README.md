# docker run to docker-compose.yaml converter

This is a simple web tool to help convert ```docker run``` command into ```docker-compose.yaml``` file. It will take most common parameters and create a useful file.

![Example page 1](/img/example1.png)

## Usage ##

Personally I recommend using venv for running apps, just to not taint your local environment.

Clone this repository, cd into into it and run

```python3 -m venv .```

After that install dependancies:

```pip install -r requirements.txt```

Start the app:

```python3 app.py```

Navigate to [The app](http://localhost:5000).

## Windows, Mac setup

Sorry, can't help you. I don't use Windows and don't own a Mac. Open a Support ticket with message on how to make it work if you do know how to and I'll add it.

![Sorry](/img/sorry.png)

## Disclaimer

This was written mostly by ChatGPT and not checked for errors, exploits and command sanitation. That's why it's limited to localhost IP. Still use with care! You were warned.
