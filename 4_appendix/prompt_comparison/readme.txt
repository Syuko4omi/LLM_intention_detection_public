This is for the comparison of two prompt styles.
One is succinct prompt, which has only script, question and four options.
The other is detailed prompt, which consists of two answering steps. The first step is reason explanation, which requires answering what is the intention of the last utterance. The second step is answer extraction, which let LLMs select the most appropriate option from four options.

# Prepare for the experiment
1. Run scripts in the "preprocess" folder (convert_xlsx_to_jsonl.py -> create_annotation_sheet.py)
2. Annotate intention descriptions to the utterances in the dev data (description_annotated_data.xlsx)
3. Run scripts in the "postprocess" folder (confirm_speaker_description_corres.py -> convert_annotated_data_to_jsonl.py -> concatenate_data.py -> create_four_options.py)


# Experiment
1. Create prompts by executing create_prompt.py
2. Input prompts to the model (gpt-4-0613) and receive its outputs by executing send_request.py
3. Convert the output style by executing result_json_to_xlsx.py


# Result
Succinct -> 0.930 (507/545)
Detailed -> 0.938 (511/545)