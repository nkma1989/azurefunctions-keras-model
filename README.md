# azurefunction-keras-model

stuff
blob trigger
can also easily be converted to a http trigger.


# Prerequisites

Before you get started a working python installation is required. This 
For this tutorial i've used python 3.6.6 (https://www.python.org/downloads/release/python-366/)

- Install Azure Functions Core Tools version 2.2.70 or later (requires .NET Core 2.x SDK).
	- https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local#v2
- Install the Azure CLI version 2.x or later.
	- https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest
	
	
	
pip install virtualenv

virtualenv venv --python=<path to python 3.6>

pip install -r requirements.txt

# Creating project resources

initially we are creating a function project using the azure functions core tools
```
func init keras-mnist-model

select python as the worker runtime
```
 This directory is the equivalent of a function app in Azure and can contain multiple functions that share local and
 hosting configurations.
 
# HTTP trigger function
 
 Initially we are creating a function that triggers through an http request. First thing you need to do is open a 
 powershell or cmd window. and activate the virtual environment then navigate to the \keras-mnist-model folder.
``` 
venv\scripts\activate
cd <folderpath>
```

Now we are ready to create our first function. For this we again use the Azure functions core tool. 

In order to run the function use the following command:
``` 
cd <\keras-mnist-model folder>
func host start
```
It should look like following:
![host_start](readme_images\host_start.jpg)