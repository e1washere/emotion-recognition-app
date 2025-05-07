This is a directory for data preprocessing

Right now you have three original datasets: FER2013, KDEF and NAtural Human Face Images
To augment them, copy images to the mixed set and create arrays for model traing you need to run create_sets.py for each of them

From the main directory (Datasets preprocessing) run this command  "python -m Directory_name.create_sets" for all three directories
After that run  "python -m Mixed.Preprocess" to obtain arrays for Mixed dataset

Directory models_code contains files for model training. In the development, Kaggle was used instead of development environment like VSCode