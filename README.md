# Social Media Hashtag Trend Analyzer Application

## Project Description
This project is a __Streamlit-based web application__ that allows users to compose and publish posts containing text and hashtags. It analyzes trending hashtags in real time and provides insights into popular topics. The backend integrates __AWS Lambda__, __API Gateway__, and __DynamoDB__ to process and store data efficiently. It helps users see which hashtags are trending in real-time, making it useful for social media insights.

## Why this project?

1. __See Trending Hashtags__: Helps find out which hashtags are popular right now.
2. __Learn New Tools__: Taught me how to use AWS, DynamoDB, and Streamlit.
3. __Easy to Use__: The app is simple for anyone to post and see trending hashtags.
4. __Practice Real-Time Data__: Learned how to handle and show live data updates.
5. __Grow My Skills__: Improved my knowledge for a future in data engineering.
6. __Cost-Effective Design__ : The project uses serverless tech, so it’s affordable and efficient.

## Key Features

1. __Post Composition__: Users can write posts with hashtags in a single text box.
2. __Post Submission__: Posts are sent to AWS Lambda for backend processing.
3. __AWS Lambda Integration__: Automatically extracts hashtags and stores them in DynamoDB.
4. __Hashtag Extraction__: Hashtags are automatically identified and processed.
5. __Trending Hashtag Analysis__: Fetches and displays the top 10 most frequently used hashtags dynamically.
6. __Real-Time Updates__: As new posts are submitted, the trending hashtags are updated instantly..
7. __User-Friendly UI__: Streamlit ensures simplicity and ease of use.

## Architecture Diagram

Below is the architecture diagram for the Social Media Hashtag Trend Analyzer project:

