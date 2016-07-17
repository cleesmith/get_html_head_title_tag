# Python and AWS Lambda tutorial

***
#### July 17, 2016
> Added code to send results to Amazon's Simple Queue Service (SQS) when a queue name is provided.
>
> IAM role **fetch_title_role** permissions: attached **AmazonSQSFullAccess** policy
>
> This is preparation for handling a list of URL's and gathering their **title tag** values asynchronously.
>
> You know, async, as in really fast
>
> ... like in parallel, well, AWS Lambda is limited to 100 concurrent executions per region per account.
>
> See [AWS Lambda limits](http://docs.aws.amazon.com/lambda/latest/dg/limits.html)

***
#### Install aws cli
```
sudo pip install awscli
aws --version
```

***
#### AWS Credentials
see: http://docs.aws.amazon.com/lambda/latest/dg/setup.html
```
aws configure
nano ~/.aws/config
nano ~/.aws/credentials
export AWS_ACCOUNT_ID (nano ~/.bash_profile)
```

***
#### Setup a virtual environment for python
```
cd ~/aws_lambda_python/get_html_head_title_tag
virtualenv env
source env/bin/activate (use deactivate to switch to another project)
echo $VIRTUAL_ENV ... shows where python packages are located
```

***
#### Install packages via pip
```
pip install requests
pip install beautifulsoup4 (bs4)
```
> For this lambda project we are using **requests** to fetch an URL and **bs4** to extract the html head title tag from the page.

***
#### Develop and test code locally
see: https://github.com/cleesmith/get_html_head_title_tag (a non-hello world example)

> Note: always include code like this to test locally:

```
if __name__ == '__main__':
  event = {"url": "http://cleesmith.github.io/"}
  pt = lambda_handler(event, 'handler')
  print(pt)
```

***
#### Create an IAM role
see: http://codurance.com/2016/05/11/aws-lambdas/
```
aws iam create-role --profile pylambs --role-name fetch_title_role --assume-role-policy-document file://trust.json
aws iam update-assume-role-policy --profile pylambs --role-name fetch_title_role --policy-document file://trust.json
```
> Note: “pylambs” may be whatever your profile is called in ~/.aws/credentials.

***
#### Zip and deploy
```
zip -9 bundle.zip fetch_title.py
cd $VIRTUAL_ENV/lib/python2.7/site-packages
zip -r9 ~/aws_lambda_python/get_html_head_title_tag/bundle.zip *
cd ~/aws_lambda_python/get_html_head_title_tag
aws lambda create-function --region us-east-1 --function-name fetch_title --role arn:aws:iam::${AWS_ACCOUNT_ID}:role/fetch_title_role --handler fetch_title.lambda_handler --runtime python2.7 --profile pylambs --zip-file fileb://bundle.zip
```

***
#### Invoke and test the aws lambda function
```
aws lambda invoke --invocation-type RequestResponse --function-name fetch_title --profile pylambs --payload '{"url":"http://cleesmith.github.io/"}' results.txt
{ "StatusCode": 200 }
cat results.txt
```

***
#### Edit code and re-deploy
```
rm bundle.zip
zip -9 bundle.zip fetch_title.py
cd $VIRTUAL_ENV/lib/python2.7/site-packages
zip -r9 ~/aws_lambda_python/get_html_head_title_tag/bundle.zip *
cd ~/aws_lambda_python/get_html_head_title_tag
aws lambda update-function-code --function-name fetch_title --profile pylambs --zip-file fileb://bundle.zip --publish
```
> … rinse and repeat ...

***
#### Resources
* https://github.com/cleesmith/get_html_head_title_tag
* http://docs.aws.amazon.com/lambda/latest/dg/welcome.html
* http://codurance.com/2016/05/11/aws-lambdas/
* http://www.perrygeo.com/running-python-with-compiled-code-on-aws-lambda.html

***
***
