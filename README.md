# Incorporating Source Syntax into Transformer based NMT

### NLA Project - Team 24: Weapons of Mass Translation

- Ujwal Narayan - 20171170
- Saujas Vadugru - 20171098

## Description 

We've seen the effectiveness of transformer based approaches for various NLP tasks. But Transformers still struggle in a moderate to low resource setting.
In this project we explore one possible avenue of alleviating this issue, i.e the injection of syntax into the source side of the transformer. 
We explore two types of syntactical structers:
- Constituency Parses
- Dependency Parses 

The parses are linearised and fed into the transformer architecture. We propose two different experimental setups to train on.

1. Multi Task: In this setting, we augment the source sentences with a tag, <TR>, <CP> or <DP> and based on this tag the transformer is expected to give the translation, the constituency parse and the dependency parse respectively. 
2. Mixed Encoder: In this setting, we feed in the constiuency parses and the dependency parses onto the source side and the transformer is expected to translate the sentence irrespective of the form.

We evaluate the translations based on thier BLEU scores. We further analyse the results in two ways.

1. Sentence complexity: We define three measures of sentence complexity, the length of the sentence, and the depths of their corresponding parse trees. We evaluate the performance of the model over varying lengths and depths, and present our findings.
2. Dependency tree induction:   We use theencoder attention heads to induce trees for the training set of the CoNLL 2017 Shared Task,  and compare unlabelled attachment scores (UAS) across layers and attention heads.

## Data and Models

The processed data and trained models for the experiments are available over [here](https://iiitaphyd-my.sharepoint.com/:f:/g/personal/ujwal_narayan_research_iiit_ac_in/EkI50A3_bHFOvGtkWFpMANQBH63OijkHFzjcR75akiLL-w?e=VmkawX)




