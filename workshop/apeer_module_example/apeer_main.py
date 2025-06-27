from apeer_dev_kit import adk
import apply_filter

if __name__ == "__main__":

    # get the inputs from module
    inputs = adk.get_inputs()
    print(inputs)

    # # execute the main function to apply the filter
    outputs = apply_filter.execute(inputs["input_image"],
                                   filtertype=inputs["filtertype"],
                                   kernelsize=inputs["filter_kernel_size"])

    # finalize the output
    adk.set_file_output("output_image", outputs["output_image"])
    adk.finalize()
