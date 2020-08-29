from lambda_function import LambdaFunction
from api_gateway import Authorizer, Resource, Method

if __name__ == '__main__':

    # some lambda function name
    functions = [
        'LambdaFunctionName',
    
    ]
    for function in functions:
        newLayerArn ='YOUR_LAYER_ARN_HERE'
        layerSplited = newLayerArn.split(':')
        newLayer = layerSplited[-2] # Layer name
        newLayerVer = layerSplited[-1] # Layer Version
        
        # get lamda by function name
        thisFunction = LambdaFunction.get(function)
        
        for oldLayer in thisFunction.layers:
            if newLayer in oldLayer:
                # if layer exist
                thisFunction.layers.remove(oldLayer) # delete old layer
        # append new version
        thisFunction.layers.append(newLayerArn)
        # update function layer
        function = LambdaFunction.updateLayer(thisFunction.name, thisFunction.layers)
