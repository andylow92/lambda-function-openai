# este es el lambda funcionando con davinci 
import json
import openai
import boto3

def lambda_handler(event, context):
    try:
        input_prompt = event['promp'] # access the 'promp' key directly from the event


        model_to_use = "text-davinci-003"
        
        openai.api_key = get_api_key()
        response = openai.Completion.create(
            model=model_to_use,
            prompt=input_prompt,
            temperature=0,
            max_tokens=3000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        text_response = response['choices'][0]['text'].strip()

        # Return the response as a JSON string
        return {
            'statusCode': 200,
            'body': json.dumps({
                'response': text_response
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
#This function will get the code from another lambda you will have to set up with your open-ai key
def get_api_key():
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(
            FunctionName = 'arn:of-the-function-with-the-open-ai-key',
            InvocationType = 'RequestResponse'
        )

    openai_api_key = json.load(response['Payload'])['body']['api_key']
    return openai_api_key




