# Testing how-to

To test colorgram.py, first get py.test:

```
pip install pytest
```

Then install colorgram from the development copy, preferably in editable mode if you're doing any edits. Having a virtualenv helps here. In the top-level colorgram.py repository directory:

```
pip install -e .
```

# Making a new test

To add a new test (if one would ever be needed), put a new image in `tests/data`. Make sure you have node installed, and run the following to set up colorgram.js:

```
npm install colorgram
```

Then, to generate new test data, run:

```
node generate_control_data.js data/whatever_you_named_it.png data/probably_the_same_name.json
```

After that, simply follow the pattern in `tests/test_extraction.py` and add another test for the newly created files.
