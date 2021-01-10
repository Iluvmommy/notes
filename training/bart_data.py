import pandas as pd

train_data = [
    [
        "Perseus “Percy” Jackson is the main protagonist and the narrator of the Percy Jackson and the Olympians series.",
        "Percy is the protagonist of Percy Jackson and the Olympians",
    ],
    [
        "Annabeth Chase is one of the main protagonists in Percy Jackson and the Olympians.",
        "Annabeth is a protagonist in Percy Jackson and the Olympians.",
    ],
]

train_df = pd.DataFrame(
    train_data, columns=["input_text", "target_text"]
)