![Architecture Diagram](https://github.com/Jayasenthur/Socialmedia_Hashtag_Trend_Analyzer/blob/main/hashtag_dgm.jpg)

## 4. Workflow Explanation
Walk through the project workflow step by step:

### 1. User Interaction:
  * A user writes a post containing hashtags (e.g., "Learning #Python is fun!") in the Streamlit app.
  * On clicking "Post," the content is sent to the backend via the API Gateway.
    
### 2. Backend Processing:
  * The __Insert Lambda function__ extracts hashtags from the post and stores them in a DynamoDB table.
  * __DynamoDB__ maintains all posts and hashtags efficiently.
    
### 3. Trending Hashtags:   
  * When the user clicks "Show Trending Hashtags," a request is sent to the __Fetch Lambda function__ via the API Gateway.
  * The function analyzes stored hashtags, calculates their frequency using Python's `collections.Counter`, and returns the top 10 trending hashtags.

### 4. Display Results:
  * The Streamlit app displays the trending hashtags in real-time, sorted by frequency.

## Technologies Used
  * __Streamlit__: Provides a simple and user-friendly web interface for users to write posts and view trending hashtags.
  * __AWS Lambda__: Handles backend processing.
      * __Insert Function__: Parses and stores hashtags from user posts in DynamoDB.
      * __Fetch Function__: Analyzes stored hashtags and calculates trending ones.
  * __AWS DynamoDB__: NoSQL database for storing posts and hashtags, ensuring scalability and fast querying..
  * __AWS API Gateway__: Serves as the bridge between the front-end and backend Lambda functions.
  * __Python__: The primary programming language for both the Streamlit app and Lambda functions.
  * __Visual Studio Code__: Code editor for development.
    
## Setup and Installation
Follow these steps to set up the __Social Media Hashtag Trend Analyzer__  on local environment and deploy it to the cloud:

### Prerequisites
  1. __AWS Account__: Ensure you have an active AWS account.
  2. __Python Installed__: Install Python (3.8 or above) on your local machine
  3. __Streamlit Installed__: Install Streamlit for the UI.
  4. __IDE__: Use an IDE like Visual Studio Code for code editing.

## Component Details

## 1. DynamoDB Table Creation
Here is a step-by-step guide to create a table in DynamoDB using the AWS Management Console:

### Step 1: Navigate to DynamoDB
1. Log in to your AWS Management Console.
2. In the search bar at the top, type __DynamoDB__ and select it.

### Step 2: Create a New Table
1. On the DynamoDB dashboard, click Create table.

### Step 3: Define Table Details
1. Table name: Enter the name of your table (e.g., `HashtagsTable`).
2. __Partition key (Primary key)__
   * Enter a key name (e.g.,`PostId`)
   * Select the data type for the partition key (e.g., `String`).
3. __Sort key (Optional)__: If you need a composite key (e.g., to store multiple hashtags for a post), you can define a __Sort key__.
   * Example: `Hashtags` (Type: String).

## Step 4: Create the Table
1. Click __Create table__.
2. Wait for the table status to change from __Creating__ to __Active__ (this might take a few seconds).

### Step 5: Add Items to Your Table
1. On the table's Overview page, click __Explore items__.
2. Click __Create item__.
3. Enter values for the partition key and any other attributes:
    * Example :
 ```json
 {
  "PostId": "12345",
  "Hashtags": "#Python",
  "PostContent": "Learning Python is fun!"
}
```
4. Click __Create item__ to save the entry.

## Example Table Schema for the Hashtag Application:

| Attribute Name | Key Type       | Data Type |
|----------------|---------------|-----------|
| PostId        | Partition Key | String    |
| Hashtags        | Attribute     | String    |
| PostContent           | Attribute     | String    |

* __Table Name__ :`HashtagsTable`
* __Primary Key__: `PostId`
* __Attributes__:
    * `PostId` (String)
    * `PostContent` (String)
    * `Hashtags` (List)
  
  
  ### 2. Lambda Insert Function
 __Purpose__ : Process posts submitted by users, extract hashtags, and store them in DynamoDB.
  
__Key Features__: 
  * Extracts unique hashtags from the post content.     
  * Generates a unique PostId for each submission.     
  * Stores both the post and extracted hashtags in DynamoDB.

## Step-by-step guide to create a Lambda function in AWS:

### Step 1: Navigate to the Lambda Console
1. Log in to the __AWS Management Console__.
2. Search for Lambda in the search bar and click on Lambda under "Services."

### Step 2: Create a New Lambda Function
1. In the Lambda console, click on the __Create function__ button.
2. Select the __Author from scratch__ option.

### Step 3: Configure the Function
1. Basic Information:
     * __Function name__: Provide a unique name for your function (e.g., HashtagInsertFunction).
     * __Runtime__: Choose the programming language you’ll use (e.g., Python 3.x).

2. __Role__ :
    Choose the execution role for the Lambda function:
     * __Create a new role with basic Lambda permissions__ (if you're starting fresh).
     * OR __Use an existing role__ (if you’ve already created a role with permissions for DynamoDB, etc.).

## IAM Policies for Lambda Functions
1. Permissions for DynamoDB (Insert and Fetch Functions)
To interact with a DynamoDB table (for inserting and fetching data), you need the following permissions:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem",
        "dynamodb:GetItem",
        "dynamodb:Scan"
      ],
      "Resource": "arn:aws:dynamodb:<region>:<account-id>:table/<table-name>"
    }
  ]
}
```
* `dynamodb:PutItem`: Allows inserting data into the table.
* `dynamodb:GetItem`: Allows fetching individual items (if needed).
* `dynamodb:Scan`: Allows scanning the entire table to retrieve all records.
* `Resource`: Restrict the permissions to a specific table by specifying its ARN.

### Steps to Attach IAM Policies to the Lambda Execution Role
#### 1. Open the AWS Management Console
Navigate to the IAM Console.

#### 2. Find the Lambda Execution Role
1. In the IAM Console, click on Roles in the left sidebar.
2. Locate the execution role associated with Lambda function:
   * The role name usually follows this pattern: `lambda-role-[your-lambda-function-name]-....`
   * If unsure, go to the __Lambda Console__, select ther function, and check the __Execution Role__ under the "Configuration" tab.
#### 3. Edit the Role
1. Click on the role name to open its details page.
2. Navigate to the __Permissions__ tab.

#### 4. Attach an IAM Policy
1. Click the __Attach policies__ button.
2. Search for the required policies using the search bar or browse from the list. Examples of common policies include:
   * __AWSLambdaBasicExecutionRole__: Allows Lambda to write logs to CloudWatch.
   * __AmazonDynamoDBFullAccess__ or __AmazonDynamoDBReadOnlyAccess__: Grants access to DynamoDB tables.
   * __AmazonS3FullAccess__: If the function needs access to S3 buckets.
3. Check the box next to the policies you want to attach.

#### 5. Review and Save
1. Click __Attach policy__ to apply the changes.
2. The selected policies are now attached to the role.

#### 6. Verify Policy Permissions
1. Under the __Permissions__ tab, review the newly added policies.
2. Ensure that all required permissions (e.g., for DynamoDB, CloudWatch, or S3) are included.


#### 7. Test the Lambda Function
After attaching the policies, test the Lambda function to confirm that it can perform the intended actions (e.g., read/write to DynamoDB)

### Step 4: Write or Upload Code
 1. Inline Editor:
    * Scroll down to the Function code section.
    * Under "Code source," click __Edit code inline__ to paste your Python code.
          
  __Code :__
  
  ```python
