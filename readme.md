# Evaluating Intention Detection Capability of Large Language Models in Persuasive Dialogues

## Abstract

We investigate intention detection in persuasive multi-turn dialogs employing the largest available Large Language Models (LLMs).
Much of the prior research measures the intention detection capability of machine learning models without considering the conversational history.
To evaluate LLMs' intention detection capability in conversation, we modified the existing datasets of persuasive conversation and created datasets using a multiple-choice paradigm.
It is crucial to consider others' perspectives through their utterances when engaging in a persuasive conversation, especially when making a request or reply that is inconvenient for others.
This feature makes the persuasive dialogue suitable for the dataset of measuring intention detection capability.
We incorporate the concept of `face acts,' which categorize how utterances affect mental states.
This approach enables us to measure intention detection capability by focusing on crucial intentions and to conduct comprehensible analysis according to intention types.

## Repo Details

### main_experiment

We experimented with whether LLMs can detect intentions with our datasets.  
The "data" file includes datasets employed in experiments such as conversational datasets with intention descriptions, or four-optional questions.  
The "src" file includes scripts for sending requests to LLMs.

### additional_experiment

This file contains data and scripts used for additional experiments on the detection of critical intentions, whose face acts are hpos-.
