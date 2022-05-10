# create an environment
conda env create -f <path_to_yaml_file>

# activate an environment
conda activate <env_name>

# with the environmet activated

# list packages in environment
conda list

# run python file
python <path_to_python_file>

# deactivate an environment
conda deactivate <env_name>

# delete an environment
conda remove -n <env_name> --all

# add an environment to jupyter (from base environment with ipykernel)
pip install ipykernel
python -m ipykernel install --user --name=<env_name>

# remove an environment from juputer
jupyter kernelspec uninstall <env_name>