import json
import boto3
import uuid
import re  # For extracting hashtags

# Initialize DynamoDB resource and specify the table name
dynamodb = boto3.resource('dynamodb')
table_name = 'HashtagsTable'  # Replace with your actual table name
table = dynamodb.Table(table_name)

def extract_hashtags(post_content):
    """Extract hashtags from the post content."""
    return re.findall(r"#(\w+)", post_content)

def lambda_handler(event, context):
    try:
        # Parse the incoming request body
        body = json.loads(event['body'])
        post_content = body.get('post_content', '').strip()

        if not post_content:
            raise ValueError("Post content is missing or empty.")

        # Generate a unique PostId
        post_id = str(uuid.uuid4())

        # Extract hashtags from the post content
        hashtags = extract_hashtags(post_content)

        if not hashtags:
            raise ValueError("No hashtags found in the post content.")

        # Insert each hashtag as a separate entry in DynamoDB
        for hashtag in hashtags:
            item = {
                'PostId': post_id,        # Partition key
                'PostContent': post_content,
                'Hashtag': hashtag       # Required attribute for your table schema
            }

            # Insert the item into the DynamoDB table
            table.put_item(Item=item)

        # Return success response
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Post and hashtags inserted successfully!'}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

    except Exception as e:
        # Return error response
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
      
   ```
### Step 5: Save and Deploy
 1. Click on __Deploy__ at the top right to save your changes.

### Step 6: Test the Function
 1. At the top of the Lambda console, click on the __Test__ button.
    
 2. __Configure a Test Event__:
    * Provide a sample payload, such as
```python
{
  "post_content": "Learning #AWS and #Lambda!"
}
```
   * Click __Create__.
3. Run the test by clicking __Test__ again and check the logs or response.

## Explanation of Lambda insert function:

### 1.  __Imports__
```python
import json
import boto3
import uuid
import re
```
* `json`: Used to parse the incoming request body and format the response.
* `boto3`: AWS SDK for Python, used here to interact with DynamoDB
* `uuid`: Generates unique IDs for each post to ensure no conflicts in the DynamoDB table
* `re`: A regular expression library used to extract hashtags from the post content

### 2. DynamoDB Initialization
```python
dynamodb = boto3.resource('dynamodb')
table_name = 'HashtagsTable'
table = dynamodb.Table(table_name)
```
* `boto3.resource('dynamodb')`: Initializes a DynamoDB resource to interact with AWS DynamoDB.
* `table_name`: The name of the DynamoDB table where data will be stored.
* `table = dynamodb.Table(table_name)`: Specifies the table object to perform operations like put_item.

### 3. Hashtag Extraction
```python
def extract_hashtags(post_content):
    return re.findall(r"#(\w+)", post_content)
```
* This function uses a regular expression #(\w+) to find all hashtags in the post content.
   * `#`: Matches the hash symbol.
   * `\w+`: Matches one or more alphanumeric characters or underscores.
