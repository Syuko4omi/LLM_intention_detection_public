# Evaluating Intention Detection Capability of Large Language Models in Persuasive Dialogues


## Abstract
We investigate intention detection in persuasive multi-turn dialogs employing the largest available Large Language Models (LLMs).
Much of the prior research measures the intention detection capability of machine learning models without considering the conversational history.
To evaluate LLMs' intention detection capability in conversation, we modified the existing datasets of persuasive conversation and created datasets using a multiple-choice paradigm.
It is crucial to consider others' perspectives through their utterances when engaging in a persuasive conversation, especially when making a request or reply that is inconvenient for others.
This feature makes the persuasive dialogue suitable for the dataset of measuring intention detection capability.
We incorporate the concept of `face acts,' which categorize how utterances affect mental states.
This approach enables us to measure intention detection capability by focusing on crucial intentions and to conduct comprehensible analysis according to intention types.


## Files
### 1_test_data_annotated_description
Dialogues with annotated intention descriptions are stored in CSV format.  
For utterances annotated with face acts, three workers recruited through AMT annotated intentions, and the result of the majority vote among them is considered as the gold intention description.  
The previous study's original dialogue dataset annotated with face act labels is available here: https://github.com/ShoRit/face-acts

### 2_main_experiment
We experimented with whether LLMs can detect intentions with our datasets.  
The "data" file includes datasets employed in experiments such as conversational datasets with intention descriptions, or four-optional questions.  
The "results" file includes the raw results returned by LLMs.  
The "src" file includes scripts for sending requests to LLMs or sum up results.

### 3_additional_experiment_hpos-
This file contains data and scripts used for additional experiments on the detection of critical intentions.

### 4_appendix
This file contains data and scripts for experiments described in the appendix.  
The first experiment investigates how improving descriptions and adding rules for choosing options affect intention detection.  
The second experiment is for examining how Chain-of-Thought prompting influences intention detection.