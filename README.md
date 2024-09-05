# Sub-modules
Two sub-modules are included in this repository. They are necessary for the replication of our results and are briefly described below.


## OpenAI's 'Guided Diffusion'
The 'GuidedDiffusion' sub-module of this repository is our slightly modified fork of [OpenAI's 'Guided Diffusion' codebase](https://github.com/openai/guided-diffusion), which was prepared by OpenAI in conjunction with their paper: [Diffusion Models Beat GANS on Image Synthesis](http://arxiv.org/abs/2105.05233).

This fork contains small modifications and additions to the codebase such as to facilitate the reproduction of diffusion results reported by 'Training a Diffusion Model to Create Biometrically Unique Iris Textures'. It is necessary to install in order to replicate our methods of model training and sampling.

To install our fork of the Guided Diffusion Python package, run the following commands in your terminal:

```
wget https://github.com/robert-hart/IrisDB-GuidedDiffusion/archive/refs/heads/main.zip
unzip main.zip
cd IrisDB-GuidedDiffusion-main
pip install -e .
```

Bash scripts with our training parameters and sampling parameters can be found within the 'GuidedDiffusion' sub-module, and are called 'train.sh' and 'sample.sh', respectively. Before running these scripts, make sure to change file-paths and other parameters as instructed by each script's respective comments.

## 'iris-evaluation'
The 'iris-evaluation' sub-module of this repository is a custom Python package written to conduct biometric analysis upon iris textures. The specific iris recognition technique utilized by 'iris-evaluation' is that of Libor Masek, who improved upon Daugman's early iris recognition work by replacing the use of 2D Gabor Filters for feature extraction with 1D Log-Gabor Filters. 'iris-evaluation' utilizes a custom otsu threshold-based segmentation technique to separate concentric iris patterns from black backgrounds; Daugman's 'Rubber Sheet' model for normalization; and Hamming Distance to compare iris codes. More details can be found in 'Training a Diffusion Model to Create Biometrically Unique Iris Textures'; however, we provide the package's code here for the purposes of inspection and replication.

To install 'iris-evaluation', run the following commands in your terminal:

```
wget https://github.com/robert-hart/iris-evaluation/archive/refs/heads/main.zip
unzip main.zip
cd iris-evaluation
pip install -v .
```

While this package is only suitable for research purposes and is limited in the methods available for iris segmentation, feature extraction, and etc., it was designed such that other methods could be added as package modules in the future.

'iris-evaluation' utilizes PyTorch and thus performs best on devices with Apple Silicon or NVIDIA GPUs. Performance on other hardware may vary.

# Iris Recognition
The code within the 'Iris_Recognition' folder utilizes modules from 'iris-evaluation' to generate data for biometric analyses of iris images. Instructions can be found within the directory itself.

# Notebooks
The Notebooks folder contains the rendered Jupyter Notebooks used to create all paper figures.

# Data Disclaimer
Due to the sensitive nature of the data used to carry out our analyses, data to use with this code will only be made available upon request.