* It returns a list of hashtags found in the post.

### 4. Main Handler Function
The lambda_handler function is the entry point for AWS Lambda function.

### Request Parsing
```python
body = json.loads(event['body'])
post_content = body.get('post_content', '').strip()
```
* event['body']: Extracts the request payload, typically sent as JSON.
* body.get('post_content'): Retrieves the post_content key from the parsed JSON. If it’s missing, a default empty string is used.
* .strip(): Removes leading and trailing whitespace.

### Input Validation
```python
if not post_content:
    raise ValueError("Post content is missing or empty.")
```
* Ensures that post_content is not empty. If it is, a ValueError is raised and caught in the exception block.

### Generate Unique Post ID
```python
post_id = str(uuid.uuid4())
```
A unique ID for the post is generated using `uuid.uuid4()`. This ensures that each post is uniquely identifiable.

### Hashtag Extraction and Validation
```python
hashtags = extract_hashtags(post_content)

if not hashtags:
    raise ValueError("No hashtags found in the post content.")
```
* Hashtags are extracted from the post content using the `extract_hashtags` function.
* If no hashtags are found, a `ValueError` is raised.

### Insert into DynamoDB
```python
for hashtag in hashtags:
    item = {
        'PostId': post_id,
        'PostContent': post_content,
        'Hashtag': hashtag
    }
    table.put_item(Item=item)
```
* Each hashtag is inserted into the DynamoDB table as a separate entry.
* `PostId`: Acts as the partition key (unique identifier for the post).
* `PostContent`: The original text of the post.
* `Hashtag`: The extracted hashtag.
* `table.put_item(Item=item)` function in the AWS SDK for Python (Boto3) is used to insert a new item into an Amazon DynamoDB table or replace an existing item with the same primary key.

### 5. Success Response
```python
return {
    'statusCode': 200,
    'body': json.dumps({'message': 'Post and hashtags inserted successfully!'}),
    'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    }
}
```
* Returns a success response with a 200 status code if all hashtags are inserted successfully.

### Exception Handling
```python
except Exception as e:
    return {
        'statusCode': 500,
        'body': json.dumps({'error': str(e)}),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
```
* Any errors during execution (e.g., invalid input, DynamoDB issues) are caught here.
* A 500 status code is returned, along with the error message.

### Example Input and Output
### Input 
```python
{
    "post_content": "Exploring AWS Lambda! #AWS #Lambda #DynamoDB"
}
```

### DynamoDB Entries Created

The following table illustrates how data is stored in the DynamoDB table for each post:

| **PostId**                           | **PostContent**                          | **Hashtag** |
|--------------------------------------|------------------------------------------|-------------|
| 123e4567-e89b-12d3-a456-426614174000 | Exploring AWS Lambda! #AWS #Lambda #DynamoDB | AWS         |
| 123e4567-e89b-12d3-a456-426614174000 | Exploring AWS Lambda! #AWS #Lambda #DynamoDB | Lambda      |
| 123e4567-e89b-12d3-a456-426614174000 | Exploring AWS Lambda! #AWS #Lambda #DynamoDB | DynamoDB    |

### Output
```python
{
    "statusCode": 200,
    "body": "{\"message\": \"Post and hashtags inserted successfully!\"}"
}
```
## 2. Lambda Fetch Function

__Purpose__: Fetch and analyze trending hashtags from DynamoDB.

__Key Features__:
* Aggregates hashtag counts.
* Returns a sorted list of hashtags by popularity.

Follow the step by step guide mentioned in __Lamda Insert function__ to create __Lamda Fetch function__ and use the code below.

