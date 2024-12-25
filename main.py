from groq import Groq
import argparse
import datetime
import json
import random
import requests
import form  
import os

#import openai credentials from os
client = Groq(api_key=os.environ.get("GROQ_API_KEY"),)

# Define your Google Form URL here
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSchRfk1pmfgJSl__ZM-gq2R7GlTSWhAxZ6ry_zxB4bgSqR-CA/viewform"  # Replace with your Google Form URL

# List of cities in Pakistan for short answer fields
cities_in_pakistan = ["Canada","India","Kahore","LHR","Lahore, Pakistan","Lahore garrison…","Mughalpura","La…","Ni batao ga","Philippines","United kingdom","Karachi", "Lahore", "Islamabad", "Rawalpindi", "Peshawar"]

#gpt response getting
def generate_gpt_answer(text):
    chat_completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages= [{
                'role':'user',
                'content':"Given the description of PixelFiles, a service that offers customizable templates for presentations and documents, generate a simple and humanized answer (1-2 words) to the following question:"
                +"Question: "
                +text
                +"."
            }])
    print("generating response...")
    return chat_completion.choices[0].message.content.strip()

def generate_random_value(type_id, entry_id, options, is_required=False, entry_label=''):
    """
    Generate random values for form fields.
    Customize this function for specific entry IDs or types.
    """
    if entry_id == 'emailAddress':
        return 'example_email@gmail.com'
    if type_id == 0:  # Short answer
        return random.choice(cities_in_pakistan)  
    if type_id == 1: #paragraphs
            question = entry_label
            print(question)
            return generate_gpt_answer(question)  # Generate answer if required,
    if type_id == 2:  # Multiple choice
        return random.choice(options)
    if type_id == 3:  # Dropdown
        return random.choice(options)
    if type_id == 4:  # Checkboxes
        return random.sample(options, k=random.randint(1, len(options)))
    if type_id == 5:  # Linear scale
        return random.choice(options)
    if type_id == 7:  # Grid choice
        return random.choice(options)
    if type_id == 9:  # Date
        return datetime.date.today().strftime('%Y-%m-%d')
    if type_id == 10:  # Time
        return datetime.datetime.now().strftime('%H:%M')
    return ''  # Default empty response

def prepare_request_payload(url: str):
    """
    Prepare random payload data for form submission.
    """
    # Update this line to use the correct function from form.py
    response_body = form.generate_request_payload(
        url,
        output="return",  # We want to return the payload, not print it
        include_comments=False,
        data_generator=generate_random_value
    )
    response_body = json.loads(response_body)  # Convert the payload string to JSON
    return response_body  # Modify or override payload values here if needed

def send_form_submission(target_url: str, payload: any):
    """
    Submit form data to the specified URL.
    """
    target_url = form.convert_to_response_url(target_url)  # Convert to response URL
    print("Submitting to:", target_url)
    print("Payload:", payload, flush=True)
    
    response = requests.post(target_url, data=payload, timeout=5)
    if response.status_code != 200:
        print(f"Error! Failed to submit form. Status code: {response.status_code}")
    else:
        print("Submission successful!")

def run_submission(form_url: str):
    """
    Main function to generate and submit the form payload.
    """
    try:
        submission_payload = prepare_request_payload(form_url)
        send_form_submission(form_url, submission_payload)
        print("Form submission completed!")
    except Exception as err:
        print(f"Error during submission: {err}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Automate Google Form submission with custom data.")
    parser.add_argument('-u', '--url', default=form_url, help='Google Form URL (default: pre-configured URL)')
    args = parser.parse_args()

    if not args.url:
        print("Error: No URL provided. Set the `form_url` variable or pass a URL as an argument.")
    else:
        run_submission(args.url)
