import random
import math
from typing import List
import nltk


def check_children(tree: nltk.Tree, target_label: str) -> int:
    """Function to check the amount of children with a certain label"""
    amount = 0
    for branch in tree:
        if branch.label() == target_label:
            amount += 1

    return amount


def shuffle_dict_keys(item: dict) -> dict:
    """Function to randomly shuffle keys in a dictionary"""
    shuffled_keys = list(item.keys())
    values = list(item.values())
    random.shuffle(shuffled_keys)
    shuffled_dict = dict(zip(shuffled_keys, values))
    return shuffled_dict


def separate_and_shuffle_branch(branch: nltk.Tree) -> tuple:
    """A function for swapping matching branches with the 'NP' label
    and pre-calculating possible mixing combinations"""
    branch_children = {}
    live_in_place_part = {}

    for child_index, child in enumerate(branch):
        if child.label() == "NP":
            branch_children[child_index] = child
        else:
            live_in_place_part[child_index] = child

    shuffled_np = branch_children
    count = 1

    if live_in_place_part:
        shuffled_np = shuffle_dict_keys(branch_children)
        count = math.factorial(len(shuffled_np))

    live_in_place_part.update(shuffled_np)

    shuffled_dict = [
        live_in_place_part[key] for key in sorted(live_in_place_part.keys())
    ]
    return shuffled_dict, count


def paraphrase_tree(
    tree: nltk.Tree,
    paraphrased_tree: List = None,
    count_of_combination: List = None,
) -> tuple:
    """Recursive function to traverse the syntax tree, rephrase it,
    return a new tree and a list with factorials of possible
    combinations"""
    if paraphrased_tree is None:
        paraphrased_tree = []

    if count_of_combination is None:
        count_of_combination = []

    if tree.height() <= 2:
        return paraphrased_tree, count_of_combination

    temporary_result = []
    for branch in tree:
        if len(list(branch.subtrees())) > 1:
            if branch.label() == "NP" and check_children(branch, "NP") >= 2:
                (
                    shuffled_branch,
                    amount_of_combinations,
                ) = separate_and_shuffle_branch(branch)
                if amount_of_combinations > 1:
                    count_of_combination.append(amount_of_combinations)

                shuffled_branch_with_current_label = nltk.Tree(
                    branch.label(),
                    [nltk.Tree(branch.label(), shuffled_branch)],
                )
                temporary_result.extend(shuffled_branch_with_current_label)

            else:
                paraphrase_tree(branch, temporary_result, count_of_combination)
        else:
            temporary_result.append(nltk.Tree(branch.label(), branch))

    paraphrased_tree.append(nltk.Tree(tree.label(), temporary_result))
    return paraphrased_tree, count_of_combination


def take_sentence_of_tree(tree: paraphrase_tree) -> str:
    """Function to get a string (sense of sentence) representation of a tree"""
    sentence = ""
    for branch in tree:
        if isinstance(branch, nltk.Tree):
            sentence += " ".join(branch.leaves()) + " "
    return sentence


def prepare_response(tree: str, limit: int) -> dict:
    """The response preparation function
    generates all possible variants of the paraphrased syntax tree,
    returns the required number of options to the user,
    or all possible ones if the number of possible combinations
    is less than the number in the request."""
    all_paraphrase_combination = set()

    tree = nltk.Tree.fromstring(tree)

    base_tree = (take_sentence_of_tree(tree), str(tree).replace("\n", ""))
    all_paraphrase_combination.add(base_tree)

    first_paraphrase, count_possible_combinations = paraphrase_tree(tree)

    first_paraphrase, count_possible_combinations = first_paraphrase[
        0
    ], math.prod(count_possible_combinations)

    if count_possible_combinations <= 1:
        return {
            "status": 200,
            "data": None,
            "detail": "This tree dont have any paraphrase variants",
        }

    all_paraphrase_combination.add(
        (
            take_sentence_of_tree(first_paraphrase),
            str(first_paraphrase).replace("\n", ""),
        )
    )

    while len(all_paraphrase_combination) != count_possible_combinations:
        paraphrase = paraphrase_tree(tree)[0]
        sentence = take_sentence_of_tree(paraphrase)
        paraphrase = str(paraphrase[0]).replace("\n", "")
        all_paraphrase_combination.add((sentence, paraphrase))

    list_of_paraphrased_trees = [
        {"sentence": combination[0], "tree": combination[1]}
        for combination in all_paraphrase_combination
        if combination != base_tree
    ]

    response_data = (
        list_of_paraphrased_trees[:limit]
        if count_possible_combinations > limit
        else list_of_paraphrased_trees
    )

    response_detail = (
        f"This tree have only {count_possible_combinations}"
        f" paraphrased variants."
        if limit > count_possible_combinations
        else f"{limit} paraphrased variants of ur Tree"
    )

    return {"status": 200, "data": response_data, "detail": response_detail}