__Code :__
```python
import json
import boto3
from collections import Counter

# Initialize DynamoDB resource and specify table name
dynamodb = boto3.resource('dynamodb')
table_name = 'HashtagsTable'  # Replace with your DynamoDB table name
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Scan the DynamoDB table to retrieve all items
        response = table.scan()
        items = response.get('Items', [])  # Use the correct key 'Items'
        
        # Extract hashtags from items
        hashtags = [item['Hashtag'] for item in items if 'Hashtag' in item]
        
        if not hashtags:
            return {
                'statusCode': 200,
                'body': json.dumps({'trending_hashtags': []}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
        
        # Count occurrences of each hashtag
        hashtag_counts = Counter(hashtags)
        
        # Sort hashtags by count in descending order
        trending = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Format the response (Top 10 trending hashtags)
        trending_hashtags = [{"Hashtag": tag, "count": count} for tag, count in trending[:10]]
        
        return {
            'statusCode': 200,
            'body': json.dumps({'trending_hashtags': trending_hashtags}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    except Exception as e:
        # Handle any errors that occur
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

```
### Test the Function :
 1. At the top of the Lambda console, click on the __Test__ button.
    
 2. __Configure a Test Event__:
    * Provide a sample payload, such as
```python
{
  "body": "{\"post_content\": \"Learning #Streamlit and #Python is amazing!\"}"
}
```
   * Click __Create__.
3. Run the test by clicking __Test__ again and check the logs or response.

## Explanation of Lambda Fetch function:

### 1.  __Imports__
```python
import json
import boto3
from collections import Counter
```
* `json`: Used for formatting the input and output.
* `boto3`: AWS SDK for Python, used to interact with DynamoDB.
* `Counter`: From the collections module, used to count occurrences of hashtags.

### 2. Initialize DynamoDB
```python
dynamodb = boto3.resource('dynamodb')
table_name = 'HashtagsTable'  # Replace with your DynamoDB table name
table = dynamodb.Table(table_name)
```
* Establishes a connection to the DynamoDB resource.
* Specifies the table (`HashtagsTable`) from which data will be fetched.
  
### 3. Lambda Handler Function
```python
def lambda_handler(event, context):
    try:
        # Scan the DynamoDB table to retrieve all items
        response = table.scan()
        items = response.get('Items', [])
```
* __Purpose__: Scans the DynamoDB table to retrieve all records.
* __Key Operation__: `table.scan()`
    * Retrieves all data in the table (not efficient for very large datasets but works for this project).
    * Extracts the list of items under the 'Items' key.
 
### 4. Extract Hashtags
```python
hashtags = [item['Hashtag'] for item in items if 'Hashtag' in item]
```
* iterates through the retrieved items and extracts the `Hashtag` field for each record.
* Ensures only records with a `Hashtag` field are considered.

### 5. Handle No Hashtags
```python
if not hashtags:
    return {
        'statusCode': 200,
        'body': json.dumps({'trending_hashtags': []}),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
```
* If no hashtags are found:
    * Responds with an empty list for trending_hashtags

### 6. Count and Sort Hashtags
```python
# Count occurrences of each hashtag
hashtag_counts = Counter(hashtags)

# Sort hashtags by count in descending order
trending = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)
```
* Counting: Uses `Counter` to calculate how many times each hashtag appears.
* Sorting: Arranges the hashtags in descending order of frequency.

### 7. Format Response
```python
# Format the response (Top 10 trending hashtags)
trending_hashtags = [{"Hashtag": tag, "count": count} for tag, count in trending[:10]]

return {
    'statusCode': 200,
    'body': json.dumps({'trending_hashtags': trending_hashtags}),
    'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    }
}
```
* Top 10 Hashtags: Selects the top 10 trending hashtags with their counts.
* Format: Converts the hashtags and counts into a list of dictionaries for easy readability.
* Response: Returns a JSON-formatted response.
  
Example of the response:
```python
{
    "trending_hashtags": [
        {"Hashtag": "AWS", "count": 15},
        {"Hashtag": "Lambda", "count": 10},
        {"Hashtag": "DynamoDB", "count": 8}
    ]
}
```
### 8. Error Handling
```python
except Exception as e:
    return {
        'statusCode': 500,
        'body': json.dumps({'error': str(e)}),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
```
* Catches any exceptions and returns an error message.
* Sets the HTTP status code to `500`.

## 3. API Gateway Configuration

Here is a step-by-step guide to configure API Gateway for the endpoints __POST /processPost__ and __GET /trendingHashtags__ using __HTTP API__ in AWS:

