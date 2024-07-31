# Florae Demo with Appium
Android automation demo with Appium.

The implementation of the `TestCore` class in [src/tests/core.py](src/tests/core.py) allows you to have IntelliSense for methods from `self.driver` such as `.find_element()`.  
I was not able to identify how to accomplish this using a fixture approach.

## To-do
- Write more actual tests (lol)
- Write CLI script
- Implement docker
- Write screen recording methods

## Setup
### Prequisites
[python](https://www.python.org/downloads/)  
[poetry](https://pipx.pypa.io/stable/installation/)  
[appium](https://appium.io/docs/en/2.0/quickstart/install/)  
[avd](https://developer.android.com/studio/run/emulator)  
[allure](https://allurereport.org/docs/install/)

### Install dependencies
```bash
cd <project_directory>
poetry install
```

### Set venv
```bash
poetry env use <python version>
```

### Configuration file
Ensure `android_id_virtual` in [config.cfg](config.cfg) is set to the name of your AVD.  
This can be found using the command `emulator -list-avds`

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