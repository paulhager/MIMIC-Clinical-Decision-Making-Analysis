# MIMIC Clinical Decision Making Analysis

For a video overview of the paper, checkout this talk I held for the BZKF: https://www.youtube.com/watch?v=sCDaUC16mHA

## News

**🔥 New Addition: Llama 3.3 has been added to the leaderboard! 🔥**

**🔥 New Addition: Llama 3.1 has been added to the leaderboard! 🔥**

**🔥 New Addition: OpenBio has been added to the leaderboard! 🔥**

**🔥 New Addition: Llama 3 has been added to the leaderboard! 🔥**

## Overview

This folder contains the code used during the analysis of the paper "Evaluating and Mitigating Limitations of Large Language Models in Clinical Decision Making".

To run the analysis, you must first download the appropriate models.

Llama 2 chat: https://huggingface.co/TheBloke/Llama-2-70B-Chat-GPTQ

OASST: https://huggingface.co/TheBloke/Llama2-70B-OASST-SFT-v10-GPTQ

WizardLM: https://huggingface.co/TheBloke/WizardLM-70B-V1.0-GPTQ

Clinical Camel: https://huggingface.co/wanglab/ClinicalCamel-70B (The model must first be quantized using quantize.py)

Meditron: https://huggingface.co/TheBloke/meditron-70B-GPTQ

Then, after creating the dataset using the code from https://github.com/paulhager/MIMIC-Clinical-Decision-Making-Dataset, run all experiments with the code from https://github.com/paulhager/MIMIC-Clinical-Decision-Making-Framework.

The experiments that need to be run are specified in jobs_to_run.sh. Note the comment at the top of the file. As these are hundreds of experiments, we highly recommend using a cluster with some type of multi-job scheduling. We leave the exact implementation up to the specifics of the users system.

Once the files are created, they can be aggregated and pulled using download.py. The results should be grouped by experiment in seperate folders evaluate_cdm.py and evaluate_fi.py. Then, execute all of the cells of benchmark.ipynb, specifying the path to each experiment, to generate all results of the paper.

Visit https://huggingface.co/spaces/MIMIC-CDM/leaderboard to check out the current leaderboard. I will update this as new models are released. If you would like a model to be tested and put on the board, please write me an email at paul (dot) hager (at) tum (dot) de.

## Environment

To setup the environment, create a new virtual environment with python=3.10 of your choosing and then run 

```
pip install --no-deps -r requirements.txt
```


# Citation

If you found this code and dataset useful, please cite our paper and dataset with:

Hager, P., Jungmann, F., Holland, R. et al. Evaluation and mitigation of the limitations of large language models in clinical decision-making. Nat Med (2024). https://doi.org/10.1038/s41591-024-03097-1
```
@article{hager_evaluation_2024,
	title = {Evaluation and mitigation of the limitations of large language models in clinical decision-making},
	issn = {1546-170X},
	url = {https://doi.org/10.1038/s41591-024-03097-1},
	doi = {10.1038/s41591-024-03097-1},,
	journaltitle = {Nature Medicine},
	shortjournal = {Nature Medicine},
	author = {Hager, Paul and Jungmann, Friederike and Holland, Robbie and Bhagat, Kunal and Hubrecht, Inga and Knauer, Manuel and Vielhauer, Jakob and Makowski, Marcus and Braren, Rickmer and Kaissis, Georgios and Rueckert, Daniel},
	date = {2024-07-04},
}
```

Hager, P., Jungmann, F., & Rueckert, D. (2024). MIMIC-IV-Ext Clinical Decision Making: A MIMIC-IV Derived Dataset for Evaluation of Large Language Models on the Task of Clinical Decision Making for Abdominal Pathologies (version 1.0). PhysioNet. https://doi.org/10.13026/2pfq-5b68.
```
@misc{hager_mimic-iv-ext_nodate,
	title = {{MIMIC}-{IV}-Ext Clinical Decision Making: A {MIMIC}-{IV} Derived Dataset for Evaluation of Large Language Models on the Task of Clinical Decision Making for Abdominal Pathologies},
	url = {https://physionet.org/content/mimic-iv-ext-cdm/1.0/},
	shorttitle = {{MIMIC}-{IV}-Ext Clinical Decision Making},
	publisher = {{PhysioNet}},
	author = {Hager, Paul and Jungmann, Friederike and Rueckert, Daniel},
	urldate = {2024-07-04},
	doi = {10.13026/2PFQ-5B68},
	note = {Version Number: 1.0
Type: dataset},
}
```