### Step 1: Create an HTTP API

1. Go to the __API Gateway__ console.
2. Click __Create API > HTTP API__.
3. Select __Build__ under __HTTP API__.
4. Provide a name for your API (e.g., `SocialMediaAPI`).
5. Click __Next__ and then __Create__.

### Step 2: Add Routes
### Add POST /`processPost` Route
1. In your API dashboard, click __Routes__ in the left-hand menu.
2. Click __Create__
3. Enter the route as:
    * __Resource path__: /`processPost`
    * __Method__: `POST`
4. Click __Create__ Route

### Add GET /`trendingHashtags` Route
1. Repeat the steps above, but
    * __Resource path__: /`trendingHashtags`
    * __Method__: `GET`
2. Click __Create__ Route

### Step 3: Attach Lambda Integrations
For each route, link it to the appropriate Lambda function.

1. Click on the __POST__ /`processPost` route in the Routes list.
2. Under __Integration__, click __Attach integration__.
3. Select __Create and attach an integration__.
4. Choose __Lambda function__.
5. Under __Lambda function__, select the Lambda function responsible for processing posts (e.g., `HashTagAnalysis_Insert`).
6. Click __Create__.

### Attach Lambda to GET /trendingHashtags:
1. Click on the `GET /trendingHashtags` route in the Routes list.
2. Repeat the same process as above, but select the Lambda function responsible for fetching trending hashtags (e.g., `HashTagAnalysis_Fetch`).

### Step 4: Deploy the API
1. In the left-hand menu, click __Deployments__.
2. Click __Create__
3. Choose a stage name, such as `prod` or `dev`.
4. Click __Deploy__.

### Step 5: Test the API
### POST /processPost

1. Use a tool like __Postman__ or your Streamlit app.
2. URL: `https://<your-api-id>.execute-api.<region>.amazonaws.com/processPost`
3. Method: `POST`
4. Body
```json
{
  "post_content": "Learning #Python and #AWS is awesome!"
}

```
### GET /trendingHashtags
1. Use __Postman__ or a browser.
2. URL: `https://<your-api-id>.execute-api.<region>.amazonaws.com/trendingHashtags`
3. Method: `GET`.


   
## 5. Streamlit App
User-friendly interface for composing posts and viewing trending hashtags.

__Code :__
```python
import streamlit as st
import requests
import json
import uuid

# Define the API Gateway URL (replace with your actual URL)
insert_post_api_url = 'https://hvrbau1nj1.execute-api.us-east-1.amazonaws.com/prod/processPost'
fetch_post_api_url='https://hvrbau1nj1.execute-api.us-east-1.amazonaws.com/dev/trendingHashtags'

# Streamlit app UI
st.title("Social Media Post Analyzer")

# Post Composition
st.header("Compose a Post")
post_content = st.text_area("Write your post with hashtags here (e.g., Learning #Python is fun!)")

if st.button("Post"):
    if post_content.strip():
        payload = {'post_content': post_content}
        headers = {'Content-Type': 'application/json'}

        try:
            # Send POST request to the API Gateway endpoint
            response = requests.post(insert_post_api_url, data=json.dumps(payload), headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                post_id = response_data.get("PostId", "N/A")
                #st.success(f"Post submitted successfully! Post ID: {post_id}")
                st.success("Post submitted successfully!")

                
            else:
                # Display detailed error from the API response
                try:
                    error_message = response.json().get('error', response.text)
                except json.JSONDecodeError:
                    error_message = response.text
                st.error(f"Failed to submit post: {error_message}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with the API: {str(e)}")
    else:
        st.warning("Please write a post before submitting.")

# Show Trending Hashtags
st.header("Trending Hashtags")
if st.button("Show Trending Hashtags"):
    try:
        # Fetch trending hashtags from the API Gateway endpoint
        trending_response = requests.get(fetch_post_api_url)

        if trending_response.status_code == 200:
            # Parse the response for hashtags
            try:
                hashtags = trending_response.json().get("trending_hashtags", [])
            except json.JSONDecodeError:
                st.error("Error parsing response from the server.")
                hashtags = []

            if hashtags:
                st.write("### Current Trending Hashtags")
                for item in hashtags:
                    st.write(f"#{item['Hashtag']}: {item['count']} mentions")
            else:
                st.write("No trending hashtags found.")
        else:
            st.error(f"Failed to fetch trending hashtags: {trending_response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the API: {str(e)}")
```
## Code Explanation 
### 1. Importing Libraries
```python
import streamlit as st
import requests
import json
import uuid
```
* `streamlit`: Used for building the web app UI.
* `requests`: For making HTTP requests to the API Gateway endpoints.
* `json`: To handle JSON data for API communication.
* `uuid:` Not directly used in this code but typically used to generate unique identifiers (possibly for debugging or future use).

