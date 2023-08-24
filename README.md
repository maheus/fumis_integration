# fumis integration testing  
this integration using modified lib https://github.com/frenck/python-fumis

- checkout repository in custom_components/ directory:

```git  clone -b refactor --single-branch  https://github.com/maheus/fumis_integration.git fumis```
or
```git  clone -b refactor --single-branch  git@github.com:maheus/fumis_integration.git fumis```

- copy Directory `custom_components/fumis/` in your `custom_components/`
- restart HA
- adding integration with HA ui (configuration -> integrations -> add integration -> search fumis).
