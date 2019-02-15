# Azurefunctions-keras-model

I've pre-trained a model to predict the Handwritten digits based on the MNIST dataset(http://yann.lecun.com/exdb/mnist/). It will not be shown how to train the model as it is not the scope of this 
tutorial. This tutorial will show you how to user Azure Functions to deploy the model. This tutorial will show you how to create an http trigger but also how to automatically 
trigger on uploading images into blob store.
This tutorial is only tested on a windows machine.
stuff
blob trigger
can also easily be converted to a http trigger.


# Prerequisites

Before you get started a working python installation is required. This 
For this tutorial i've used python 3.6.6 (https://www.python.org/downloads/release/python-366/)

- Install Azure Functions Core Tools version 2.2.70 or later (requires .NET Core 2.x SDK and Node.js).
	- https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local#v2
- Install the Azure CLI version 2.x or later.
	- https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest
- Install Docker Dekstop for your OS.
	- https://www.docker.com/products/docker-desktop
	
In order to host the functions locally you need a virtual environment. If you have a fresh installation of python you can install the library virtualenv to create virtual environments(make sure 
to add python as environment variable):
```
pip install virtualenv
```
Open a powershell or cmd window and navigate to the cloned repository:
```
cd <path to local repository>
```
Create a virtual environment for your project:
```
virtualenv venv --python=<path to python 3.6>
```
Activate the virtual environment:
```
venv\scripts\activate
```
Now install the dependencies in order to host the functions locally:
```
pip install -r venv_requirements.txt
```
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
```

Now we are ready to create our first function. For this we again use the Azure functions core tool. 

In order to run the function use the following command:
``` 
cd <Path to repository>\keras-mnist-model\ 
func host start
```
It should look like following:
![host_start](https://github.com/nkma1989/azurefunctions-keras-model/blob/master/readme_images/host_start.jpg)

The localhost endpoint of your function will be shown in the console as can be seen in the red box.


# Testing the http-trigger

Once the function is running open a new powershell or cmd window and navigate to the repository:
```
cd <path to local repository>
```
Activate the virtual environment:
``` 
venv\scripts\activate
```
Run the testAPI.py file using the parameter -e <Endpoint> to point to the function endpoint.
```
python testAPI.py -e http://localhost:7071/api/mnist-httptrigger
```
This python script will take the images located in testimages and send it to the function API and show the label vs. the prediction. It can also be used to test published functions by passing
the published endpoint. The output should look like the following:

![host_start](https://github.com/nkma1989/azurefunctions-keras-model/blob/master/readme_images/func_test.jpg)

# Blob Trigger
for this to work, you need a storage account on azure. look at the section Publishing to Azure to see how that can be done.
stuffff
change the storage account under local.settings.json



# Publishing to Azure
First step of publishing to Azure is to create the necessary resources. For this we will use the Azure CLI, which requires a login. Open a powershell or cmd console and type.
```
Az login
```
This will open a browser and you will be asked to login with your Azure user.
Now that we are logged in we can begin setting up the resources. First we will create a resource group.
```
az group create --name keras-mnist-tutorial --location westeurope
```
Next we will set up a storage account.
```
az storage account create --name mnistfunctionstorage --location westeurope --resource-group keras-mnist-tutorial --sku Standard_LRS
```
Now open the azure portal and click on your deployed storage account and create 2 blob containers as shown in the following image(used by the blob trigger function):

![host_start](https://github.com/nkma1989/azurefunctions-keras-model/blob/master/readme_images/storage_setup.jpg)

Next step is creating the Azure Function App.
```
az functionapp create --resource-group keras-mnist-tutorial --os-type Linux --consumption-plan-location westeurope  --runtime python --name keras-mnist-functionapp --storage-account  mnistfunctionstorage
```
We need to set a few app settings before publishing(You might need a subscription ID input for this function if you have multiple subscriptions on your Azure user):
```
az functionapp config appsettings set --name keras-mnist-functionapp --resource-group keras-mnist-tutorial --settings ModelWeightsPath=./modelfiles/Keras-Mnist_weights.pkl ModelJSONPath=./modelfiles/Keras-Mnist_json.pkl
```


Now we are ready to publish our functionapps(you need to be in the keras-mnist-model folder). The --build-native-deps will compiles the dependencies in a docker container and deploy the functionapp as such. 
```
func azure functionapp publish keras-mnist-functionapp --build-native-deps
```
This step might take a while and the console output should look like this:

![host_start](https://github.com/nkma1989/azurefunctions-keras-model/blob/master/readme_images/deploy_func.jpg)

When finished the output should look as follows. In the red box the endpoint for the published function can be seen:

![host_start](https://github.com/nkma1989/azurefunctions-keras-model/blob/master/readme_images/func_endpoint.jpg)

You can test this endpoint using the python script testAPI.py
```
python testAPI.py -e https://keras-mnist-functionapp.azurewebsites.net/api/mnist-httptrigger?code=FcRtK6oRY3ookPegxwv04ba2HDapTuOgwCg6lfPsdplVC9miouRTuw==
```
To clean up resources you can delete the resource group by running the following command:
```
az group delete --name keras-mnist-tutorial
```