### 2. API URLs
```python
insert_post_api_url = 'https://hvrbau1nj1.execute-api.us-east-1.amazonaws.com/prod/processPost'
fetch_post_api_url = 'https://hvrbau1nj1.execute-api.us-east-1.amazonaws.com/dev/trendingHashtags'
```
* These variables define the URLs for API Gateway endpoints.
* Replace with your actual API Gateway URLs if they change.

### 3. App Title
```python
st.title("Social Media Post Analyzer")
```
* Displays the title of the application at the top of the page.
### 4. Post Composition Section
```python
st.header("Compose a Post")
post_content = st.text_area("Write your post with hashtags here (e.g., Learning #Python is fun!)")
```
* Adds a header (Compose a Post) and a text area for users to input posts containing hashtags.

### 5. Submit Post Button
```python
if st.button("Post"):
    if post_content.strip():
        payload = {'post_content': post_content}
        headers = {'Content-Type': 'application/json'}
```
* Adds a "Post" button for submitting posts.
* Validation: Ensures the post content is not empty (post_content.strip()).
* Prepares the payload (post content as JSON) and sets headers for the API request.

### 6. Submit Post API Request
```python
try:
    # Send POST request to the API Gateway endpoint
    response = requests.post(insert_post_api_url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        st.success("Post submitted successfully!")
    else:
        try:
            error_message = response.json().get('error', response.text)
        except json.JSONDecodeError:
            error_message = response.text
        st.error(f"Failed to submit post: {error_message}")
except requests.exceptions.RequestException as e:
    st.error(f"Error communicating with the API: {str(e)}")
```
* __API Call__: Sends a POST request to insert_post_api_url with the post content.
* __Response Handling__:
  * If successful (status_code == 200), displays a success message.
  * If not, parses and displays the error message from the response.
* __Exception Handling__: Catches any issues during the API communication, such as connection errors.

### 7. Trending Hashtags Section
```python
st.header("Trending Hashtags")
```
* Adds a header for the trending hashtags section.

### 8. Show Trending Hashtags Button
```python
if st.button("Show Trending Hashtags"):
    try:
        # Fetch trending hashtags from the API Gateway endpoint
        trending_response = requests.get(fetch_post_api_url)
```
* Adds a "Show Trending Hashtags" button.
* Sends a GET request to the fetch_post_api_url to retrieve trending hashtags.

### 9. Handle Trending Hashtags Response
```python
if trending_response.status_code == 200:
    try:
        hashtags = trending_response.json().get("trending_hashtags", [])
    except json.JSONDecodeError:
        st.error("Error parsing response from the server.")
        hashtags = []
```
* Parses the API response:
   * If successful, retrieves the trending_hashtags field from the response JSON.
   * Handles parsing errors gracefully with an error message.

### 10. Display Trending Hashtags
```python
if hashtags:
    st.write("### Current Trending Hashtags")
    for item in hashtags:
        st.write(f"#{item['Hashtag']}: {item['count']} mentions")
else:
    st.write("No trending hashtags found.")
```
* Displays the top trending hashtags along with their mention counts.
* If no hashtags are found, shows a fallback message.

