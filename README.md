# MIMIC Clinical Decision Making Analysis

This folder contains the code used during the analysis of the paper "Evaluating and Mitigating Limitations of Large Language Models in Clinical Decision Making".

To run the analysis, you must first download the appropriate models.

Llama 2 chat: https://huggingface.co/TheBloke/Llama-2-70B-Chat-GPTQ

OASST: https://huggingface.co/TheBloke/Llama2-70B-OASST-SFT-v10-GPTQ

WizardLM: https://huggingface.co/TheBloke/WizardLM-70B-V1.0-GPTQ

Clinical Camel: https://huggingface.co/wanglab/ClinicalCamel-70B (The model must first be quantized using quantize.py)

Meditron: https://huggingface.co/TheBloke/meditron-70B-GPTQ

Then, after creating the dataset using the code from https://github.com/paulhager/MIMIC-Clinical-Decision-Making-Dataset, run all experiments with the code from https://github.com/paulhager/MIMIC-Clinical-Decision-Making-Framework.

The experiments that need to be run are specified in jobs_to_run.sh. As these are hundreds of experiments, we highly recommend using a cluster with some type of multi-job scheduling. We leave the exact implementation up to the specifics of the users system.

Once the files are created, they can be aggregated and pulled using download.py. The results should be grouped by experiment in seperate folders and then analysed using evaluate_cdm.py and evaluate_fi.py. Then, execute all of the cells of benchmark.ipynb, specifying the path to each experiment, to generate all results of the paper.