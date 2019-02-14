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

#Creating project resources

initially we are creating a function project using the azure functions core tools
```
func init keras-mnist-model
```
 This directory is the equivalent of a function app in Azure and can contain multiple functions that share local and
 hosting configurations.
 
 # HTTP trigger function
 
 Initially we are creating a function that triggers through an http request. First thing you need to do is open a 
 powershell or cmd window. navigate to the \keras-mnist-model folder and activate the virtual environment.
``` 
cd <folderpath>
venv\scripts\activate
```