# tidals
This python package contains analysis tools and utility functions that
may be helpful when loading, cleaning, and analyzing Tidepool data. This
package is currently in development.
 

## Contribute to the tidals package
If you want to add to this package, please submit a pull request


## Testing
This project uses the testing framework named pyTest. https://docs.pytest.org/en/latest/

After following the project setup instructions, including creating and activating the
virtual environment, you can simply run your tests within Bash

``` bash
# Run tests via  
pytest 
```

## Running Tests with Test Coverage 
This project uses pytest-cov (https://pytest-cov.readthedocs.io/en/latest/) to run test and produce code 
test coverage. 

To execute a basic test coverage report, run the following from within the virtual environment created during project setup
. This will give the output directly in the Terminal.
``` bash
# Run tests via  
pytest --cov 
```

To execute a detailed test coverage report, run the following command from within the virtual environment created during 
the project setup. 
This will create an htmlcov directory containing an index.html page with coverage details.
``` bash
# Run tests via  
pytest --cov --cov-report html
```