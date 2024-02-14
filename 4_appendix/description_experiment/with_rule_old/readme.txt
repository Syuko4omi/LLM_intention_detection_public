This is for the comparison of two settings: using refined descriptions, and settings rules when selecting distractors.

# Prepare for the experiment
1. Run scripts in the "preprocess" folder (convert_xlsx_to_jsonl.py -> create_annotation_sheet.py)
2. Annotate intention descriptions to the utterances in the dev data (description_annotated_data.xlsx)
3. Run scripts in the "postprocess" folder (confirm_speaker_description_corres.py -> convert_annotated_data_to_jsonl.py -> concatenate_data.py -> create_four_options.py)


# Experiment
1. Create prompts by executing create_prompt.py
2. Input prompts to the model and receive its outputs by executing send_request.py
3. Convert the output style by executing result_json_to_xlsx.py
