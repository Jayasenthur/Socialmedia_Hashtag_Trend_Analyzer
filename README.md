# Social Media Hashtag Trend Analyzer Application

## Project Description
This project is a __Streamlit-based web application__ that allows users to compose and publish posts containing text and hashtags. It analyzes trending hashtags in real time and provides insights into popular topics. The backend integrates __AWS Lambda__, __API Gateway__, and __DynamoDB__ to process and store data efficiently. The user interface allows users to seamlessly engage with the application and stay informed about popular topics.

## Key Features

1. __Post Composition__: Users can write posts with hashtags in a single text box.
2. __Post Submission__: Posts are sent to AWS Lambda for processing.
3. __AWS Lambda Integration__: Automatically extracts hashtags and stores them in DynamoDB.
4. __Trending Hashtag Analysis__: Fetches and displays real-time trending hashtags.
5. __Dynamic Updates__: Updates trending hashtags as new posts are submitted.
6. __User-Friendly UI__: Built using Streamlit for a responsive and easy-to-use interface.

## Architecture Diagram

Below is the architecture diagram for the Social Media Hashtag Trend Analyzer project:

![Architecture Diagram](https://github.com/Jayasenthur/Socialmedia_Hashtag_Trend_Analyzer/blob/main/hashtag_dgm.jpg)


## Technologies Used
  * __Streamlit__: Frontend for the user interface.
  * __AWS Lambda__: Serverless backend functions for processing posts and fetching trending hashtags.
  * __AWS DynamoDB__: NoSQL database for storing posts and hashtags.
  * __AWS API Gateway__: API endpoints for communication between the frontend and backend.
  * __Python__: Primary programming language.
  * __Visual Studio Code__: Code editor for development.
    
## Setup and Installation
Follow these steps to set up the __Social Media Hashtag Trend Analyzer__  on your local environment and deploy it to the cloud:

### Prerequisites
  1. __AWS Account__: Ensure you have an active AWS account.
  2. __Python Installed__: Install Python (3.8 or above) on your local machine
  3. __Streamlit Installed__: Install Streamlit for the UI.
  4. __IDE__: Use an IDE like Visual Studio Code for code editing.

## Component Details
  ### 1. Lambda Insert Function
 __Purpose__ : Process posts submitted by users, extract hashtags, and store them in DynamoDB.
  
__Key Features__: 
  * Extracts unique hashtags from the post content.     
  * Generates a unique PostId for each submission.     
  * Stores both the post and extracted hashtags in DynamoDB.

### Step-by-step guide to create a Lambda function in AWS:

#### Step 1: Navigate to the Lambda Console
1. Log in to the __AWS Management Console__.
2. Search for Lambda in the search bar and click on Lambda under "Services."

#### Step 2: Create a New Lambda Function
1. In the Lambda console, click on the __Create function__ button.
2. Select the __Author from scratch__ option.

#### Step 3: Configure the Function
1. Basic Information:
     __Function name__: Provide a unique name for your function (e.g., HashtagInsertFunction).
     __Runtime__: Choose the programming language you’ll use (e.g., Python 3.x).

2. __Role__ :
    Choose the execution role for the Lambda function:
     * __Create a new role with basic Lambda permissions__ (if you're starting fresh).
     * OR __Use an existing role__ (if you’ve already created a role with permissions for DynamoDB, etc.).

### IAM Policies for Lambda Functions
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

#### Steps to Attach IAM Policies to the Lambda Execution Role
1. Identify the Execution Role:

#### Step 4: Write or Upload Code
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
#### Step 5: Save and Deploy
 1. Click on __Deploy__ at the top right to save your changes.

#### Step 6: Test the Function
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

## 1.  __Imports__
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

## 2. DynamoDB Initialization
```python
dynamodb = boto3.resource('dynamodb')
table_name = 'HashtagsTable'
table = dynamodb.Table(table_name)
```
* `boto3.resource('dynamodb')`: Initializes a DynamoDB resource to interact with AWS DynamoDB.
* `table_name`: The name of the DynamoDB table where data will be stored.
* `table = dynamodb.Table(table_name)`: Specifies the table object to perform operations like put_item.

## 3. Hashtag Extraction
```python
def extract_hashtags(post_content):
    return re.findall(r"#(\w+)", post_content)
```
* This function uses a regular expression #(\w+) to find all hashtags in the post content.
   * `#`: Matches the hash symbol.
   * `\w+`: Matches one or more alphanumeric characters or underscores.
* It returns a list of hashtags found in the post.

## 4. Main Handler Function
The lambda_handler function is the entry point for your AWS Lambda function.

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

## 3. API Gateway Configuration

Here is a step-by-step guide to configure API Gateway for the endpoints __POST /processPost__ and __GET /trendingHashtags__ using __HTTP API__ in AWS:

#### Step 1: Create an HTTP API

1. Go to the __API Gateway__ console.
2. Click __Create API > HTTP API__.
3. Select __Build__ under __HTTP API__.
4. Provide a name for your API (e.g., `HashtagAPI`).
5. Click __Next__ and then __Create__.

#### Step 2: Add Routes
#### Add POST /`processPost` Route
1. In your API dashboard, click __Routes__ in the left-hand menu.
2. Click __Create__
3. Enter the route as:
    * __Resource path__: /`processPost`
    * __Method__: `POST`
4. Click __Create__ Route

#### Add GET /`trendingHashtags` Route
1. Repeat the steps above, but
    * __Resource path__: /`trendingHashtags`
    * __Method__: `GET`
2. Click __Create__ Route

#### Step 3: Attach Lambda Integrations
For each route, link it to the appropriate Lambda function.

1. Click on the __POST__ /`processPost` route in the Routes list.
2. Under __Integration__, click __Attach integration__.
3. Select __Create and attach an integration__.
4. Choose __Lambda function__.
5. Under __Lambda function__, select the Lambda function responsible for processing posts (e.g., `ProcessPostFunction`).
6. Click __Create__.

#### Attach Lambda to GET /trendingHashtags:
1. Click on the `GET /trendingHashtags` route in the Routes list.
2. Repeat the same process as above, but select the Lambda function responsible for fetching trending hashtags (e.g., `TrendingHashtagsFunction`).

#### Step 4: Deploy the API
1. In the left-hand menu, click __Deployments__.
2. Click __Create__
3. Choose a stage name, such as `prod` or `dev`.
4. Click __Deploy__.

#### Step 5: Test the API
#### POST /processPost

1. Use a tool like __Postman__ or your Streamlit app.
2. URL: `https://<your-api-id>.execute-api.<region>.amazonaws.com/processPost`
3. Method: `POST`
4. Body
```json
{
  "post_content": "Learning #Python and #AWS is awesome!"
}

```
#### GET /trendingHashtags
1. Use __Postman__ or a browser.
2. URL: `https://<your-api-id>.execute-api.<region>.amazonaws.com/trendingHashtags`
3. Method: `GET`.

### 4. DynamoDB Table Creation
Here is a step-by-step guide to create a table in DynamoDB using the AWS Management Console:

#### Step 1: Navigate to DynamoDB
1. Log in to your AWS Management Console.
2. In the search bar at the top, type __DynamoDB__ and select it.

#### Step 2: Create a New Table
1. On the DynamoDB dashboard, click Create table.

#### Step 3: Define Table Details
1. Table name: Enter the name of your table (e.g., `HashtagsTable`).
2. __Partition key (Primary key)__
   * Enter a key name (e.g.,`PostId`)
   * Select the data type for the partition key (e.g., `String`).
3. __Sort key (Optional)__: If you need a composite key (e.g., to store multiple hashtags for a post), you can define a __Sort key__.
   * Example: `Hashtags` (Type: String).

#### Step 4: Create the Table
1. Click __Create table__.
2. Wait for the table status to change from __Creating__ to __Active__ (this might take a few seconds).

#### Step 5: Add Items to Your Table
1. On the table's Overview page, click __Explore items__.
2. Click __Create item__.
3. Enter values for the partition key and any other attributes:
    * Example :
 ```json
 {
  "item_id": "12345",
  "hashtag": "#Python",
  "text": "Learning Python is fun!"
}
```
4. Click __Create item__ to save the entry.

### Example Table Schema for the Hashtag Application:

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
2. Select the Insert Function (`HashTagAnalysis_Fetch`)
4. Click __Test__ .
5. Use an empty test event (no payload required) and run the function.
6. Verify that :
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
  





         
   
