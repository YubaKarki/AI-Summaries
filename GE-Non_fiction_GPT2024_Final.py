# Number of documents: 62
#J:\R and Python_ Projects\GE_Project2024\Document list Non-Fiction


from openai import OpenAI
import time
from tqdm import tqdm
import os
import json
Key ="API KEY"
client = OpenAI(api_key=Key)

#path = "./Non-Fiction Article"
path = r'J:\R and Python_ Projects\GE_Project2024\Non-Fiction Article'

def merge_summaries(summaries):
  # Initialize a string to hold the merged summaries
  merged_summaries = ""
 
  # Iterate over the summaries
  for summary in summaries:
    # Add the summary to the merged summaries
    merged_summaries += summary #!!!! I get an error here
 
  # Return the merged summaries
  return merged_summaries
 
 
 
 
def generate_chunk_summaries(chunk):
   
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
   
        messages=[
            {
                "role": "system",
                "content": f"""Please write summary as a professional writer. This is a work of nonfiction by George Eliot. Provide a summary of approximately 300 words, start with the article name, author and year of publication. After summary paragraph, identify the GENRE (usually an article or a book review). If it is a book reviewed by George Eliot then identify the title(s) and author(s) of the book(s) being reviewed and include it before five Key word. 
                """
            },
            {
                "role": "user",
                "content": chunk
            }
        ],
        temperature=0.6,
        max_tokens=2048, # Adjust max_tokens to a lower value
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1)
    
    return response.choices[0].message.content

def write_summary(summaries):
   
    response = client.chat.completions.create(
    model="gpt-4",
  
        messages=[
            {
                "role": "system",
                "content": """Please write  summary of approximately 300 words, start with the article name, author and year of publication. After summary paragraph, identify the GENRE (usually an article or a book review). If it is a book reviewed by George Eliot then identify the title(s) and author(s) of the book(s) being reviewed. Also, provide five Key word from this article. """
            },
            {
                "role": "user",
                "content": summaries
            }
        ],
        temperature=0.6,
        max_tokens=1024, # Adjust max_tokens to a lower value 1024,720,512,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1)
    
    return response.choices[0].message.content

# Function to read text from a file
def read_text(filename):
    with open(os.path.join(path,filename),"r") as f:
        data = f.read()
    return data
#For only one article
# all_books = ["Mackay's Progress of the Intellect text.txt"]
# For all books in the folder
all_books = os.listdir(path)


# Batch size for processing documents
#batch_size = 1
#count = len(os.listdir("./Py-Script/GPT-Code/Results/"))



# Process documents one by one
for book in tqdm(all_books, desc= "Books"):
    start = time.time()
    content = read_text(book)  # Read the content of the file
    
    # Split content into smaller chunks
    chunk_size = 2000  # Adjust chunk size as needed
    chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
    print("chunk size: ",len(chunks))

    # Process each chunk and accumulate responses
    summary = []
    for chunk in tqdm(chunks,desc="chunks"):
        response = generate_chunk_summaries(chunk)  # Pass the content chunk to the function
        summary.append(f"""{response}""")  # Accumulate responses
    # print("Summary: ",summary)

    merged_summaries_ = merge_summaries(summary)

    ###################################

    chunk_size = 2000  # Adjust chunk size as needed
    chunks2 = [content[i:i+chunk_size] for i in range(0, len(merged_summaries_), chunk_size)]
    print("chunk size: ",len(chunks))

    # Process each chunk and accumulate responses
    summary2 = []
    for chunk in tqdm(chunks2,desc="chunks2"):
        response2 = generate_chunk_summaries(chunk)  # Pass the content chunk to the function
        summary2.append(f"""{response2}""")  # Accumulate responses
    # print("Summary: ",summary)

    final_merged_summaries_ = merge_summaries(summary2)

    final_summary = write_summary(final_merged_summaries_)
    print("final summary \n", final_summary)
    # Write accumulated response to JSON file
    end = time.time()
    # Calculate the difference in seconds
    execution_time_seconds = end - start 
    # Convert to hours, minutes, and seconds
    hours = int(execution_time_seconds // 3600) 
    minutes = int((execution_time_seconds % 3600) // 60)
    seconds = int(execution_time_seconds % 60) 
    # Print the result
    save=[final_summary,{"time":f" {hours} hr: {minutes} m: {seconds} s"}]
    print("Execution time:", hours, "hr:", minutes, "m:", seconds, "s")
 # Write accumulated response to JSON file
    with open(f"J:/R and Python_ Projects/GE_Project2024/Py-Script/GPT-Code/Results/new_{book[:-4]}_summary_new.json", "w") as f:
        json.dump(save, f)  

        # Function to write text to a file
def write_text(filename, data):
    with open(filename, "w") as f:
        f.write(data)
    # Write final summary to a text file
    write_text(f"J:/R and Python_ Projects/GE_Project2024/Py-Script/GPT-Code/Results/new_{book[:-4]}_summary_new.txt", final_summary)

   
       # Write final summary to text file
    with open(f"J:/R and Python_ Projects/GE_Project2024/Py-Script/GPT-Code/Results/text_outputGT3.5/new_{book[:-4]}_summary_new.txt", "w") as f:
        f.write(final_merged_summaries_)
 