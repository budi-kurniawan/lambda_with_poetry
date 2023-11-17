# Lambda handler with Poetry

## Prerequisites
- Python 3.10 or later
- Poetry
- An S3 bucket created with AWSLambdaExecute policy attached to the corresponding role.

## Starting the Project
```
 $ poetry new lambda-with-poetry
 $ cd to lambda-with-poetry
 $ Open the pyproject.toml file and add dependencies to the [tool.poetry.dependencies] section.
 $ Create a lambda_handler.py file.
 $ Write Lambda handler in the file.
 $ Run #poetry install# to create a virtual environment:
```

## Creating A Package (zip file)
AWS Lambda accepts a zip file containing one or multiple handlers plus all the dependencies. See https://docs.aws.amazon.com/lambda/latest/dg/python-package.html.

```
$ poetry build # it will create a dist folder
$ poetry run pip install --upgrade -t package dist/complete-file-name.whl
$ cd package 
$ jar cvf ../artifact.zip -R .
$ or zip -r ../artifact.zip . -x '*.pyc'
```

## Running the Test
```
$ python test.py
```

## References
- https://chariotsolutions.com/blog/post/building-lambdas-with-poetry/
- https://stackoverflow.com/questions/48945389/how-could-i-use-aws-lambda-to-write-file-to-s3-python
- https://docs.python.org/3/library/asyncio-task.html
- https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