### 11. Handle Errors
```python
else:
    st.error(f"Failed to fetch trending hashtags: {trending_response.text}")
except requests.exceptions.RequestException as e:
    st.error(f"Error communicating with the API: {str(e)}")
```
* Displays appropriate error messages if:
    * The API request fails.
    * An exception occurs during communication.
      
## Testing Instructions
Follow these steps to test the functionality of the project after completing the setup and installation:

## 1. Testing the Lambda Insert Function

### Steps:
1. Open the AWS Management Console.
2. Navigate to __AWS Lambda__
3. Select the Insert Function (`HashTagAnalysis_Insert`)
4. Click __Test__ at the top of the page.
5. Create a test event with the following payload:
```json
{
    "post_content": "Learning #Streamlit and #Python is amazing!"
}
```
6. Click __Save and Test__.
7. Verify that:
    * The Lambda function executes successfully.
    * A new entry is added to the DynamoDB table `HashtagsTable`.
    * The response returns a success message
```json
{
    "statusCode": 200,
    "body": "{\"message\": \"Data stored successfully\"}"
}
```

## 2. Testing the Lambda Fetch Function

1. Navigate to the AWS Management Console and open __Lambda__.
2. Select the Fetch Function (`HashTagAnalysis_Fetch`)
4. Click __Test__ .
5. create an test event with the following payload:
```json
{
"body": "{\"post_content\": \"Learning #Streamlit and #Python is amazing!\"}"
}
```
7. Verify that :
    * The Lambda function executes successfully.
    * The response contains trending hashtags from the __DynamoDB table__.
    * Example response:
```json
{
    "statusCode": 200,
    "body": "[{\"hashtag\": \"Streamlit\", \"count\": 5}, {\"hashtag\": \"Python\", \"count\": 3}]"
}
```
## 3. Testing the API Gateway Endpoints
### Testing the POST Endpoint (/processPost):
1. Use a tool like Postman, curl, or the API Gateway Test Tool.
2. Send a __POST__ request to your API Gateway endpoint:
```php
https://<api-id>.execute-api.<region>.amazonaws.com/post/processPost
```
3. Add the following payload in the request body
```json
{
    "post_content": "Exploring #AWS and #DynamoDB!"
}
```
4. Verify that:
The response returns a success message :
```json
{
    "message": "Data stored successfully"
}
```
Testing the GET Endpoint (/`trendingHashtags`):

1. Use Postman, curl, or the API Gateway Test Tool.
2. Send a GET request to the following endpoint :
```php
https://<api-id>.execute-api.<region>.amazonaws.com/get/trendingHashtags
```
3. Verify that:
* The response returns a list of trending hashtags with counts
```json
[
    {"hashtag": "AWS", "count": 10},
    {"hashtag": "DynamoDB", "count": 7}
]
```

## 4. Testing the Streamlit Application
1. Run the Streamlit app locally
```bash
streamlit run hashtag.py
```
2. Open the app in your browser (default URL: http://localhost:8501).
3. Test the Post Composition
  * Enter a post with hashtags (e.g., "Working on #Python and #AWS projects!").
  * Click the Post button
  * Verify that the post is successfully sent to the Lambda function and stored in DynamoDB.
4. Test the Trending Hashtags Section:
  * Click Show Trending Hashtags.
  * Verify that trending hashtags are displayed, dynamically updating as new posts are submitted.
## 5. Verify End-to-End Functionality
1. Compose a new post in the Streamlit app
2. Verify the post's data in DynamoDB using the AWS Management Console.
3. Check that the trending hashtags in the Streamlit app reflect the updates
4. Test for edge cases, such as
    * Submitting empty or invalid posts.
    * Posts with no hashtags.
    * Very large posts with multiple hashtags.


## Challenges Faced

* Setting up the backend processing using AWS Lambda.
* Python functions and connect them to DynamoDB.
* Testing the API Gateway integration.
* Testing each component.
  
## Project Benefits

* Provides real-time insights into trending topics.
* Demonstrates a practical use case of serverless architecture with __AWS__.
* Offers scalability and efficiency through __DynamoDB__ and __Lambda__.
* Simplifies user interaction with a clean __Streamlit UI__.






         
   
