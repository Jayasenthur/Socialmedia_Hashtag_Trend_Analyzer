# Social Media Hashtag Trend Analyzer Application

## Project Description
This project is a __Streamlit-based web application__ that allows users to compose and publish posts containing text and hashtags. It analyzes trending hashtags in real time and provides insights into popular topics. The backend integrates __AWS Lambda__, __API Gateway__, and __DynamoDB__ to process 
and store data efficiently

## Workflow
### Post submission :
  * Users compose posts in the Streamlit app.
  * The app sends the post to an API Gateway endpoint.
  * AWS Lambda processes the post, extracts hashtags, and stores the data in DynamoDB.

### Trending Hashtags:
  * Users can view trending hashtags by clicking the "Show Trending Hashtags" button.
  * The app retrieves data from another API Gateway endpoint, which is powered by a Lambda function querying DynamoDB.

## Technologies Used
  * __Streamlit__: Frontend for the user interface.
  * __AWS Lambda__: Serverless backend functions for processing posts and fetching trending hashtags.
  * __AWS DynamoDB__: NoSQL database for storing posts and hashtags.
  * __AWS API Gateway__: API endpoints for communication between the frontend and backend.
  * __Python__: Primary programming language.
  * __Visual Studio Code__: Code editor for development.

## Component Details
  ### 1. Lambda Insert Function
 __Purpose__ : Process posts submitted by users, extract hashtags, and store them in DynamoDB.
  
__Key Features__: 
  * Extracts unique hashtags from the post content.     
  * Generates a unique PostId for each submission.     
  * Stores both the post and extracted hashtags in DynamoDB.
     
  Code :
  
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
### 2. Lambda Fetch Function

__Purpose__: Fetch and analyze trending hashtags from DynamoDB.

__Key Features__:
* Aggregates hashtag counts.
* Returns a sorted list of hashtags by popularity.

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

         
   
