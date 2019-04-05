# Display mongo records for NowTv test users
Connect to Mongo and find user records
 - This tool requires corporate network access and assumes QA tests have been checked out 
### Example:

```
$ passes movies
$ passes 33445566
```

## Dependencies

- Python3
- Pyenv
- zsh complete


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
pip uninstall logs
pyenv deactivate
```

**Development**

```
pyenv local tools3
pytest
```

**zsh Completion**

```
Add script to .oh-my-zsh/custom/plugins
```

