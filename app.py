from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)

openai.api_type = "azure"
openai.api_base = "https://nitoropenai.openai.azure.com/"
openai.api_version = "2022-12-01"
os.environ["OPENAI_API_KEY"] = "78d406f975874c20ac2298c6d83e2f7d"
os.environ["OPENAI_API_VERSION"] ="2022-12-01"
os.environ["OPENAI_API_BASE"] = "https://nitoropenai.openai.azure.com/"
openai.api_key = "78d406f975874c20ac2298c6d83e2f7d"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        source_language = request.form.get("source")
        target_language = request.form.get("target")
        code = request.form.get("code")
        
        prompt = f"""
                    I want you act as an experienced Software Developer who has a deep understanding of the {source_language} and {target_language} programming languages.
                    I want you to translate the code from {source_language} into {target_language}.
                    
                    Instructions:
                    - While translating code ensure that the code is clean and readable.
                    - Ensure the syntax of the code is correct.
                    - Ensure the code has comment blocks.
                    
                    Understand the below code and check whether the syntax of the code matches as that of {source_language}.
                    If yes, translate the code but if not write the output as `Code is not in {source_language}`
                    
                    {code}
                
                """

        response = openai.Completion.create(
            engine="text-davinci-003",
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=1050,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["###"]
        )

        output = response.choices[0].text
        return render_template(
                                "index.html", 
                                input=code, 
                                output=output, 
                                source=source_language, 
                                target=target_language
                            )


if __name__ == '__main__':
    app.run(port=6000, debug=True)
