# How to test your module locally**

1. First place the test files inside the correct folder
2. Navigate to the GIT repository and build the docker container

```bash
docker build -t sebi06/apeer_simplepython:latest .
```

3. Run the container using the input specified files and parameters inside the wfe.env file

```JSON
WFE_INPUT_JSON={"input_image":"/input/T=6_Z=15_CH=2.czi", "filtertype":"Median", "filter_kernel_size":5, "WFE_output_params_file":"/output.json"}
```

4. Now run the just created docker image using

```bash
docker run -it --rm -v ${PWD}/input:/input -v ${PWD}/output:/output --env-file wfe.env sebi06/apeer_simplepython:latest
```
