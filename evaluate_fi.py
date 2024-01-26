from os.path import join
import pickle
import glob

from dataset.utils import load_hadm_from_file
from utils.logging import read_from_pickle_file
from run import load_evaluator


def calculate_average(evals, field, pathology):
    average = 0
    for patient in evals.keys():
        average += evals[patient]["scores"][field]

    average /= len(evals)
    # print(f'{pathology}: {average:0.02} (n={len(evals)})'.rjust(30))
    return average, len(evals)


def calculate_percentages(evals, field):
    for patient in evals.keys():
        evals[patient]["scores"][field] = (
            evals[patient]["scores"][field[: -len(" Percentage")]]
            / evals[patient]["max_scores"][field[: -len(" Percentage")]]
        )
    return evals


def count_unnecessary(evals, field):
    for patient in evals.keys():
        evals[patient]["scores"][field] = len(evals[patient]["answers"][field])
    return evals


# Check new evaluation strategy
base_hosp = join("mimic-iv", "hosp")

id_difficulty = pickle.load(open("id_difficulty.pkl", "rb"))
difficulty = "first_diag"

experiment_results = {}
experiment_evals = {}
experiment_scores = {}

for experiment in [
    "FI_H",
    "FI_I",
    "FI_ILP",
    "FI_IPL",
    "FI_L",
    "FI_LIP",
    "FI_LPI",
    "FI_P",
    "FI_PIL",
    "FI_PLI",
    "FI_PLI_ACUTE",
    "FI_PLI_CONFIRM",
    "FI_PLI_DR_NOABBR",
    "FI_PLI_MAINDIAGNOSIS",
    "FI_PLI_MINIMALSYSTEM",
    "FI_PLI_NOFINAL",
    "FI_PLI_NOMEDICAL",
    "FI_PLI_NOPROMPT",
    "FI_PLI_NOSUMMARY",
    "FI_PLI_NOSYSTEM",
    "FI_PLI_NOSYSTEMNOUSER",
    "FI_PLI_P",
    "FI_PLI_PRIMARYDIAGNOSIS",
    "FI_PLI_SERIOUS",
    "FI_PLI_ONLYABNORMAL",
]:
    print(experiment)
    model_scores = {}
    model_results = {}
    model_evals = {}

    for model in [
        "Llama-2-70B-chat-GPTQ",
        "Llama2-70B-OASST-SFT-v10-GPTQ",
        "WizardLM-70B-V1.0-GPTQ",
        # "ClinicalCamel-70B-GPTQ",
        # "Meditron-70B-GPTQ",
    ]:
        run = f"_{model}_*_FULL_INFO_*results.pkl"
        assert "result" in run

        all_evals = {}
        all_results = {}
        for patho in [
            "appendicitis",
            "cholecystitis",
            "diverticulitis",
            "pancreatitis",
        ]:
            # evaluator = load_evaluator(patho)
            # Load patient data
            hadm_info_clean = load_hadm_from_file(f"{patho}_hadm_info_first_diag")
            all_evals[patho] = {}
            all_results[patho] = {}

            results_log_path = f"logs/SOTA/{experiment}/{patho}{run}"

            results = []
            for r in read_from_pickle_file(glob.glob(results_log_path)[0]):
                results.append(r)
            results = {k: v for d in results for k, v in d.items()}

            for _id in id_difficulty[patho][difficulty]:
                if _id not in results:
                    print(f"Skipping {_id} | {glob.glob(results_log_path)[0]}")
                    continue
                if "PROBS" in experiment or "SELFCONSISTENCY" in experiment:
                    result = "Final Diagnosis: " + results[_id]["Diagnosis"]
                    diag_probs = results[_id]["Probabilities"]
                    diag_probs = None
                else:
                    result = "Final Diagnosis: " + results[_id]
                    diag_probs = None

                evaluator = load_evaluator(patho)

                eval = evaluator._evaluate_agent_trajectory(
                    prediction=result,
                    input="",
                    reference=(
                        hadm_info_clean[_id]["Discharge Diagnosis"],
                        hadm_info_clean[_id]["ICD Diagnosis"],
                        hadm_info_clean[_id]["Procedures ICD9"],
                        hadm_info_clean[_id]["Procedures ICD10"],
                        hadm_info_clean[_id]["Procedures Discharge"],
                    ),
                    agent_trajectory=[],
                    diagnosis_probabilities=diag_probs,
                )
                all_evals[patho][_id] = eval
                all_results[patho][_id] = result
        model_evals[model] = all_evals
        model_results[model] = all_results
        avg_scores = {}
        avg_samples = {}

        for field in ["Diagnosis", "Gracious Diagnosis"]:
            avg_scores[field] = {}
            avg_samples[field] = {}
            for patho in [
                "appendicitis",
                "cholecystitis",
                "diverticulitis",
                "pancreatitis",
            ]:
                avg, n = calculate_average(all_evals[patho], field, patho)

                avg_scores[field][patho] = avg
                avg_samples[field][patho] = n
        model_scores[model] = avg_scores

        if difficulty == "first_diag" or difficulty == "dr_eval":
            pickle.dump(
                all_evals,
                open(
                    f"logs/SOTA/{experiment}/{model}_evals.pkl",
                    "wb",
                ),
            )
            pickle.dump(
                all_results,
                open(
                    f"logs/SOTA/{experiment}/{model}_results.pkl",
                    "wb",
                ),
            )
            pickle.dump(
                avg_scores,
                open(
                    f"logs/SOTA/{experiment}/{model}_scores.pkl",
                    "wb",
                ),
            )
    if difficulty == "first_diag" or difficulty == "dr_eval":
        pickle.dump(
            model_evals,
            open(
                f"logs/SOTA/{experiment}/evals.pkl",
                "wb",
            ),
        )
        pickle.dump(
            model_results,
            open(
                f"logs/SOTA/{experiment}/results.pkl",
                "wb",
            ),
        )
        pickle.dump(
            model_scores,
            open(
                f"logs/SOTA/{experiment}/scores.pkl",
                "wb",
            ),
        )
    experiment_results[experiment] = model_results
    experiment_evals[experiment] = model_evals
    experiment_scores[experiment] = model_scores
