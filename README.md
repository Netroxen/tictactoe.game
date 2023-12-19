# Tic Tac Toe

A simple Tic Tac Toe game with a win counter and continuous play functionality.

## HowTo

This Python app does not require additional libraries to run.

To run the game, execute the following:

```bash
docker run -it --rm --name tictactoe -v "$PWD":/usr/src/app -w /usr/src/app python:3.7-alpine python main.py
```

To run the included example tests for the TicTacToeApp, execute the following:

```bash
docker run -it --rm --name tictactoe -e TICTACTOE_TEST="true" -v "$PWD":/usr/src/app -w /usr/src/app python:3.7-alpine python -m unittest tictactoe/tests/test_app.py
```

If everything ran successfully, the tests should return `OK`.

## Notes

Alternatively, the `main.py` can be executed directly from a local Python
environment.

Credits: Jesse Stippel
