import nipype.interfaces.utility as niu
import nipype.pipeline.engine as pe

from nipype.interfaces.niftyreg.regutils import RegResample

from macapype.nodes.prepare import padding_cropped_img


def create_pad_brain_extraction_pipe(seg_pipe, params, data_preparation_pipe,
                                     brain_extraction_pipe, inputnode,
                                     outputnode):

    if "short_preparation_pipe" in params.keys():
        if "crop_T1" in params["short_preparation_pipe"].keys():

            print("Padding mask in native space")

            pad_mask = pe.Node(
                niu.Function(
                    input_names=['cropped_img_file', 'orig_img_file',
                                 'indiv_crop'],
                    output_names=['padded_img_file'],
                    function=padding_cropped_img),
                name="pad_mask")

            seg_pipe.connect(brain_extraction_pipe,
                             "outputnode.brain_mask",
                             pad_mask, "cropped_img_file")

            seg_pipe.connect(data_preparation_pipe,
                             "outputnode.native_T1",
                             pad_mask, "orig_img_file")

            seg_pipe.connect(inputnode, "indiv_params",
                             pad_mask, "indiv_crop")

            seg_pipe.connect(pad_mask, "padded_img_file",
                             outputnode, "brain_mask")

            print("Padding debiased_T1 in native space")

            pad_debiased_T1 = pe.Node(
                niu.Function(
                    input_names=['cropped_img_file', 'orig_img_file',
                                 'indiv_crop'],
                    output_names=['padded_img_file'],
                    function=padding_cropped_img),
                name="pad_debiased_T1")

            seg_pipe.connect(brain_extraction_pipe,
                             "outputnode.debiased_T1",
                             pad_debiased_T1, "cropped_img_file")

            seg_pipe.connect(data_preparation_pipe,
                             "outputnode.native_T1",
                             pad_debiased_T1, "orig_img_file")

            seg_pipe.connect(inputnode, "indiv_params",
                             pad_debiased_T1, "indiv_crop")

            seg_pipe.connect(pad_debiased_T1, "padded_img_file",
                             outputnode, "debiased_T1")

        else:
            print("Using reg_aladin transfo to pad mask back")
            pad_mask = pe.Node(RegResample(inter_val="NN"),
                               name="pad_mask")

            seg_pipe.connect(brain_extraction_pipe,
                             "outputnode.brain_mask",
                             pad_mask, "flo_file")

            seg_pipe.connect(data_preparation_pipe,
                             "outputnode.native_T1",
                             pad_mask, "ref_file")

            seg_pipe.connect(data_preparation_pipe,
                             "inv_tranfo.out_file",
                             pad_mask, "trans_file")

            print("Using reg_aladin transfo to pad debiased_T1 back")
            pad_debiased_T1 = pe.Node(RegResample(),
                                      name="pad_debiased_T1")

            seg_pipe.connect(brain_extraction_pipe,
                             "outputnode.debiased_T1",
                             pad_debiased_T1, "flo_file")

            seg_pipe.connect(data_preparation_pipe,
                             "outputnode.native_T1",
                             pad_debiased_T1, "ref_file")

            seg_pipe.connect(data_preparation_pipe,
                             "inv_tranfo.out_file",
                             pad_debiased_T1, "trans_file")

            print("Using reg_aladin transfo to pad \
                masked_debiased_T1 back")

            pad_masked_debiased_T1 = pe.Node(
                RegResample(),
                name="pad_masked_debiased_T1")

            seg_pipe.connect(brain_extraction_pipe,
                             "outputnode.masked_debiased_T1",
                             pad_masked_debiased_T1, "flo_file")

            seg_pipe.connect(data_preparation_pipe,
                             "outputnode.native_T1",
                             pad_masked_debiased_T1, "ref_file")

            seg_pipe.connect(data_preparation_pipe,
                             "inv_tranfo.out_file",
                             pad_masked_debiased_T1, "trans_file")

            # pad_masked_debiased_T2
            pad_masked_debiased_T2 = pe.Node(
                RegResample(),
                name="pad_masked_debiased_T2")

            seg_pipe.connect(brain_extraction_pipe,
                             "outputnode.masked_debiased_T2",
                             pad_masked_debiased_T2, "flo_file")

            seg_pipe.connect(data_preparation_pipe,
                             "align_T2_on_T1.out_file",
                             pad_masked_debiased_T2, "ref_file")

            seg_pipe.connect(data_preparation_pipe,
                             "inv_tranfo.out_file",
                             pad_masked_debiased_T2, "trans_file")

            # outputnode
            seg_pipe.connect(pad_mask, "out_file",
                             outputnode, "brain_mask")

            seg_pipe.connect(pad_debiased_T1, "out_file",
                             outputnode, "debiased_T1")

            seg_pipe.connect(pad_masked_debiased_T1, "out_file",
                             outputnode, "masked_debiased_T1")

            seg_pipe.connect(pad_masked_debiased_T2, "out_file",
                             outputnode, "masked_debiased_T2")

    elif "long_single_preparation_pipe" in params.keys():
        if "prep_T1" in params["long_single_preparation_pipe"].keys():

            print("Padding mask in native space \
                (long_single_preparation_pipe)")

            pad_mask = pe.Node(
                niu.Function(
                    input_names=['cropped_img_file', 'orig_img_file',
                                 'indiv_crop'],
                    output_names=['padded_img_file'],
                    function=padding_cropped_img),
                name="pad_mask")

            seg_pipe.connect(brain_extraction_pipe,
                             "outputnode.brain_mask",
                             pad_mask, "cropped_img_file")

            seg_pipe.connect(data_preparation_pipe,
                             "outputnode.native_T1",
                             pad_mask, "orig_img_file")

            seg_pipe.connect(inputnode, "indiv_params",
                             pad_mask, "indiv_crop")

            seg_pipe.connect(pad_mask, "padded_img_file",
                             outputnode, "brain_mask")

            print("Padding debiased_T1 in native space")

            pad_debiased_T1 = pe.Node(
                niu.Function(
                    input_names=['cropped_img_file', 'orig_img_file',
                                 'indiv_crop'],
                    output_names=['padded_img_file'],
                    function=padding_cropped_img),
                name="pad_debiased_T1")

            seg_pipe.connect(brain_extraction_pipe,
                             "outputnode.debiased_T1",
                             pad_debiased_T1, "cropped_img_file")

            seg_pipe.connect(data_preparation_pipe,
                             "outputnode.native_T1",
                             pad_debiased_T1, "orig_img_file")

            seg_pipe.connect(inputnode, "indiv_params",
                             pad_debiased_T1, "indiv_crop")

            seg_pipe.connect(pad_debiased_T1, "padded_img_file",
                             outputnode, "debiased_T1")

    return (pad_mask, pad_masked_debiased_T1, pad_masked_debiased_T2)
