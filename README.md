# Lambda Handler with Poetry

## Prerequisites
- Python 3.10 or later
- Poetry
- An S3 bucket created with **AWSLambdaExecute** policy attached to the corresponding role. (See https://docs.aws.amazon.com/AmazonS3/latest/userguide/add-bucket-policy.html)

## Attaching A Policy to Lambda-Linked Role
After you create an S3 bucket and a lambda handler, it is crucial to follow these steps to grant permissions to the lambda handler to write to the S3 bucket:
- Go to the Lambda's Configuration page
- Click the "Permissions" tab
- Click on the role name, a new window will open
- Select the "Permissions" tab of the role
- Click the Add permissions button and select "Attach policies"
- Search for "AWSLambdaExecute" and add the permission to the role


## Starting the Project
- Create a new poetry project:
```
$ poetry new lambda-with-poetry
$ cd to lambda-with-poetry
```
- Open the pyproject.toml file and add dependencies to the [tool.poetry.dependencies] section.
- Create a lambda_handler.py file.
- Write Lambda handler in the file.
- Run this command to create a virtual environment:
```
$ poetry install
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

## Running MyPy
```
$ python lambda_function.py
```

## Running PyLint
```
$ pylint lambda_function.py
```

## References
- https://chariotsolutions.com/blog/post/building-lambdas-with-poetry/
- https://stackoverflow.com/questions/48945389/how-could-i-use-aws-lambda-to-write-file-to-s3-python
- https://docs.python.org/3/library/asyncio-task.html
- https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
