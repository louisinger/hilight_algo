# The buildspec.yml file

Use for configure codebuild AWS service in the pipeline.

# Lambdas functions
 
### PREPROCESSING

**folder:** preprocessing
**lambda arn:**: arn:aws:lambda:eu-west-3:671560023774:function:preprocessing
**s3 bucket:**: s3://lambda-preprocessing/

### COMPARE HILIGHT GOOD

**folder:** compareHilightGood
**lambda arn:**: arn:aws:lambda:eu-west-3:671560023774:function:compareHilightGood
**s3 bucket:**: s3://lambda-comparehilightgood/

### LAUNCH HILIGHT 

**folder:** LaunchHiLight
**lambda arn:**: arn:aws:lambda:eu-west-3:671560023774:function:LaunchHilight
**s3 bucket:**: s3://hilightalgo/