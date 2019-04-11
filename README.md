# Display mongo records for NowTv test users
Connect to Mongo and find user records
 - This tool requires corporate network access and assumes QA tests have been checked out 
### Example:

```
passes [test username|profileId]
$ passes movies
$ passes 33445566
```

## Dependencies

- Python3
- Pyenv
- zsh complete
- Popcorn Mongo db 

## Installing to the pyenv 'tools3'

**Installation**

```
pyenv activate tools3
pip install .
pyenv deactivate

# or use the script:
reinstall
```

**Uninstalling**

```
pyenv activate tools3
pip uninstall passes
pyenv deactivate
```

**Development**

```
pyenv local tools3
pip install -e .
py.test -vs
```

**zsh Completion**

```
Add script to .oh-my-zsh/custom/plugins
```

**Testing**
```
cd tests
py.test -v

py.test --cov-report html --cov user.passes
open htmlcov/index.html
```
