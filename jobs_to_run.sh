# NOTE: These experiments must be run multiple times with all combinations of model and pathology:
# model=WizardLM70B , model=OASST70B , model=Llama2Chat70B
# pathology=appendicits , pathology=cholecystitis , pathology=diverticulitis , pathology=pancreatitis

# For run_full_info.py, additionally run all pathologies with the models model=Meditron70B , model=ClinicalCamel70B

# CDM Analysis
python train.py
python train.py summarize=False

# CDM FI Analysis
python run_full_info.py
python run_full_info.py order=p
python run_full_info.py order=l
python run_full_info.py order=i
python run_full_info.py order=
python run_full_info.py order=pil
python run_full_info.py order=lip
python run_full_info.py order=lpi
python run_full_info.py order=ipl
python run_full_info.py order=ilp
python run_full_info.py prompt_template=NOSYSTEMNOUSER
python run_full_info.py prompt_template=NOMEDICAL
python run_full_info.py prompt_template=NOSYSTEM
python run_full_info.py prompt_template=MINIMALSYSTEM
python run_full_info.py prompt_template=SERIOUS
python run_full_info.py prompt_template=MAINDIAGNOSIS
python run_full_info.py prompt_template=NOFINAL
python run_full_info.py prompt_template=PRIMARYDIAGNOSIS
python run_full_info.py only_abnormal_labs=True
python run_full_info.py fewshot=True
python run_full_info.py abbreviated=False

# Laboratory Test Interpretation Analysis. Does not require pathology specification as it loops over all pathologies. Model must still be specified.
python ref_range_test.py