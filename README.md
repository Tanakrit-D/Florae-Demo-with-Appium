# Florae-Demo-with-Appium
 Android automation demo with Appium.

## To-do
- Write some actual tests (lol)
- Implement POM
- Write CLI script
- Implement docker
- Write screen recording methods

## Setup
### Prequisites
[python](https://www.python.org/downloads/)  
[pipx](https://pipx.pypa.io/stable/installation/)  
[poetry](https://pipx.pypa.io/stable/installation/)
[appium](https://appium.io/docs/en/2.0/quickstart/install/)
[allure](https://allurereport.org/docs/install/)

### Dependencies
```bash
cd <project_directory>
poetry install
poetry env use <python version>
```

## Reporting (Allure)
Use of the pytest `addopts` configuration in `pytest.ini` means executing tests inline will automatically generate reports.

### Manually run tests
```bash
python -m pytest --alluredir reporting/allure-results
```

### Generate a report
```bash
allure serve reporting/allure-results
```

### Generate single page .html
```bash
allure generate --single-file reporting/allure-results --report-dir reporting/allure-single-page --clean
```

## Archiving reports
The default flag for running reports is `--clean-alluredir`.  
This means the previous output will be overwritten on each execution.  

If you'd like to archive previous reports, you can execute the following script:
```bash
bash bin/archive_reports.sh
```

This will move the contents of:
- `reporting/allure-results` to `reporting/historical/$timestamp/allure-results`  
- `reporting/allure-single-page` to `reporting/historical/$timestamp/allure-single-page`  

`$timestamp` refers to the format of `%Y-%m-%d_%H-%M-%S`.