## Lambda 

This is a very simple lambda function. Install boto3 to the directory

```
pip3 install boto3 --target ./<projectdir> (--system may need to be appended because ubuntu flavors can break this)
```

Zip it all up. Create a blank lambda function with permissions to publish to SNS and this works. I'll make this do more soon.